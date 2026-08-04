"""
fairwork_ai.py

FairWork AI
AI Method: Uniform Cost Search (UCS)

Author: Your Name
"""

# ==========================================================
# Imports
# ==========================================================

import csv
import heapq
from dataclasses import dataclass

# ==========================================================
# Student Class
# ==========================================================

@dataclass
class Student:
    """
    Represents a student's profile used by the FairWork AI agent.
    """

    age: int
    skills: list[str]
    available_start: int
    available_end: int
    max_hours: int
    max_distance: float

    def display(self):
        print("\n========== Student Profile ==========")
        print(f"Age               : {self.age}")
        print(f"Skills            : {', '.join(self.skills)}")
        print(
            f"Available Time    : "
            f"{self.available_start}:00 - {self.available_end}:00"
        )
        print(f"Maximum Hours     : {self.max_hours} hrs/week")
        print(f"Maximum Distance  : {self.max_distance} km")
        print("=====================================\n")

# ==========================================================
# Job Class
# ==========================================================

@dataclass(order=True)
class Job:
    """
    Represents a part-time job vacancy.

    The 'cost' attribute is placed first so that heapq can
    automatically compare Job objects based on their UCS cost.
    """

    cost: float = 0

    title: str = ""
    min_age: int = 18
    required_skill: str = ""

    distance: float = 0
    hours: int = 0
    salary: float = 0

    shift_start: int = 0
    shift_end: int = 0

    def display(self):
        """Display job information."""

        print("\n========== Job Information ==========")
        print(f"Job Title         : {self.title}")
        print(f"Minimum Age       : {self.min_age}")
        print(f"Required Skill    : {self.required_skill}")
        print(f"Distance          : {self.distance} km")
        print(f"Working Hours     : {self.hours} hrs/week")
        print(f"Salary            : RM {self.salary}/hour")
        print(
            f"Shift             : "
            f"{self.shift_start}:00 - {self.shift_end}:00"
        )
        print(f"UCS Cost          : {self.cost:.2f}")
        print("=====================================\n")

        # ==========================================================
# Load Jobs from CSV
# ==========================================================

def load_jobs(filename):
    """
    Load job vacancies from a CSV file.

    Parameters
    ----------
    filename : str
        Path to the jobs.csv file.

    Returns
    -------
    list[Job]
        A list of Job objects.
    """

    jobs = []

    try:

        with open(filename, mode="r", newline="", encoding="utf-8") as csv_file:

            reader = csv.DictReader(csv_file)

            for row in reader:

                job = Job(
                    title=row["title"],
                    min_age=int(row["min_age"]),
                    required_skill=row["required_skill"],
                    distance=float(row["distance"]),
                    hours=int(row["hours"]),
                    salary=float(row["salary"]),
                    shift_start=int(row["shift_start"]),
                    shift_end=int(row["shift_end"]),
                    cost=0
                )

                jobs.append(job)

    except FileNotFoundError:
        print(f"\nError: '{filename}' was not found.")
        return []

    except KeyError as e:
        print(f"\nError: Missing column in CSV file: {e}")
        return []

    except ValueError:
        print("\nError: Invalid data format in jobs.csv.")
        return []

    return jobs

# ==========================================================
# Check Job Constraints
# ==========================================================

