"""
Test cases for the FairWork AI A* prototype.

Run from the project root:

    python -m pytest tests/test_fairwork_ai.py -v

Tests:
1. Suitable job recommendation
2. Schedule conflict rejection
3. No suitable job
4. A* selects lowest-cost job
5. Age constraint
6. Distance constraint
7. Working-hours constraint
8. Skill constraint
9. A* search result metrics
10. JSON job data loading
11. A* expands multiple search stages
12. A* reaches a goal state
"""

import sys
from pathlib import Path

# ==========================================================
# Allow tests/ to import modules from src/
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from fairwork_ai import (
    Student,
    Job,
    SearchResult,
    load_jobs,
    check_constraints,
    a_star_search,
)


# ==========================================================
# DATA PATH
# ==========================================================

DATA_PATH = PROJECT_ROOT / "data" / "jobs.json"


# ==========================================================
# TEST CASE 1
# ==========================================================

def test_suitable_job_recommendation():
    """
    Test Case 1:

    A student with reasonable requirements should receive
    at least one suitable job recommendation.
    """

    student = Student(
        age=21,
        skills=["Customer Service"],
        available_start=15,
        available_end=22,
        max_hours=20,
        max_distance=10,
    )

    jobs = load_jobs(DATA_PATH)

    result = a_star_search(student, jobs)

    # A SearchResult object should always be returned.
    assert result is not None
    assert isinstance(result, SearchResult)

    # At least one suitable job should exist.
    assert result.job is not None

    # The selected job must satisfy all hard constraints.
    assert check_constraints(
        student,
        result.job
    ) is True

    # The selected result must have a finite cost.
    assert result.cost < float("inf")


# ==========================================================
# TEST CASE 2
# ==========================================================

def test_schedule_conflict_is_rejected():
    """
    Test Case 2:

    A job outside the student's available working period
    must be rejected.
    """

    student = Student(
        age=21,
        skills=["Customer Service"],
        available_start=15,
        available_end=22,
        max_hours=20,
        max_distance=10,
    )

    conflicting_job = Job(
        id="TEST001",
        company="Test Cafe",
        title="Conflicting Evening Worker",
        min_age=18,
        skills=["Customer Service"],
        distance=3,
        hours=10,
        salary=12,
        shift_start=23,
        shift_end=24,
    )

    assert check_constraints(
        student,
        conflicting_job
    ) is False


# ==========================================================
# TEST CASE 3
# ==========================================================

def test_no_suitable_job():
    """
    Test Case 3:

    A highly restrictive student profile should result in
    no suitable job.

    Expected:
        result.job == None
        result.cost == infinity
    """

    student = Student(
        age=17,
        skills=["Customer Service"],
        available_start=15,
        available_end=18,
        max_hours=5,
        max_distance=1,
    )

    jobs = load_jobs(DATA_PATH)

    result = a_star_search(student, jobs)

    assert result is not None
    assert isinstance(result, SearchResult)

    # No job should satisfy all constraints.
    assert result.job is None

    # No valid search cost exists.
    assert result.cost == float("inf")


# ==========================================================
# TEST CASE 4
# ==========================================================

def test_astar_selects_lowest_cost_job():
    """
    Test Case 4:
    Two jobs satisfy all hard constraints.

    A* should select the job with the better overall
    suitability cost.
    """

    student = Student(
        age=21,
        skills=["Customer Service"],
        available_start=15,
        available_end=22,
        max_hours=20,
        max_distance=10,
    )

    far_job = Job(
        id="TEST002",
        company="Far Cafe",
        title="Far Customer Service Job",
        min_age=18,
        skills=["Customer Service"],
        distance=8,
        hours=20,
        salary=12,
        shift_start=15,
        shift_end=19,
    )

    nearby_job = Job(
        id="TEST003",
        company="Nearby Cafe",
        title="Nearby Customer Service Job",
        min_age=18,
        skills=["Customer Service"],
        distance=2,
        hours=15,
        salary=11,
        shift_start=15,
        shift_end=19,
    )

    jobs = [far_job, nearby_job]

    # Both jobs must satisfy the hard constraints.
    assert check_constraints(student, far_job) is True
    assert check_constraints(student, nearby_job) is True

    # Run A*.
    result = a_star_search(student, jobs)

    assert result is not None
    assert isinstance(result, SearchResult)
    assert result.job is not None

    # The nearby job should be preferred because it has
    # lower distance and fewer working hours.
    assert result.job.id == "TEST003"


# ==========================================================
# TEST CASE 5
# ==========================================================

def test_age_constraint():
    """
    Test Case 5:

    A student below the minimum age requirement must be
    rejected.
    """

    student = Student(
        age=17,
        skills=["Customer Service"],
        available_start=15,
        available_end=22,
        max_hours=20,
        max_distance=10,
    )

    job = Job(
        id="TEST004",
        company="Test Company",
        title="Adult Customer Service Job",
        min_age=18,
        skills=["Customer Service"],
        distance=2,
        hours=10,
        salary=12,
        shift_start=16,
        shift_end=20,
    )

    assert check_constraints(
        student,
        job
    ) is False


# ==========================================================
# TEST CASE 6
# ==========================================================

def test_distance_constraint():
    """
    Test Case 6:

    A job beyond the student's maximum travel distance
    must be rejected.
    """

    student = Student(
        age=21,
        skills=["Customer Service"],
        available_start=15,
        available_end=22,
        max_hours=20,
        max_distance=5,
    )

    job = Job(
        id="TEST005",
        company="Far Company",
        title="Far Away Job",
        min_age=18,
        skills=["Customer Service"],
        distance=8,
        hours=10,
        salary=12,
        shift_start=16,
        shift_end=20,
    )

    assert check_constraints(
        student,
        job
    ) is False


