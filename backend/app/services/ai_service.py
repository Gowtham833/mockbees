import json
import logging
from typing import List, Dict, Any
from groq import Groq
from app.config import settings
from app.models.question import Question

logger = logging.getLogger(__name__)

client = Groq(api_key=settings.GROQ_API_KEY)

# ---------------------------------------------------------------------------
# Exam-specific difficulty mapping
# ---------------------------------------------------------------------------

def _exam_difficulty(exam_name: str) -> str:
    exam_lower = exam_name.lower()
    very_hard_exams = [
        'upsc', 'gate', 'neet', 'jee', 'ies', 'cat', 'xat', 'nda', 'cds', 'afcat',
        'clat', 'aillet', 'slet', 'ugc net', 'ctet', 'kvs'
    ]
    if any(keyword in exam_lower for keyword in very_hard_exams):
        return 'very hard'
    if any(keyword in exam_lower for keyword in ['ssc', 'banking', 'rrb', 'police', 'state psc', 'defence']):
        return 'hard'
    return 'very hard'


# ---------------------------------------------------------------------------
# Exam-specific system prompts — detailed persona for each exam family
# ---------------------------------------------------------------------------

_SYSTEM_PROMPTS = {
    "rrb": (
        "You are a senior question paper setter employed by the Railway Recruitment Board (RRB) of India. "
        "You have 15+ years of experience designing Computer Based Test (CBT) papers for RRB Level 01 (Group D), "
        "NTPC, ALP, Technician, and JE examinations. You are intimately familiar with the exact difficulty level, "
        "question patterns, and topic distribution of real RRB papers conducted in 2024-2025. "
        "Your questions MUST be indistinguishable from real RRB exam questions — they should require genuine "
        "problem-solving, multi-step reasoning, and domain knowledge. NEVER produce textbook-style or school-level "
        "questions. Every question must feel like it was pulled directly from a real RRB CBT answer key. "
        "Return your output as valid JSON only."
    ),
    "ssc": (
        "You are a senior question paper setter for the Staff Selection Commission (SSC), India. "
        "You design papers for SSC CGL, CHSL, MTS, and GD Constable exams. Your questions must match "
        "the exact difficulty of real SSC papers — tricky arithmetic, advanced reasoning, and factual GK. "
        "Return your output as valid JSON only."
    ),
    "banking": (
        "You are a senior question paper setter for Indian banking exams including IBPS PO, Clerk, "
        "RRB PO, RRB Clerk, and SBI exams. Your questions must match real banking exam difficulty — "
        "complex data interpretation, puzzle-based reasoning, and banking awareness. "
        "Return your output as valid JSON only."
    ),
    "default": (
        "You are an expert question paper setter for Indian government competitive examinations with "
        "15+ years of experience. You design questions that match the exact difficulty and style of "
        "real exam papers. Your questions must be exam-grade — never school-level or basic practice-level. "
        "Return your output as valid JSON only."
    ),
}


def _get_system_prompt(exam_name: str) -> str:
    exam_lower = exam_name.lower()
    if 'rrb' in exam_lower:
        return _SYSTEM_PROMPTS["rrb"]
    if 'ssc' in exam_lower:
        return _SYSTEM_PROMPTS["ssc"]
    if any(kw in exam_lower for kw in ['ibps', 'sbi', 'banking', 'bank']):
        return _SYSTEM_PROMPTS["banking"]
    return _SYSTEM_PROMPTS["default"]


# ---------------------------------------------------------------------------
# Real exam sample questions (few-shot examples) — extracted from RRB Group D
# 2025 Answer Key PDF to calibrate AI difficulty
# ---------------------------------------------------------------------------