def check_constraints(student, job):
    """
    Check whether a job satisfies all mandatory constraints.

    Parameters
    ----------
    student : Student
        Student profile entered by the user.

    job : Job
        Job vacancy loaded from jobs.csv.

    Returns
    -------
    tuple(bool, str)
        (True, "Eligible") if the job is suitable.
        (False, reason) if the job violates a constraint.
    """

    # ------------------------------------------------------
    # Age Requirement
    # ------------------------------------------------------
    if student.age < job.min_age:
        return False, "Student does not meet the minimum age requirement."

    # ------------------------------------------------------
    # Working Hours
    # ------------------------------------------------------
    if job.hours > student.max_hours:
        return False, "Job exceeds the student's maximum working hours."

    # ------------------------------------------------------
    # Travel Distance
    # ------------------------------------------------------
    if job.distance > student.max_distance:
        return False, "Job exceeds the student's maximum travel distance."

    # ------------------------------------------------------
    # Skill Requirement
    # ------------------------------------------------------
    if job.required_skill not in student.skills:
        return False, "Required skill not found in the student's profile."

    # ------------------------------------------------------
    # Availability Check
    # Student must be available for the entire shift.
    # ------------------------------------------------------
    if job.shift_start < student.available_start:
        return False, "Job starts before the student's available time."

    if job.shift_end > student.available_end:
        return False, "Job ends after the student's available time."

    # ------------------------------------------------------
    # All Constraints Passed
    # ------------------------------------------------------
    return True, "Eligible"       

# ==========================================================
# Calculate Job Cost
# ==========================================================

def calculate_cost(student, job):
    """
    Calculate the Uniform Cost Search (UCS) cost for a job.

    Lower cost = Better recommendation.

    Cost Factors
    ------------
    • Distance
    • Working hours
    • Skill match
    • Salary
    """

    cost = 0

    # ------------------------------------------------------
    # Distance Cost
    # Closer jobs are preferred.
    # ------------------------------------------------------
    cost += job.distance

    # ------------------------------------------------------
    # Working Hours Cost
    # Longer working hours increase the cost.
    # ------------------------------------------------------
    cost += job.hours * 0.5

    # ------------------------------------------------------
    # Skill Match
    # If the student's skill matches the job requirement,
    # reduce the cost.
    # ------------------------------------------------------
    if job.required_skill in student.skills:
        cost -= 5
    else:
        cost += 10

    # ------------------------------------------------------
    # Salary Benefit
    # Higher salary reduces the overall cost.
    # ------------------------------------------------------
    cost -= job.salary * 0.2

    # Prevent negative costs.
    if cost < 0:
        cost = 0

    return round(cost, 2)

# ==========================================================
# Uniform Cost Search (UCS)
# ==========================================================

def uniform_cost_search(student, jobs):
    """
    Perform Uniform Cost Search to recommend the most suitable job.

    Parameters
    ----------
    student : Student
        Student profile.

    jobs : list[Job]
        List of available jobs.

    Returns
    -------
    Job | None
        The lowest-cost suitable job, or None if no suitable job exists.
    """

    # Priority queue (frontier)
    frontier = []

    # Explored jobs (to avoid processing duplicates)
    explored = set()

    print("\n======================================")
    print("Uniform Cost Search")
    print("======================================")

    # ------------------------------------------------------
    # Add valid jobs to the frontier
    # ------------------------------------------------------
    for job in jobs:

        valid, reason = check_constraints(student, job)

        if not valid:
            print(f"Rejected: {job.title}")
            print(f"Reason   : {reason}\n")
            continue

        # Calculate UCS cost
        job.cost = calculate_cost(student, job)

        # Push into priority queue
        heapq.heappush(frontier, job)

        print(f"Added to Frontier: {job.title}")
        print(f"Cost             : {job.cost:.2f}\n")

    # ------------------------------------------------------
    # No valid jobs
    # ------------------------------------------------------
    if not frontier:
        return None

    print("--------------------------------------")
    print("Expanding Jobs")
    print("--------------------------------------")

    # ------------------------------------------------------
    # UCS Loop
    # ------------------------------------------------------
    while frontier:

        # Remove the lowest-cost job
        current = heapq.heappop(frontier)

        # Skip duplicates
        if current.title in explored:
            continue

        explored.add(current.title)

        print(
            f"Expanded: {current.title:<25}"
            f"Cost = {current.cost:.2f}"
        )

        # --------------------------------------------------
        # Goal Test
        # --------------------------------------------------
        # Since all jobs are already valid, the first job
        # removed from the priority queue has the minimum cost.
        return current

    return None