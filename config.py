"""Configuration file for the hospital simulation.

This module defines various parameters that control the behavior of the hospital 
simulation, including staff numbers, resource capacities, patient arrival intervals, 
and simulation duration.
"""

# Random seed for reproducibility
random_seed = 42  

# Number of hospital staff
num_doctors = 60  # Total number of doctors available
num_nurses = 100  # Total number of nurses available
num_auxiliaries = 100  # Total number of auxiliary nurses available

# Hospital resource capacities
capacity_emergencies = 20  # Number of available emergency room beds
capacity_waiting_room = 80  # Maximum number of patients in the waiting room
capacity_xray_room = 4  # Number of available X-ray machines
capacity_surgery_rooms = 10  # Number of operating rooms
capacity_rooms = 10  # Number of patient recovery rooms

# Patient arrival intervals (in minutes)
normal_arrival_interval = 5  # Average time between normal patient arrivals
emergency_arrival_interval = 1  # Average time between emergency patient arrivals

# Simulation duration (in minutes)
simulation_duration = 480  # Total simulation time (8 hours)

# Doctor office capacities by specialty
doctor_office_capacity = {
    "Cardiologist": 1,  # Number of cardiology consultation rooms
    "Pulmonologist": 1,  # Number of pulmonology consultation rooms
    "Traumatologist": 1,  # Number of traumatology consultation rooms
    "Internist": 1,  # Number of internal medicine consultation rooms
    "Oncologist": 1  # Number of oncology consultation rooms
}
