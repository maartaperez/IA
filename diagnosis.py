import random
import numpy as np

def perform_diagnosis(env, patient, hospital):
    """Simulates the diagnosis process for a patient in the hospital.

    This function manages the diagnosis of a patient, which may include 
    performing an X-ray if required. The process takes a random amount of time.

    Args:
        env (simpy.Environment): The simulation environment.
        patient (Patient): The patient undergoing diagnosis.
        hospital (Hospital): The hospital where the diagnosis takes place.

    Yields:
        simpy.Event: A process representing the time taken for diagnosis 
        and possible X-ray examination.
    """
    print(f"{env.now}: Diagnosis for {patient.id}")

    # If the patient's symptom requires an X-ray before diagnosis
    if patient.symptom in ["Fracture", "Respiratory Difficulty"]:
        yield env.process(hospital.perform_xray(patient))  

    # Simulate the time taken for diagnosis (random between 10 and 20 minutes)
    yield env.timeout(np.random.uniform(10, 20))

    print(f"{env.now}: Diagnosis completed for {patient.id}")