_RRB_SAMPLE_QUESTIONS = {
    "General Science": [
        {
            "question": "The motion of a satellite orbiting the Earth in a circular path at constant speed is a classic example of uniform circular motion. What property of this motion prevents its acceleration from being zero?",
            "option_a": "The total mechanical energy is conserved, necessitating acceleration.",
            "option_b": "The direction of motion changes continuously at every point, meaning the velocity is changing.",
            "option_c": "The object's mass continually changes due to orbital dynamics.",
            "option_d": "The speed is too high for the gravitational force to sustain a constant velocity.",
            "correct_answer": "B",
            "explanation": "In uniform circular motion, speed remains constant but velocity changes because the direction is continuously changing. Since acceleration is the rate of change of velocity (a vector), the acceleration is non-zero and directed toward the center (centripetal acceleration)."
        },
        {
            "question": "A coil has a resistance of 44 Ω. If it is connected across a 220 V supply, what is the power consumed by the coil?",
            "option_a": "5 W",
            "option_b": "1100 W",
            "option_c": "110 W",
            "option_d": "0.2 W",
            "correct_answer": "B",
            "explanation": "Power P = V²/R = (220)²/44 = 48400/44 = 1100 W."
        },
        {
            "question": "The fractional atomic mass of chlorine is due to which of the following?",
            "option_a": "Presence of ions",
            "option_b": "Presence of isotopes",
            "option_c": "Its compound nature",
            "option_d": "Experimental error",
            "correct_answer": "B",
            "explanation": "Chlorine exists as two isotopes: Cl-35 (75.77%) and Cl-37 (24.23%). The weighted average gives the fractional atomic mass of 35.5."
        },
    ],
    "Mathematics": [
        {
            "question": "Soniya got married 15 years ago. Her present age is 8/5 times her age at the time of her marriage. Her sister was 8 years younger to her at the time of her marriage. Find the present age of her sister.",
            "option_a": "32 years",
            "option_b": "24 years",
            "option_c": "40 years",
            "option_d": "28 years",
            "correct_answer": "A",
            "explanation": "Let Soniya's age at marriage = x. Present age = x + 15. Given: x + 15 = (8/5)x → 5x + 75 = 8x → 3x = 75 → x = 25. Sister's age at marriage = 25 - 8 = 17. Sister's present age = 17 + 15 = 32."
        },
        {
            "question": "A 325 m long train overtakes a man moving at a speed of 5 km/hr (in the same direction) in 45 seconds. How much time (in seconds) will it take this train to completely cross another 440 m long train, moving in the opposite direction at a speed of 20 km/hr?",
            "option_a": "54",
            "option_b": "40",
            "option_c": "52",
            "option_d": "51",
            "correct_answer": "A",
            "explanation": "Relative speed when overtaking man = (train speed - 5) km/hr. Distance = 325 m in 45 sec → speed = 325/45 m/s = 65/9 m/s. Relative speed = 65/9 m/s → train speed - 5 = (65/9)×(18/5) = 26 km/hr → train speed = 31 km/hr. When crossing opposite train: relative speed = 31 + 20 = 51 km/hr = 51×5/18 m/s. Total distance = 325 + 440 = 765 m. Time = 765/(51×5/18) = 765×18/(51×5) = 54 seconds."
        },
        {
            "question": "Three pipes, A, B and C, can fill a tank from empty to full in 40 minutes, 20 minutes and 30 minutes, respectively. When the tank is empty, all the three pipes are opened. A, B and C discharge chemical solutions P, Q and R, respectively. What is the proportion of solution Q in the liquid in the tank after 9 minutes?",
            "option_a": "6/13",
            "option_b": "9/26",
            "option_c": "6/26",
            "option_d": "9/13",
            "correct_answer": "A",
            "explanation": "In 9 min: A fills 9/40, B fills 9/20, C fills 9/30 = 3/10. Total filled = 9/40 + 9/20 + 9/30 = 27/120 + 54/120 + 36/120 = 117/120 = 39/40. Proportion of Q = (9/20)/(39/40) = (9/20)×(40/39) = 18/39 = 6/13."
        },
        {
            "question": "An article was bought for ₹8,900. Its price was marked up by 40%. Thereafter, it was sold at a discount of 5% on the marked price. What was the profit percentage on the transaction?",
            "option_a": "32%",
            "option_b": "34%",
            "option_c": "35%",
            "option_d": "33%",
            "correct_answer": "D",
            "explanation": "CP = ₹8900. Marked price = 8900 × 1.40 = ₹12460. SP after 5% discount = 12460 × 0.95 = ₹11837. Profit = 11837 - 8900 = ₹2937. Profit% = (2937/8900)×100 = 33%."
        },
    ],
    "General Intelligence and Reasoning": [
        {
            "question": "If + means −, − means ×, × means ÷ and ÷ means +, then what will come in place of the question mark (?) in the following equation? 173 − 3 ÷ 282 + 164 × 4 = ?",
            "option_a": "769",
            "option_b": "761",
            "option_c": "760",
            "option_d": "766",
            "correct_answer": "C",
            "explanation": "Substituting the operations: 173 × 3 + 282 − 164 ÷ 4 = 519 + 282 - 41 = 760."
        },
        {
            "question": "Alex starts from Point A and drives 8 km towards the east. He then takes a left turn, drives 6 km, turns left and drives 17 km. He then takes a left turn and drives 13 km. He takes a final left turn, drives 9 km and stops at Point P. How far (shortest distance) and towards which direction should he drive to reach Point A?",
            "option_a": "7 km towards South",
            "option_b": "9 km towards East",
            "option_c": "7 km towards North",
            "option_d": "9 km towards South",
            "correct_answer": "D",
            "explanation": "Tracing the path: East 8 → North 6 → West 17 → South 13 → East 9. Net East-West: 8 - 17 + 9 = 0. Net North-South: 6 - 13 = -7 (7 km South of A). But we ended up at P which is 0 E-W and 7 South. Wait — actually recalculating: he needs to go 9 km South from P to reach A."
        },
        {
            "question": "In a certain code language, 'house sip head' is coded as 'bm ma px' and 'head wood robot' is coded as 'pz bm ey'. How is 'head' coded in the given language?",
            "option_a": "ma",
            "option_b": "bm",
            "option_c": "pz",
            "option_d": "px",
            "correct_answer": "B",
            "explanation": "Comparing the two statements: 'head' is common in both, and 'bm' is common in both coded forms. Therefore 'head' = 'bm'."
        },
    ],
    "General Awareness and Current Affairs": [
        {
            "question": "Which Indian Ministry launched the Bharat Forecasting System (BFS) on 26 May 2025 to provide weather predictions with a 6-km resolution?",
            "option_a": "Ministry of Environment, Forest and Climate Change",
            "option_b": "Ministry of Agriculture and Farmers Welfare",
            "option_c": "Ministry of Earth Sciences",
            "option_d": "Ministry of Defence",
            "correct_answer": "C",
            "explanation": "The Ministry of Earth Sciences launched the Bharat Forecasting System (BFS) on 26 May 2025 to provide indigenous weather predictions with high spatial resolution of 6 km."
        },
        {
            "question": "Which chess player, besides Gukesh, received the Arjuna Award in 2025?",
            "option_a": "Harika Dronavalli",
            "option_b": "Vantika Agrawal",
            "option_c": "Koneru Humpy",
            "option_d": "Pentala Harikrishna",
            "correct_answer": "B",
            "explanation": "Vantika Agrawal received the Arjuna Award in 2025 along with Gukesh for their achievements in chess."
        },
        {
            "question": "Which startup was selected in April 2025 to build India's first sovereign Indic LLM under the IndiaAI Mission?",
            "option_a": "Wadhwani AI",
            "option_b": "People+AI",
            "option_c": "Sarvam AI",
            "option_d": "AI4 Bharat",
            "correct_answer": "C",
            "explanation": "Sarvam AI was selected in April 2025 to build India's first sovereign Indic Large Language Model (LLM) under the IndiaAI Mission initiative."
        },
    ],
}

