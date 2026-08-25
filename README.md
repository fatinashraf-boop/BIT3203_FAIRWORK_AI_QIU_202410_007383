# AI Changemaker Agent for Social Impact

This repository is for the individual assignment in **BCS2143/BIT3203 Artificial Intelligence**, Study Intake 202607.

## Student information

- Student name: FATIN NUR HANNAH BINTI MUHAMMAD ASHRAF
- Student ID: QIU-202410-007383
- Programme: BIT
- Course code: BIT3203
- GitHub username: fatinashraf-boop

## Project title

**FairWork AI: Intelligent Student Part-Time Job Recommendation System**

## Problem summary

University students often need part-time employment to support their financial needs and gain work experience. However, finding a suitable job can be difficult when students must consider multiple constraints, including age requirements, skills, academic schedules, maximum working hours and travel distance.

FairWork AI is an AI-based student job recommendation prototype designed to help students identify suitable part-time employment opportunities. The system evaluates available job vacancies against the student's requirements and removes jobs that violate essential constraints.

The target users are university and college students looking for part-time employment. The system uses A* heuristic search to evaluate valid job candidates based on accumulated cost and heuristic suitability. The expected social value is to reduce the time and effort required to identify suitable employment while helping students avoid jobs that conflict with their academic commitments.

The prototype uses simulated job vacancy data stored in `data/jobs.json`. It is intended as a demonstration of AI search rather than a production recruitment platform.

---

## AI method

**Principal AI method: A* Heuristic Search**

FairWork AI uses A* Search to select a suitable job from the available vacancies.

The search evaluates:

- Hard constraints
  - Minimum age
  - Required skills
  - Working-time availability
  - Maximum working hours
  - Maximum travel distance

- Suitability factors
  - Skill matching
  - Travel distance
  - Working-hour suitability
  - Salary preference

The A* evaluation follows:
f(n) = g(n) + h(n)

## PEAS

- **Performance Measure:**
  - Recommendation accuracy
  - Constraint satisfaction
  - Search cost
  - Execution time
  - Number of jobs expanded
  - User suitability

- **Environment:**
  - Student profile
  - Part-time job dataset
  - Job requirements
  - Working schedules
  - Distance constraints
  - Student preferences

- **Actuators:**
  - Reject unsuitable jobs
  - Calculate job costs
  - Expand search states
  - Rank suitable jobs
  - Recommend the best job

- **Sensors:**
  - Student age
  - Student skills
  - Available working hours
  - Maximum working hours
  - Maximum travel distance
  - Job age requirements
  - Job skills
  - Job distance
  - Job schedule
  - Job salary

## Installation

```powershell
py -V:3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Running the Prototype

After installing the dependencies, run the FairWork AI prototype from
the project root:

```powershell
python src/main.py
```

## Testing

Test Case 1 — Suitable Job Recommendation
Age: 21
Skills: Customer Service
Start time: 15
End time: 22
Maximum working hours/week: 20
Maximum travel distance: 10

Expected result:
A suitable job is returned.
The returned job is valid.
The A* cost is finite.

Test Case 2 — Schedule Conflict
Age: 21
Skills: Customer Service
Available Time: 15:00–22:00
Maximum Hours: 20 hours/week
Maximum Distance: 10 km

Expected result:
Job rejected

Test Case 3 — No Suitable Job
Age: 17
Skills: Customer Service
Available Time: 15:00–18:00
Maximum Hours: 5 hours/week
Maximum Distance: 1 km

Expected result:
No suitable job found
Cost = infinity

## Repository structure

- `src/` — Python source code
- `tests/` — test scripts and test cases
- `data/` — permitted sample or simulated data
- `results/` — outputs, figures and testing evidence
- `docs/` — problem statement, PEAS and Responsible AI notes
- `presentation/` — slides and approved video link
- `DEVELOPMENT_LOG.md` — development decisions and milestones
- `AI_USE_DECLARATION.md` — compulsory AI-use declaration

## Known limitations

Technical limitations
- The A* search performance may change when the dataset becomes significantly larger.
- The heuristic depends on the suitability factors defined by the developer.
- The cost weights may require further tuning using real-world evaluation data.
Data limitations
- Job information in jobs.json is simulated.
- The accuracy of recommendations depends on the accuracy and completeness of the job data.
- The system does not currently obtain live job vacancies.
User limitations
- Users must provide accurate information about their skills, availability and constraints.
- The current prototype does not automatically verify student information.
- The system does not replace a student's own judgement when selecting a job.
Deployment limitations
- It does not currently provide a production web or mobile interface.
- Real deployment would require further usability, security and performance testing.
Responsible AI limitations
- The recommendation depends on predefined constraints and cost weights.
- A low search cost does not guarantee that a job is objectively the best choice for every student.
- The system may produce less useful recommendations when important user preferences are not represented in the input.
- Simulated data limits the ability to evaluate fairness using real-world recruitment outcomes.

## Submission

Final deadline: **24 August 2026, 12:00 am**.

Submit the private repository URL, final commit SHA and repository ZIP through eQIU. The written report is submitted through Turnitin.
