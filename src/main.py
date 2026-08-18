"""
FairWork AI - Interactive Console Application

Run from the project root:

    python src/main.py

The program:
    1. Loads jobs from data/jobs.json.
    2. Collects a student profile.
    3. Runs Uniform Cost Search.
    4. Displays the recommended job.
    5. Displays search metrics.
"""

from pathlib import Path

from fairwork_ai import (
    Student,
    load_jobs,
    uniform_cost_search,
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
# Input Validation
# ==========================================================

def get_int_input(
    prompt,
    minimum=None,
    maximum=None
):
    """Read and validate an integer."""

    while True:

        try:

            value = int(input(prompt))

            if minimum is not None and value < minimum:
                print(
                    f"Please enter a value of at least {minimum}."
                )
                continue

            if maximum is not None and value > maximum:
                print(
                    f"Please enter a value of at most {maximum}."
                )
                continue

            return value

        except ValueError:

            print(
                "Invalid input. Please enter a whole number."
            )


def get_float_input(
    prompt,
    minimum=None,
    maximum=None
):
    """Read and validate a decimal number."""

    while True:

        try:

            value = float(input(prompt))

            if minimum is not None and value < minimum:
                print(
                    f"Please enter a value of at least {minimum}."
                )
                continue

            if maximum is not None and value > maximum:
                print(
                    f"Please enter a value of at most {maximum}."
                )
                continue

            return value

        except ValueError:

            print(
                "Invalid input. Please enter a number."
            )


def get_skills():
    """Read one or more student skills."""

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
# Student Input
# ==========================================================

def get_student_profile():
    """Collect the student's requirements."""

    print()
    print("=" * 50)
    print("          STUDENT PROFILE")
    print("=" * 50)

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

    while available_end <= available_start:

        print(
            "End time must be later than start time."
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
    """Display the collected student information."""

    print()
    print("=" * 50)
    print("          STUDENT PROFILE")
    print("=" * 50)

    print(f"Age               : {student.age}")

    print(
        "Skills            : "
        + ", ".join(student.skills)
    )

    print(
        f"Available Time    : "
        f"{student.available_start}:00 - "
        f"{student.available_end}:00"
    )

    print(
        f"Maximum Hours     : "
        f"{student.max_hours} hrs/week"
    )

    print(
        f"Maximum Distance  : "
        f"{student.max_distance:g} km"
    )

    print("=" * 50)


# ==========================================================
# Display Search Result
# ==========================================================

def display_result(result):
    """Display the FairWork AI recommendation."""

    print()
    print("=" * 50)
    print("             FAIRWORK AI")
    print("=" * 50)

    if not result.found:

        print()
        print("No suitable job was found.")
        print()
        print(
            "The AI could not find a vacancy satisfying "
            "the student's constraints."
        )

        print()
        print(f"Jobs expanded  : {result.jobs_expanded}")
        print(f"Search cost    : {result.cost}")

        print(
            f"Execution time : "
            f"{result.execution_time_s * 1000:.3f} ms"
        )

        print("=" * 50)

        return

    job = result.job

    print()
    print("RECOMMENDED JOB")
    print("-" * 50)

    print(f"Job ID          : {job.id}")
    print(f"Job             : {job.title}")
    print(f"Company         : {job.company}")
    print(f"Minimum Age     : {job.min_age}")
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
    print("AI SEARCH METRICS")
    print("-" * 50)

    print(
        f"Search Cost     : "
        f"{result.cost:.4f}"
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
    print("AI Method       : Uniform Cost Search")
    print(
        "Decision        : Lowest-cost valid job"
    )

    print("=" * 50)


# ==========================================================
# Main
# ==========================================================

def main():
    """Run the FairWork AI prototype."""

    print()
    print("=" * 50)
    print("              FAIRWORK AI")
    print("      Intelligent Student Job Matching")
    print("=" * 50)

    print()
    print("AI Method  : Uniform Cost Search")
    print("Data       : data/jobs.json")

    # ------------------------------------------------------
    # Load CSV
    # ------------------------------------------------------

    try:

        jobs = load_jobs(DATA_PATH)

    except FileNotFoundError as error:

        print()
        print("ERROR: Job data file not found.")
        print(error)

        return

    except ValueError as error:

        print()
        print("ERROR: Invalid job data.")
        print(error)

        return

    except Exception as error:

        print()
        print("ERROR: Could not load job data.")
        print(error)

        return

    if not jobs:

        print()
        print("No jobs are available.")

        return

    print()
    print(
        f"{len(jobs)} jobs loaded successfully."
    )

    # ------------------------------------------------------
    # Student input
    # ------------------------------------------------------

    student = get_student_profile()

    display_student(student)

    # ------------------------------------------------------
    # Run AI
    # ------------------------------------------------------

    print()
    print("Running FairWork AI...")
    print(
        "Applying constraints and Uniform Cost Search..."
    )

    try:

        result = uniform_cost_search(
            student,
            jobs
        )

    except Exception as error:

        print()
        print("ERROR: AI search failed.")
        print(error)

        return

    # ------------------------------------------------------
    # Output
    # ------------------------------------------------------

    display_result(result)


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    main()
