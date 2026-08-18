"""
Test cases for the FairWork AI prototype.

Run:
    python -m pytest tests/test_fairwork_ai.py -v

The tests evaluate:
1. Normal / solvable recommendation
2. Schedule conflict constraint
3. No suitable job / edge case
4. UCS cost-based job selection
"""

import sys
from pathlib import Path

# ------------------------------------------------------------
# Allow Python to find the src/ directory
# ------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"

sys.path.insert(0, str(SRC_DIR))

from fairwork_ai import (  # noqa: E402
    Student,
    Job,
    SearchResult,
    load_jobs,
    check_constraints,
    uniform_cost_search,
)


# ------------------------------------------------------------
# JSON data path
# ------------------------------------------------------------

DATA_PATH = ROOT_DIR / "data" / "jobs.json"


# ============================================================
# TEST CASE 1
# ============================================================

def test_suitable_job_recommendation():
    """
    Test Case 1: Normal / solvable case.

    A student with reasonable requirements should receive
    a suitable job recommendation from the FairWork AI.
    """

    student = Student(
        age=21,
        skills=["Customer Service"],
        available_start=15,
        available_end=22,
        max_hours=20,
        max_distance=10
    )

    jobs = load_jobs(DATA_PATH)

    result = uniform_cost_search(student, jobs)

    # Expected: a suitable job should be found.
    assert result is not None

    # SearchResult should contain a job.
    assert result.job is not None

    # The returned job must satisfy all hard constraints.
    assert check_constraints(student, result.job) is True

    # The result should have a valid search cost.
    assert result.cost < float("inf")


# ============================================================
# TEST CASE 2
# ============================================================

def test_schedule_conflict_is_rejected():
    """
    Test Case 2: Constraint / invalid-input condition.

    A job whose shift is outside the student's available
    working period must be rejected.

    This tests the schedule constraint independently of
    the search algorithm.
    """

    student = Student(
        age=21,
        skills=["Customer Service"],
        available_start=15,
        available_end=22,
        max_hours=20,
        max_distance=10
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
        shift_end=24
    )

    result = check_constraints(student, conflicting_job)

    # Expected: job is rejected because it is outside
    # the student's available time.
    assert result is False


# ============================================================
# TEST CASE 3
# ============================================================

def test_no_suitable_job():
    """
    Test Case 3: Unsolvable / over-constrained case.

    The student's requirements are deliberately restrictive:
    - age below most job requirements
    - very short maximum working hours
    - very small travel distance

    Expected outcome:
        No valid job is returned.

    The system should handle this cleanly instead of crashing.
    """

    student = Student(
        age=17,
        skills=["Customer Service"],
        available_start=15,
        available_end=18,
        max_hours=5,
        max_distance=1
    )

    jobs = load_jobs(DATA_PATH)

    result = uniform_cost_search(student, jobs)

    # SearchResult should still be returned.
    assert result is not None

    # No suitable job should be found.
    assert result.job is None

    # No valid finite path/cost should exist.
    assert result.cost == float("inf")


# ============================================================
# TEST CASE 4
# ============================================================

def test_ucs_selects_lowest_cost_job():
    """
    Test Case 4: AI search / cost comparison.

    Two jobs satisfy the student's hard constraints.

    UCS should select the job with the lower calculated cost.

    This verifies that the AI is actually using its cost
    function rather than simply returning the first job.
    """

    student = Student(
        age=21,
        skills=["Customer Service"],
        available_start=15,
        available_end=22,
        max_hours=20,
        max_distance=10
    )

    jobs = [
        Job(
            id="TEST002",
            company="Far Cafe",
            title="Far Customer Service Job",
            min_age=18,
            skills=["Customer Service"],
            distance=8,
            hours=20,
            salary=12,
            shift_start=15,
            shift_end=19
        ),

        Job(
            id="TEST003",
            company="Nearby Cafe",
            title="Nearby Customer Service Job",
            min_age=18,
            skills=["Customer Service"],
            distance=2,
            hours=15,
            salary=11,
            shift_start=15,
            shift_end=19
        )
    ]

    result = uniform_cost_search(student, jobs)

    # Expected: UCS finds a valid job.
    assert result is not None
    assert result.job is not None

    # Both jobs are valid.
    assert check_constraints(student, jobs[0]) is True
    assert check_constraints(student, jobs[1]) is True

    # The lower-cost job should be selected.
    assert result.job.title == "Nearby Customer Service Job"

    # The selected job should be cheaper according to
    # the AI's cost function.
    far_result = uniform_cost_search(student, [jobs[0]])

    assert result.cost < far_result.cost


# ============================================================
# Optional direct constraint test
# ============================================================

def test_age_constraint():
    """
    Additional edge-case test.

    A student below the minimum age requirement must not
    be considered eligible for the job.
    """

    student = Student(
        age=17,
        skills=["Customer Service"],
        available_start=15,
        available_end=22,
        max_hours=20,
        max_distance=10
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
        shift_end=20
    )

    assert check_constraints(student, job) is False