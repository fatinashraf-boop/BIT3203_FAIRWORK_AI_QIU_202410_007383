# Results
# Testing and Results

FairWork AI was evaluated using 10 automated pytest test cases covering
normal recommendation, constraint validation, edge cases, search behaviour,
JSON loading and search metrics.

## Test Results

The latest test execution produced:

    10 passed

The tests verified:

- Suitable job recommendation
- Age constraint
- Distance constraint
- Working-hours constraint
- Skill constraint
- Schedule conflict rejection
- No suitable job scenario
- Search result metrics
- Job JSON loading
- Lowest-cost job selection

## Search Metrics

The prototype records:

- g(n): accumulated search cost
- h(n): heuristic estimate
- f(n): total estimated cost
- Jobs generated
- Jobs expanded
- Execution time

A lower f(n) indicates a more favourable candidate under the
defined suitability model. The search metrics provide evidence that
the recommendation is based on the defined cost and heuristic rather
than simply returning the first job in the dataset.

## Interpretation

The successful test results demonstrate that the constraint-checking
logic correctly removes unsuitable jobs before recommendation.
The search metrics also demonstrate that the prototype can record
the computational behaviour of the search process, including the
number of states considered and execution time.

The current dataset is simulated and relatively small. Therefore,
the results demonstrate prototype correctness rather than real-world
employment recommendation accuracy.