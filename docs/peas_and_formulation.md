# PEAS and Formal AI Problem Formulation

## PEAS

**Performance measure (how success is judged): The agent evaluates based on how accurately it recommends suitable part-time jobs that match student’s class schedule, age eligibility, skills, preferred distance and maximum working hours. It should minimise unsuitable recommendations, avoid conflicts with the schedule and provide fair and safe job suggestions.**


**Environment (where the agent operates): The agent will be operating in a digital job-matching environment encompassing student profiles and part-time job vacancies. Information such as job location, working hours, required skills, minimum age, job category and shift schedule would be included in the environment.**


**Actuators (how the agent acts): The agent filters out unsuitable vacancies, and ranking jobs according to student’s preferences and constraints, which would recommend the most suitable opportunities. It can also provide reasons explaining why a job is recommended or rejected.**


**Sensors (what the agent perceives): The agent perceives student information such as age, skills, class timetable, preferred location, maximum working hours and transportation limitations. It also perceives job vacancy information including job requirements, location, salary, working hours, shifts and other available details.**

## Environment properties

- Observable: (partially) The agent can observe available information about students and job vacancies, but it cannot know all real-world factors, such as whether a job is truly safe, whether the employer is reliable, or unexpected changes in work schedules.
- Deterministic: (no) The same student and job information may not always lead to the same outcome because vacancies can change, employers may reject applicants, and job information may be incomplete or inaccurate.
- Sequential: The agent's decisions can influence later actions. For example, a student may view a recommendation, apply for a job and later update their preferences or profile based on the outcome.
- Dynamic: Job vacancies, availability, working hours and employer requirements may change while the agent is operating. New jobs can be added and existing jobs can become unavailable.
- Discrete: The agent mainly works with discrete data and decisions, such as eligible/not eligible, suitable/unsuitable, recommended/not recommended and different job categories.

## State or variables
The state in FairWork AI represents the current job candidate being evaluated for a particular student. The complete problem state is defined by the student's profile, constraints and the available job vacancies.

Important variables include:
Student variables:
-Age
-Skills
-Available working start time
-Available working end time
-Maximum working hours per week
-Maximum travel distance

Job variables:
-Job ID and title
-Minimum age requirement
-Required skills
-Distance from the student
-Working hours
-Salary
-Shift start and end time

## Initial state
The initial state is created when FairWork AI receives the student's profile and the available job dataset.

Student Profile + Available Jobs + Student Constraints

Before A* evaluates the suitability of a job, the system first applies the hard constraints. Jobs that clearly violate essential requirements are removed from consideration.

This prevents the search algorithm from recommending an unsuitable job simply because it has a low calculated cost.

## Actions or domains
The actions describe what FairWork AI can do while searching through the available jobs.

At each step, the system can:
1.  Select an unexamined job.
2.  Check the student's age against the job's minimum age.
3.  Check whether the student's skills match the required skills.
4.  Check whether the job fits the student's available schedule.
5.  Check whether the working hours are within the student's limit.
6.  Check whether the job is within the maximum travel distance.
7.  Reject the job if a hard constraint is violated.
8.  Calculate the actual cost g(n) for a valid job.
9.  Calculate the heuristic h(n).
10. Calculate the A* evaluation value: f(n) = g(n) + h(n)
11. Add the candidate to the priority queue.
12. Expand the candidate with the lowest f(n) value.

## Transition model or constraints
The agent removes a job if it violates essential constraints, such as age requirements, class schedule conflicts, maximum working hours or travel distance. Jobs that satisfy these constraints are then evaluated based on skills and preferences. These constraints are treated as mandatory constraints rather than soft preferences.

## Goal test
The goal of A* is to identify the most suitable valid job for the student.

A candidate satisfies the goal requirements when:
-The student meets the minimum age.
-At least one required skill matches.
-The job fits the student's available schedule.
-The job does not exceed the student's maximum working hours.
-The job is within the student's maximum travel distance.

Among the valid candidates, A* selects the candidate with the lowest estimated total cost: 
f(n) = g(n) + h(n)

Therefore:

Goal = Find the valid job with the lowest A* evaluation cost.

If no job satisfies the hard constraints, the system returns:
No suitable job found.

## Path cost
In FairWork AI, g(n) represents the actual suitability cost calculated for a valid job.

A lower cost means the job is more suitable.

The cost can combine several factors: 
g(n) = Skill Mismatch Cost + Distance Cost + Working Hours Cost + Salary Preference Cost

In the implemented system, these factors can be weighted according to their importance.

## Heuristic, where applicable
The heuristic h(n) estimates the remaining cost or potential disadvantage of a candidate job.

For FairWork AI, the heuristic can consider:
Skill mismatch
Travel distance
Working-hour suitability
Salary preference
Schedule convenience

A simple heuristic can be represented as:
h(n) = Estimated Skill Cost + Estimated Distance Cost + Estimated Hours Cost + Estimated Salary Cost

A* considers both the current cost and the estimated cost.

This allows the system to make a more informed search decision.

---

## Appendix: draft simple reflex agent rules (early sketch, Part D)

Rule 1 — Schedule

IF the student's available time conflicts with the job's working hours, THEN reject the job.

Rule 2 — Age

IF the student's age is below the job's minimum age, THEN reject the job.

Rule 3 — Working Hours

IF the job's weekly hours exceed the student's maximum working hours, THEN reject the job.

Rule 4 — Distance

IF the job's distance exceeds the student's maximum travel distance, THEN reject the job.

Rule 5 — Skill

IF there is no matching skill between the student and job, THEN reject the job.

Rule 6 — A* Recommendation

IF the job satisfies all hard constraints, THEN calculate g(n), calculate h(n), calculate f(n) = g(n) + h(n), and place the candidate in the A* priority queue.

Rule 7 — Selection

IF multiple valid jobs exist, THEN select the candidate with the lowest f(n) value as the preferred recommendation.
