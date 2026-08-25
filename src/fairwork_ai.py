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

A* stages:
    Stage 0 - Skill matching
    Stage 1 - Distance suitability
    Stage 2 - Working-hour suitability
    Stage 3 - Salary preference
    Stage 4 - Goal state
"""

from __future__ import annotations

import heapq
import json
import time

from dataclasses import dataclass
from pathlib import Path

from heuristics import (
    skill_mismatch_cost,
    distance_cost,
    working_hours_cost,
    salary_cost,
)


# ==========================================================
# STUDENT
# ==========================================================

@dataclass
class Student:
    age: int
    skills: list[str]
    available_start: int
    available_end: int
    max_hours: int
    max_distance: float


# ==========================================================
# JOB
# ==========================================================

@dataclass
class Job:
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
# SEARCH NODE
# ==========================================================

@dataclass
class SearchNode:
    """
    Represents a candidate job at one stage of the A* search.
    """

    job: Job
    stage: int
    g_cost: float
    h_cost: float

    @property
    def f_cost(self) -> float:
        """
        A* evaluation function.

        f(n) = g(n) + h(n)
        """
        return self.g_cost + self.h_cost

    @property
    def is_goal(self) -> bool:
        """
        Stage 4 represents the goal state.
        """
        return self.stage == 4


# ==========================================================
# SEARCH RESULT
# ==========================================================

@dataclass
class SearchResult:
    job: Job | None
    cost: float
    jobs_expanded: int
    nodes_generated: int
    execution_time_s: float
    g_cost: float = 0.0
    h_cost: float = 0.0

    @property
    def found(self) -> bool:
        return self.job is not None

    @property
    def jobs_generated(self) -> int:
        """
        Backward-compatible name for reporting.
        """
        return self.nodes_generated


# ==========================================================
# LOAD JOBS
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

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "jobs.json must contain a list of job objects."
        )

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

    jobs = []

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

        jobs.append(
            Job(
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
        )

    return jobs


# ==========================================================
# HARD CONSTRAINTS
# ==========================================================

def check_constraints(
    student: Student,
    job: Job
) -> bool:
    """
    Check all mandatory eligibility constraints.
    """

    # Age
    if student.age < job.min_age:
        return False

    # Distance
    if job.distance > student.max_distance:
        return False

    # Maximum working hours
    if job.hours > student.max_hours:
        return False

    # Working availability
    if job.shift_start < student.available_start:
        return False

    if job.shift_end > student.available_end:
        return False

    # Skill requirement
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
# STAGE COST
# ==========================================================

def stage_cost(
    student: Student,
    job: Job,
    stage: int
) -> float:
    """
    Calculate the cost contributed by each A* stage.

    Stage 0:
        Skill mismatch = 40%

    Stage 1:
        Distance = 30%

    Stage 2:
        Working hours = 20%

    Stage 3:
        Salary = 10%
    """

    if stage == 0:
        return (
            skill_mismatch_cost(student, job)
            * 0.40
        )

    if stage == 1:
        return (
            distance_cost(student, job)
            * 0.30
        )

    if stage == 2:
        return (
            working_hours_cost(student, job)
            * 0.20
        )

    if stage == 3:
        return (
            salary_cost(job)
            * 0.10
        )

    return 0.0


# ==========================================================
# COMPLETE COST
# ==========================================================

def calculate_cost(
    student: Student,
    job: Job
) -> float:
    """
    Calculate the complete suitability cost of a job.

    Lower cost = better match.

    This function combines all four weighted components:
        40% skill mismatch
        30% distance
        20% working hours
        10% salary
    """

    return (
        skill_mismatch_cost(student, job) * 0.40
        + distance_cost(student, job) * 0.30
        + working_hours_cost(student, job) * 0.20
        + salary_cost(job) * 0.10
    )


# ==========================================================
# HEURISTIC
# ==========================================================

def heuristic(
    student: Student,
    job: Job,
    stage: int
) -> float:
    """
    Estimate the remaining cost from the current stage.

    h(n) contains only costs from future stages.

    This keeps:
        f(n) = g(n) + h(n)

    and avoids double-counting costs.
    """

    if stage == 0:

        return (
            distance_cost(student, job) * 0.30
            + working_hours_cost(student, job) * 0.20
            + salary_cost(job) * 0.10
        )

    if stage == 1:

        return (
            working_hours_cost(student, job) * 0.20
            + salary_cost(job) * 0.10
        )

    if stage == 2:

        return (
            salary_cost(job) * 0.10
        )

    return 0.0


# ==========================================================
# A* SEARCH
# ==========================================================

def a_star_search(
    student: Student,
    jobs: list[Job]
) -> SearchResult:
    """
    Perform A* search over valid job candidates.

    Each valid job moves through four evaluation stages:

        0 -> Skill
        1 -> Distance
        2 -> Hours
        3 -> Salary
        4 -> Goal

    The frontier is ordered using:

        f(n) = g(n) + h(n)
    """

    start_time = time.perf_counter()

    frontier = []

    counter = 0

    jobs_expanded = 0
    nodes_generated = 0

    # ------------------------------------------------------
    # INITIAL STATE
    # ------------------------------------------------------

    for job in jobs:

        # Apply hard constraints first.
        if not check_constraints(student, job):
            continue

        g = stage_cost(
            student,
            job,
            0
        )

        h = heuristic(
            student,
            job,
            0
        )

        node = SearchNode(
            job=job,
            stage=0,
            g_cost=g,
            h_cost=h
        )

        heapq.heappush(
            frontier,
            (
                node.f_cost,
                counter,
                node
            )
        )

        counter += 1
        nodes_generated += 1

    # ------------------------------------------------------
    # NO VALID JOBS
    # ------------------------------------------------------

    if not frontier:

        return SearchResult(
            job=None,
            cost=float("inf"),
            jobs_expanded=0,
            nodes_generated=0,
            execution_time_s=(
                time.perf_counter()
                - start_time
            ),
            g_cost=float("inf"),
            h_cost=0.0
        )

    # ------------------------------------------------------
    # A* LOOP
    # ------------------------------------------------------

    while frontier:

        _, _, current = heapq.heappop(frontier)

        jobs_expanded += 1

        # --------------------------------------------------
        # GOAL TEST
        # --------------------------------------------------

        if current.is_goal:

            return SearchResult(
                job=current.job,
                cost=current.g_cost,
                jobs_expanded=jobs_expanded,
                nodes_generated=nodes_generated,
                execution_time_s=(
                    time.perf_counter()
                    - start_time
                ),
                g_cost=current.g_cost,
                h_cost=current.h_cost
            )

        # --------------------------------------------------
        # EXPAND NEXT STAGE
        # --------------------------------------------------

        next_stage = current.stage + 1

        additional_cost = stage_cost(
            student,
            current.job,
            next_stage
        )

        new_g = (
            current.g_cost
            + additional_cost
        )

        new_h = heuristic(
            student,
            current.job,
            next_stage
        )

        child = SearchNode(
            job=current.job,
            stage=next_stage,
            g_cost=new_g,
            h_cost=new_h
        )

        heapq.heappush(
            frontier,
            (
                child.f_cost,
                counter,
                child
            )
        )

        counter += 1
        nodes_generated += 1

    # ------------------------------------------------------
    # FALLBACK
    # ------------------------------------------------------

    return SearchResult(
        job=None,
        cost=float("inf"),
        jobs_expanded=jobs_expanded,
        nodes_generated=nodes_generated,
        execution_time_s=(
            time.perf_counter()
            - start_time
        ),
        g_cost=float("inf"),
        h_cost=0.0
    )