"""
fairwork_ai.py

FairWork AI
AI Method: Uniform Cost Search (UCS)

Author: Fatin Nur Hannah Binti Muhammad Ashraf
"""

import heapq


# ==========================================================
# Student
# ==========================================================

class Student:
    def __init__(
        self,
        age,
        skills,
        available_start,
        available_end,
        max_hours,
        max_distance
    ):
        self.age = age
        self.skills = skills
        self.available_start = available_start
        self.available_end = available_end
        self.max_hours = max_hours
        self.max_distance = max_distance


# ==========================================================
# Job
# ==========================================================

class Job:

    def __init__(
        self,
        title,
        min_age,
        skills,
        distance,
        hours,
        salary,
        shift_start,
        shift_end
    ):

        self.title = title
        self.min_age = min_age
        self.skills = skills
        self.distance = distance
        self.hours = hours
        self.salary = salary
        self.shift_start = shift_start
        self.shift_end = shift_end

        self.cost = 0

    def __lt__(self, other):
        return self.cost < other.cost


# ==========================================================
# Sample Dataset
# ==========================================================

def create_jobs():

    return [

        Job(
            "Cafe Crew",
            18,
            ["Customer Service"],
            3,
            20,
            12,
            15,
            20
        ),

        Job(
            "Retail Assistant",
            18,
            ["Communication"],
            7,
            24,
            13,
            16,
            22
        ),

        Job(
            "Data Entry Assistant",
            18,
            ["Microsoft Office"],
            5,
            15,
            15,
            15,
            19
        ),

        Job(
            "Delivery Rider",
            21,
            ["Driving"],
            10,
            30,
            18,
            18,
            23
        ),

        Job(
            "Bookstore Assistant",
            18,
            ["Customer Service"],
            4,
            18,
            11,
            15,
            19
        ),

        Job(
            "Library Assistant",
            18,
            ["Microsoft Office"],
            2,
            15,
            10,
            15,
            18
        )

    ]


# ==========================================================
# Cost Function
# ==========================================================

def calculate_cost(student, job):

    # Hard Constraints

    if student.age < job.min_age:
        return None

    if job.hours > student.max_hours:
        return None

    if job.distance > student.max_distance:
        return None

    # Class Schedule Conflict

    if (
    job.shift_start < student.available_start
    or job.shift_end > student.available_end
    ): return None

    cost = 0

    # Distance penalty
    cost += job.distance

    # Working hours penalty
    cost += job.hours * 0.5

    # Skill penalty

    matched = False

    for skill in job.skills:
        if skill in student.skills:
            matched = True

    if not matched:
        cost += 10

    return cost


# ==========================================================
# Uniform Cost Search
# ==========================================================

def uniform_cost_search(student, jobs):

    frontier = []

    # Add all valid jobs to frontier

    for job in jobs:

        cost = calculate_cost(student, job)

        if cost is None:
            continue

        job.cost = cost

        heapq.heappush(frontier, job)

    if not frontier:
        return None

    print("\nUniform Cost Search Expansion Order")
    print("-----------------------------------")

    explored = []

    while frontier:

        current = heapq.heappop(frontier)

        explored.append(current.title)

        print(f"{current.title:<25} Cost = {current.cost}")

        # Goal Test
        return current

    return None