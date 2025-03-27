import time

class SudokuAI:
    def __init__(self, grid):
        #initialize grid
        self.grid = grid
        # Initialize domains for each variable in grid
        self.domains = [
            [
                {var} if var != 0 else set(range(1, 10))  # Set domain for all variables (either prefilled value or 1-9)
                for var in row
            ]
            for row in grid
        ]


    def is_valid(self, row, col, value):
        # Check if assigning value to (row, col) is valid.
        # Check row
        if value in self.grid[row]:
            return False
        # Check column
        if value in [self.grid[r][col] for r in range(9)]:
            return False
        # Check 3x3 subgrid
        box_row, box_col = 3 * (row // 3), 3 * (col // 3) #identify the 3x3 subgrid
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if self.grid[r][c] == value:
                    return False
        return True

    def forward_check(self, row, col, value):
        #Update domains after assigning a value
        #updates domain of all variables in the same row
        for r in range(9):
            if r != row and value in self.domains[r][col]:
                self.domains[r][col].remove(value)
                if not self.domains[r][col]:  # If domain is empty, return False
                    #print("empty domain (row), backtrack")
                    return False
        #updates domain of all variables in the same column
        for c in range(9):
            if c != col and value in self.domains[row][c]:
                self.domains[row][c].remove(value)
                if not self.domains[row][c]:
                    #print("empty domain (column), backtrack")
                    return False
        sg_row, sg_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(sg_row, sg_row + 3):
            for c in range(sg_col, sg_col + 3):
                if (r, c) != (row, col) and value in self.domains[r][c]:
                    self.domains[r][c].remove(value)
                    if not self.domains[r][c]:
                        #print("empty domain (subgrid), backtrack")
                        return False
        return True


    def select_variable(self):
        #Select the next variable using MRV and degree heuristics.
        min_domain_size = 10 # No variable can have a domain larger than 9 so start with 10 for comparing to find smalleest domain
        candidates = [] #holds all variables with the smallest domain size
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:  # if unassigned, updatge min_domain_size and candidates accordingly
                    domain_size = len(self.domains[row][col])
                    if domain_size < min_domain_size:
                        min_domain_size = domain_size
                        candidates = [(row, col)]
                    elif domain_size == min_domain_size:
                        candidates.append((row, col))

        # Apply degree heuristic to break tie
        max_degree = -1 #same logic as min_domain_size, but reversed
        best_var = None
        for row, col in candidates:
            #coutns the number of unassigned variables in the same row and column as the one being considered
            degree = sum(1 for r in range(9) if self.grid[r][col] == 0 and r != row) + \
                     sum(1 for c in range(9) if self.grid[row][c] == 0 and c != col)
            if degree > max_degree:
                max_degree = degree
                best_var = (row, col)

        return best_var

    def solve(self):
        #Recursive backtracking to solve
        # Base case: Check if grid is complete
        if all(self.grid[row][col] != 0 for row in range(9) for col in range(9)):
            return True

        # Select next variable
        row, col = self.select_variable()

        # Try all values in domain
        for value in sorted(self.domains[row][col]):
            if self.is_valid(row, col, value):
                # Assign value and forward check
                self.grid[row][col] = value
                original_domains = [[var.copy() for var in row] for row in self.domains]
                if self.forward_check(row, col, value):
                    if self.solve():  # Recur
                        #print("Row: ", row, "col: ", col, "value: ", value, "Domain: ", self.domains[row][col])
                        return True
                # Undo assignment and restore domains
                self.grid[row][col] = 0
                self.domains = original_domains
        #print("error 7")
        return False


    def print_grid(self):
        #Print the Sudoku grid with formatting
        for i, row in enumerate(self.grid):
            if i % 3 == 0 and i != 0:
                print("-" * 21)  # Print a horizontal line every 3 rows
            for j, var in enumerate(row):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")  # Print a vertical line every 3 columns
                print(var if var != 0 else ".", end=" ")
            print()  # Move to the next line after each row

        print("\n")


# Example Usage
if __name__ == "__main__":
    grida = [
        [0, 0, 1, 0, 0, 2, 0, 0, 0],
        [0, 0, 5, 0, 0, 6, 0, 3, 0],
        [4, 6, 0, 0, 0, 5, 0, 0, 0],
        [0, 0, 0, 1, 0, 4, 0, 0, 0],
        [6, 0, 0, 8, 0, 0, 1, 4, 3],
        [0, 0, 0, 0, 9, 0, 5, 0, 8],
        [8, 0, 0, 0, 4, 9, 0, 5, 0],
        [1, 0, 0, 3, 2, 0, 0, 0, 0],
        [0, 0, 9, 0, 0, 0, 3, 0, 0]
    ]

    gridb = [
        [0, 0, 5, 0, 1, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 4, 0, 3, 0],
        [1, 0, 9, 0, 0, 0, 2, 0, 6],
        [2, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 4, 0, 0, 0, 0, 7, 0, 0],
        [5, 0, 0, 0, 0, 7, 0, 0, 1],
        [0, 0, 0, 6, 0, 3, 0, 0, 0],
        [0, 6, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 7, 0, 0, 5, 0]
    ]

    gridc = [
        [6, 7, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 5, 0, 0, 0, 0, 0, 0],
        [0, 9, 0, 5, 6, 0, 2, 0, 0],
        [3, 0, 0, 0, 8, 0, 9, 0, 0],
        [0, 0, 0, 0, 0, 0, 8, 0, 1],
        [0, 0, 0, 4, 7, 0, 0, 0, 0],
        [0, 0, 8, 6, 0, 0, 0, 9, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 6, 0, 5, 0, 0, 7, 0]
    ]

    
    start_time = time.time()  # Record start time
    solver = SudokuAI(grida)
    if solver.solve():
        solver.print_grid()
    else:
        print("No solution exists.")
    end_time = time.time()  # Record end time
    time_taken = end_time - start_time # Calculate time taken
    print(f"Time taken: {time_taken:.4f} seconds\n")  # Print time taken


    start_time = time.time()  # Record start time
    solver = SudokuAI(gridb)
    if solver.solve():
        solver.print_grid()
    else:
        print("No solution exists.")
    end_time = time.time()  # Record end time
    time_taken = end_time - start_time # Calculate time taken
    print(f"Time taken: {time_taken:.4f} seconds\n")  # Print time taken


    start_time = time.time()  # Record start time
    solver = SudokuAI(gridc)
    if solver.solve():
        solver.print_grid()
    else:
        print("No solution exists.")
    end_time = time.time()  # Record end time
    time_taken = end_time - start_time # Calculate time taken
    print(f"Time taken: {time_taken:.4f} seconds\n")  # Print time taken

