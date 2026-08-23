# Development Log

Record substantive decisions, implementation progress, testing and debugging.
Do not list trivial file saves.

## 24 July 2026 — Concept Checkpoint

### Problem and target users
- Identified the difficulty students face when finding part-time employment that fits their academic schedules, working-hour limits, skills and travel preferences.
- Target users are university and college students looking for suitable part-time employment.

### Evidence and social value
- Students may experience difficulty balancing employment requirements with academic commitments.
- FairWork AI aims to reduce unsuitable job recommendations by considering student-specific constraints before ranking vacancies.
- The expected social value is improved accessibility to suitable part-time employment and reduced time spent manually comparing job vacancies.

### Draft PEAS
- Performance Measure: Suitable job recommendations, constraint satisfaction, search cost, execution time and successful test cases.
- Environment: Student profiles and a simulated JSON dataset of part-time job vacancies.
- Actuators: Recommend and rank suitable jobs.
- Sensors: Student input and job information from `jobs.json`.

### Proposed AI method
- Initially considered Uniform Cost Search (UCS).
- A* Search was selected as the final method because the project requires heuristic guidance to estimate job suitability.
- The system uses:
  - `g(n)` = cost accumulated from job suitability factors.
  - `h(n)` = estimated remaining suitability cost.
  - `f(n) = g(n) + h(n)` = total A* evaluation value.

### Risks or questions
- Need to ensure that hard constraints are checked before a job enters the A* frontier.
- Need to ensure the heuristic does not produce misleading recommendations.
- Need to test cases where no suitable job exists.

---

## 30 July 2026 — Technical Checkpoint

### Formal problem formulation
- Defined the initial state as a student profile combined with available job vacancies.
- Defined job candidates as states evaluated by the search process.
- Defined actions as selecting and evaluating job candidates.
- Defined hard constraints:
  - Minimum age
  - Skill compatibility
  - Available working time
  - Maximum working hours
  - Maximum travel distance
- Defined the goal as finding the most suitable valid job.

### Working baseline
- Implemented Python classes for `Student`, `Job` and search results.
- Implemented JSON job loading from `data/jobs.json`.
- Implemented constraint checking.
- Implemented suitability cost calculations.

### Algorithm or heuristic decisions
- Replaced the initial UCS approach with A* Search.
- Implemented a priority queue using Python's `heapq`.
- The A* priority is based on:

  `f(n) = g(n) + h(n)`

- The cost model considers:
  - Skill mismatch
  - Travel distance
  - Working-hour suitability
  - Salary preference
- Hard constraints are treated as filtering conditions rather than merely adding penalties.

### Testing completed
- Tested normal suitable-job recommendations.
- Tested schedule-conflict rejection.
- Tested age constraints.
- Tested cases where no suitable job exists.
- Tested whether the search selects the lower-cost candidate.

### Problems found and corrections
- Encountered an import error involving `calculate_suitability_cost` in `heuristics.py`.
- Corrected the module structure so that the heuristic functions are available to `fairwork_ai.py`.
- Updated test imports to access modules from the `src/` directory.
- Verified that the project can be executed from the project root.

---

## 4 August 2026 — Readiness Checkpoint

### Three test cases and results

#### Test Case 1 — Suitable Job
- Student:
  - Age: 21
  - Skill: Customer Service
  - Available time: 15:00–22:00
  - Maximum hours: 20 hours/week
  - Maximum distance: 10 km
- Expected result: A suitable job is recommended.
- Result: Passed.

#### Test Case 2 — Schedule Conflict
- Created a job with a working shift outside the student's available time.
- Expected result: The job is rejected.
- Result: Passed.

#### Test Case 3 — No Suitable Job
- Used restrictive student requirements.
- Expected result: No valid job is returned and the system handles the case without crashing.
- Result: Passed.

### Responsible AI reflection
- Hard constraints prevent clearly unsuitable jobs from being recommended.
- Student information should be limited to information necessary for job matching.
- The recommendation factors should be visible so users understand why a job was preferred.
- The system is intended as a decision-support tool rather than a replacement for the student's final employment decision.

### Limitations
- The job dataset is simulated and may not represent the complete real-world employment market.
- Job distance is based on the dataset rather than real-time route information.
- Skill matching currently depends on predefined skill labels.
- The prototype does not account for all factors that may influence a student's employment decision.
- A* performance and recommendation quality may change with larger or more diverse datasets.

### Slides and video status
- Completed presentation structure within the five-slide requirement.
- Prepared a live demonstration of the Python prototype.
- Prepared a backup demonstration recording in case of technical failure.
- Presentation focuses on the problem, A* method, prototype demonstration, testing and Responsible AI.

### Remaining work
- Finalise report and references.
- Verify all test results.
- Update README instructions.
- Finalise GitHub repository.
- Complete AI-use declaration.
- Prepare final presentation and competition-ready video.
- Verify that all supporting files can reproduce the prototype.

---

## 24 August 2026 — Final Submission

### Final commit SHA
- To be completed after the final GitHub commit.

### Final tag
- To be completed after creating the final release/tag.

### Summary of final changes
- Finalised FairWork AI as an A* heuristic search prototype.
- Finalised student and job data structures.
- Finalised `jobs.json` sample dataset.
- Implemented hard constraint checking.
- Implemented suitability cost and heuristic functions.
- Implemented A* search and priority queue processing.
- Added automated test cases.
- Added README and installation instructions.
- Added requirements/dependency file.
- Added testing evidence and results.
- Added Responsible AI documentation.
- Added presentation slides and demonstration video.
- Added compulsory AI-use declaration.
- Completed final report and supporting documentation.