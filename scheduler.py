import simpy
from models.patient import Patient

class Scheduler:
    """Manages the scheduling and execution of events in the simulation.

    The Scheduler class is responsible for storing scheduled events and 
    processing them within the simulation environment.

    Attributes:
        env (simpy.Environment): The simulation environment.
        events (list): A list storing all scheduled events.
    """

    def __init__(self, env: simpy.Environment) -> None:
        """Initializes the Scheduler with a simulation environment.

        Args:
            env (simpy.Environment): The simulation environment where events will be scheduled.
        """
        self.env = env
        self.events = []

    def schedule_event(self, event, patient: Patient) -> None:
        """Schedules an event and starts its processing.

        Args:
            event: The event to be scheduled.
            patient (Patient): The patient associated with the event.
        """
        self.events.append(event)
        self.env.process(self.process_event(event, patient))
    
    def process_event(self, event, patient: Patient):
        """Processes the scheduled event by waiting for the required duration.

        Args:
            event: The event to be processed.
            patient (Patient): The patient associated with the event.

        Yields:
            simpy.Event: A process representing the waiting time for the event.
        """
        yield self.env.timeout(event.time)