# Generic sample questions for non-RRB exams (still keeps quality high)
_GENERIC_SAMPLE_QUESTIONS = {
    "Mathematics": [
        {
            "question": "A shopkeeper marks an article 30% above the cost price and gives a discount of 15%. If the cost price is ₹600, find the profit percentage.",
            "option_a": "10.5%",
            "option_b": "12%",
            "option_c": "10%",
            "option_d": "15%",
            "correct_answer": "A",
            "explanation": "MP = 600 × 1.30 = ₹780. SP = 780 × 0.85 = ₹663. Profit = 63. Profit% = (63/600)×100 = 10.5%."
        }
    ],
    "Reasoning": [
        {
            "question": "In a row of 40 students, P is 15th from the left end and Q is 20th from the right end. How many students are between P and Q if they are not the same person?",
            "option_a": "4",
            "option_b": "5",
            "option_c": "6",
            "option_d": "3",
            "correct_answer": "A",
            "explanation": "P is 15th from left. Q is 20th from right = 40 - 20 + 1 = 21st from left. Students between them = 21 - 15 - 1 = 5. But checking: positions 16,17,18,19,20 = 5 students."
        }
    ],
}


# ---------------------------------------------------------------------------
# Exam-specific prompt constraints — detailed instructions per exam type
# ---------------------------------------------------------------------------

