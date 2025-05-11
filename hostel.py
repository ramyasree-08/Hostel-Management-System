import sqlite3
import pandas as pd
from collections import deque
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np



patient_queue = deque()

class LinkedListNode:
    def __init__(self, patient_data):
        self.data = patient_data
        self.next = None

class PatientLinkedList:
    def __init__(self):
        self.head = None

    def add_patient(self, patient_data):
        new_node = LinkedListNode(patient_data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def display_patients(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

assignment_history = [] 
severity_priority = {
    "Severe": 1,
    "Moderate": 2,
    "Mild": 3
}
disease_symptoms = {
    " Cold": ["runny nose", "sore throat", "cough", "sneezing", "fatigue"],
    "Flu": ["fever", "cold","body aches", "fatigue", "cough","sneezing", "headache"],
    "COVID-19": ["fever", "dry cough", "tiredness", "loss of taste or smell"],
    "Allergies": ["sneezing", "itchy eyes", "runny nose", "congestion"],
    "Migraine": ["severe headache", "nausea", "sensitivity to light", "sensitivity to sound"],
    "Food Poisoning": ["nausea", "vomiting", "diarrhea", "abdominal pain", "fever"],
    "Asthma": ["shortness of breath", "wheezing", "chest tightness", "coughing"],
    "Diabetes": ["increased thirst", "frequent urination", "blurred vision", "fatigue"],
    "Hypertension": ["headache", "shortness of breath", "nosebleeds", "chest pain"],
    "Arthritis": ["joint pain", "stiffness", "swelling", "decreased range of motion"]
}


class DepartmentNode:
    def __init__(self, department_name):
        self.name = department_name
        self.left = None
        self.right = None

class DepartmentTree:
    def __init__(self):
        self.root = None

    def insert(self, department_name):
        if not self.root:
            self.root = DepartmentNode(department_name)
        else:
            self._insert(self.root, department_name)

    def _insert(self, current, department_name):
        if department_name < current.name:
            if current.left:
                self._insert(current.left, department_name)
            else:
                current.left = DepartmentNode(department_name)
        else:
            if current.right:
                self._insert(current.right, department_name)
            else:
                current.right = DepartmentNode(department_name)

    def search(self, department_name):
        return self._search(self.root, department_name)

    def _search(self, current, department_name):
        if not current:
            return None
        if department_name == current.name:
            return current
        elif department_name < current.name:
            return self._search(current.left, department_name)
        else:
            return self._search(current.right, department_name)

department_tree = DepartmentTree()
departments = ['Cardiology', 'Neurology', 'Pediatrics', 'Oncology', 'Orthopedics', 'Dermatology']
for department in departments:
    department_tree.insert(department)


disease_department_map = {
    "Heart Disease": "Cardiology",
    "Stroke"       : "Neurology",
    "Child Care"   : "Pediatrics",
    "Cancer"       : "Oncology",
    "Bone Fracture": "Orthopedics",
    "Skin Allergy" : "Dermatology",
    
}


def setup_database():
    conn = sqlite3.connect('hospital.db', timeout=10)
    cursor = conn.cursor()

    
    try:
       
        cursor.execute('DROP TABLE IF EXISTS Tasks')
       
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS Departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department_id INTEGER,
            password TEXT NOT NULL,
            FOREIGN KEY (department_id) REFERENCES Departments(id)
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            disease TEXT NOT NULL,
            severity TEXT NOT NULL,
            doctor_id INTEGER,
            tasks_completed INTEGER DEFAULT 0,
            total_discount INTEGER DEFAULT 0,
            FOREIGN KEY (doctor_id) REFERENCES Doctors(id)
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Symptoms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            symptom_name TEXT NOT NULL,
            severity INTEGER NOT NULL,
            date TEXT NOT NULL,
            duration TEXT,
            triggers TEXT,
            FOREIGN KEY (username) REFERENCES Users(username)
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            description TEXT NOT NULL,
            discount INTEGER NOT NULL
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS TaskCompletions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            task_id INTEGER,
            FOREIGN KEY (patient_id) REFERENCES Patients(id),
            FOREIGN KEY (task_id) REFERENCES Tasks(id)
        )''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS HealthCards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                max_amount INTEGER,
                priority INTEGER
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Treatments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                health_card_name TEXT,
                treatment_name TEXT,
                treatment_priority INTEGER,
                FOREIGN KEY (health_card_name) REFERENCES HealthCards(name)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PatientsHealth (
            patient_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            health_card TEXT NOT NULL,
            claimed_treatment TEXT,
            claimed_amount INTEGER,
            urgency INTEGER,
            max_amount INTEGER,  
            remaining_amount INTEGER  

            )
        ''')

       
        cursor.execute("SELECT COUNT(*) FROM HealthCards")
        if cursor.fetchone()[0] == 0:
            health_cards = [
                ("Ayushman Bharat Yojana (PMJAY)", 500000, 1),
                ("CGHS", 200000, 2),
                ("ESI", 100000, 3),
                ("CMCHIS", 500000, 2),
                ("Bhamashah Swasthya Bima Yojana", 300000, 2),
                ("AABY", 50000, 4),
                ("Karunya Health Scheme", 200000, 2)
            ]
            cursor.executemany('''
                INSERT INTO HealthCards (name, max_amount, priority)
                VALUES (?, ?, ?)
            ''', health_cards)

            treatments = [
                ("Ayushman Bharat Yojana (PMJAY)", "Cardiology", 1),
                ("Ayushman Bharat Yojana (PMJAY)", "Oncology", 2),
                ("Ayushman Bharat Yojana (PMJAY)", "Orthopedics", 3),
                ("Ayushman Bharat Yojana (PMJAY)", "Neurology", 2),
                ("CGHS", "General Medicine", 3),
                ("CGHS", "Surgery", 1),
                ("CGHS", "Diagnostics", 2),
                ("ESI", "Maternity", 1),
                ("ESI", "Disability", 2),
                ("ESI", "Inpatient care", 3),
            ]
            cursor.executemany('''
                INSERT INTO Treatments(health_card_name, treatment_name, treatment_priority)
                VALUES (?, ?, ?)
            ''', treatments)

        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")
    return conn, cursor


def add_initial_data(cursor):
    cursor.executemany('INSERT INTO Departments (name) VALUES (?)', [(d,) for d in departments])

    doctors = [
        ('Dr. Spandana', 1, 'password1'), ('Dr. Leela', 1, 'password2'), ('Dr. Ranvindra', 1, 'password3'),
        ('Dr. Mahesh', 2, 'password1'), ('Dr. Rishitha', 2, 'password2'), ('Dr. Sai', 2, 'password3'),
        ('Dr. Sravan', 3, 'password1'), ('Dr. Prathima', 3, 'password2'), ('Dr. Sharada', 3, 'password3'),
        ('Dr. Deepika', 4, 'password1'), ('Dr. Raghava', 4, 'password2'), ('Dr. Nikkitha', 4, 'password3'),
        ('Dr. Nehal', 5, 'password1'), ('Dr. Srinish', 5, 'password2'), ('Dr. Akul', 5, 'password3'),
        ('Dr. Akhil', 6, 'password1'), ('Dr. Panvi', 6, 'password2'), ('Dr. Susheel', 6, 'password3')
        
    ]
    cursor.executemany('INSERT INTO Doctors (name, department_id, password) VALUES (?, ?, ?)', doctors)

    tasks = [
        ("10,000 Steps Walked", "Complete 10,000 steps of walking", 5),
        ("Burn 500 Calories", "Burn at least 500 calories", 5),
        ("Eat 2000 Calories", "Maintain a 2000 calorie diet", 5)
    ]
    cursor.executemany('INSERT INTO Tasks (task_name, description, discount) VALUES (?, ?, ?)', tasks)
    conn.commit()



def get_doctor_by_disease(disease, severity, cursor):
    department_name = disease_department_map.get(disease)
    if not department_name:
        print(f"No department found for disease: {disease}")
        return None

    
    if not department_tree.search(department_name):
        print(f"No department found in tree for: {department_name}")
        return None


    cursor.execute('SELECT id FROM Departments WHERE name = ?', (department_name,))
    department = cursor.fetchone()
    if not department:
        print(f"No department found with name: {department_name}")
        return None

    department_id = department[0]


    severity_level = severity_priority.get(severity.capitalize(), None)
    if severity_level is None:
        print(f"Invalid severity level: {severity}")
        return None

    doctor_id = None
    if severity_level == 1:  # Severe
        cursor.execute('SELECT id FROM Doctors WHERE department_id = ? ORDER BY id LIMIT 1', (department_id,))
    elif severity_level == 2:  # Moderate
        cursor.execute('SELECT id FROM Doctors WHERE department_id = ? ORDER BY id LIMIT 1 OFFSET 1', (department_id,))
    elif severity_level == 3:  # Mild
        cursor.execute('SELECT id FROM Doctors WHERE department_id = ? ORDER BY id LIMIT 1 OFFSET 2', (department_id,))

    doctor = cursor.fetchone()
    return doctor[0] if doctor else None

def add_patient(cursor, patient_list):
    name = input("Enter patient name: ")
    disease = input("Enter disease: ")
    severity = input("Enter severity (Mild, Moderate, Severe): ")

    cursor.execute("SELECT id, name, max_amount FROM HealthCards")
    health_cards = cursor.fetchall()

    print("\nAvailable Health Cards:")
    for idx, (card_id, card_name, max_amount) in enumerate(health_cards):
        print(f"{idx + 1}. {card_name} ")

    while True:
        try:
            health_card_index = int(input("Enter the number corresponding to the health card: ")) - 1
            if 0 <= health_card_index < len(health_cards):
                health_card_name = health_cards[health_card_index][1]
                max_amount = health_cards[health_card_index][2]
                remaining_amount = max_amount
                break
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    doctor_id = get_doctor_by_disease(disease, severity, cursor)
    if doctor_id:
        cursor.execute('INSERT INTO Patients (name, disease, severity, doctor_id) VALUES (?, ?, ?, ?)',
                       (name, disease, severity, doctor_id))
        patient_id = cursor.lastrowid

        # Check if patient already exists in PatientsHealth
        cursor.execute('SELECT * FROM PatientsHealth WHERE patient_id = ?', (patient_id,))
        existing_patient_health = cursor.fetchone()

        if existing_patient_health:
            # If the patient already exists, update the record
            cursor.execute('''
                UPDATE PatientsHealth
                SET name = ?, health_card = ?, max_amount = ?, remaining_amount = ?
                WHERE patient_id = ?
            ''', (name, health_card_name, max_amount, remaining_amount, patient_id))
        else:
            # If the patient doesn't exist, insert a new record
            cursor.execute('INSERT INTO PatientsHealth (patient_id, name, health_card, max_amount, remaining_amount) VALUES (?, ?, ?, ?, ?)',
                           (patient_id, name, health_card_name, max_amount, remaining_amount))

        patient_queue.append(name)
        assignment_history.append((name, doctor_id))
        patient_list.add_patient(f"ID: {patient_id:04d}, Name: {name}, Disease: {disease}, Severity: {severity}, Doctor ID: {doctor_id}, Health Card: {health_card_name}")
        print(f"Patient {name} assigned to doctor with ID: {doctor_id}. Unique Patient ID: {patient_id:04d}")
    else:
        print("No suitable doctor found for the given disease and severity.")
def doctor_login(cursor):
    name = input("Enter your name: ")
    password = input("Enter your password: ")

    cursor.execute('SELECT id, department_id FROM Doctors WHERE name = ? AND password = ?', (name, password))
    doctor = cursor.fetchone()
    if doctor:
        doctor_id, department_id = doctor
        print(f"Welcome, {name}! Here are your patients:")
        display_doctor_patients(doctor_id, cursor)  
    else:
        print("Invalid credentials. Please try again.")

def display_doctor_patients(doctor_id, cursor):
    cursor.execute('''SELECT p.name, p.disease, p.severity, ph.health_card
                      FROM Patients p
                      LEFT JOIN PatientsHealth ph ON p.id = ph.patient_id
                      WHERE p.doctor_id = ?''', (doctor_id,))
    results = cursor.fetchall()

    if results:
        
        print("\nYour Patients:")
        print(f"{'Name':<10} {'Disease':<15} {'Severity':<10} {'Health Card':<30}")
        print("-" * 85)

        
        for patient in results:
            if len(patient) == 4:  
                name, disease, severity, health_card = patient  
                print(f"{name:<10} {disease:<15} {severity:<10} {health_card if health_card else 'N/A':<30}")
            else:
                print("Unexpected patient data format:", patient)
    else:
        print("You have no patients assigned.")



def register_user(cursor, username):
    """Register a new user in the system."""
    try:
        cursor.execute("INSERT INTO Users (username) VALUES (?)", (username,))
        conn.commit()
        print(f"[INFO] User '{username}' registered successfully.")
    except sqlite3.IntegrityError:
        print(f"[ERROR] Username '{username}' already exists. Please try another.")

def add_symptom(cursor, username):
    """Add a symptom entry for a user with custom date."""
    display_severity_scale()  
    symptom_name = input("Enter symptom name: ")
    severity = input("Enter severity (1-10): ")
   
    while True:
        try:
            date_str = input("Enter date (YYYY-MM-DD) or press enter for current date: ")
            if date_str.strip() == "":
                
                date = datetime.now()
            else:
                
                date = datetime.strptime(date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")
    
    duration = input("Enter duration of symptoms (in days): ")
    triggers = input("Enter triggers (optional): ")
    
    try:
        severity = int(severity)
        if 1 <= severity <= 10:
            cursor.execute("""
                INSERT INTO Symptoms (username, symptom_name, severity, date, duration, triggers)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, symptom_name, severity, date.strftime("%Y-%m-%d %H:%M:%S"), duration, triggers))
            conn.commit()
            print(f"[INFO] Symptom '{symptom_name}' logged for user '{username}' with severity {severity}.")
        else:
            print("[ERROR] Severity must be between 1 and 10.")
    except ValueError:
        print("[ERROR] Invalid severity input. Please enter a number.")
def analyze_severity_pattern(symptoms_data):
    """Analyze severity patterns for symptoms and generate warnings."""
    symptom_patterns = {}
    
    
    for data in symptoms_data:
        symptom_name = data[2]  
        severity = data[3]      
        date = datetime.strptime(data[4], "%Y-%m-%d %H:%M:%S")  
        
        if symptom_name not in symptom_patterns:
            symptom_patterns[symptom_name] = []
        symptom_patterns[symptom_name].append((date, severity))

    warnings = []
    for symptom, occurrences in symptom_patterns.items():
        if len(occurrences) > 1:  
            
            occurrences.sort(key=lambda x: x[0])
            
            
            initial_severity = occurrences[0][1]
            latest_severity = occurrences[-1][1]
            severity_change = latest_severity - initial_severity
            
            
            time_span = (occurrences[-1][0] - occurrences[0][0]).days
            frequency = len(occurrences)
            
            if severity_change > 3:
                warnings.append(f"WARNING: {symptom} severity has increased significantly "
                              f"from {initial_severity} to {latest_severity} over {time_span} days.")
                
                
                department_found = False
                for disease, symptoms in disease_symptoms.items():
                    symptom_lower = symptom.lower()
                    if (symptom_lower in disease.lower() or 
                        any(symptom_lower in s.lower() for s in symptoms) or
                        (symptom_lower == "cold" and "Common Cold" in disease)):
                        department = get_department(disease)
                        warnings.append(f"Recommended to consult {department} department.")
                        department_found = True
                        break
                
                if not department_found:
                    warnings.append("Recommended to consult General Medicine department.")
            
            
            if time_span == 0:
                warnings.append(f"ALERT: {symptom} reported {frequency} times in the same day "
                              f"with increasing severity.")
            elif frequency/time_span >= 0.5:  
                warnings.append(f"ALERT: High frequency of {symptom} reports: "
                              f"{frequency} times in {time_span} days.")
            
            if latest_severity >= 8:
                warnings.append(f"URGENT: {symptom} current severity level ({latest_severity}) is very high. "
                              f"Immediate medical attention may be required.")

    return warnings
def view_logs(cursor, username):
    """View all symptoms logged by a user with pattern analysis."""
    cursor.execute("""
        SELECT * FROM Symptoms 
        WHERE username = ? 
        ORDER BY date
    """, (username,))
    rows = cursor.fetchall()
    
    if rows:
        print(f"\n--- Symptom History for {username} ---")
        
        
        for row in rows:
            print(f"Date: {row[4]}, Symptom: {row[2]}, Severity: {row[3]}, "
                  f"Duration: {row[5]}, Triggers: {row[6]}")
        
        
        warnings = analyze_severity_pattern(rows)
        if warnings:
            print("\n=== Health Alerts ===")
            for warning in warnings:
                print(warning)
            print("\nPlease consider consulting a healthcare provider if symptoms persist or worsen.")
        
        print("-----------------------")
    else:
        print(f"[INFO] No symptoms logged yet for {username}.")

def analyze_severity_pattern(symptoms_data):
    """Analyze severity patterns for symptoms and generate warnings."""
    symptom_patterns = {}
    
    
    for data in symptoms_data:
        symptom_name = data[2]  
        severity = data[3]     
        date = datetime.strptime(data[4], "%Y-%m-%d %H:%M:%S")  
        
        if symptom_name not in symptom_patterns:
            symptom_patterns[symptom_name] = []
        symptom_patterns[symptom_name].append((date, severity))

    warnings = []
    for symptom, occurrences in symptom_patterns.items():
        if len(occurrences) > 1:  
            
            occurrences.sort(key=lambda x: x[0])
            
            
            initial_severity = occurrences[0][1]
            latest_severity = occurrences[-1][1]
            severity_change = latest_severity - initial_severity
            
            
            time_span = (occurrences[-1][0] - occurrences[0][0]).days
            frequency = len(occurrences)
            
            
            if severity_change > 3:  
                warnings.append(f"WARNING: {symptom} severity has increased significantly "
                              f"from {initial_severity} to {latest_severity}.")
                
                
                for disease, symptoms in disease_symptoms.items():
                    if symptom.lower() in [s.lower() for s in symptoms]:
                        department = get_department(disease)
                        warnings.append(f"Recommended to consult {department} department.")
                        break
            
            if frequency >= 3 and time_span <= 7:  
                warnings.append(f"ALERT: {symptom} has been reported {frequency} times in {time_span} days.")
                
            if latest_severity >= 8:  
                warnings.append(f"URGENT: {symptom} current severity level ({latest_severity}) is very high.")

    return warnings


    
def filter_by_symptom(cursor, username, symptom_name):
    """Filter symptoms by a specific symptom name for a user."""
    cursor.execute("SELECT * FROM Symptoms WHERE username = ? AND symptom_name = ?", (username, symptom_name))
    rows = cursor.fetchall()
    if rows:
        print(f"\n--- Logs for '{symptom_name}' for user {username} ---")
        for row in rows:
            print(f"Date: {row[4]}, Severity: {row[3]}, Duration: {row[5]}, Triggers: {row[6]}")
        print("---------------------------")
    else:
        print(f"[INFO] No entries found for '{symptom_name}' under user '{username}'.")

def clear_logs(cursor, username):
    """Clear all symptoms for a specific user."""
    cursor.execute("DELETE FROM Symptoms WHERE username = ?", (username,))
    conn.commit()
    print(f"[INFO] All symptom logs cleared for user '{username}'.")






def predict_disease(input_symptoms):
    possible_diseases = []
    for disease, symptoms in disease_symptoms.items():
        matching_symptoms = set(input_symptoms) & set(symptoms)
        if len(matching_symptoms) >= 2:  
            possible_diseases.append((disease, len(matching_symptoms)))
    
    if possible_diseases:
        
        possible_diseases.sort(key=lambda x: x[1], reverse=True)
        return possible_diseases
    else:
        return None

def get_department(disease):
    disease_department = {
        "Common Cold": "General Medicine",
        "Flu": "General Medicine",
        "COVID-19": "Infectious Diseases",
        "Allergies": "Allergy and Immunology",
        "Migraine": "Neurology",
        "Food Poisoning": "Gastroenterology",
        "Asthma": "Pulmonology",
        "Diabetes": "Endocrinology",
        "Hypertension": "Cardiology",
        "Arthritis": "Rheumatology"
    }
    return disease_department.get(disease, "General Medicine")

def display_severity_scale():
    """Display the severity scale for symptoms."""
    print("\n--- Severity Scale ---")
    print("1: Minimal or no symptoms; not bothersome.")
    print("2-3: Mild symptoms; manageable.")
    print("4-5: Moderate symptoms ; noticeable discomfort.")
    print("6-7: Severe symptoms; significant discomfort.")
    print("8-9: Very severe symptoms; extreme discomfort.")
    print("10: Worst possible symptoms; unbearable.")
    print("-----------------------")

def food_recommendation(condition):
    
    recommendations = {
        "coronary artery disease": [
            "Oily fish (salmon, mackerel)", "Whole grains", "Leafy greens",
            "Fruits (especially berries)", "Nuts (almonds, walnuts)", "Legumes"
        ],
        "heart disease": [  
            "Low-sodium foods", "Lean proteins", "Fruits and vegetables",
            "Whole grains", "Healthy fats (olive oil, avocados)"
        ],
        "arrhythmias": [
            "Fruits (bananas, oranges)", "Leafy greens", "Fish rich in omega-3 fatty acids",
            "Whole grains", "Nuts and seeds"
        ],
        "hypertension": [
            "Fruits (especially bananas)", "Leafy greens", "Low-fat dairy",
            "Whole grains", "Lean protein", "Foods high in potassium and magnesium"
        ],
        "stroke": [
            "Fruits and vegetables", "Whole grains", "Oily fish",
            "Nuts", "Legumes "
        ],
        "diabetes": [
            "Leafy greens", "Whole grains", "Nuts and seeds",
            "Lean protein", "Low-fat dairy", "Non-starchy vegetables"
        ],
        "asthma": [
            "Fruits and vegetables rich in antioxidants", "Omega-3 fatty acids",
            "Whole grains", "Low-fat dairy"
        ],
        "cancer": [
            "Fruits and vegetables", "Whole grains", "Lean proteins",
            "Healthy fats", "Legumes"
        ],
        "osteoarthritis": [
            "Fruits (berries, cherries)", "Leafy greens", "Omega-3 fatty acids",
            "Whole grains", "Low-fat dairy"
        ],
        "eczema": [
            "Omega-3 rich foods (fatty fish, walnuts)", "Fruits and vegetables",
            "Whole grains", "Probiotic-rich foods (yogurt, kefir)"
        ],
        "IBD": [
            "Low-fiber foods during flare-ups", "Lean proteins",
            "Nutrient-rich fruits and vegetables", "Healthy fats"
        ],
        "skin allergy": [
            "Fatty fish (salmon, sardines, mackerel)", "Chia seeds", "Flaxseeds, Walnuts",
            "Bell peppers", "Oranges", "Strawberries", "Yogurt"
        ],
        "digestive issue": [
            "Fiber-rich foods", "Avocados", "Unsaturated fats", "Eggs"
        ],
        "cough": [
            "Drinking plenty of water", "Gargling salt water",
            "Having herbal tea, like ginger or peppermint",
            "Reducing inflammation with ginger", "Having a warm turmeric drink",
            "Adding probiotics to your diet"
        ],
        "cold": [
            "Bananas", "Berries", "Broth", "Carrots", "Chamomile Tea",
            "Cherries", "Citrus Fruits", "Garlic"
        ],
        "bone fractures": [
            "Red meat", "Dark-meat chicken or turkey", "Oily fish", "Eggs",
            "Dried fruits", "Leafy green veggies", "Whole-grain breads",
            "Fortified cereals"
        ]
    }

    
    if condition.lower() in recommendations:
        return f"Recommended foods for {condition}:\n" + ", ".join(recommendations[condition.lower()])
    else:
        return "Sorry, no specific recommendations available for that condition."


class DiseaseNode:
    def __init__(self, name):
        self.name = name
        self.medications = []

    def add_medication(self, medication):
        self.medications.append(medication)

class MedicationInteractionGraph:
    def __init__(self):
        self.graph = {}

    def add_interaction(self, med1, med2, description, alternatives):
        if med1 not in self.graph:
            self.graph[med1] = {}
        if med2 not in self.graph:
            self.graph[med2] = {}

        self.graph[med1][med2] = (description, alternatives)
        self.graph[med2][med1] = (description, alternatives)

    def check_interaction(self, med1, med2):
        if med1 in self.graph and med2 in self.graph[med1]:
            return self.graph[med1][med2]
        return None

class HospitalManagementSystem:
    def __init__(self):
        self.diseases = {}
        self.interaction_graph = MedicationInteractionGraph()

    def add_disease(self, disease_name):
        if disease_name not in self.diseases:
            self.diseases[disease_name] = DiseaseNode(disease_name)

    def add_medication_to_disease(self, disease_name, medication_name):
        if disease_name in self.diseases:
            self.diseases[disease_name].add_medication(medication_name)
        else:
            print(f"Disease '{disease_name}' not found. Please add it first.")

    def add_interaction(self, med1, med2, description, alternatives):
        self.interaction_graph.add_interaction(med1, med2, description, alternatives)

    def check_interaction(self, med1, med2):
        return self.interaction_graph.check_interaction(med1, med2)

    def input_patient_data(self):
        while True:
            
            print("\nEnter two diseases to check for medication interactions.")
            disease1 = input("Enter the first disease: ").strip()
            disease2 = input("Enter the second disease: ").strip()

            
            medication1 = input(f"Enter medication for {disease1}: ").strip()
            medication2 = input(f"Enter medication for {disease2}: ").strip()

            
            interaction = self.check_interaction(medication1, medication2)
            if interaction:
                description, alternatives = interaction
                print(f"Interaction Alert: {medication1} and {medication2} - {description}")
                print("Consider alternatives:", ", ".join(alternatives))
            else:
                print(f"No interaction found between {medication1} and {medication2}.")

            
            another_check = input("Do you want to check another pair of diseases? (yes/no): ").strip().lower()
            if another_check != 'yes':
                print("Thank you for using the Hospital Management System.")
                break


hospital_system = HospitalManagementSystem()

 
hospital_system.add_disease("Diabetes")
hospital_system.add_disease("Hypertension")
hospital_system.add_disease("Asthma")

hospital_system.add_medication_to_disease("Diabetes", "Metformin")
hospital_system.add_medication_to_disease("Diabetes", "Insulin")
hospital_system.add_medication_to_disease("Hypertension", "Lisinopril")
hospital_system.add_medication_to_disease("Hypertension", "Atenolol")
hospital_system.add_medication_to_disease("Asthma", "Albuterol")
hospital_system.add_medication_to_disease("Asthma", "Fluticasone")


hospital_system.add_interaction("Metformin", "Lisinopril", "Risk of blood sugar fluctuations.", ["Insulin"])
hospital_system.add_interaction("Insulin", "Atenolol", "May mask hypoglycemia symptoms.", ["Metformin"])
hospital_system.add_interaction("Lisinopril", "Albuterol", "Possible reduced effectiveness of Albuterol.", ["Fluticasone"])
hospital_system.add_interaction("Fluticasone", "Atenolol", "Increased risk of respiratory issues.", ["Albuterol"])

def add_task_completion(cursor):
    patient_id = int(input("Enter patient ID: "))
    task_id = int(input("Enter task ID: "))

   
    cursor.execute('SELECT * FROM TaskCompletions WHERE patient_id = ? AND task_id = ?', (patient_id, task_id))
    if cursor.fetchone():
        print("This task has already been completed by the patient.")
        return

   
    cursor.execute('SELECT * FROM Patients WHERE id = ?', (patient_id,))
    patient = cursor.fetchone()
    if patient:
        cursor.execute('SELECT * FROM Tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
        if task:
            
            cursor.execute('UPDATE Patients SET tasks_completed = tasks_completed + 1, total_discount = total_discount + ? WHERE id = ?', (task[3], patient_id))
            
            cursor.execute('INSERT INTO TaskCompletions (patient_id, task_id) VALUES (?, ?)', (patient_id, task_id))
            conn.commit()
            print(f"Task completion updated for patient {patient_id}. Discount of {task[3]} applied.")
        else:
            print("Task not found.")
    else:
        print("Patient not found.")

def view_patient_task_status(cursor):
    patient_id = int(input("Enter patient ID: "))
    cursor.execute('SELECT * FROM Patients WHERE id = ?', (patient_id,))
    patient = cursor.fetchone()
    if patient:
        print(f"Patient {patient_id} has completed {patient[5]} tasks.")
        print(f"Total discount applied: {patient[6]}")
    else:
        print("Patient not found.")


departments = {
    "Cardiology": {
        'Hemoglobin': (12, 16),
        'Blood Pressure': (90, 120),
        'Cholesterol': (125, 200)
    },
    "Neurology": {
        'EEG': (0.5, 2.5),
        'MRI': (0, 1),
        'Cognitive Tests': (24, 30)
    },
    "Pediatrics": {
        'Growth Screening': (10, 90),
        'Hemoglobin': (11, 14),
        'Immunization': (0, 1)
    }
}


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None

    def is_empty(self):
        return len(self.stack) == 0

    def get_all(self):
        return self.stack


def get_patient_data(tests):
    patient_stack = Stack()
    print("\nEnter the patient's report values (type 'undo' to remove the last entry):")

    i = 0  
    while i < len(tests):
        test = tests[i]  
        value = input(f"Enter {test} value: ")

        if value.lower() == 'undo':
            if not patient_stack.is_empty():
                removed = patient_stack.pop()
                print(f"Removed the last entry: {removed}")
                i -= 1  
            else:
                print("Nothing to undo!")
        else:
            try:
                patient_stack.push((test, float(value)))
                i += 1 
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    return dict(patient_stack.get_all())


def compare_reports(normal_ranges, patient_values, department):
    tests = list(normal_ranges.keys())
    patient_data = list(patient_values.values())

    print(f"\n--- Comparison Report with Health Messages for {department} ---")
    for i, test in enumerate(tests):
        lower, upper = normal_ranges[test]
        patient_value = patient_values[test]

        if patient_value < lower:
            print(f"For {test}: Patient's value ({patient_value}) is LOWER than the healthy range ({lower}-{upper}).")
            print(f"Warning: {generate_warning(test, 'low')}")
        elif patient_value > upper:
            print(f"For {test}: Patient's value ({patient_value}) is HIGHER than the healthy range ({lower}-{upper}).")
            print(f"Warning: {generate_warning(test, 'high')}")
        else:
            print(f"For {test}: Patient's value ({patient_value}) is within the healthy range.")
            print(f"Message: {generate_good_message(test)}")

    x = np.arange(len(tests))
    width = 0.2

    normal_data = [(lower + upper) / 2 for lower, upper in normal_ranges.values()]

    plt.figure(figsize=(10, 6))
    plt.bar(x - width/2, normal_data, width=width, label='Normal Values', color='green')
    plt.bar(x + width/2, patient_data, width=width, label='Patient Values', color='red')

    plt.yscale('log')
    plt.xlabel ('Tests')
    plt.ylabel('Values (log scale)')
    plt.title(f'Patient Report Comparison - {department}')
    plt.xticks(x, tests, rotation=45)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0f}'.format(y) if y < 1000 else '{:.0f}k'.format(y / 1000)))
    plt.legend()
    plt.tight_layout()
    plt.show()


def generate_warning(test, condition):
    warnings = {
        'Hemoglobin': {'high': "Risk of heart issues.", 'low': "Risk of anemia."},
        'Blood Pressure': {'high': "Risk of heart disease.", 'low': "Risk of dizziness."},
        'Cholesterol': {'high': "Risk of heart disease.", 'low': "Possible liver issues."},
        'EEG': {'high': "Possible neurological issues.", 'low': "Reduced brain activity."},
        'MRI': {'high': "Further investigation needed.", 'low': "Normal findings."},
        'Cognitive Tests': {'low': "Possible cognitive impairment.", 'high': "Strong cognitive function."},
        'Growth Screening': {'high': "Rapid growth observed.", 'low': "Growth issues."}
    }
    return warnings.get(test, {}).get(condition, "No specific warning available.")


def generate_good_message(test):
    good_messages = {
        'Hemoglobin': "Hemoglobin level is good.",
        'Blood Pressure': "Blood pressure is within the healthy range.",
        'Cholesterol': "Cholesterol level is healthy.",
        'EEG': "EEG is within normal range.",
        'MRI': "MRI shows no abnormalities.",
        'Cognitive Tests': "Cognitive function is healthy.",
        'Growth Screening': "Growth is normal for age."
    }
    return good_messages.get(test, "All values are normal.")



def get_highest_priority_patients(cursor):
    print("Fetching highest priority patients...")
    
    
    cursor.execute('''
        SELECT p.name, p.disease, p.severity, ph.health_card
        FROM Patients p
        LEFT JOIN PatientsHealth ph ON p.id = ph.patient_id
    ''')
    patients = cursor.fetchall()

    if not patients:
        print("No patients found.")
        return

    
    sorted_patients = sorted(patients, key=lambda x: severity_priority.get(x[2].capitalize(), float('inf')))

    
    print("\nHighest Priority Patients:")
    for patient in sorted_patients:
        print(f"Name: {patient[0]}, Disease: {patient[1]}, Severity: {patient[2]}, Health Card: {patient[3]}")

def get_health_card_details(cursor):
    try:
        patient_id = int(input("Enter patient ID: "))
        cursor.execute('''
            SELECT p.name, p.disease, ph.health_card, ph.max_amount, ph.remaining_amount
            FROM PatientsHealth ph
            JOIN Patients p ON ph.patient_id = p.id
            WHERE ph.patient_id = ?
        ''', (patient_id,))
        
        details = cursor.fetchone()
        if details:
            name, disease, health_card, max_amount, remaining_amount = details
            print(f"\nPatient Name: {name}")
            print(f"Disease: {disease}")
            print(f"Health Card: {health_card}")
            print(f"Maximum Amount: INR {max_amount}")
            print(f"Remaining Amount: INR {remaining_amount}")

           
            department = disease_department_map.get(disease)
            if not department:
                print(f"No department found for disease '{disease}'.")
                return

            
            cursor.execute('''
                SELECT treatment_name
                FROM Treatments
                WHERE health_card_name = ? AND treatment_name = ?
            ''', (health_card, department))
            eligible_treatment = cursor.fetchone()

            if eligible_treatment:
                treatment_amount = float(input("Enter the treatment amount: "))
                if treatment_amount <= remaining_amount:
                    
                    new_remaining_amount = remaining_amount - treatment_amount
                    cursor.execute('''
                        UPDATE PatientsHealth
                        SET remaining_amount = ?
                        WHERE patient_id = ?
                    ''', (new_remaining_amount, patient_id))
                    conn.commit()
                    print(f"Amount claimed: INR {treatment_amount}. Remaining amount in card: INR {new_remaining_amount}.")
                    print("No remaining amount to be paid by the patient.")
                else:
                    
                    claimed_amount = remaining_amount
                    remaining_amount_due = treatment_amount - claimed_amount

                    
                    new_remaining_amount = 0  
                    cursor.execute('''
                        UPDATE PatientsHealth
                        SET remaining_amount = ?
                        WHERE patient_id = ?
                    ''', (new_remaining_amount, patient_id))
                    conn.commit()

                    print(f"Amount claimed: INR {claimed_amount}. Remaining amount in card: INR {new_remaining_amount}.")
                    print(f"Remaining amount to be paid by patient: INR {remaining_amount_due}.")
            else:
                print(f"The health card '{health_card}' is not eligible for treatment of disease '{disease}' in the '{department}' department.")
        else:
            print("No patient found with the given ID.")
    except ValueError:
        print("Invalid patient ID format. Please enter a valid number.")

def display_patients_by_department(cursor, department_name):
    cursor.execute('''SELECT p.id, p.name AS PatientName, p.disease, p.severity, d.name AS DoctorName
                      FROM Patients p
                      JOIN Doctors d ON p.doctor_id = d.id
                      JOIN Departments dep ON d.department_id = dep.id
                      WHERE dep.name = ?
                      ORDER BY p.id''', (department_name,))
    results = cursor.fetchall()
    if results:
        df = pd.DataFrame(results, columns=['Patient ID', 'Patient Name', 'Disease', 'Severity', 'Doctor Name'])
        print(f"\nPatients in {department_name} Department:\n")
        print(df.to_string(index=False))
    else:
        print(f"No patients found in the {department_name} department.")


def main():
    global conn, cursor
    conn, cursor = setup_database()
    add_initial_data(cursor)
    patient_list = PatientLinkedList()

    try:
        while True:
            print("\nHospital Management System")
            print("1. Patient Management")
            print("2. Doctor Management")
            print("3. Hospital Records")
            print("4. Exit")

            choice = input("Choose an option: ")
            if choice == '1':
                while True:
                    print("\nPatient Management")
                    print("1. Add Patient")
                    print("2. Symptom Tracker ")
                    print("3. Food Recommendations")
                    print("4. Medication Interaction")
                    print("5. Gamified discounts")
                    print("6. Reports Analyzer")
                    print("7. Health Card Management")
                    print("8. Return to Main Menu")

                    patient_choice = input("Choose an option: ")
                    if patient_choice == '1':
                        add_patient(cursor, patient_list)
                        conn.commit()  
                    elif patient_choice == '2':
                        username = input("Enter your username: ")
                        if not cursor.execute("SELECT * FROM Users WHERE username = ?", (username,)).fetchone():
                            register = input(f"Username '{username}' not found. Do you want to register ? (y/n): ").lower()
                            if register == 'y':
                                register_user(cursor, username)
                            else:
                                print("[INFO] Exiting application.")
                                return
                        while True:
                            print(f"\n--- Symptom Tracker for {username} ---")
                            print("1. Add Symptom")
                            print("2. View Logs")
                            print("3. Filter by Symptom")
                            print("4.Pridect Disease")
                            print("5. Clear Logs")
                            print("6. Exit")
                            symptom_choice = input("Choose an option (1-6): ")

                            if symptom_choice == "1":
                                add_symptom(cursor, username)
                            elif symptom_choice == "2":
                                view_logs(cursor, username)
                            elif symptom_choice == "3":
                                symptom_name = input("Enter symptom name to filter: ")
                                filter_by_symptom(cursor, username, symptom_name)
                            elif symptom_choice == "4":
                                symptoms = input("Enter symptoms (comma-separated): ").lower().split(',')
                                symptoms = [symptom.strip() for symptom in symptoms]
                                possible_diseases = predict_disease(symptoms)
                                if possible_diseases:
                                    print("\nPossible diseases based on your symptoms:")
                                    for disease, match_count in possible_diseases:
                                        department = get_department(disease)
                                        print(f"- {disease} (Matching symptoms: {match_count})")
                                        print(f"  Consult: {department} department")
                                else:
                                    print("No specific diseases matched your symptoms. Please consult a general physician.")


                            
                            elif symptom_choice == "5":
                                clear_logs(cursor, username)
                            elif symptom_choice == "6":
                                print(f"[INFO] Exiting the Symptom Tracker for {username}.")
                                break
                            else:
                                print("[ERROR] Invalid choice. Please select a valid option.")
                    elif patient_choice == '3':
                        condition = input("Enter your dietary condition (e.g., cold, cough, cancer, stroke, bone fractures): ")
                        print(food_recommendation(condition))
                    elif patient_choice == '4':
                        hospital_system.input_patient_data()
                    elif patient_choice == '5':
                        
                        while True:
                            print("\nTask Management")
                            print("1. Display Tasks")
                            print("2. Add Task Completion")
                            print("3. View Patient Task Status")
                            print("4. Return to Patient Management")

                            task_choice = input("Choose an option: ")
                            if task_choice == '1':
                                cursor.execute('SELECT * FROM Tasks')
                                tasks = cursor.fetchall()
                                if tasks:
                                    print("\nAvailable Tasks:")
                                    for task in tasks:
                                        print(f"Task ID: {task[0]}, Task Name: {task[1]}, Description: {task[2]}, Discount: {task[3]}")
                                else:
                                    print("No tasks available.")
                            elif task_choice == '2':
                                add_task_completion(cursor)
                            elif task_choice == '3':
                                view_patient_task_status(cursor)
                            elif task_choice == '4':
                                break
                            else:
                                print("Invalid choice. Please try again.")
                    elif patient_choice == '6':
                        while True:
                            print("\nDepartments available: Cardiology, Neurology, Pediatrics")
                            department = input("Enter the department: ").strip()
                            if department not in departments:
                                print("Invalid department. Please try again.")
                                continue
                            patient_data = get_patient_data(list(departments[department].keys()))  
                            compare_reports(departments[department], patient_data, department)
                            print("Would you like to compare another report? (yes/no):")
                            repeat = input().strip().lower()
                            if repeat != 'yes':
                                print("Exiting the program. Thank you!")
                                break
                    elif patient_choice == '7':
                        while True:
                            print("\nHealth Card Management")
                            print("1. Display Health Card Details")
                            print("2. Return to Patient Management")

                            health_choice = input("Choose an option: ")
                            if health_choice == '1':
                                get_health_card_details(cursor)
                                
                            elif health_choice == '2':
                                break
                            else:
                                print("Invalid choice. Please try again.")

                    elif patient_choice == '8':
                        break
                    else:
                        print("Invalid choice. Please try again.")

            elif choice == '2':
                while True:
                    print("\nDoctor Management")
                    print("1. Doctor Login")
                    print("2. Return to Main Menu")

                    doctor_choice = input("Choose an option: ")
                    if doctor_choice == '1':
                        doctor_login(cursor)
                    elif doctor_choice == '2':
                        break
                    else:
                        print("Invalid choice. Please try again.")

            elif choice == '3':
                while True:
                    print("\nHospital Records")
                    print("1. Display All Patients by Department")
                    print("2. Return to Main Menu")

                    record_choice = input("Choose an option: ")
                    if record_choice == '1':
                        department = input("Enter the department name: ").strip()
                        display_patients_by_department(cursor, department)
                    elif record_choice == '2':
                        break
                    else:
                        print("Invalid choice. Please try again.")

            elif choice == '4':
                print("Exiting the system.")
                break
            else:
                print("Invalid choice. Please try again.")
    finally:
        conn.close()  
if __name__ == "__main__":
    main()