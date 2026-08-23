"""
FairWork AI - Interactive A* Application

Run from the project root:

    python src/main.py

The program:

1. Loads jobs from data/jobs.json.
2. Collects a student profile.
3. Applies hard constraints.
4. Runs A* search.
5. Displays the recommended job.
6. Displays A* search metrics.
"""


from pathlib import Path

from fairwork_ai import (
    Student,
    load_jobs,
    a_star_search,
)


# ==========================================================
# DATA PATH
# ==========================================================

DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "jobs.json"
)


# ==========================================================
# Integer Input
# ==========================================================

def get_int_input(
    prompt,
    minimum=None,
    maximum=None
):
    """
    Read and validate integer input.
    """

    while True:

        try:

            value = int(
                input(prompt)
            )

            if (
                minimum is not None
                and value < minimum
            ):
                print(
                    f"Please enter a value "
                    f"of at least {minimum}."
                )
                continue

            if (
                maximum is not None
                and value > maximum
            ):
                print(
                    f"Please enter a value "
                    f"of at most {maximum}."
                )
                continue

            return value

        except ValueError:

            print(
                "Invalid input. "
                "Please enter a whole number."
            )


# ==========================================================
# Float Input
# ==========================================================

def get_float_input(
    prompt,
    minimum=None,
    maximum=None
):
    """
    Read and validate decimal input.
    """

    while True:

        try:

            value = float(
                input(prompt)
            )

            if (
                minimum is not None
                and value < minimum
            ):
                print(
                    f"Please enter a value "
                    f"of at least {minimum}."
                )
                continue

            if (
                maximum is not None
                and value > maximum
            ):
                print(
                    f"Please enter a value "
                    f"of at most {maximum}."
                )
                continue

            return value

        except ValueError:

            print(
                "Invalid input. "
                "Please enter a number."
            )


# ==========================================================
# Skills
# ==========================================================

def get_skills():
    """
    Read one or more student skills.
    """

    while True:

        raw = input(
            "Skills (separate with commas): "
        ).strip()

        if raw:

            skills = [
                skill.strip()
                for skill in raw.split(",")
                if skill.strip()
            ]

            if skills:
                return skills

        print(
            "Please enter at least one skill."
        )


# ==========================================================
# Student Profile
# ==========================================================

def get_student_profile():
    """
    Collect student requirements.
    """

    print()
    print("=" * 60)
    print("                 STUDENT PROFILE")
    print("=" * 60)

    age = get_int_input(
        "Age: ",
        minimum=15,
        maximum=100
    )

    skills = get_skills()

    print()
    print("Available working time")

    available_start = get_int_input(
        "Start time (0-23): ",
        minimum=0,
        maximum=23
    )

    available_end = get_int_input(
        "End time (1-24): ",
        minimum=1,
        maximum=24
    )

    while (
        available_end
        <= available_start
    ):

        print(
            "End time must be later "
            "than start time."
        )

        available_end = get_int_input(
            "End time (1-24): ",
            minimum=1,
            maximum=24
        )

    max_hours = get_int_input(
        "Maximum working hours/week: ",
        minimum=1,
        maximum=168
    )

    max_distance = get_float_input(
        "Maximum travel distance (km): ",
        minimum=0
    )

    return Student(
        age=age,
        skills=skills,
        available_start=available_start,
        available_end=available_end,
        max_hours=max_hours,
        max_distance=max_distance,
    )


# ==========================================================
# Display Student
# ==========================================================

def display_student(student):
    """
    Display student profile.
    """

    print()
    print("=" * 60)
    print("                 STUDENT PROFILE")
    print("=" * 60)

    print(
        f"Age              : {student.age}"
    )

    print(
        "Skills           : "
        + ", ".join(student.skills)
    )

    print(
        f"Available Time   : "
        f"{student.available_start}:00 - "
        f"{student.available_end}:00"
    )

    print(
        f"Maximum Hours    : "
        f"{student.max_hours} hrs/week"
    )

    print(
        f"Maximum Distance : "
        f"{student.max_distance:g} km"
    )

    print("=" * 60)


# ==========================================================
# Display Result
# ==========================================================