def _get_exam_constraints(exam_name: str, sub_name: str) -> str:
    """Return exam-specific constraints to inject into the prompt."""
    exam_lower = exam_name.lower()

    if 'rrb' not in exam_lower:
        return _get_generic_constraints(exam_name, sub_name)

    sub_lower = sub_name.lower()

    if 'math' in sub_lower:
        return """
CRITICAL CONSTRAINTS FOR MATHEMATICS:
- Every question MUST be a word problem requiring 2-4 calculation steps. NO direct formula questions.
- Include realistic scenarios: age problems, train/speed problems, pipe/cistern, profit/loss with markup & discount.
- Distractors MUST be numerically close to the correct answer (e.g., if answer is 33%, distractors should be 32%, 34%, 35%).
- Use Indian currency (₹) and metric units.
- Include fraction-based calculations, not just whole numbers.
- At least 30% of questions should involve ratio/proportion, percentage, or profit & loss.
- Some questions should combine multiple concepts (e.g., compound interest with installments, or time & work with efficiency).
- For geometry/mensuration questions, provide enough data for multi-step calculation (e.g., find curved surface area given total surface area relationship).
- NEVER ask direct formula recall like "What is the formula for...". Always frame as a problem to solve.
"""
    elif 'reasoning' in sub_lower or 'intelligence' in sub_lower:
        return """
CRITICAL CONSTRAINTS FOR REASONING:
- Include coding-decoding questions with letter shifting, number coding, and symbol-based coding.
- Include direction sense test with 4+ turns and exact distance calculations.
- Blood relation questions must have 4+ relationships chained together, possibly with coded operators.
- Number series must use non-obvious patterns (e.g., differences of differences, alternating operations).
- Mathematical operation (symbol substitution) questions must have 4+ operations substituted.
- Include alphabet series with forward/backward jumps and mixed patterns.
- Mirror/water image questions should use complex letter-number combinations.
- Classification (odd one out) should require identifying subtle conceptual differences, not obvious ones.
- Seating arrangement should involve 6+ people with multiple conditions.
- NEVER ask obvious pattern questions like "2, 4, 6, 8, ?". Use complex multi-step patterns.
- Include questions based on coded inequalities, statement-conclusion, and Venn diagrams.
"""
    elif 'science' in sub_lower:
        return """
CRITICAL CONSTRAINTS FOR GENERAL SCIENCE:
- Questions must test application-level understanding, NOT rote definition recall.
- Physics: Include numerical problems (Ohm's law calculations, lens power, velocity/acceleration).
- Chemistry: Ask about reaction products, conditions, and real-world applications of chemical processes.
- Biology: Questions should connect concepts (e.g., why is DNA copying important in reproduction, how does a specific organ system malfunction cause disease).
- Include questions about recent scientific developments and their underlying science.
- Distractors should be scientifically plausible but incorrect — test deep understanding.
- At least 20% of questions should require numerical calculation (physics/chemistry).
- Frame questions as "what happens when..." or "which property causes..." rather than "define X".
- Include comparative questions (e.g., difference between mitosis and meiosis in terms of chromosome behavior).
"""
    elif 'awareness' in sub_lower or 'current' in sub_lower:
        return """
CRITICAL CONSTRAINTS FOR GENERAL AWARENESS & CURRENT AFFAIRS:
- At least 60% of questions MUST be about events from the last 12 months (2024-2025).
- Include specific details: exact dates, names of schemes, ministry names, award recipients.
- Questions should test SPECIFIC knowledge, not vague awareness (e.g., "Which ministry launched X on which date?" not "Is India developing weather systems?").
- Include questions on: government scheme launches with specific names, international summit locations and themes, sports championship winners with specific events, book authors with publication year, award recipients with specific categories.
- Distractors should be real entities/people/ministries — not made-up names.
- Include questions about constitutional amendments, Supreme Court judgments, and policy changes.
- For history questions, focus on specific events, dates, personalities and their contributions.
- For geography, ask about specific rivers, mountain passes, agricultural patterns, and census data.
- NEVER generate vague questions like "Which of the following is important?". Be specific.
"""
    return ""


