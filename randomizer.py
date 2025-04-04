import random
from models.patient import Patient

# Global counter to assign unique IDs to each generated patient
patient_counter = 1

def generate_patient():
    """Generates a new patient with random severity and symptoms.

    This function creates a new patient instance, assigning a unique ID and randomly selecting 
    the severity level and symptom from predefined lists.

    Returns:
        Patient: A new patient instance with assigned severity, symptom, and unique ID.
    """
    global patient_counter  # Keep track of patient IDs
    
    # Randomly assign severity level
    severity = random.choice(["Critical", "Severe", "Mild"])
    
    # Randomly assign a symptom
    symptom = random.choice(["Chest Pain", "Fracture", "Lump", "Respiratory Difficulty", "Sore Throat"])

    # Create a new Patient instance
    patient = Patient(severity, symptom, patient_counter)
    
    # Increment the counter for the next patient
    patient_counter += 1
    
    return patient

