"""
FairWork AI - A* Job Recommendation System

FairWork AI recommends suitable part-time jobs for students.

Search method:
    A* Search

Evaluation:
    f(n) = g(n) + h(n)

Hard constraints:
    1. Minimum age
    2. Maximum distance
    3. Maximum working hours
    4. Working availability
    5. At least one matching skill
"""


from __future__ import annotations

import heapq
import json
import time

from dataclasses import dataclass
from pathlib import Path

from heuristics import (
    calculate_g_cost,
    calculate_h_cost,
    calculate_f_cost,
)


# ==========================================================
# Student
# ==========================================================

@dataclass
class Student:
    """
    Represents a student's profile and requirements.
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
    Stores the result of A* search.

    Metrics:
        job
        cost = f(n)
        g_cost
        h_cost
        jobs_expanded
        jobs_generated
        execution_time_s
    """

    job: Job | None
    cost: float
    g_cost: float
    h_cost: float
    jobs_expanded: int
    jobs_generated: int
    execution_time_s: float

    @property
    def found(self) -> bool:
        """
        Return True if a suitable job was found.
        """

        return self.job is not None


# ==========================================================
# Load Jobs
# ==========================================================

def load_jobs(path: str | Path) -> list[Job]:
    """
    Load job vacancies from jobs.json.
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Job data file was not found: {path}"
        )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

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

    for index, item in enumerate(
        data,
        start=1
    ):

        if not isinstance(item, dict):
            raise ValueError(
                f"Job record {index} must be a JSON object."
            )

        missing = (
            required_fields
            - set(item.keys())
        )

        if missing:
            raise ValueError(
                f"Job record {index} is missing fields: "
                f"{', '.join(sorted(missing))}"
            )

        if not isinstance(
            item["skills"],
            list
        ):
            raise ValueError(
                f"Job record {index}: "
                "'skills' must be a list."
            )

        job = Job(
            id=str(item["id"]),
            title=str(item["title"]),
            company=str(item["company"]),
            min_age=int(item["min_age"]),
            skills=[
                str(skill).strip()
                for skill in item["skills"]
            ],
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

def check_constraints(
    student: Student,
    job: Job
) -> bool:
    """
    Check all hard constraints.

    A job is valid only if:

        age is sufficient
        distance is acceptable
        hours are acceptable
        shift fits availability
        at least one skill matches
    """

    # ------------------------------------------------------
    # Age
    # ------------------------------------------------------

    if student.age < job.min_age:
        return False

    # ------------------------------------------------------
    # Distance
    # ------------------------------------------------------

    if job.distance > student.max_distance:
        return False

    # ------------------------------------------------------
    # Working Hours
    # ------------------------------------------------------

    if job.hours > student.max_hours:
        return False

    # ------------------------------------------------------
    # Schedule
    # ------------------------------------------------------

    if job.shift_start < student.available_start:
        return False

    if job.shift_end > student.available_end:
        return False

    # ------------------------------------------------------
    # Skills
    # ------------------------------------------------------

    student_skills = {
        skill.strip().lower()
        for skill in student.skills
    }

    job_skills = {
        skill.strip().lower()
        for skill in job.skills
    }

    if not student_skills.intersection(
        job_skills
    ):
        return False

    return True


# ==========================================================
# Cost Calculation
# ==========================================================

def calculate_cost(
    student: Student,
    job: Job
) -> float:
    """
    Return complete A* cost f(n).

    Invalid jobs receive infinity.
    """

    if not check_constraints(
        student,
        job
    ):
        return float("inf")

    return calculate_f_cost(
        student,
        job
    )


# ==========================================================
# A* SEARCH
# ==========================================================

def a_star_search(
    student: Student,
    jobs: list[Job]
) -> SearchResult:
    """
    Perform A* search for the most suitable job.

    A* evaluation:

        f(n) = g(n) + h(n)

    State representation:

        START
          |
          +---- Job 1
          |
          +---- Job 2
          |
          +---- Job 3
          |
         ...
          |
         GOAL

    Invalid jobs are removed before entering the frontier.

    Returns:
        SearchResult
    """

    start_time = time.perf_counter()

    # ------------------------------------------------------
    # Priority queue
    #
    # Tuple:
    #
    # (f_cost, counter, job, g_cost, h_cost)
    # ------------------------------------------------------

    frontier = []

    counter = 0

    jobs_generated = 0
    jobs_expanded = 0

    # ------------------------------------------------------
    # Generate valid job states
    # ------------------------------------------------------

    for job in jobs:

        if not check_constraints(
            student,
            job
        ):
            continue

        g_cost = calculate_g_cost(
            student,
            job
        )

        h_cost = calculate_h_cost(
            student,
            job
        )

        f_cost = round(
            g_cost + h_cost,
            4
        )

        heapq.heappush(
            frontier,
            (
                f_cost,
                counter,
                job,
                g_cost,
                h_cost,
            )
        )

        counter += 1
        jobs_generated += 1

    # ------------------------------------------------------
    # No valid jobs
    # ------------------------------------------------------

    if not frontier:

        return SearchResult(
            job=None,
            cost=float("inf"),
            g_cost=float("inf"),
            h_cost=float("inf"),
            jobs_expanded=0,
            jobs_generated=0,
            execution_time_s=(
                time.perf_counter()
                - start_time
            ),
        )

    # ------------------------------------------------------
    # A* Search
    # ------------------------------------------------------

    while frontier:

        (
            f_cost,
            _,
            job,
            g_cost,
            h_cost,
        ) = heapq.heappop(
            frontier
        )

        jobs_expanded += 1

        # --------------------------------------------------
        # Goal Test
        #
        # The first valid job removed from the A*
        # priority queue has the lowest f(n).
        # --------------------------------------------------

        return SearchResult(
            job=job,
            cost=f_cost,
            g_cost=g_cost,
            h_cost=h_cost,
            jobs_expanded=jobs_expanded,
            jobs_generated=jobs_generated,
            execution_time_s=(
                time.perf_counter()
                - start_time
            ),
        )

    # ------------------------------------------------------
    # Safety fallback
    # ------------------------------------------------------

    return SearchResult(
        job=None,
        cost=float("inf"),
        g_cost=float("inf"),
        h_cost=float("inf"),
        jobs_expanded=jobs_expanded,
        jobs_generated=jobs_generated,
        execution_time_s=(
            time.perf_counter()
            - start_time
        ),
    )


# ==========================================================
# Backward-Compatible Alias
# ==========================================================

def uniform_cost_search(
    student: Student,
    jobs: list[Job]
) -> SearchResult:
    """
    Backward-compatible wrapper.

    The project now uses A*.

    This function is retained so older code does not
    immediately break, but new code should use:

        a_star_search()
    """

    return a_star_search(
        student,
        jobs
    )


# ==========================================================
# Module Test
# ==========================================================

if __name__ == "__main__":

    print(
        "FairWork AI module loaded successfully."
    )

    print(
        "Search method: A*"
    )