"""
FairWork AI - A* Heuristic and Cost Functions

A* evaluation:

    f(n) = g(n) + h(n)

For FairWork AI:

    g(n) = skill mismatch cost + distance cost

    h(n) = working-hours cost + salary cost

    f(n) = total suitability cost

Lower cost = better job recommendation.

Hard constraints such as age, availability,
maximum hours and maximum distance are handled
before a job enters the A* search.
"""


# ==========================================================
# Skill Mismatch Cost
# ==========================================================

def skill_mismatch_cost(student, job):
    """
    Calculate the skill mismatch cost.

    A higher skill match produces a lower cost.

    Cost range:
        0 = complete skill match
        10 = no matching skill
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

def distance_cost(student, job):
    """
    Calculate travel distance cost.

    A closer job receives a lower cost.

    The student's maximum acceptable distance
    is used as the reference value.
    """

    if student.max_distance <= 0:
        return 0.0

    ratio = job.distance / student.max_distance

    return ratio * 10.0


# ==========================================================
# Working Hours Cost
# ==========================================================

def working_hours_cost(student, job):
    """
    Calculate working-hours cost.

    Jobs requiring fewer hours receive a lower cost
    because they provide greater flexibility for students.
    """

    if student.max_hours <= 0:
        return 0.0

    ratio = job.hours / student.max_hours

    return ratio * 10.0


# ==========================================================
# Salary Cost
# ==========================================================

def salary_cost(job):
    """
    Convert salary into a preference cost.

    Higher salary = lower cost.

    RM20/hour is used as the reference salary.

    Salary is deliberately given a lower weight so that
    salary does not dominate student-job suitability.
    """

    if job.salary <= 0:
        return 10.0

    maximum_reference_salary = 20.0

    cost = (
        1.0
        - min(job.salary, maximum_reference_salary)
        / maximum_reference_salary
    )

    return cost * 5.0


# ==========================================================
# G(N) - Accumulated Cost
# ==========================================================

def calculate_g_cost(student, job):
    """
    Calculate g(n), the cost accumulated so far.

    g(n) includes:

        Skill mismatch = 40%
        Distance       = 30%

    These represent the first part of the suitability
    evaluation.
    """

    skill_cost = skill_mismatch_cost(
        student,
        job
    )

    distance = distance_cost(
        student,
        job
    )

    g_cost = (
        (skill_cost * 0.40)
        + (distance * 0.30)
    )

    return round(g_cost, 4)


# ==========================================================
# H(N) - Heuristic Cost
# ==========================================================

def calculate_h_cost(student, job):
    """
    Calculate h(n), the estimated remaining cost.

    h(n) includes:

        Working hours = 20%
        Salary        = 10%

    These represent the remaining preference factors.

    For this one-step job-selection graph, the value is
    the exact remaining preference cost rather than an
    overestimate. Therefore it is admissible.
    """

    hours = working_hours_cost(
        student,
        job
    )

    salary = salary_cost(
        job
    )

    h_cost = (
        (hours * 0.20)
        + (salary * 0.10)
    )

    return round(h_cost, 4)


# ==========================================================
# F(N) - A* Evaluation
# ==========================================================

def calculate_f_cost(student, job):
    """
    Calculate the A* evaluation:

        f(n) = g(n) + h(n)

    Lower f(n) indicates a better candidate.
    """

    g_cost = calculate_g_cost(
        student,
        job
    )

    h_cost = calculate_h_cost(
        student,
        job
    )

    return round(
        g_cost + h_cost,
        4
    )


# ==========================================================
# Complete Suitability Cost
# ==========================================================

def calculate_suitability_cost(student, job):
    """
    Calculate the complete suitability cost.

    This is equivalent to:

        f(n) = g(n) + h(n)

    Weighting:

        Skill mismatch = 40%
        Distance       = 30%
        Working hours  = 20%
        Salary         = 10%

    Lower cost = better recommendation.
    """

    return calculate_f_cost(
        student,
        job
    )


# ==========================================================
# Heuristic Function
# ==========================================================

def heuristic(student, job):
    """
    A* heuristic function h(n).

    Returns the estimated remaining preference cost.
    """

    return calculate_h_cost(
        student,
        job
    )


# ==========================================================
# Exported Functions
# ==========================================================

__all__ = [
    "skill_mismatch_cost",
    "distance_cost",
    "working_hours_cost",
    "salary_cost",
    "calculate_g_cost",
    "calculate_h_cost",
    "calculate_f_cost",
    "calculate_suitability_cost",
    "heuristic",
]