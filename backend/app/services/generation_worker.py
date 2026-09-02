import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.test_attempt import TestAttempt
from app.models.exam import Exam
from app.services.ai_service import generate_questions
from app.models.question import Question

logger = logging.getLogger(__name__)

# Thread pool for running blocking AI generation without blocking the async loop
_thread_pool = ThreadPoolExecutor(max_workers=2)


def _run_generation_sync(attempt_id: int):
    """Run question generation synchronously (called inside a thread)."""
    db: Session = SessionLocal()
    try:
        attempt = db.query(TestAttempt).filter(TestAttempt.id == attempt_id).first()
        if not attempt or attempt.generation_status not in ('PENDING', 'GENERATING'):
            return

        attempt.generation_status = 'GENERATING'
        db.commit()

        exam = db.query(Exam).filter(Exam.id == attempt.exam_id).first()
        if not exam:
            attempt.generation_status = 'FAILED'
            attempt.error_message = "Exam not found"
            db.commit()
            return

        def save_questions_callback(questions):
            # Save questions incrementally
            local_db = SessionLocal()
            try:
                for q in questions:
                    q.test_attempt_id = attempt_id
                    q.exam_id = exam.id
                    local_db.add(q)
                local_db.commit()
                logger.info(f"Saved batch of {len(questions)} questions for attempt {attempt_id}")
            except Exception as e:
                logger.error(f"Error saving questions: {e}")
            finally:
                local_db.close()

        try:
            questions = generate_questions(
                exam.name, 
                exam.subjects, 
                attempt.total_questions, 
                negative_marks=exam.negative_marking,
                batch_callback=save_questions_callback
            )
            
            # Verify if we actually have the required amount in DB
            db.refresh(attempt)
            current_q_count = db.query(Question).filter(Question.test_attempt_id == attempt_id).count()
            
            if current_q_count >= attempt.total_questions:
                attempt.generation_status = 'READY'
                logger.info(f"Generation READY for attempt {attempt_id}: {current_q_count}/{attempt.total_questions} questions")
            else:
                attempt.generation_status = 'FAILED'
                attempt.error_message = f"Failed to generate enough questions. Expected {attempt.total_questions}, got {current_q_count}"
                logger.error(f"Generation FAILED for attempt {attempt_id}: {current_q_count}/{attempt.total_questions}")
                
        except Exception as e:
            attempt.generation_status = 'FAILED'
            attempt.error_message = str(e)
            logger.error(f"Generation exception for attempt {attempt_id}: {e}")
            
        db.commit()
        
    except Exception as e:
        logger.error(f"Error in generation worker: {e}")
    finally:
        db.close()


async def _process_generation(attempt_id: int):
    """Run question generation in a thread pool to avoid blocking the async loop."""
    loop = asyncio.get_event_loop()
    logger.info(f"Starting threaded generation for attempt {attempt_id}")
    await loop.run_in_executor(_thread_pool, _run_generation_sync, attempt_id)


async def generation_worker_loop():
    logger.info("Starting background generation worker loop...")
    while True:
        try:
            db: Session = SessionLocal()
            pending_attempts = db.query(TestAttempt).filter(
                TestAttempt.generation_status.in_(['PENDING'])
            ).all()
            
            if pending_attempts:
                # Process all pending attempts concurrently
                tasks = []
                for attempt in pending_attempts:
                    logger.info(f"Picked up generation for attempt {attempt.id}")
                    tasks.append(_process_generation(attempt.id))
                
                db.close()
                # Run all generations concurrently
                await asyncio.gather(*tasks, return_exceptions=True)
            else:
                db.close()
                
        except Exception as e:
            logger.error(f"Generation loop error: {e}")
            
        await asyncio.sleep(3)  # Poll every 3 seconds