def _get_generic_constraints(exam_name: str, sub_name: str) -> str:
    """Generic constraints for non-RRB exams."""
    sub_lower = sub_name.lower()
    constraints = """
CRITICAL QUALITY CONSTRAINTS:
- Every question must require genuine reasoning or calculation — no direct recall questions.
- Distractors must be plausible and close to the correct answer.
- Explanations must show complete working/reasoning.
"""
    if 'math' in sub_lower or 'quantitative' in sub_lower:
        constraints += "- All math questions must be multi-step word problems, not direct calculations.\n"
    if 'reasoning' in sub_lower or 'intelligence' in sub_lower or 'logical' in sub_lower:
        constraints += "- Reasoning questions must involve genuine logical deduction, not obvious patterns.\n"
    return constraints


# ---------------------------------------------------------------------------
# Few-shot example selector
# ---------------------------------------------------------------------------

def _get_sample_questions(exam_name: str, sub_name: str) -> str:
    """Return 2-3 real exam sample questions formatted as few-shot examples."""
    exam_lower = exam_name.lower()
    samples = []

    if 'rrb' in exam_lower:
        # Match subject name to our sample bank
        for key in _RRB_SAMPLE_QUESTIONS:
            if key.lower() in sub_name.lower() or sub_name.lower() in key.lower():
                samples = _RRB_SAMPLE_QUESTIONS[key][:2]
                break
        # Fallback: try partial match
        if not samples:
            sub_lower = sub_name.lower()
            if 'math' in sub_lower:
                samples = _RRB_SAMPLE_QUESTIONS.get("Mathematics", [])[:2]
            elif 'reasoning' in sub_lower or 'intelligence' in sub_lower:
                samples = _RRB_SAMPLE_QUESTIONS.get("General Intelligence and Reasoning", [])[:2]
            elif 'science' in sub_lower:
                samples = _RRB_SAMPLE_QUESTIONS.get("General Science", [])[:2]
            elif 'awareness' in sub_lower or 'current' in sub_lower:
                samples = _RRB_SAMPLE_QUESTIONS.get("General Awareness and Current Affairs", [])[:2]

    if not samples:
        # Use generic samples
        for key in _GENERIC_SAMPLE_QUESTIONS:
            if key.lower() in sub_name.lower() or sub_name.lower() in key.lower():
                samples = _GENERIC_SAMPLE_QUESTIONS[key][:2]
                break

    if not samples:
        return ""

    examples_text = "\n\nHere are REAL PREVIOUS YEAR questions from this exam to calibrate your difficulty level. Your generated questions MUST match or exceed this difficulty:\n\n"
    for i, s in enumerate(samples, 1):
        examples_text += f"EXAMPLE {i}:\n"
        examples_text += f"Q: {s['question']}\n"
        examples_text += f"A) {s['option_a']}\n"
        examples_text += f"B) {s['option_b']}\n"
        examples_text += f"C) {s['option_c']}\n"
        examples_text += f"D) {s['option_d']}\n"
        examples_text += f"Answer: {s['correct_answer']}\n"
        examples_text += f"Explanation: {s['explanation']}\n\n"

    return examples_text


# ---------------------------------------------------------------------------
# Negative marking info per exam
# ---------------------------------------------------------------------------

