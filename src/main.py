"""
FairWork AI
Main Entry Point

Author: Your Name
AI Method: Uniform Cost Search (UCS)
"""

from fairwork_ai import Student, load_jobs, uniform_cost_search


# ==========================================================
# Input Validation Functions
# ==========================================================

def get_int(prompt, minimum=None, maximum=None):
    """Read an integer with validation."""

    while True:

        try:
            value = int(input(prompt))

            if minimum is not None and value < minimum:
                print(f"Value must be at least {minimum}.")
                continue

            if maximum is not None and value > maximum:
                print(f"Value must not exceed {maximum}.")
                continue

            return value

        except ValueError:
            print("Invalid input. Please enter a number.")


def get_skills():
    """Read student's skills."""

    while True:

        skills = input(
            "\nEnter your skills (comma separated)\n> "
        ).strip()

        if skills == "":
            print("Please enter at least one skill.")
            continue

        return [skill.strip() for skill in skills.split(",")]


# ==========================================================
# Display Student Profile
# ==========================================================

def display_student(student):

    print("\n======================================")
    print("Student Profile")
    print("======================================")

    print(f"Age                 : {student.age}")
    print(f"Skills              : {', '.join(student.skills)}")
    print(
        f"Available Time      : "
        f"{student.available_start}:00 - "
        f"{student.available_end}:00"
    )
    print(f"Maximum Hours       : {student.max_hours} hrs/week")
    print(f"Maximum Distance    : {student.max_distance} km")


# ==========================================================
# Display Recommendation
# ==========================================================

def display_result(job):

    print("\n======================================")
    print("Recommended Job")
    print("======================================")

    print(f"Job Title           : {job.title}")
    print(f"Salary              : RM {job.salary}/hour")
    print(f"Distance            : {job.distance} km")
    print(f"Working Hours       : {job.hours} hrs/week")
    print(
        f"Shift               : "
        f"{job.shift_start}:00 - {job.shift_end}:00"
    )
    print(f"Uniform Cost        : {job.cost:.2f}")

    print("\nReason for Recommendation")

    print("✓ Meets minimum age requirement")
    print("✓ Within travel distance")
    print("✓ Within working hour limit")
    print("✓ Matches availability")
    print("✓ Lowest total cost found by UCS")


# ==========================================================
# Main Program
# ==========================================================

def main():

    print("=" * 50)
    print("          FAIRWORK AI")
    print(" Intelligent Part-Time Job Matching")
    print("=" * 50)

    print("\nPlease enter your profile.\n")

    age = get_int(
        "Age: ",
        minimum=16,
        maximum=100
    )

    skills = get_skills()

    available_start = get_int(
        "Available Start Time (0-23): ",
        0,
        23
    )

    available_end = get_int(
        "Available End Time (0-23): ",
        0,
        23
    )

    while available_end <= available_start:

        print("End time must be after start time.")

        available_end = get_int(
            "Available End Time (0-23): ",
            0,
            23
        )

    max_hours = get_int(
        "Maximum Working Hours per Week: ",
        1,
        40
    )

    max_distance = get_int(
        "Maximum Travel Distance (km): ",
        1,
        50
    )

    student = Student(
        age=age,
        skills=skills,
        available_start=available_start,
        available_end=available_end,
        max_hours=max_hours,
        max_distance=max_distance
    )

    display_student(student)

    print("\nLoading job vacancies...")

    jobs = load_jobs("../data/jobs.csv")
    print(f"{len(jobs)} jobs loaded successfully.")

    print("\nRunning Uniform Cost Search...\n")

    best_job = uniform_cost_search(
        student,
        jobs
    )

    if best_job is None:

        print("\n======================================")
        print("No Suitable Jobs Found")
        print("======================================")

        print(
            "No available job satisfies all "
            "constraints."
        )

    else:

        display_result(best_job)

    print("\nThank you for using FairWork AI.")


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    main()