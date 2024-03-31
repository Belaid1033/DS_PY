import random
import tkinter as tk
from collections import deque
from PIL import Image, ImageDraw
import os

class Grid:
    def __init__(self, rows, cols):  
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for i in range(cols)] for i in range(rows)]

    def generate_random_black_cells(self, num_black_cells):
        black_cells = random.sample([(r, c) for r in range(
            self.rows) for c in range(self.cols)], num_black_cells)
        for cell in black_cells:
            self.grid[cell[0]][cell[1]] = 1

    def is_black(self, row, col):
        return self.grid[row][col] == 1

    def is_white(self, row, col):
        return self.grid[row][col] == 0

    def display_grid(self):
        for row in self.grid:
            print(" ".join(map(str, row)))

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

        start_row, start_col = -1, -1
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_white(row, col):
                    start_row, start_col = row, col
                    break
            if start_row != -1:
                break

        if start_row == -1:
            return True

        dfs(start_row, start_col)

        return len(visited) == sum(row.count(0) for row in self.grid)

    def find_shortest_paths(self, start, end, max_paths=4):
        paths = []
        queue = deque([(start, [])])
        visited = set()

        while queue and len(paths) < max_paths:
            current, path = queue.popleft()
            if current == end:
                paths.append(path + [current])

            if current in visited:
                continue

            visited.add(current)
            for neighbor in self.get_adjacent_white_cells(current):
                queue.append((neighbor, path + [current]))

        return paths

    def get_adjacent_white_cells(self, cell):
        row, col = cell
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        adjacent_cells = []
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols and self.is_white(new_row, new_col):
                adjacent_cells.append((new_row, new_col))
        return adjacent_cells


class GridGUI:
    def __init__(self, master, grid):  
        self.master = master
        self.grid = grid
        self.canvas = tk.Canvas(
            master, width=grid.cols*30, height=grid.rows*30)
        self.canvas.pack()

    def draw_grid(self, paths):
        start_color = "green"
        end_color = "red"
        for path in paths:
            if len(path) == 0:
                continue
            for row in range(self.grid.rows):
                for col in range(self.grid.cols):
                    x1, y1 = col * 30, row * 30
                    x2, y2 = x1 + 30, y1 + 30
                    if (row, col) == path[0]:
                        color = start_color
                    elif (row, col) == path[-1]:
                        color = end_color
                    elif (row, col) in path:
                        color = "yellow"
                    elif self.grid.is_black(row, col):
                        color = "black"
                    else:
                        color = "white"
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def save_image(self, paths, username, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, f"{username}.png")
        image = Image.new("RGB", (self.grid.cols * 30, self.grid.rows * 30), color="white")
        draw = ImageDraw.Draw(image)
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                x1, y1 = col * 30, row * 30
                x2, y2 = x1 + 30, y1 + 30
                if self.grid.is_black(row, col):
                    draw.rectangle([x1, y1, x2, y2], fill="black")
                elif any((row, col) == path[0] for path in paths):
                    draw.rectangle([x1, y1, x2, y2], fill="green")
                elif any((row, col) == path[-1] for path in paths):
                    draw.rectangle([x1, y1, x2, y2], fill="red")
                elif any((row, col) in path for path in paths):
                    draw.rectangle([x1, y1, x2, y2], fill="yellow")
        image.save(file_path)

def display_results(grid, result_label):
    grid.display_grid()
    if grid.are_all_white_cells_connected():
        result_label.config(
            text="Les cases blanches sont connectées entre elles.")
    else:
        result_label.config(
            text="Les cases blanches ne sont pas connectées entre elles.")

def run_program():
    rows = int(input("Entrez le nombre de lignes de la grille : "))
    cols = int(input("Entrez le nombre de colonnes de la grille : "))
    num_black_cells = int(input("Entrez le nombre de cellules noires : "))

    grid = Grid(rows, cols)
    grid.generate_random_black_cells(num_black_cells)

    root = tk.Tk()
    grid_gui = GridGUI(root, grid)

    # Trouver jusqu'à 4 chemins les plus courts
    start_cell = (0, 0)  
    end_cell = (rows - 1, cols - 1)  
    shortest_paths = grid.find_shortest_paths(start_cell, end_cell)

    grid_gui.draw_grid(shortest_paths)

    result_label = tk.Label(root)
    result_label.pack()

    display_results(grid, result_label)

    username = input("Entrez votre nom d'utilisateur : ")
    folder_path = r"C:\Users\MOHA BOUTA\OneDrive - uca.ac.ma\Bureau\ds"
    grid_gui.save_image(shortest_paths, username, folder_path)

    root.mainloop()

run_program()
