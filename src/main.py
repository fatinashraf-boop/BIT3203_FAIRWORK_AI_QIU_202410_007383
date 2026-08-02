"""Main entry point for the AI Changemaker assignment.

Replace this starter code with your own implementation.
"""

"""
FairWork AI
Main Entry Point
"""

from fairwork_ai import Student, create_jobs, uniform_cost_search


def main():

    student = Student(
    age=21,
    skills=["Customer Service"],
    available_start=15,
    available_end=22,
    max_hours=20,
    max_distance=10
    )

    jobs = create_jobs()

    best_job = uniform_cost_search(student, jobs)

    print("=" * 60)
    print("FairWork AI")
    print("=" * 60)

    if best_job is None:
        print("No suitable jobs found.")
    else:
        print("\nRecommended Job")
        print("---------------------------")
        print(f"Title    : {best_job.title}")
        print(f"Salary   : RM {best_job.salary}")
        print(f"Distance : {best_job.distance} km")
        print(f"Hours    : {best_job.hours} hrs/week")
        print(f"Cost     : {best_job.cost}")


if __name__ == "__main__":
    main()