import csv
from datetime import datetime


class Patient:
    """Represents a single row of daily case data."""
    def __init__(self, day, date_of_diagnosis, number_of_cases):
        self.day = int(day)
        self.date_of_diagnosis = datetime.strptime(date_of_diagnosis, "%Y-%m-%d").date()
        self.number_of_cases = int(number_of_cases)

    def __repr__(self):
        return f"Patient(day={self.day}, date={self.date_of_diagnosis}, cases={self.number_of_cases})"


class Patients:
    """Collection of Patient records loaded from a CSV."""

    def __init__(self):
        self.records = []

    def __iter__(self):
        return iter(self.records)

    def __len__(self):
        return len(self.records)

    @classmethod
    def instantiate_from_csv(cls, filepath):
        """Load patient records from a CSV and return a Patients instance."""
        instance = cls()
        with open(filepath, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                patient = Patient(
                    day=row['day'],
                    date_of_diagnosis=row['date'],
                    number_of_cases=row['active reported daily cases']
                )
                instance.records.append(patient)
        return instance