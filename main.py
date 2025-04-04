import simpy
import random
import numpy as np
from config import *
from models.patient import Patient
from models.hospital import Hospital
from simulation.scheduler import Scheduler
from models.event import Event
from simulation.triage import perform_triage
from simulation.diagnosis import perform_diagnosis
from simulation.treatment import perform_treatment
from utils.randomizer import generate_patient
import pandas as pd
from tqdm import tqdm
from itertools import product
import os

def patient_arrival(env, hospital, scheduler, arrival_rate):
    """Simulates the continuous arrival of patients at the hospital.

    Patients arrive at the hospital following an exponential distribution based on the arrival rate.
    Each patient is generated with random severity and symptoms, and an arrival event is scheduled.

    Args:
        env (simpy.Environment): The simulation environment.
        hospital (Hospital): The hospital instance where patients are treated.
        scheduler (Scheduler): The event scheduler handling patient events.
        arrival_rate (float): The average time between patient arrivals.
    """
    while True:
        yield env.timeout(np.random.exponential(arrival_rate))  # Wait before the next patient arrival
        patient = generate_patient()  # Generate a new patient
        event = Event("Arrival", env.now, patient.id)  # Create an arrival event
        scheduler.schedule_event(event, patient)  # Schedule the event
        env.process(hospital.receive_patient(patient))  # Start patient treatment process

def main(scenario="normal"):
    """Runs the hospital simulation with the specified scenario.

    This function initializes the simulation environment, hospital, and scheduler. It then 
    starts the patient arrival process and runs the simulation for a predefined duration.

    Args:
        scenario (str, optional): The simulation scenario. Options:
            - "normal": Regular patient arrival rate.
            - "mass_emergency": High patient influx simulating a crisis. Defaults to "normal".
    """
    random.seed(random_seed)  # Set random seed for reproducibility
    np.random.seed(random_seed)

    # Diccionario que mapea los escenarios a las tasas de llegada
    arrival_rate_map = {
        "mass_emergency": emergency_arrival_interval,
        "normal": normal_arrival_interval
    }

    # Asigna la tasa de llegada según el escenario
    arrival_rate = arrival_rate_map.get(scenario, normal_arrival_interval)  # Si no se encuentra el escenario, usa el valor por defecto

    # Initialize simulation environment and hospital
    env = simpy.Environment()
    hospital = Hospital(env, capacity_emergencies, num_doctors, num_nurses, capacity_waiting_room, capacity_surgery_rooms)
    scheduler = Scheduler(env)

    env.process(patient_arrival(env, hospital, scheduler, arrival_rate))  # Start patient arrival process
    env.run(until=simulation_duration)  # Run the simulation

def choose_scenario():
    """Displays a menu to select the scenario for the simulation."""
    print("Select the type of simulation:")
    print("1. Normal emergency")
    print("2. Mass emergency")
    choice = input("Enter the number of the desired option (1 or 2): ")

    if choice == "1":
        return "normal"
    elif choice == "2":
        return "mass_emergency"
    else:
        print("Invalid option. 'Normal emergency' will be selected by default.")
        return "normal"


if __name__ == "__main__":
    """
    Main entry point for the hospital simulation. This function runs a series of simulations with varying hospital capacities,
    generates patient data, and saves the results to a CSV file.
    """

    # Print a message indicating the start of the simulation
    print("Simulación Hospitalaria")
    
    # Obtener la selección del usuario para el tipo de simulación
    scenario = choose_scenario()
    
    # Ejecutar la simulación con el escenario seleccionado
    main(scenario=scenario)
    
    # Capacity configurations for various hospital resources
    capacities_emergencies = [1, 2, 3, 4, 5]
    capacities_doctors = [1, 2, 3, 4, 5]
    capacities_nurses = [2, 4, 6, 8, 10]
    capacities_waiting_room = [5, 10, 20, 30]
    capacities_operating_room = [1, 2, 3, 5]
    
    # List to store all simulation data
    all_data = []
    
    # Total number of simulations based on combinations of capacities
    total_simulations = (
        len(capacities_emergencies) * len(capacities_doctors) * len(capacities_nurses) * len(capacities_waiting_room) * len(capacities_operating_room)
    )

    # Run simulations with progress bar
    for capacity in tqdm(product(capacities_emergencies, capacities_doctors, capacities_nurses, capacities_waiting_room, capacities_operating_room), total=total_simulations):
        env = simpy.Environment()
        hospital = Hospital(env, *capacity)
        
        # Generate and process 5 patients for each simulation run
        for i in range(5):
            patient = generate_patient()
            env.process(hospital.receive_patient(patient))
        
        # Run the simulation silently and collect the event data
        history = hospital.silent()
        all_data.extend(history)
    
    # Create the "data_analysis" directory if it doesn't exist
    if not os.path.exists("data_analysis"):
        os.makedirs("data_analysis")

    # Save the collected data into a CSV file in the "data_analysis" folder
    df = pd.DataFrame(all_data, columns=["Patient ID", "Symptom", "Severity", "Arrival Time", "Departure Time"])
    
    # Map severity and symptom values to numerical values for analysis
    severity_map = {"Mild": 0, "Severe": 1, "Critical": 2}
    symptom_map = {
        "Chest Pain": 0,
        "Fracture": 1,
        "Sore Throat": 2,
        "Difficulty Breathing": 3,
        "Lump": 4
    }

    # Convert "Severity" and "Symptom" columns to numerical values
    df["Severity"] = df["Severity"].map(severity_map)
    df["Symptom"] = df["Symptom"].map(symptom_map)
    
    # Save the data as a CSV file
    df.to_csv("data_analysis/hospital_simulation.csv", index=False)

    # Print a message indicating the completion of the simulations and data saving
    print("\nSimulations completed. The data has been saved in 'data_analysis/hospital_simulation.csv'")