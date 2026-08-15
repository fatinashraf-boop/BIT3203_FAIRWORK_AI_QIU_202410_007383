"""
FairWork AI - Core AI Search Module

AI methods:
1. Uniform Cost Search (UCS) - baseline
2. A* Search - improved method

The system matches students with suitable part-time jobs
while respecting hard constraints such as:
- minimum age
- maximum working hours
- maximum travel distance
- class schedule conflicts

Job data is loaded from a JSON file.
"""

from __future__ import annotations

import heapq
import json
import time

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# ==========================================================
# Student
# ==========================================================

@dataclass
class Student:
    """Represents a student's profile."""

    age: int
    skills: list[str]
    class_start: int
    class_end: int
    max_hours: int
    max_distance: float


# ==========================================================
# Job
# ==========================================================

@dataclass
class Job:
    """Represents a part-time job vacancy."""

    id: str
    title: str
    company: str
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
    """Stores the result and performance metrics of a search."""

    job: Optional[Job]
    cost: float
    jobs_expanded: int
    execution_time_s: float

    @property
    def found(self) -> bool:
        return self.job is not None


# ==========================================================
# Load JSON Data
# ==========================================================

def load_jobs(path: str | Path) -> list[Job]:
    """
    Load simulated job vacancy data from a JSON file.
    """

    path = Path(path)

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    jobs = []

    for item in data:
        jobs.append(
            Job(
                id=item["id"],
                title=item["title"],
                company=item["company"],
                min_age=item["min_age"],
                skills=item["skills"],
                distance=item["distance"],
                hours=item["hours"],
                salary=item["salary"],
                shift_start=item["shift_start"],
                shift_end=item["shift_end"],
            )
        )

    return jobs


# ==========================================================
# Constraint Checking
# ==========================================================

def check_constraints(student: Student, job: Job) -> bool:
    """
    Check hard constraints.

    A job is rejected if:
    - student is below minimum age
    - working hours exceed student's maximum
    - distance exceeds student's maximum
    - work shift overlaps with class
    """

    # Age constraint
    if student.age < job.min_age:
        return False

    # Maximum weekly working hours
    if job.hours > student.max_hours:
        return False

    # Maximum travel distance
    if job.distance > student.max_distance:
        return False

    # Class schedule conflict
    if (
        job.shift_start < student.class_end
        and job.shift_end > student.class_start
    ):
        return False

    return True


# ==========================================================
# Cost Function
# ==========================================================

def calculate_cost(student: Student, job: Job) -> Optional[float]:
    """
    Calculate the cost of a valid job.

    Lower cost = better match.

    Cost components:
    - distance penalty
    - working-hours penalty
    - skill mismatch penalty
    """

    if not check_constraints(student, job):
        return None

    cost = 0.0

    # Distance penalty
    cost += job.distance

    # Working-hours penalty
    cost += job.hours * 0.5

    # Skill matching
    student_skills = {
        skill.strip().lower()
        for skill in student.skills
    }

    job_skills = {
        skill.strip().lower()
        for skill in job.skills
    }

    matched_skills = student_skills.intersection(job_skills)

    if not matched_skills:
        cost += 10

    else:
        # Small reward for each matched skill
        cost -= len(matched_skills) * 2

    return max(cost, 0.0)


# ==========================================================
# Heuristic
# ==========================================================

def heuristic(student: Student, job: Job) -> float:
    """
    Estimate the remaining matching cost.

    The heuristic uses information that contributes to
    job suitability.

    It is deliberately lightweight so that A* can be
    compared against UCS.
    """

    student_skills = {
        skill.strip().lower()
        for skill in student.skills
    }

    job_skills = {
        skill.strip().lower()
        for skill in job.skills
    }

    matched = len(student_skills.intersection(job_skills))

    if matched == 0:
        skill_estimate = 10.0
    else:
        skill_estimate = 0.0

    distance_estimate = job.distance

    return distance_estimate + skill_estimate


# ==========================================================
# Uniform Cost Search
# ==========================================================

def uniform_cost_search(
    student: Student,
    jobs: list[Job]
) -> SearchResult:
    """
    Baseline uninformed search.

    UCS selects the currently available job with the
    lowest accumulated cost.
    """

    start_time = time.perf_counter()

    frontier = []

    counter = 0

    jobs_expanded = 0

    for job in jobs:

        cost = calculate_cost(student, job)

        if cost is None:
            continue

        heapq.heappush(
            frontier,
            (cost, counter, job)
        )

        counter += 1

    while frontier:

        cost, _, job = heapq.heappop(frontier)

        jobs_expanded += 1

        return SearchResult(
            job=job,
            cost=cost,
            jobs_expanded=jobs_expanded,
            execution_time_s=time.perf_counter() - start_time
        )

    return SearchResult(
        job=None,
        cost=float("inf"),
        jobs_expanded=jobs_expanded,
        execution_time_s=time.perf_counter() - start_time
    )


# ==========================================================
# A* Search
# ==========================================================

def a_star_search(
    student: Student,
    jobs: list[Job]
) -> SearchResult:
    """
    Improved informed search using A*.

    f(n) = g(n) + h(n)

    g(n) = current matching cost
    h(n) = estimated remaining matching cost
    """

    start_time = time.perf_counter()

    frontier = []

    counter = 0

    jobs_expanded = 0

    for job in jobs:

        cost = calculate_cost(student, job)

        if cost is None:
            continue

        h = heuristic(student, job)

        f = cost + h

        heapq.heappush(
            frontier,
            (f, counter, cost, job)
        )

        counter += 1

    while frontier:

        _, _, cost, job = heapq.heappop(frontier)

        jobs_expanded += 1

        return SearchResult(
            job=job,
            cost=cost,
            jobs_expanded=jobs_expanded,
            execution_time_s=time.perf_counter() - start_time
        )

    return SearchResult(
        job=None,
        cost=float("inf"),
        jobs_expanded=jobs_expanded,
        execution_time_s=time.perf_counter() - start_time
    )