"""
FairWork AI - Core Artificial Intelligence Module

AI method:
    Uniform Cost Search (UCS)

Purpose:
    Match students with suitable part-time jobs while respecting
    hard constraints such as age, availability, maximum working
    hours and maximum travel distance.

The system:
    1. Loads job data from CSV.
    2. Checks hard constraints.
    3. Calculates a cost for each valid job.
    4. Uses Uniform Cost Search to select the lowest-cost job.

SearchResult is used so that the system can report:
    - selected job
    - search cost
    - number of jobs expanded
    - execution time
"""

from __future__ import annotations

import json
import heapq
import time

from dataclasses import dataclass
from pathlib import Path

from heuristics import calculate_suitability_cost


# ==========================================================
# Student
# ==========================================================

@dataclass
class Student:
    """
    Represents a student's profile.
    """

    age: int
    skills: list[str]
    available_start: int
    available_end: int
    max_hours: int
    max_distance: float


# ==========================================================
# Job
# ==========================================================

@dataclass
class Job:
    """
    Represents a part-time job vacancy.
    """

    id: str
    company: str
    title: str
    min_age: int
    skills: list[str]
    distance: float
    hours: int
    salary: float
    shift_start: int
    shift_end: int


# ==========================================================
# Search Result
# ==========================================================

@dataclass
class SearchResult:
    """
    Stores the result of the Uniform Cost Search.
    """

    job: Job | None
    cost: float
    jobs_expanded: int
    execution_time_s: float

    @property
    def found(self) -> bool:
        """Return True when a suitable job was found."""

        return self.job is not None


# ==========================================================
# Load Jobs from CSV
# ==========================================================

def load_jobs(path: str | Path) -> list[Job]:
    """
    Load simulated job vacancies from a JSON file.

    Expected JSON structure:

    [
        {
            "id": "J001",
            "title": "Cafe Crew",
            "company": "Campus Cafe",
            "min_age": 18,
            "skills": ["Customer Service", "Communication"],
            "distance": 2.0,
            "hours": 10,
            "salary": 12.0,
            "shift_start": 18,
            "shift_end": 22
        }
    ]
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Job data file was not found: {path}"
        )

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "jobs.json must contain a list of job objects."
        )

    jobs: list[Job] = []

    required_fields = {
        "id",
        "title",
        "company",
        "min_age",
        "skills",
        "distance",
        "hours",
        "salary",
        "shift_start",
        "shift_end",
    }

    for index, item in enumerate(data, start=1):

        if not isinstance(item, dict):
            raise ValueError(
                f"Job record {index} must be a JSON object."
            )

        missing = required_fields - set(item.keys())

        if missing:
            raise ValueError(
                f"Job record {index} is missing fields: "
                f"{', '.join(sorted(missing))}"
            )

        skills = item["skills"]

        if not isinstance(skills, list):
            raise ValueError(
                f"Job record {index}: 'skills' must be a list."
            )

        job = Job(
            id=str(item["id"]),
            title=str(item["title"]),
            company=str(item["company"]),
            min_age=int(item["min_age"]),
            skills=[str(skill).strip() for skill in skills],
            distance=float(item["distance"]),
            hours=int(item["hours"]),
            salary=float(item["salary"]),
            shift_start=int(item["shift_start"]),
            shift_end=int(item["shift_end"]),
        )

        jobs.append(job)

    return jobs


# ==========================================================
# Constraint Checking
# ==========================================================

def check_constraints(student: Student, job: Job) -> bool:
    """
    Check whether a job satisfies all hard constraints.

    Hard constraints:
        1. Minimum age
        2. Maximum travel distance
        3. Maximum weekly working hours
        4. Working shift must fit student's availability
        5. At least one required skill should match
    """

    # ------------------------------------------------------
    # Age constraint
    # ------------------------------------------------------

    if student.age < job.min_age:
        return False

    # ------------------------------------------------------
    # Distance constraint
    # ------------------------------------------------------

    if job.distance > student.max_distance:
        return False

    # ------------------------------------------------------
    # Maximum working hours
    # ------------------------------------------------------

    if job.hours > student.max_hours:
        return False

    # ------------------------------------------------------
    # Availability constraint
    # ------------------------------------------------------

    if job.shift_start < student.available_start:
        return False

    if job.shift_end > student.available_end:
        return False

    # ------------------------------------------------------
    # Skill constraint
    # ------------------------------------------------------

    student_skills = {
        skill.strip().lower()
        for skill in student.skills
    }

    job_skills = {
        skill.strip().lower()
        for skill in job.skills
    }

    if not student_skills.intersection(job_skills):
        return False

    return True


# ==========================================================
# Cost Calculation
# ==========================================================

def calculate_cost(student: Student, job: Job) -> float:
    """
    Calculate the cost of a valid job.

    Lower cost = better match.

    The cost considers:
        - skill mismatch
        - travel distance
        - working-hour suitability
        - salary preference

    Hard constraints should already be checked before this
    function is called.
    """

    if not check_constraints(student, job):
        return float("inf")

    return calculate_suitability_cost(student, job)


# ==========================================================
# Uniform Cost Search
# ==========================================================

def uniform_cost_search(
    student: Student,
    jobs: list[Job]
) -> SearchResult:
    """
    Uniform Cost Search for the best suitable job.

    Each valid job is treated as a state/action candidate.
    The priority queue always expands the job with the lowest
    cumulative cost.

    Returns:
        SearchResult
    """

    start_time = time.perf_counter()

    frontier: list[tuple[float, int, Job]] = []

    counter = 0
    jobs_expanded = 0

    # ------------------------------------------------------
    # Add valid jobs to the frontier
    # ------------------------------------------------------

    for job in jobs:

        if not check_constraints(student, job):
            continue

        cost = calculate_cost(student, job)

        heapq.heappush(
            frontier,
            (cost, counter, job)
        )

        counter += 1

    # ------------------------------------------------------
    # No valid jobs
    # ------------------------------------------------------

    if not frontier:

        return SearchResult(
            job=None,
            cost=float("inf"),
            jobs_expanded=0,
            execution_time_s=(
                time.perf_counter() - start_time
            ),
        )

    # ------------------------------------------------------
    # Uniform Cost Search
    # ------------------------------------------------------

    while frontier:

        cost, _, job = heapq.heappop(frontier)

        jobs_expanded += 1

        return SearchResult(
            job=job,
            cost=cost,
            jobs_expanded=jobs_expanded,
            execution_time_s=(
                time.perf_counter() - start_time
            ),
        )

    # Safety fallback

    return SearchResult(
        job=None,
        cost=float("inf"),
        jobs_expanded=jobs_expanded,
        execution_time_s=(
            time.perf_counter() - start_time
        ),
    )