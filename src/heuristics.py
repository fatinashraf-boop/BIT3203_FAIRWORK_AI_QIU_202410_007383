"""
FairWork AI - Heuristic / Suitability Functions

These functions estimate how suitable a job is for a student.

The value returned is a COST:

    Lower cost = better job
    Higher cost = worse job

This module is separate from the search algorithm so that the
cost calculation can be improved without changing the UCS
implementation.
"""


# ==========================================================
# Skill Match
# ==========================================================

def skill_mismatch_cost(student, job) -> float:
    """
    Calculate a cost based on skill matching.

    A matching skill produces a low cost.
    No matching skill produces a high cost.

    Normally, jobs without matching skills are already rejected
    by check_constraints().
    """

    student_skills = {
        skill.strip().lower()
        for skill in student.skills
    }

    job_skills = {
        skill.strip().lower()
        for skill in job.skills
    }

    if not job_skills:
        return 10.0

    matched_skills = student_skills.intersection(job_skills)

    if not matched_skills:
        return 10.0

    match_ratio = (
        len(matched_skills) / len(job_skills)
    )

    return (1.0 - match_ratio) * 10.0


# ==========================================================
# Distance Cost
# ==========================================================

def distance_cost(student, job) -> float:
    """
    Penalise jobs that are farther away.

    A closer job receives a lower cost.
    """

    if student.max_distance <= 0:
        return 0.0

    ratio = job.distance / student.max_distance

    return ratio * 10.0


# ==========================================================
# Working Hours Cost
# ==========================================================

def working_hours_cost(student, job) -> float:
    """
    Estimate how suitable the number of working hours is.

    Jobs requiring fewer hours than the student's maximum are
    generally more flexible.
    """

    if student.max_hours <= 0:
        return 0.0

    ratio = job.hours / student.max_hours

    return ratio * 10.0


# ==========================================================
# Salary Cost
# ==========================================================

def salary_cost(job) -> float:
    """
    Convert salary into a small cost.

    Higher salary = slightly lower cost.

    This prevents salary from dominating the other factors.
    """

    if job.salary <= 0:
        return 10.0

    maximum_reference_salary = 20.0

    cost = (
        1.0 -
        min(job.salary, maximum_reference_salary)
        / maximum_reference_salary
    )

    return cost * 5.0


# ==========================================================
# Combined Suitability Cost
# ==========================================================

def calculate_suitability_cost(student, job) -> float:
    """
    Calculate the total suitability cost.

    Lower cost means a better recommendation.

    Weighted factors:

        Skill match       = 40%
        Distance          = 30%
        Working hours     = 20%
        Salary            = 10%

    Hard constraints such as age, availability, distance limit
    and maximum working hours are handled separately.
    """

    skill_cost = skill_mismatch_cost(
        student,
        job
    )

    distance = distance_cost(
        student,
        job
    )

    hours = working_hours_cost(
        student,
        job
    )

    salary = salary_cost(
        job
    )

    total_cost = (
        (skill_cost * 0.40)
        + (distance * 0.30)
        + (hours * 0.20)
        + (salary * 0.10)
    )

    return round(total_cost, 4)