# ==========================================================
# TEST CASE 7
# ==========================================================

def test_working_hours_constraint():
    """
    Test Case 7:

    A job requiring more hours than the student's maximum
    must be rejected.
    """

    student = Student(
        age=21,
        skills=["Customer Service"],
        available_start=15,
        available_end=22,
        max_hours=10,
        max_distance=10,
    )

    job = Job(
        id="TEST006",
        company="Long Hours Company",
        title="Long Hours Job",
        min_age=18,
        skills=["Customer Service"],
        distance=3,
        hours=20,
        salary=12,
        shift_start=16,
        shift_end=20,
    )

    assert check_constraints(
        student,
        job
    ) is False


# ==========================================================
# TEST CASE 8
# ==========================================================

def test_skill_constraint():
    """
    Test Case 8:

    A job with no matching student skills must be rejected.
    """

    student = Student(
        age=21,
        skills=["Customer Service"],
        available_start=15,
        available_end=22,
        max_hours=20,
        max_distance=10,
    )

    job = Job(
        id="TEST007",
        company="Technology Company",
        title="Technical Support Job",
        min_age=18,
        skills=[
            "Python",
            "Technical Support"
        ],
        distance=3,
        hours=10,
        salary=13,
        shift_start=16,
        shift_end=20,
    )

    assert check_constraints(
        student,
        job
    ) is False


# ==========================================================
# TEST CASE 9
# ==========================================================

def test_astar_search_result_metrics():
    """
    Test Case 9:

    The A* result should contain valid search metrics.
    """

    student = Student(
        age=21,
        skills=["Customer Service"],
        available_start=15,
        available_end=22,
        max_hours=20,
        max_distance=10,
    )

    jobs = load_jobs(DATA_PATH)

    result = a_star_search(
        student,
        jobs
    )

    assert isinstance(
        result,
        SearchResult
    )

    # Execution time should never be negative.
    assert result.execution_time_s >= 0

    # Jobs expanded should be zero or greater.
    assert result.jobs_expanded >= 0

    # Nodes generated should be zero or greater.
    assert result.nodes_generated >= 0

    # If a job is found, cost must be finite.
    if result.job is not None:

        assert result.cost < float("inf")

        assert result.jobs_expanded > 0

        assert result.nodes_generated > 0

    # If no job is found, cost should be infinity.
    else:

        assert result.cost == float("inf")


# ==========================================================
# TEST CASE 10
# ==========================================================

def test_json_job_data_is_loaded():
    """
    Test Case 10:

    Verify that jobs.json exists and contains valid Job
    objects.
    """

    assert DATA_PATH.exists()

    jobs = load_jobs(
        DATA_PATH
    )

    assert isinstance(
        jobs,
        list
    )

    assert len(jobs) > 0

    for job in jobs:

        assert isinstance(
            job,
            Job
        )

        assert job.id
        assert job.title
        assert job.company

        assert job.min_age >= 0
        assert job.distance >= 0
        assert job.hours >= 0
        assert job.salary >= 0

        assert isinstance(
            job.skills,
            list
        )

        assert len(job.skills) > 0

        assert job.shift_start >= 0
        assert job.shift_end <= 24

        assert (
            job.shift_end >
            job.shift_start
        )


# ==========================================================
# TEST CASE 11
# ==========================================================

def test_astar_expands_multiple_search_stages():
    """
    Test Case 11:

    Verify that A* does not immediately treat a valid job
    as a goal.

    The multi-stage A* implementation should expand:

        Stage 0 -> Skill
        Stage 1 -> Distance
        Stage 2 -> Working Hours
        Stage 3 -> Salary
        Stage 4 -> Goal
    """

    student = Student(
        age=21,
        skills=["Customer Service"],
        available_start=15,
        available_end=22,
        max_hours=20,
        max_distance=10,
    )

    jobs = [
        Job(
            id="TEST008",
            company="Test Cafe",
            title="Customer Service Job",
            min_age=18,
            skills=["Customer Service"],
            distance=2,
            hours=10,
            salary=12,
            shift_start=15,
            shift_end=19,
        )
    ]

    result = a_star_search(
        student,
        jobs
    )

    assert result is not None

    assert result.job is not None

    # At least five nodes should be expanded:
    #
    # Stage 0
    # Stage 1
    # Stage 2
    # Stage 3
    # Stage 4 / Goal
    #
    assert result.jobs_expanded >= 5

    # Multiple nodes should have been generated.
    assert result.nodes_generated >= 5


# ==========================================================
# TEST CASE 12
# ==========================================================

def test_astar_reaches_goal_state():
    """
    Test Case 12:

    Verify that A* returns a completed candidate after
    passing through all evaluation stages.
    """

    student = Student(
        age=21,
        skills=["Customer Service"],
        available_start=15,
        available_end=22,
        max_hours=20,
        max_distance=10,
    )

    job = Job(
        id="TEST009",
        company="Goal Test Cafe",
        title="Goal State Job",
        min_age=18,
        skills=["Customer Service"],
        distance=2,
        hours=10,
        salary=12,
        shift_start=15,
        shift_end=19,
    )

    result = a_star_search(
        student,
        [job]
    )

    assert result.job is not None

    assert result.job.id == "TEST009"

    assert result.cost < float("inf")

    # A* must perform actual search before returning.
    assert result.jobs_expanded >= 5