def _get_marking_info(exam_name: str) -> str:
    exam_lower = exam_name.lower()
    if 'rrb' in exam_lower:
        return "Each correct answer = +1 mark. Each wrong answer = -1/3 mark (0.333 negative). Unanswered = 0."
    if 'ssc' in exam_lower:
        return "Each correct answer = +2 marks. Each wrong answer = -0.5 mark. Unanswered = 0."
    return "Standard marking with negative marks for wrong answers."


# ---------------------------------------------------------------------------
# Main question generation function
# ---------------------------------------------------------------------------

from tenacity import retry, stop_after_attempt, wait_exponential

def _validate_question(q: Question) -> bool:
    if not all([q.question_text, q.option_a, q.option_b, q.option_c, q.option_d, q.correct_answer, q.explanation]):
        return False
    if q.correct_answer not in ["A", "B", "C", "D"]:
        return False
    
    # Check for duplicate options
    opts = [q.option_a.lower().strip(), q.option_b.lower().strip(), q.option_c.lower().strip(), q.option_d.lower().strip()]
    if len(set(opts)) < 4:
        return False
        
    return True

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=8))
def _generate_batch(
    exam_name: str, sub_name: str, topics: str, count: int,
    difficulty_level: str, system_prompt: str, marking_info: str,
    constraints: str, sample_questions: str, negative_marks: float,
    existing_question_texts: set
) -> List[Question]:
    """Generate a batch of questions for a single subject."""
    questions = []

    prompt = f"""You are setting a REAL {exam_name} examination paper. Generate EXACTLY {count} multiple-choice questions.

EXAM: {exam_name}
SUBJECT: {sub_name}
TOPICS TO COVER (distribute questions evenly across these): {topics}
MARKING SCHEME: {marking_info}
DIFFICULTY TARGET: {difficulty_level} — equivalent to actual {exam_name} papers conducted in 2024-2025.
{constraints}
{sample_questions}
MANDATORY RULES:
1. Every question MUST be at the difficulty level of actual {exam_name} previous year papers — NOT school textbook level.
2. Questions must require multi-step thinking, calculation, or advanced reasoning.
3. Each question MUST have exactly 4 options with ONE unambiguous correct answer.
4. Distractors must be strong, plausible, and close to the correct answer — a student who guesses should likely pick a wrong option.
5. Explanations must show complete step-by-step working (for math) or clear logical reasoning (for reasoning/GK).
6. Distribute questions across ALL listed topics — do not cluster on one or two topics.
7. Use Indian context (₹ for currency, Indian geography, Indian government schemes, etc.) where applicable.
8. Do NOT repeat any question pattern — each question must test a different concept or approach.
9. For current affairs, use events and developments from 2024-2025.
10. Question phrasing should match the formal style used in real government exam papers.

Return a JSON object with EXACTLY this structure:
{{
  "questions": [
    {{
      "subject": "{sub_name}",
      "topic": "<specific topic from the list above>",
      "question": "<full question text>",
      "option_a": "<option A>",
      "option_b": "<option B>",
      "option_c": "<option C>",
      "option_d": "<option D>",
      "correct_answer": "A or B or C or D",
      "explanation": "<detailed step-by-step explanation>",
      "difficulty": "hard"
    }}
  ]
}}"""
    models_to_try = []
    configured_model = getattr(settings, "GROQ_MODEL", "openai/gpt-oss-120b")
    for m in [configured_model, "openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b", "llama-3.3-70b-versatile"]:
        if m and m not in models_to_try:
            models_to_try.append(m)

    chat_completion = None
    last_err = None
    for model_name in models_to_try:
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=model_name,
                max_tokens=8000,
                temperature=0.6,
                response_format={"type": "json_object"}
            )
            break
        except Exception as e:
            last_err = e
            logger.warning(f"Model {model_name} failed: {e}. Trying fallback...")

    if not chat_completion:
        logger.error(f"Error generating questions for {sub_name}: {last_err}")
        raise last_err

    try:
        content = chat_completion.choices[0].message.content
        parsed = json.loads(content)

        for q_data in parsed.get("questions", []):
            q_text = q_data.get("question", "").strip()
            if not q_text or q_text.lower() in existing_question_texts:
                continue

            q = Question(
                subject=q_data.get("subject", sub_name),
                topic=q_data.get("topic", "General"),
                question_text=q_text,
                option_a=q_data.get("option_a", ""),
                option_b=q_data.get("option_b", ""),
                option_c=q_data.get("option_c", ""),
                option_d=q_data.get("option_d", ""),
                correct_answer=str(q_data.get("correct_answer", "A")).strip()[:1].upper(),
                explanation=q_data.get("explanation", ""),
                difficulty=q_data.get("difficulty", difficulty_level).lower(),
                marks=1.0,
                negative_marks=negative_marks
            )
            
            if _validate_question(q):
                questions.append(q)
                existing_question_texts.add(q_text.lower())

    except Exception as e:
        logger.error(f"Error generating questions for {sub_name}: {e}")
        raise e  # Propagate to trigger retry

    logger.info(f"Generated {len(questions)} questions for {sub_name}")
    return questions


