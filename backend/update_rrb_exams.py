import sqlite3
import json
import shutil
import os

DB_PATH = r"c:\Users\Dell\Desktop\mockbees\backend\mockbees.db"
BAK_PATH = r"c:\Users\Dell\Desktop\mockbees\backend\mockbees.db.bak"

def get_subjects(exam_type):
    group_d_gs = {
        "name": "General Science",
        "weightage": 25,
        "topics": [
            "Work/Energy/Power", "Light & Optics (Refraction/Reflection/Lenses)",
            "Electricity (Resistance/Ohm's Law/Power)", "Motion & Newton's Laws",
            "Sound Waves", "Heat & Thermodynamics", "Chemical Reactions & Equations",
            "Acids Bases & Salts", "Metals & Non-metals", "Carbon & its Compounds",
            "Periodic Table & Classification", "Cell Biology & Cell Division (Mitosis/Meiosis)",
            "Human Physiology (Respiratory/Circulatory/Digestive)", "Diseases & Prevention",
            "Genetics & Heredity", "Plant Biology & Photosynthesis", "Reproduction in Plants & Animals",
            "Nutrition & Food", "Environmental Science & Ecology"
        ]
    }
    
    group_d_math = {
        "name": "Mathematics",
        "weightage": 25,
        "topics": [
            "Number System & HCF/LCM", "Percentage", "Profit Loss & Discount",
            "Simple & Compound Interest", "Ratio Proportion & Partnership", "Average & Ages Problems",
            "Time & Work (Pipes & Cisterns)", "Time Speed & Distance (Train Problems)",
            "Algebra (Linear Equations/Polynomials/Substitution)", "Geometry (Triangles/Circles/Quadrilaterals)",
            "Mensuration (Surface Area/Volume of Solids)", "Trigonometry (Heights & Distances)",
            "Data Interpretation (Tables/Bar Charts)", "Statistics (Mean/Median/Mode)",
            "Simplification & Approximation"
        ]
    }
    
    group_d_reasoning = {
        "name": "General Intelligence & Reasoning",
        "weightage": 25,
        "topics": [
            "Number Series & Patterns", "Letter/Alphabet Series", "Coding-Decoding (Letter/Number/Symbol)",
            "Analogy (Word & Number)", "Blood Relations", "Direction Sense Test", "Syllogism",
            "Mirror & Water Image", "Paper Folding & Cutting", "Venn Diagrams",
            "Mathematical Operations (Symbol Substitution)", "Order & Ranking", "Classification (Odd One Out)",
            "Statement & Conclusion", "Seating Arrangement", "Calendar & Clock Problems",
            "Counting Figures", "Embedded Figures", "Dice & Cubes"
        ]
    }
    
    group_d_ga = {
        "name": "General Awareness & Current Affairs",
        "weightage": 25,
        "topics": [
            "Current Affairs (Government Schemes/Awards/Appointments/Summits)", "Indian Polity & Constitution",
            "Indian History (Ancient/Medieval/Modern/Freedom Movement)", "Indian Geography (Physical/Economic/Climate)",
            "Indian Economy (Budget/GDP/Banking/RBI Policies)", "Science & Technology (Space Missions/Defense/Digital India)",
            "Sports & Championships", "Books & Authors", "Important Days & Themes",
            "International Organizations (UN/WHO/WTO)", "Culture & Heritage", "Awards & Honours (Padma/Bharat Ratna/Nobel)"
        ]
    }
    
    group_d = [group_d_gs, group_d_math, group_d_reasoning, group_d_ga]
    
    ntpc_math = dict(group_d_math)
    ntpc_math["topics"] = list(ntpc_math["topics"]) + ["Data Sufficiency", "Number Series (Advanced)"]
    
    ntpc_reasoning = dict(group_d_reasoning)
    ntpc_reasoning["topics"] = list(ntpc_reasoning["topics"]) + ["Statement & Assumption", "Logical Reasoning", "Analytical Reasoning"]
    
    ntpc_ga = dict(group_d_ga)
    ntpc_ga["name"] = "General Awareness"
    ntpc_ga["topics"] = list(ntpc_ga["topics"]) + ["Computer Awareness basics"]
    
    ntpc_gs = dict(group_d_gs)
    
    ntpc_graduate = [ntpc_math, ntpc_reasoning, ntpc_ga, ntpc_gs]
    
    alp_math = {
        "name": "Mathematics",
        "weightage": 25,
        "topics": ["Number System", "BODMAS", "Fractions/Decimals", "LCM/HCF", "Ratio/Proportion", "Percentage", "Mensuration", "Time & Work", "Time Speed & Distance", "Simple & Compound Interest", "Algebra", "Geometry", "Trigonometry", "Statistics"]
    }
    
    alp_reasoning = {
        "name": "General Intelligence & Reasoning",
        "weightage": 25,
        "topics": ["Analogies", "Alphabetical/Number Series", "Coding-Decoding", "Mathematical Operations", "Relationships", "Syllogism", "Jumbling", "Venn Diagram", "Data Interpretation", "Statement & Conclusion", "Direction Sense", "Blood Relations"]
    }
    
    alp_gs = {
        "name": "General Science",
        "weightage": 25,
        "topics": ["Physics (Units/Measurements/Force/Motion/Work/Energy/Heat/Light/Sound/Electricity)", "Chemistry (Chemical Reactions/Elements/Compounds/Mixtures/Acids/Bases/Salts/Metals)", "Biology (Cell Structure/Human Body/Diseases/Food/Nutrition/Health/Hygiene/Environment)"]
    }
    
    alp_ga = {
        "name": "General Awareness & Current Affairs",
        "weightage": 25,
        "topics": ["Current Events", "Science & Technology", "Sports", "Culture", "Economy", "Polity", "Important Personalities", "Important Days"]
    }
    
    alp = [alp_math, alp_reasoning, alp_gs, alp_ga]
    
    tech_math = dict(alp_math)
    tech_math["topics"] = list(tech_math["topics"]) + ["Profit & Loss", "Average", "Ages"]
    
    tech_ga = dict(alp_ga)
    tech_ga["topics"] = list(tech_ga["topics"]) + ["Indian History", "Geography"]
    
    technician = [tech_math, alp_reasoning, alp_gs, tech_ga]
    
    je_math = {
        "name": "Mathematics",
        "weightage": 25,
        "topics": ["Number System", "BODMAS", "Decimals/Fractions", "LCM/HCF", "Ratio/Proportion", "Percentage", "Mensuration", "Time & Work", "Time Speed & Distance", "SI/CI", "Algebra", "Geometry & Trigonometry", "Elementary Statistics"]
    }
    
    je_reasoning = {
        "name": "General Intelligence & Reasoning",
        "weightage": 25,
        "topics": ["Analogies", "Alphabetical/Number Series", "Coding-Decoding", "Mathematical Operations", "Relationships", "Syllogism", "Venn Diagram", "Data Interpretation", "Statement & Conclusion", "Direction Sense", "Blood Relations", "Spatial Reasoning"]
    }
    
    je_ga = {
        "name": "General Awareness",
        "weightage": 25,
        "topics": ["Current Affairs", "Indian Polity", "Indian History", "Geography", "Economy", "Physics", "Chemistry", "Biology", "Computer Basics", "Sports", "Awards"]
    }
    
    je = [je_math, je_reasoning, je_ga, group_d_gs]
    
    if exam_type == "group_d":
        return group_d
    elif exam_type == "ntpc_grad":
        return ntpc_graduate
    elif exam_type == "ntpc_ug":
        return ntpc_graduate # "Same as NTPC Graduate" based on prompt
    elif exam_type == "alp":
        return alp
    elif exam_type == "technician":
        return technician
    elif exam_type == "je":
        return je
    
    return []

