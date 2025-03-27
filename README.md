The SudokuAI class solves puzzles using:

- Backtracking Search – Tries possible assignments recursively.
- Forward Checking – Removes invalid values from neighboring cells' domains after each assignment.
- Minimum Remaining Values (MRV) – Chooses the most constrained cell first.
- Degree Heuristic – Breaks ties by selecting the variable that affects the most others.

Together, these techniques dramatically reduce the number of guesses and improve performance.