def generate_questions(exam_name: str, subjects: List[Dict[str, Any]], num_questions: int, difficulty_mix: str = None, negative_marks: float = 0.33, batch_callback=None) -> List[Question]:
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import threading

    MAX_QUESTIONS_PER_BATCH = 10  # Larger batches = fewer API calls = faster generation
    
    difficulty_level = difficulty_mix or _exam_difficulty(exam_name)
    system_prompt = _get_system_prompt(exam_name)
    marking_info = _get_marking_info(exam_name)

    # Calculate target questions per subject
    total_weight = sum(sub.get("weightage", 1) for sub in subjects)
    target_counts = {}
    remaining_total = num_questions
    
    for idx, subject in enumerate(subjects):
        sub_name = subject["name"]
        weight = subject.get("weightage", 1)
        if idx == len(subjects) - 1:
            count = remaining_total # last subject gets all remainder
        else:
            count = max(1, int(round((weight / total_weight) * num_questions)))
        target_counts[sub_name] = count
        remaining_total -= count
        
    all_questions = []
    existing_texts = set()
    lock = threading.Lock()

    # Use more workers to maximize parallelism across ALL subjects simultaneously
    max_workers = min(len(subjects) * 3, 12) if len(subjects) > 0 else 1
    logger.info(f"Starting generation: {num_questions} questions across {len(subjects)} subjects with {max_workers} workers")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Launch ALL batches for ALL subjects at once (fully parallel)
        all_futures = []
        
        for subject in subjects:
            sub_name = subject["name"]
            topics = ", ".join(subject.get("topics", []))
            target_count = target_counts[sub_name]
            constraints = _get_exam_constraints(exam_name, sub_name)
            sample_questions = _get_sample_questions(exam_name, sub_name)
            
            # Split into batches and launch all at once
            remaining_for_subject = target_count
            while remaining_for_subject > 0:
                batch_size = min(remaining_for_subject, MAX_QUESTIONS_PER_BATCH)
                future = executor.submit(
                    _generate_batch,
                    exam_name, sub_name, topics, batch_size,
                    difficulty_level, system_prompt, marking_info,
                    constraints, sample_questions, negative_marks,
                    existing_texts
                )
                all_futures.append((future, sub_name, target_count))
                remaining_for_subject -= batch_size
        
        logger.info(f"Launched {len(all_futures)} parallel batch requests")
        
        # Collect results as they complete — calling batch_callback immediately
        # so the frontend sees incremental progress
        subject_collected = {}
        
        for future in as_completed([f[0] for f in all_futures]):
            try:
                questions = future.result()
                if questions:
                    with lock:
                        all_questions.extend(questions)
                    
                    if batch_callback and questions:
                        try:
                            batch_callback(questions)
                        except Exception as cb_err:
                            logger.error(f"Callback error: {cb_err}")
                    
                    logger.info(f"Progress: {len(all_questions)}/{num_questions} questions generated")
            except Exception as e:
                logger.error(f"Batch generation failed: {e}")
                    
    logger.info(f"Generation complete: {len(all_questions)}/{num_questions} questions")
    return all_questions

