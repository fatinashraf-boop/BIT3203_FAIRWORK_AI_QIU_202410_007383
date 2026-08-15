"""
Heuristic functions for FairWork AI.
"""

from fairwork_ai import Job, Student


def job_matching_heuristic(
    student: Student,
    job: Job
) -> float:
    """
    Estimate the remaining matching cost.

    Lower estimated cost represents a potentially better
    job match.
    """

    student_skills = {
        skill.strip().lower()
        for skill in student.skills
    }

    job_skills = {
        skill.strip().lower()
        for skill in job.skills
    }

    matched_skills = student_skills.intersection(job_skills)

    skill_penalty = 0.0

    if not matched_skills:
        skill_penalty = 10.0

    distance_penalty = job.distance

    return distance_penalty + skill_penalty