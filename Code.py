import random
import tkinter as tk

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for i in range(cols)] for i in range(rows)]  # Initialize grid with all white cells

    def generate_random_black_cells(self, num_black_cells):
        black_cells = random.sample([(r, c) for r in range(self.rows) for c in range(self.cols)], num_black_cells)
        for cell in black_cells:
            self.grid[cell[0]][cell[1]] = 1

    def is_black(self, row, col):
        return self.grid[row][col] == 1

    def is_white(self, row, col):
        return self.grid[row][col] == 0

    def display_grid(self):
        for row in self.grid:
            print(" ".join(map(str, row)))
            
    def is_adjacent_white(self, row, col):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Horizontal and vertical directions
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols and self.is_white(new_row, new_col):
                return True
        return False

    def are_all_white_cells_connected(self):
        visited = set()

        def dfs(row, col):
            if (row, col) in visited:
                return
            visited.add((row, col))
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < self.rows and 0 <= new_col < self.cols and self.is_white(new_row, new_col):
                    dfs(new_row, new_col)

        # Find a white cell as the starting point
        start_row, start_col = -1, -1
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_white(row, col):
                    start_row, start_col = row, col
                    break
            if start_row != -1:
                break

        # If there is no white cell, they are considered connected
        if start_row == -1:
            return True

        # Start DFS from the first white cell
        dfs(start_row, start_col)

        # If all white cells are visited, they are connected
        return len(visited) == sum(row.count(0) for row in self.grid)

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

def display_results():
    grid.display_grid()
    if grid.are_all_white_cells_connected():
        result_label.config(text="Les cases blanches sont connectées entre elles.")
    else:
        result_label.config(text="Les cases blanches ne sont pas connectées entre elles.")

# Example usage
rows = 10
cols = 10
num_black_cells = 25

grid = Grid(rows, cols)
grid.generate_random_black_cells(num_black_cells)

root = tk.Tk()
grid_gui = GridGUI(root, grid)
grid_gui.draw_grid()

result_label = tk.Label(root)
result_label.pack()

display_results()

root.mainloop()
