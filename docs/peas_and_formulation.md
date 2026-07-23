# PEAS and Formal AI Problem Formulation

## PEAS

**Performance measure (how success is judged): The agent evaluates based on how accurately it recommends suitable part-time jobs that match student’s class schedule, age eligibility, skills, preferred distance and maximum working hours. It should minimise unsuitable recommendations, avoid conflicts with the schedule and provide fair and safe job suggestions.**


**Environment (where the agent operates): The agent will be operating in a digital job-matching environment encompassing student profiles and part-time job vacancies. Information such as job location, working hours, required skills, minimum age, job category and shift schedule would be included in the environment.**


**Actuators (how the agent acts): The agent filters out unsuitable vacancies, and ranking jobs according to student’s preferences and constraints, which would recommend the most suitable opportunities. It can also provide reasons explaining why a job is recommended or rejected.**


**Sensors (what the agent perceives): The agent perceives student information such as age, skills, class timetable, preferred location, maximum working hours and transportation limitations. It also perceives job vacancy information including job requirements, location, salary, working hours, shifts and other available details.**


## Environment properties

- Observable: <!-- (partially) The agent can observe available information about students and job vacancies, but it cannot know all real-world factors, such as whether a job is truly safe, whether the employer is reliable, or unexpected changes in work schedules.-->
- Deterministic: <!-- (no) The same student and job information may not always lead to the same outcome because vacancies can change, employers may reject applicants, and job information may be incomplete or inaccurate. -->
- Sequential: <!-- The agent's decisions can influence later actions. For example, a student may view a recommendation, apply for a job and later update their preferences or profile based on the outcome. -->
- Dynamic: <!-- Job vacancies, availability, working hours and employer requirements may change while the agent is operating. New jobs can be added and existing jobs can become unavailable. -->
- Discrete: <!-- The agent mainly works with discrete data and decisions, such as eligible/not eligible, suitable/unsuitable, recommended/not recommended and different job categories. -->

## State or variables
The state consists of the student's profile and the available part-time job vacancies. Important variables include student age, skills, class schedule, preferred location, maximum travel distance, maximum working hours, job requirements, job location and job working hours.

## Initial state
The agent starts with a student's profile and a list of available part-time job vacancies. The student's requirements and constraints are used to evaluate the available jobs.

## Actions or domains
The agent checks the student's eligibility, compares job requirements with student preferences, filters unsuitable jobs, calculates suitability scores and ranks the remaining jobs.

## Transition model or constraints
The agent removes a job if it violates essential constraints, such as age requirements, class schedule conflicts, maximum working hours or travel distance. Jobs that satisfy these constraints are then evaluated based on skills and preferences.

## Goal test
The goal is achieved when the agent identifies and ranks suitable part-time jobs that satisfy the student's essential requirements without conflicting with their studies or exceeding their working limitations.

## Path cost
The path cost represents how unsuitable a job is for the student. Higher costs are assigned to jobs with longer travel distances, lower skill matches, inconvenient working times or excessive working hours. Jobs that violate essential constraints are rejected.

## Heuristic, where applicable
The heuristic estimates how suitable a job is for the student based on factors such as skill matching, schedule compatibility, travel distance, working-hour suitability and personal preferences. A higher suitability score indicates a better job match.

---

## Appendix: draft simple reflex agent rules (early sketch, Part D)

- Rule 1 — if: The student's class schedule overlaps with the job’s working hours. then: Filter out the job.
- Rule 2 — if: The student's age is below the job's minimum age requirement. then: Filter out the job.
- Rule 3 — if: The student's skills, preferred location and maximum working hours match the job requirement. then: Recommend and rank the job as a suitable opportunity.
