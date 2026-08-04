# Tests

## Test Case 1: Suitable Job Recommendation

Objective:
To verify that FairWork AI correctly recommends the most suitable part-time job using Uniform Cost Search (UCS).

Input:

Age: 21
Skills: Customer Service
Available Time: 15:00–22:00
Maximum Working Hours: 20 hours/week
Maximum Distance: 10 km

Expected Outcome:
The AI filters out unsuitable jobs, calculates the path cost for all valid jobs, and recommends the job with the lowest UCS cost.

Actual Outcome:
The AI rejected jobs that violated the student's constraints, calculated the path costs of the remaining jobs, and recommended Cafe Crew because it had the lowest cost among all suitable jobs.

Result:
Passed 

## Test Case 2: Underage Student

Objective:
To verify that the AI rejects job recommendations when the student does not satisfy the minimum age requirement.

Input:

Age: 17
Skills: Customer Service
Available Time: 15:00–22:00
Maximum Working Hours: 20 hours/week
Maximum Distance: 10 km

Expected Outcome:
All jobs requiring applicants aged 18 or above are rejected, and the system reports that no suitable jobs are available.

Actual Outcome:
The AI rejected every job because the student did not meet the minimum age requirement and displayed the message "No suitable jobs found."

Result:
Passed 

## Test Case 3: Working Hours Constraint

Objective:
To verify that the AI rejects jobs exceeding the student's maximum working hours.

Input:

Age: 21
Skills: Customer Service
Available Time: 15:00–22:00
Maximum Working Hours: 10 hours/week
Maximum Distance: 10 km

Expected Outcome:
Jobs that require more than 10 working hours per week are rejected. If no suitable jobs remain, the system should return no recommendation.

Actual Outcome:
The AI correctly rejected all jobs that exceeded the student's maximum working hours and displayed "No suitable jobs found."

Result:
Passed 