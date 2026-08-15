"""
FairWork AI
Command-line entry point.

The user enters their student profile.
Job vacancies are loaded from jobs.json.
UCS and A* are then executed and compared.
"""

from __future__ import annotations

from pathlib import Path

from fairwork_ai import (
    Student,
    load_jobs,
    uniform_cost_search,
    a_star_search,
)


DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "jobs.json"
)


# ==========================================================
# Input Helpers
# ==========================================================

def get_integer(prompt: str, minimum: int = 0) -> int:

    while True:

        try:

            value = int(input(prompt))

            if value < minimum:
                print(
                    f"Please enter a value >= {minimum}."
                )
                continue

            return value

        except ValueError:

            print("Please enter a valid whole number.")


def get_float(prompt: str, minimum: float = 0) -> float:

    while True:

        try:

            value = float(input(prompt))

            if value < minimum:
                print(
                    f"Please enter a value >= {minimum}."
                )
                continue

            return value

        except ValueError:

            print("Please enter a valid number.")


def get_skills() -> list[str]:

    while True:

        skills_input = input(
            "Enter your skills "
            "(comma separated): "
        ).strip()

        if skills_input:

            return [
                skill.strip()
                for skill in skills_input.split(",")
                if skill.strip()
            ]

        print("Please enter at least one skill.")


# ==========================================================
# Student Input
# ==========================================================

def input_student() -> Student:

    print("\n========================================")
    print("         STUDENT PROFILE INPUT")
    print("========================================")

    age = get_integer(
        "Age: ",
        minimum=15
    )

    skills = get_skills()

    class_start = get_integer(
        "Class start hour (0-23): ",
        minimum=0
    )

    while class_start > 23:

        print("Hour must be between 0 and 23.")

        class_start = get_integer(
            "Class start hour (0-23): ",
            minimum=0
        )

    class_end = get_integer(
        "Class end hour (0-23): ",
        minimum=0
    )

    while class_end <= class_start or class_end > 23:

        print(
            "Class end must be later than class start "
            "and no greater than 23."
        )

        class_end = get_integer(
            "Class end hour (0-23): ",
            minimum=0
        )

    max_hours = get_integer(
        "Maximum working hours per week: ",
        minimum=1
    )

    max_distance = get_float(
        "Maximum travel distance (km): ",
        minimum=0
    )

    return Student(
        age=age,
        skills=skills,
        class_start=class_start,
        class_end=class_end,
        max_hours=max_hours,
        max_distance=max_distance,
    )


# ==========================================================
# Display
# ==========================================================

def display_student(student: Student) -> None:

    print("\n========================================")
    print("           STUDENT PROFILE")
    print("========================================")

    print(f"Age              : {student.age}")
    print(
        f"Skills           : "
        f"{', '.join(student.skills)}"
    )

    print(
        f"Class time       : "
        f"{student.class_start}:00 - "
        f"{student.class_end}:00"
    )

    print(
        f"Maximum hours    : "
        f"{student.max_hours} hrs/week"
    )

    print(
        f"Maximum distance : "
        f"{student.max_distance} km"
    )


def display_result(
    name: str,
    result
) -> None:

    print(f"\n{name}")

    print("-" * 45)

    if result.found:

        job = result.job

        print(f"Job              : {job.title}")
        print(f"Company          : {job.company}")
        print(f"Salary           : RM {job.salary:.2f}/hour")
        print(f"Distance         : {job.distance} km")
        print(f"Working hours    : {job.hours} hrs/week")
        print(
            f"Shift            : "
            f"{job.shift_start}:00 - "
            f"{job.shift_end}:00"
        )

        print(f"Search cost      : {result.cost:.2f}")

        print(
            f"Jobs expanded    : "
            f"{result.jobs_expanded}"
        )

        print(
            f"Execution time   : "
            f"{result.execution_time_s * 1000:.3f} ms"
        )

    else:

        print("No suitable job found.")

        print(
            f"Jobs expanded    : "
            f"{result.jobs_expanded}"
        )


# ==========================================================
# Main
# ==========================================================

def main() -> None:

    print("=" * 60)
    print("                 FAIRWORK AI")
    print("=" * 60)

    print(
        "\nAI-powered part-time job recommendation prototype"
    )

    print(
        "\nLoading simulated job vacancy data..."
    )

    try:

        jobs = load_jobs(DATA_PATH)

    except FileNotFoundError:

        print(
            "\nERROR: jobs.json was not found."
        )

        print(
            f"Expected location:\n{DATA_PATH}"
        )

        return

    except (KeyError, ValueError) as error:

        print(
            f"\nERROR: Invalid jobs.json data: {error}"
        )

        return

    print(
        f"{len(jobs)} jobs loaded successfully."
    )

    student = input_student()

    display_student(student)

    print("\nSearching for suitable jobs...")

    # ------------------------------------------------------
    # Baseline
    # ------------------------------------------------------

    baseline = uniform_cost_search(
        student,
        jobs
    )

    # ------------------------------------------------------
    # Improved AI method
    # ------------------------------------------------------

    improved = a_star_search(
        student,
        jobs
    )

    print("\n")
    print("=" * 60)
    print("                 SEARCH RESULTS")
    print("=" * 60)

    display_result(
        "Baseline: Uniform Cost Search (UCS)",
        baseline
    )

    display_result(
        "Improved: A* Search",
        improved
    )

    # ------------------------------------------------------
    # Comparison
    # ------------------------------------------------------

    print("\n========================================")
    print("              COMPARISON")
    print("========================================")

    if baseline.found and improved.found:

        print(
            f"UCS cost        : "
            f"{baseline.cost:.2f}"
        )

        print(
            f"A* cost         : "
            f"{improved.cost:.2f}"
        )

        print(
            f"UCS expansions  : "
            f"{baseline.jobs_expanded}"
        )

        print(
            f"A* expansions   : "
            f"{improved.jobs_expanded}"
        )

        print(
            f"UCS time        : "
            f"{baseline.execution_time_s * 1000:.3f} ms"
        )

        print(
            f"A* time         : "
            f"{improved.execution_time_s * 1000:.3f} ms"
        )

    else:

        print(
            "No suitable job was found under "
            "the student's constraints."
        )


if __name__ == "__main__":
    main()