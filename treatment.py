import random
import numpy as np

def perform_treatment(self, env, patient, hospital):
    """Manages the treatment process for a patient.

    This function determines the appropriate treatment based on the patient's severity.
    Critical patients undergo surgery, while non-critical patients receive standard treatment.

    Args:
        self: The object instance (if applicable).
        env (simpy.Environment): The simulation environment.
        patient: The patient undergoing treatment.
        hospital: The hospital instance managing the treatment process.

    Yields:
        simpy.Event: A process representing the time taken for treatment and discharge.
    """
    print(f"{env.now}: Treatment for patient {patient.id}")

    if patient.severity == "Critical":
        # If the patient is in critical condition, they require surgery
        yield env.process(hospital.perform_surgery(patient))
    else:
        # Standard treatment for non-critical patients
        yield env.timeout(np.random.uniform(10, 30))  # Treatment duration

    print(f"{env.now}: Treatment completed for patient {patient.id}")

    # Patient is discharged after treatment
    yield env.process(hospital.perform_discharge(patient))



