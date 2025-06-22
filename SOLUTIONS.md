## Solution notes

### Task 01 – Run‑Length Encoder

- Language: Python
- Approach:
  1. First, check if the string is blank — if so, return "".
  2. Initialize a result list, a counter variable, and set the first character as the current reference character.
  3. Then iterate through the string starting from the second character.
  4. If the current character matches the reference, increment the counter.
  5. If it doesn't match, append the reference character and its count to the result list, then reset the counter and reference character.
  6. After the loop ends, append the final character group to the result list.
  7. Finally, use ''.join() to convert the result list to a string and return.
- Why:
  - The approach is simple, readable, and runs in O(n) time, which is optimal for this type of linear traversal problem.
  - Using a list for intermediate results avoids expensive string concatenation in the loop, which is more memory-efficient.
  - The logic is easy to maintain and extend (e.g., for decoding or case-insensitive variations).
  - The trade-off is that it assumes the input is mostly ASCII or small character ranges — it may not be optimal for high-performance or streaming contexts.
- Time spent: ~12 mins
- Edge cases considered:
  - Empty string
  - Single-character input
  - Case sensitivity (e.g., 'aaAA' → 'a2A2')
- AI tools used: VS Code Copilot and Google search for Python built-in functions

### Task 02 – Fix‑the‑Bug

- Language: Python
- Approach:
  1. The original occurred from a race condition where multiple threads could access and modify the shared \_current variable simultaneously.
  2. I fixed this by introducing a threading.Lock() and wrapping the critical section (\_current += 1) within a with \_lock: block.
  3. This ensures mutual exclusion, allowing only one thread at a time to increment the counter safely.
- Why:
  - Using threading.Lock is the most straightforward and effective solution for synchronizing access to shared state in multithreaded Python programs.
  - It avoids complication, preserves readability, and eliminates data races without significant performance impact in this use case.
- Time spent: ~10 min
- AI tools used: VS Code Copilot and ChatGPT (for Python multithreading guidance)

### Task 03 – Sync Aggregator

- Language: Python
- Approach:
  1. The aggregator reads a list of file paths, then concurrently processes each file using a fixed-size process pool (multiprocessing.Pool) to parallelize I/O.
  2. Each file is handed off to a subprocess that wraps the core logic inside a thread with join-timeout, ensuring a per-file timeout.
  3. Results are captured in the same order as the input by tracking their index in the results list.
- Why:
  - This hybrid approach combines the robustness of process-based concurrency (to leverage CPU cores and avoid GIL bottlenecks) with per-file timeout enforcement using threads.
  - It strikes a good balance: the multiprocessing pool provides scalability and isolation, while the per-file thread ensures that individual file hangs don’t block the worker process indefinitely.
  - Input order is preserved by tracking indices in the result array.
- Time spent: ~1 hour
- AI tools used: Vs Code Copilot and ChatGPT (for file reading, worker pool and threading)

### Task 04 – SQL Reasoning

- Language: Python
- Approach:
  For Task A, the query aggregates total pledged THB per campaign and computes the percentage toward the campaign target using LEFT JOIN, GROUP BY, and ORDER BY.

  For Task B, a WITH clause constructs two ordered sets (global and Thailand-based donations), then calculates the 90th percentile (P90) for each group using OFFSET and LIMIT.

  I created two indexes to optimize:

  1. pledge(campaign_id) for faster JOIN and GROUP BY operations in Task A.
  2. donor(country, id) for filtering Thai donors and joining donor ID in Task B.

- Why:
  The SQL queries are structured to match business needs using clear CTEs (WITH blocks) for readability and maintainability. The percentile calculation logic is made explicit through sorted subqueries. Index choices focus on reducing full-table scans on the most frequently filtered or joined columns. Trade-off: using OFFSET for percentile calculation is computationally linear and could be optimized further with window functions in databases that support them.

- Edge cases considered:

  - Campaigns with no pledges (handled by LEFT JOIN)
  - Donors without matching pledges

- Time spent: ~30 mins
- AI tools used: VS Code Copilot and ChatGPT (for OFFSET percentile patterns and SQLite index strategies)