def main():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        # Try to continue if running from different dir, though path is absolute
        return
        
    print(f"Backing up database to {BAK_PATH}")
    shutil.copy2(DB_PATH, BAK_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    updates = [
        (1, get_subjects("ntpc_grad")),
        (25, get_subjects("ntpc_grad")),
        (26, get_subjects("ntpc_ug")),
        (27, get_subjects("group_d")),
        (28, get_subjects("alp")),
        (29, get_subjects("technician")),
        (30, get_subjects("je")),
    ]
    
    # Check schema to see what the duration column is named (duration or duration_minutes)
    cursor.execute("PRAGMA table_info(exams)")
    columns = [col[1] for col in cursor.fetchall()]
    dur_col = "duration_minutes" if "duration_minutes" in columns else "duration" if "duration" in columns else None
    
    for exam_id, subjects in updates:
        subjects_json = json.dumps(subjects)
        cursor.execute("UPDATE exams SET subjects = ? WHERE id = ?", (subjects_json, exam_id))
        
    if dur_col:
        cursor.execute(f"UPDATE exams SET {dur_col} = 90 WHERE id = 1")
    
    conn.commit()
    print("Updates applied successfully.")
    
    print("\n--- Verifying Updates ---")
    cursor.execute("SELECT id, name, duration_minutes, subjects FROM exams WHERE id IN (1,25,26,27,28,29,30)")
    rows = cursor.fetchall()
    for r in rows:
        print(f"ID: {r[0]} | Name: {r[1]} | Duration: {r[2]}")
        # Truncate subjects for printing
        subj = json.loads(r[3]) if r[3] else []
        for s in subj:
            print(f"  - {s.get('name')} (Wt: {s.get('weightage')}): {len(s.get('topics', []))} topics")
        print()
        
    conn.close()

if __name__ == '__main__':
    main()
