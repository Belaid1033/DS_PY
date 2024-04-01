import os
import random
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageDraw

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

    def set_black(self, row, col):
        self.grid[row][col] = 1

    def set_white(self, row, col):
        self.grid[row][col] = 0

    def display_grid(self):
        for row in self.grid:
            print(" ".join(map(str, row)))

class GridGUI:
    def __init__(self, master, grid, start, end, save_callback):
        self.master = master
        self.grid = grid
        self.start = start
        self.end = end
        self.save_callback = save_callback
        self.canvas = tk.Canvas(master, width=grid.cols*30, height=grid.rows*30)
        self.canvas.pack()

    def draw_grid(self):
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                x1, y1 = col*30, row*30
                x2, y2 = x1 + 30, y1 + 30
                color = "black" if self.grid.is_black(row, col) else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        # Dessiner le point de départ en vert
        start_x1, start_y1 = self.start[1]*30+5, self.start[0]*30+5
        start_x2, start_y2 = self.start[1]*30+25, self.start[0]*30+25
        self.canvas.create_oval(start_x1, start_y1, start_x2, start_y2, fill="green", tags="oval")

        # Dessiner le point d'arrivée en rouge
        end_x1, end_y1 = self.end[1]*30+5, self.end[0]*30+5
        end_x2, end_y2 = self.end[1]*30+25, self.end[0]*30+25
        self.canvas.create_oval(end_x1, end_y1, end_x2, end_y2, fill="red", tags="oval")

        self.save_button = tk.Button(self.master, text="Save Image", command=self.save_callback)
        self.save_button.pack()

def draw_grid(canvas, grid, paths, start, end, include_paths=False):
    cell_width = 30
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            color = "white" if grid[i][j] == 0 else "black"
            canvas.create_rectangle(j*cell_width, i*cell_width, (j+1)*cell_width, (i+1)*cell_width, fill=color)

    # Dessiner le point de départ en vert
    start_x1, start_y1 = start[1]*30+5, start[0]*30+5
    start_x2, start_y2 = start[1]*30+25, start[0]*30+25
    canvas.create_oval(start_x1, start_y1, start_x2, start_y2, fill="green", tags="oval")

    # Dessiner le point d'arrivée en rouge
    end_x1, end_y1 = end[1]*30+5, end[0]*30+5
    end_x2, end_y2 = end[1]*30+25, end[0]*30+25
    canvas.create_oval(end_x1, end_y1, end_x2, end_y2, fill="red", tags="oval")

    if include_paths:
        for path in paths:
            for i in range(len(path)-1):
                x1, y1 = path[i]
                x2, y2 = path[i+1]
                canvas.create_line(y1*cell_width+cell_width/2, x1*cell_width+cell_width/2, y2*cell_width+cell_width/2, x2*cell_width+cell_width/2, fill="blue", width=2)

def find_valid_start_end(grid):
    empty_cells = [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 0]
    if empty_cells:
        return random.choice(empty_cells), random.choice(empty_cells)
    return None, None

def find_all_paths(grid, start, end, path=[]):
    x, y = start
    if start == end:
        return [path + [(x, y)]]
    if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]) or grid[x][y] == 1 or (x, y) in path:
        return []
    paths = []
    path.append((x, y))
    for neighbor in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
        paths.extend(find_all_paths(grid, neighbor, end, path))
    path.pop()
    return paths

def path_length(path):
    return len(path)

def shortest_path(paths):
    return min(paths, key=path_length)

def save_image(username, initial_grid, final_grid, root, canvas, filename, include_paths=False, paths=None, start=None, end=None):
    dirname = os.path.join(os.getcwd(), "grid_images")
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    filename = os.path.join(dirname, filename)
    image_width = len(initial_grid[0]) * 30
    image_height = len(initial_grid) * 30
    image = Image.new("RGB", (image_width, image_height))
    draw = ImageDraw.Draw(image)
    cell_width = 30
    for i in range(len(initial_grid)):
        for j in range(len(initial_grid[0])):
            if initial_grid[i][j] == 0:
                color = "white"
            else:
                color = "black"
            draw.rectangle([j*cell_width, i*cell_width, (j+1)*cell_width, (i+1)*cell_width], fill=color)

    # Dessiner les éléments supplémentaires sur l'image
    for item in canvas.find_all():
        x1, y1, x2, y2 = canvas.coords(item)
        fill = canvas.itemcget(item, "fill")
        if "oval" in canvas.gettags(item):
            draw.ellipse([x1, y1, x2, y2], fill=fill)
        elif "rectangle" in canvas.gettags(item):
            draw.rectangle([x1, y1, x2, y2], fill=fill)
        elif "line" in canvas.gettags(item) and include_paths:  # Ajouter cette condition pour inclure les chemins
            draw.line([(x1, y1), (x2, y2)], fill=fill, width=2)

    image.save(filename)
    messagebox.showinfo("Image Saved", f"Image saved as {filename}")
    root.destroy()

def main():
    username = simpledialog.askstring("Username", "Enter your username:")
    rows = simpledialog.askinteger("Grid Dimensions", "Enter number of rows:")
    cols = simpledialog.askinteger("Grid Dimensions", "Enter number of columns:")
    num_black_cells = simpledialog.askinteger("Black Cells", "Enter number of black cells:")

    grid = Grid(rows, cols)
    grid.generate_random_black_cells(num_black_cells)

    start, end = find_valid_start_end(grid.grid)

    if start is None or end is None:
        messagebox.showerror("Error", "No valid start or end point found.")
        return

    root = tk.Tk()
    root.title("Labyrinthe")

    def save_initial_callback():
        save_image(username, grid.grid, grid.grid, root, f"{username}_initial_grid_image.png")

    def save_solution_callback():
        save_image(username, grid.grid, grid.grid, root, canvas_solution, f"{username}_solution_grid_image.png", include_paths=True, paths=all_paths, start=start, end=end)

    grid_gui = GridGUI(root, grid, start, end, save_initial_callback)
    grid_gui.draw_grid()

    all_paths = find_all_paths(grid.grid, start, end)

    if not all_paths:
        messagebox.showinfo("No Path", "No paths possible between start and end points.")
        save_image(username, grid.grid, grid.grid, root, f"{username}_initial_grid_image.png")
        return

    shortest = shortest_path(all_paths)

    canvas_solution = tk.Canvas(root, width=cols*30, height=rows*30)
    canvas_solution.pack()

    draw_grid(canvas_solution, grid.grid, all_paths, start, end, include_paths=True)

    for i in range(len(shortest)-1):
        x1, y1 = shortest[i]
        x2, y2 = shortest[i+1]
        canvas_solution.create_line(y1*30+15, x1*30+15, y2*30+15, x2*30+15, fill="red", width=3)

    save_solution_button = tk.Button(root, text="Save Solution Image", command=save_solution_callback)
    save_solution_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