def display_result(result):
    """
    Display A* recommendation and metrics.
    """

    print()
    print("=" * 60)
    print("                    FAIRWORK AI")
    print("=" * 60)

    if not result.found:

        print()
        print(
            "NO SUITABLE JOB WAS FOUND."
        )

        print()
        print(
            "The A* search could not find a "
            "vacancy satisfying all hard constraints."
        )

        print()
        print("A* SEARCH METRICS")
        print("-" * 60)

        print(
            f"Jobs Generated  : "
            f"{result.jobs_generated}"
        )

        print(
            f"Jobs Expanded   : "
            f"{result.jobs_expanded}"
        )

        print(
            f"Search Cost     : "
            f"{result.cost}"
        )

        print(
            f"Execution Time : "
            f"{result.execution_time_s * 1000:.3f} ms"
        )

        print("=" * 60)

        return

    job = result.job

    print()
    print("                RECOMMENDED JOB")
    print("-" * 60)

    print(
        f"Job ID          : {job.id}"
    )

    print(
        f"Job             : {job.title}"
    )

    print(
        f"Company         : {job.company}"
    )

    print(
        f"Minimum Age     : {job.min_age}"
    )

    print(
        f"Required Skills : "
        f"{', '.join(job.skills)}"
    )

    print(
        f"Distance        : "
        f"{job.distance:g} km"
    )

    print(
        f"Working Hours   : "
        f"{job.hours} hrs/week"
    )

    print(
        f"Salary          : "
        f"RM {job.salary:.2f}/hour"
    )

    print(
        f"Shift           : "
        f"{job.shift_start}:00 - "
        f"{job.shift_end}:00"
    )

    print()
    print("                A* SEARCH METRICS")
    print("-" * 60)

    print(
        f"g(n) Cost       : "
        f"{result.g_cost:.4f}"
    )

    print(
        f"h(n) Heuristic  : "
        f"{result.h_cost:.4f}"
    )

    print(
        f"f(n) = g+h      : "
        f"{result.cost:.4f}"
    )

    print(
        f"Jobs Generated  : "
        f"{result.jobs_generated}"
    )

    print(
        f"Jobs Expanded   : "
        f"{result.jobs_expanded}"
    )

    print(
        f"Execution Time  : "
        f"{result.execution_time_s * 1000:.3f} ms"
    )

    print()
    print("AI METHOD       : A* SEARCH")
    print(
        "DECISION        : LOWEST f(n) VALID JOB"
    )

    print("=" * 60)


# ==========================================================
# Main
# ==========================================================

def main():
    """
    Run FairWork AI.
    """

    print()
    print("=" * 60)
    print("                    FAIRWORK AI")
    print("       Intelligent Student Job Matching")
    print("=" * 60)

    print()
    print("AI Method : A* Search")
    print("Data      : data/jobs.json")

    # ------------------------------------------------------
    # Load jobs
    # ------------------------------------------------------

    try:

        jobs = load_jobs(
            DATA_PATH
        )

    except FileNotFoundError as error:

        print()
        print(
            "ERROR: Job data file not found."
        )

        print(error)

        return

    except ValueError as error:

        print()
        print(
            "ERROR: Invalid job data."
        )

        print(error)

        return

    except Exception as error:

        print()
        print(
            "ERROR: Could not load job data."
        )

        print(error)

        return

    if not jobs:

        print()
        print(
            "No jobs are available."
        )

        return

    print()
    print(
        f"{len(jobs)} jobs loaded successfully."
    )

    # ------------------------------------------------------
    # Student
    # ------------------------------------------------------

    student = get_student_profile()

    display_student(
        student
    )

    # ------------------------------------------------------
    # A* Search
    # ------------------------------------------------------

    print()
    print(
        "Running FairWork AI..."
    )

    print(
        "Applying hard constraints..."
    )

    print(
        "Running A* search..."
    )

    try:

        result = a_star_search(
            student,
            jobs
        )

    except Exception as error:

        print()
        print(
            "ERROR: A* search failed."
        )

        print(error)

        return

    # ------------------------------------------------------
    # Result
    # ------------------------------------------------------

    display_result(
        result
    )


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    main()