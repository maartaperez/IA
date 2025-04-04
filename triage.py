import numpy as np

def perform_triage(env, patient, hospital):
    """Performs triage on a patient and directs them to the appropriate care level.

    This function evaluates the severity of the patient's condition and assigns them to the correct 
    treatment path: emergency care for critical cases, urgent consultation for severe cases, or 
    general consultation for less severe cases.

    Args:
        env (simpy.Environment): The simulation environment.
        patient: The patient undergoing triage.
        hospital: The hospital instance managing patient care.

    Yields:
        simpy.Event: A process representing the triage duration and subsequent patient care actions.
    """
    print(f"{env.now} \t| Triage completed | Patient {patient.id} | Level: {patient.severity}")
    hospital.register_event(patient, "Triage", env.now)
    
    severity = patient.severity
    symptom = patient.symptom
    triage_duration = np.random.uniform(3, 7)  # Randomized triage duration

    yield env.timeout(triage_duration)  # Simulate triage processing time

    if severity == "Critical":
        print(f"{env.now} \t| Emergency: Patient {patient.id} transferred to emergency care.")
        yield env.process(hospital.emergency_attention(patient))  # Send to emergency care
    elif severity == "Severe":
        print(f"{env.now} \t| Urgent consultation for patient {patient.id}.")
        yield env.process(hospital.urgent_consultation(patient))  # Send to urgent consultation
    else:
        print(f"{env.now} \t| Normal consultation for patient {patient.id}.")
        yield env.process(hospital.general_consultation(patient))  # Send to general consultation

        # After consultation, the patient is discharged
        yield env.process(hospital.perform_discharge(patient))

