from sqlalchemy.orm import Session
from app.models.exam import ExamCategory, Exam


def seed_database(db: Session):
    categories = [
        {"name": "SSC", "description": "Staff Selection Commission (CGL, CHSL, CPO, MTS, GD, JE, Steno)", "icon": "building"},
        {"name": "Banking", "description": "Banking Exams (IBPS, SBI, RBI, NABARD, LIC)", "icon": "bank"},
        {"name": "RRB", "description": "Railway Recruitment Board", "icon": "train"},
        {"name": "UPSC", "description": "Union Public Service Commission (Prelims, Mains, Interview Prep)", "icon": "landmark"},
        {"name": "State PSC", "description": "State Public Service Commission and State Government Exams", "icon": "flag"},
        {"name": "Teaching", "description": "Teaching and Education Exams (CTET, TET, UGC NET, KVS)", "icon": "school"},
        {"name": "Defence", "description": "Defence and Military Entrance Exams", "icon": "shield"},
        {"name": "Police", "description": "Police and Law Enforcement Recruitment Exams", "icon": "police"},
        {"name": "Engineering", "description": "Engineering and Technical Entrance / Recruitment Exams", "icon": "engineering"},
        {"name": "Medical", "description": "Medical and Healthcare Entrance Exams", "icon": "medical"},
        {"name": "Management", "description": "MBA and Management Entrance Exams", "icon": "business"},
        {"name": "Law", "description": "Law Entrance and Recruitment Exams", "icon": "gavel"},
    ]

    cat_objs = {}
    existing_category_names = {cat.name for cat in db.query(ExamCategory).all()}
    for cat_data in categories:
        if cat_data["name"] not in existing_category_names:
            cat = ExamCategory(**cat_data)
            db.add(cat)
            db.flush()
            cat_objs[cat.name] = cat
        else:
            cat = db.query(ExamCategory).filter(ExamCategory.name == cat_data["name"]).first()
            cat_objs[cat.name] = cat

    # Define standard subjects for each category
    ssc_subjects = [
        {"name": "Reasoning", "weightage": 25, "topics": ["Logic", "Analogies", "Puzzles"]},
        {"name": "General Awareness", "weightage": 25, "topics": ["Current Affairs", "History", "Geography"]},
        {"name": "Quantitative Aptitude", "weightage": 25, "topics": ["Arithmetic", "Advanced Math"]},
        {"name": "English", "weightage": 25, "topics": ["Grammar", "Vocabulary", "Comprehension"]},
    ]

    banking_subjects = [
        {"name": "English", "weightage": 20, "topics": ["Reading Comprehension", "Grammar"]},
        {"name": "Quantitative Aptitude", "weightage": 30, "topics": ["Data Interpretation", "Arithmetic"]},
        {"name": "Reasoning", "weightage": 30, "topics": ["Puzzles", "Seating Arrangement", "Syllogism"]},
        {"name": "General/Banking Awareness", "weightage": 20, "topics": ["Current Affairs", "Banking Terms"]},
    ]

    rrb_subjects = [
        {"name": "Mathematics", "weightage": 25, "topics": ["Number System", "Algebra", "Geometry"]},
        {"name": "General Intelligence & Reasoning", "weightage": 25, "topics": ["Analogies", "Coding-Decoding"]},
        {"name": "General Awareness", "weightage": 25, "topics": ["Current Affairs", "Indian Polity"]},
        {"name": "General Science", "weightage": 25, "topics": ["Physics", "Chemistry", "Life Sciences"]},
    ]

    upsc_subjects = [
        {"name": "Indian History", "weightage": 20, "topics": ["Ancient", "Medieval", "Modern"]},
        {"name": "Geography", "weightage": 20, "topics": ["Physical", "Human"]},
        {"name": "Indian Polity", "weightage": 20, "topics": ["Constitution", "Governance"]},
        {"name": "Economy", "weightage": 20, "topics": ["Macroeconomics", "Budget"]},
        {"name": "Science & Tech", "weightage": 20, "topics": ["General Science", "Environment"]},
    ]

    state_subjects = [
        {"name": "General Knowledge", "weightage": 30, "topics": ["State History", "State Geography"]},
        {"name": "Reasoning", "weightage": 30, "topics": ["Logic", "Decision Making"]},
        {"name": "Mathematics", "weightage": 40, "topics": ["Arithmetic", "Data Analysis"]},
    ]

    teaching_subjects = [
        {"name": "Child Development", "weightage": 30, "topics": ["Pedagogy", "Learning"]},
        {"name": "Language", "weightage": 20, "topics": ["Grammar", "Comprehension"]},
        {"name": "General Awareness", "weightage": 25, "topics": ["Current Affairs", "Education"]},
        {"name": "Reasoning", "weightage": 25, "topics": ["Analytical Ability"]},
    ]

    defence_subjects = [
        {"name": "General Knowledge", "weightage": 30, "topics": ["Current Affairs", "History"]},
        {"name": "Reasoning", "weightage": 25, "topics": ["Analytical", "Puzzles"]},
        {"name": "Maths", "weightage": 25, "topics": ["Arithmetic", "Algebra"]},
        {"name": "English", "weightage": 20, "topics": ["Vocabulary", "Grammar"]},
    ]

    police_subjects = [
        {"name": "Reasoning", "weightage": 30, "topics": ["Analogy", "Puzzle"]},
        {"name": "Quantitative Aptitude", "weightage": 20, "topics": ["Arithmetic"]},
        {"name": "General Knowledge", "weightage": 30, "topics": ["Current Affairs", "Law"]},
        {"name": "English", "weightage": 20, "topics": ["Comprehension", "Vocabulary"]},
    ]

    engineering_subjects = [
        {"name": "Mathematics", "weightage": 30, "topics": ["Calculus", "Algebra"]},
        {"name": "Reasoning", "weightage": 20, "topics": ["Analytical", "Problem Solving"]},
        {"name": "Technical Aptitude", "weightage": 30, "topics": ["Core Concepts", "Numerical"]},
        {"name": "General Awareness", "weightage": 20, "topics": ["Science", "Current Affairs"]},
    ]

    medical_subjects = [
        {"name": "Physics", "weightage": 25, "topics": ["Mechanics", "Modern Physics"]},
        {"name": "Chemistry", "weightage": 25, "topics": ["Physical Chemistry", "Organic Chemistry"]},
        {"name": "Biology", "weightage": 30, "topics": ["Human Physiology", "Genetics"]},
        {"name": "General Awareness", "weightage": 20, "topics": ["Current Affairs", "Health"]},
    ]

    management_subjects = [
        {"name": "Verbal Ability", "weightage": 25, "topics": ["Reading Comprehension", "Grammar"]},
        {"name": "Quantitative Aptitude", "weightage": 25, "topics": ["Arithmetic", "Data Interpretation"]},
        {"name": "Logical Reasoning", "weightage": 25, "topics": ["Puzzles", "Analytical"]},
        {"name": "General Awareness", "weightage": 25, "topics": ["Current Affairs", "Business"]},
    ]

    law_subjects = [
        {"name": "Legal Reasoning", "weightage": 30, "topics": ["Principles", "Arguments"]},
        {"name": "Logical Reasoning", "weightage": 25, "topics": ["Analytical", "Syllogism"]},
        {"name": "English", "weightage": 25, "topics": ["Comprehension", "Vocabulary"]},
        {"name": "General Knowledge", "weightage": 20, "topics": ["Current Affairs", "Law"]},
    ]

    exams_data = []

    ssc_exams = [
        ("SSC CGL Tier I", 100, 200, 60, 0.5),
        ("SSC CHSL Tier I", 100, 200, 60, 0.5),
        ("SSC CPO Paper I", 200, 200, 120, 0.25),
        ("SSC MTS Session I & II", 90, 270, 90, 1.0),
        ("SSC GD CBT", 80, 160, 60, 0.5),
        ("SSC JE Paper I", 200, 200, 120, 0.25),
        ("SSC Stenographer CBT", 200, 200, 120, 0.25),
        ("SSC Selection Post CBT", 100, 200, 60, 0.5),
    ]
    for name, q, m, t, nm in ssc_exams:
        exams_data.append({"category_id": cat_objs["SSC"].id, "name": name, "description": f"{name} Examination", "total_questions": q, "total_marks": m, "duration_minutes": t, "negative_marking": nm, "subjects": ssc_subjects})

    bank_exams = [
        ("IBPS PO Prelims", 100, 100, 60, 0.25),
        ("IBPS Clerk Prelims", 100, 100, 60, 0.25),
        ("IBPS RRB PO Prelims", 80, 80, 45, 0.25),
        ("IBPS RRB Clerk Prelims", 80, 80, 45, 0.25),
        ("SBI PO Prelims", 100, 100, 60, 0.25),
        ("SBI Clerk Prelims", 100, 100, 60, 0.25),
        ("RBI Grade B Phase I", 200, 200, 120, 0.25),
        ("RBI Assistant Prelims", 100, 100, 60, 0.25),
        ("NABARD Grade A Prelims", 200, 200, 120, 0.25),
        ("LIC AAO Prelims", 100, 100, 60, 0.25),
        ("LIC ADO Prelims", 100, 100, 60, 0.25),
    ]
    for name, q, m, t, nm in bank_exams:
        exams_data.append({"category_id": cat_objs["Banking"].id, "name": name, "description": f"{name} Examination", "total_questions": q, "total_marks": m, "duration_minutes": t, "negative_marking": nm, "subjects": banking_subjects})

    rrb_exams = [
        ("RRB NTPC (Graduate) CBT 1", 100, 100, 90, 0.33),
        ("RRB NTPC (UG) CBT 1", 100, 100, 90, 0.33),
        ("RRB Group D CBT", 100, 100, 90, 0.33),
        ("RRB ALP CBT 1", 75, 75, 60, 0.33),
        ("RRB Technician CBT", 100, 100, 90, 0.33),
        ("RRB JE CBT 1", 100, 100, 90, 0.33),
    ]
    for name, q, m, t, nm in rrb_exams:
        exams_data.append({"category_id": cat_objs["RRB"].id, "name": name, "description": f"{name} Examination", "total_questions": q, "total_marks": m, "duration_minutes": t, "negative_marking": nm, "subjects": rrb_subjects})

    upsc_exams = [
        ("UPSC Prelims GS Paper I", 100, 200, 120, 0.66),
        ("UPSC Prelims CSAT", 80, 200, 120, 0.66),
        ("UPSC Mains General Studies", 100, 300, 180, 0.66),
    ]
    for name, q, m, t, nm in upsc_exams:
        exams_data.append({"category_id": cat_objs["UPSC"].id, "name": name, "description": f"{name} Examination", "total_questions": q, "total_marks": m, "duration_minutes": t, "negative_marking": nm, "subjects": upsc_subjects})

    state_exams = [
        ("State PSC Prelims", 100, 200, 120, 0.5),
        ("State Police SI", 100, 200, 90, 0.5),
        ("State Revenue Officer", 90, 180, 90, 0.5),
    ]
    for name, q, m, t, nm in state_exams:
        exams_data.append({"category_id": cat_objs["State PSC"].id, "name": name, "description": f"{name} Examination", "total_questions": q, "total_marks": m, "duration_minutes": t, "negative_marking": nm, "subjects": state_subjects})

    teaching_exams = [
        ("CTET Paper I", 150, 150, 150, 0.0),
        ("CTET Paper II", 150, 150, 150, 0.0),
        ("UGC NET Paper I", 50, 100, 60, 0.0),
        ("KVS PRT", 100, 100, 90, 0.0),
    ]
    for name, q, m, t, nm in teaching_exams:
        exams_data.append({"category_id": cat_objs["Teaching"].id, "name": name, "description": f"{name} Examination", "total_questions": q, "total_marks": m, "duration_minutes": t, "negative_marking": nm, "subjects": teaching_subjects})

    defence_exams = [
        ("NDA Exam", 120, 300, 150, 0.33),
        ("CDS Exam", 100, 200, 120, 0.33),
        ("AFCAT Exam", 100, 300, 120, 0.0),
    ]
    for name, q, m, t, nm in defence_exams:
        exams_data.append({"category_id": cat_objs["Defence"].id, "name": name, "description": f"{name} Examination", "total_questions": q, "total_marks": m, "duration_minutes": t, "negative_marking": nm, "subjects": defence_subjects})

    police_exams = [
        ("UP Police SI", 160, 160, 120, 0.25),
        ("Delhi Police Constable", 100, 100, 90, 0.25),
        ("BSF Constable", 100, 100, 90, 0.25),
    ]
    for name, q, m, t, nm in police_exams:
        exams_data.append({"category_id": cat_objs["Police"].id, "name": name, "description": f"{name} Examination", "total_questions": q, "total_marks": m, "duration_minutes": t, "negative_marking": nm, "subjects": police_subjects})

    engineering_exams = [
        ("GATE Exam", 65, 100, 180, 0.33),
        ("JEE Main", 90, 300, 180, 0.0),
        ("IES Exam", 100, 200, 180, 0.33),
    ]
    for name, q, m, t, nm in engineering_exams:
        exams_data.append({"category_id": cat_objs["Engineering"].id, "name": name, "description": f"{name} Examination", "total_questions": q, "total_marks": m, "duration_minutes": t, "negative_marking": nm, "subjects": engineering_subjects})

    medical_exams = [
        ("NEET UG", 180, 720, 180, 0.0),
        ("NEET PG", 200, 800, 210, 0.0),
        ("AIIMS Paramedical", 100, 400, 120, 0.0),
    ]
    for name, q, m, t, nm in medical_exams:
        exams_data.append({"category_id": cat_objs["Medical"].id, "name": name, "description": f"{name} Examination", "total_questions": q, "total_marks": m, "duration_minutes": t, "negative_marking": nm, "subjects": medical_subjects})

    management_exams = [
        ("CAT Exam", 66, 198, 120, 0.0),
        ("CMAT Exam", 100, 400, 180, 0.25),
        ("XAT Exam", 100, 100, 180, 0.0),
    ]
    for name, q, m, t, nm in management_exams:
        exams_data.append({"category_id": cat_objs["Management"].id, "name": name, "description": f"{name} Examination", "total_questions": q, "total_marks": m, "duration_minutes": t, "negative_marking": nm, "subjects": management_subjects})

    law_exams = [
        ("CLAT Exam", 120, 120, 120, 0.0),
        ("AILET Exam", 150, 150, 120, 0.0),
        ("SLAT Exam", 90, 90, 90, 0.0),
    ]
    for name, q, m, t, nm in law_exams:
        exams_data.append({"category_id": cat_objs["Law"].id, "name": name, "description": f"{name} Examination", "total_questions": q, "total_marks": m, "duration_minutes": t, "negative_marking": nm, "subjects": law_subjects})

    existing_exam_names = {exam.name for exam in db.query(Exam).all()}
    for exam_data in exams_data:
        if exam_data["name"] not in existing_exam_names:
            db.add(Exam(**exam_data))

    db.commit()

