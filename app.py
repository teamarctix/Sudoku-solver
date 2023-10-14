from flask import Flask, request, render_template
app = Flask(__name__)

# Sudoku solving functions
def is_valid_move(grid, row, col, num):
    if num in grid[row]:
        return False

    if num in [grid[i][col] for i in range(9)]:
        return False

    subgrid_row = (row // 3) * 3
    subgrid_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[subgrid_row + i][subgrid_col + j] == num:
                return False

    return True

def solve_sudoku(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid_move(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    # Get the Sudoku input from the form
    input_grid = []
    for i in range(9):
        row = []
        for j in range(9):
            cell_value = request.form.get(f'cell_{i}_{j}', '')
            if cell_value.isdigit():
                row.append(int(cell_value))
            else:
                row.append(0)
        input_grid.append(row)

    # Solve the Sudoku
    if solve_sudoku(input_grid):
        return render_template('solution.html', solved_grid=input_grid)
    else:
        return "No solution found for this Sudoku puzzle."

if __name__ == '__main__':
    app.run(debug=True)
