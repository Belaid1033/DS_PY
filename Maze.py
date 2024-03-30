import random
import tkinter as tk

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]  # Initialize grid with all white cells

    def generate_random_black_cells(self, num_black_cells):
        # Generate random black cells
        black_cells = random.sample([(r, c) for r in range(self.rows) for c in range(self.cols)], num_black_cells)
        for cell in black_cells:
            self.grid[cell[0]][cell[1]] = 1  # Set the cell as black

    def is_black(self, row, col):
        # Check if a cell is black
        return self.grid[row][col] == 1

    def is_white(self, row, col):
        # Check if a cell is white
        return self.grid[row][col] == 0

    def set_black(self, row, col):
        # Set a cell as black
        self.grid[row][col] = 1

    def set_white(self, row, col):
        # Set a cell as white
        self.grid[row][col] = 0

    def display_grid(self):
        # Display the grid
        for row in self.grid:
            print(" ".join(map(str, row)))

# Example usage
rows = 10
cols = 10
num_black_cells = 30

grid = Grid(rows, cols)
grid.generate_random_black_cells(num_black_cells)
grid.display_grid()


class GridGUI:
    def __init__(self, master, grid):
        self.master = master
        self.grid = grid
        self.canvas = tk.Canvas(master, width=cols*30, height=rows*30)
        self.canvas.pack()

    def draw_grid(self):
        for row in range(rows):
            for col in range(cols):
                x1, y1 = col*30, row*30
                x2, y2 = x1 + 30, y1 + 30
                color = "black" if self.grid.is_black(row, col) else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

# Example usage
root = tk.Tk()
grid_gui = GridGUI(root, grid)
grid_gui.draw_grid()
root.mainloop()
