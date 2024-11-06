from tkinter import Tk, messagebox
import pygame
import sys

# Window and layout settings
window_size = 520            # Total window width and height
grid_height = 460            # Height of the grid area for pathfinding
button_height = 40           # Height of control buttons (Start, Reset)
button_padding = 10          # Padding for control buttons

# Grid and box configuration settings
columns = 20                 # Number of columns in the grid
rows = 20                    # Number of rows in the grid
box_width = window_size // columns   # Width of each box in the grid
box_height = grid_height // rows     # Height of each box in the grid

# Data structures for grid, search queue, and final path
grid = []
queue = []
path = []

# Function to initialize the grid with Box objects and set their neighbors
def create_grid():
    global grid
    grid = []
    for i in range(columns):
        arr = []
        for j in range(rows):
            arr.append(Box(i, j))
        grid.append(arr)

    # Set neighbors for each box in the grid for pathfinding purposes
    for i in range(columns):
        for j in range(rows):
            grid[i][j].set_neighbours()

# Function to initialize the Pygame window with specified dimensions and title
def create_window():
    global window
    window = pygame.display.set_mode((window_size, window_size))
    pygame.display.set_caption("Dijkstra's Pathfinder")

# Box class representing each cell in the grid
class Box:
    def __init__(self, i, j):
        # Grid position of the box
        self.x = i
        self.y = j
        # State flags for pathfinding
        self.start = False     # Indicates the start point
        self.wall = False      # Indicates a wall (obstacle)
        self.target = False    # Indicates the target point
        self.queued = False    # Indicates the box is in the queue
        self.visited = False   # Indicates the box has been visited
        self.neighbours = []   # List of neighboring boxes
        self.prior = None      # Reference to the previous box in the path

    # Draw the box with a given color on the Pygame window
    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))

    # Add neighboring boxes to the box for Dijkstra's pathfinding
    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])

# Initialize grid and window for the application
create_window()
create_grid()

# Initialize font for button labels
pygame.font.init()
font = pygame.font.SysFont("Arial", 20, bold=True)

# Function to draw Start and Reset buttons with labels
def draw_buttons():
    # Define button rectangles and colors
    start_button = pygame.Rect(button_padding, grid_height + button_padding, (window_size - 3 * button_padding) // 2, button_height)
    reset_button = pygame.Rect(start_button.right + button_padding, grid_height + button_padding, (window_size - 3 * button_padding) // 2, button_height)

    start_color = (0, 200, 0)
    reset_color = (200, 0, 0)

    # Draw the Start and Reset buttons
    pygame.draw.rect(window, start_color, start_button, border_radius=10)
    pygame.draw.rect(window, reset_color, reset_button, border_radius=10)

    # Render and place the button labels on top of buttons
    start_text = font.render("START", True, (255, 255, 255))
    reset_text = font.render("RESET", True, (255, 255, 255))

    window.blit(start_text, (start_button.x + start_button.width // 2 - start_text.get_width() // 2,
                              start_button.y + start_button.height // 2 - start_text.get_height() // 2))
    window.blit(reset_text, (reset_button.x + reset_button.width // 2 - reset_text.get_width() // 2,
                              reset_button.y + reset_button.height // 2 - reset_text.get_height() // 2))

# Function to reset the grid, clearing all pathfinding states
def reset_grid():
    global queue, path
    queue.clear()
    path.clear()
    for row in grid:
        for box in row:
            box.start = False
            box.wall = False
            box.target = False
            box.queued = False
            box.visited = False
            box.prior = None

# Main loop to handle events, pathfinding, and updating the display
def main():
    begin_search = False      # Flag to start pathfinding
    target_box_set = False    # Flag indicating if the target is set
    searching = True          # Flag for ongoing search
    target_box = None         # Reference to the target box
    start_box_set = False     # Flag indicating if the start is set
    start_box = None          # Reference to the start box

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Handle window close event
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:  # Handle mouse events
                x, y = pygame.mouse.get_pos()
                i = x // box_width
                j = y // box_height

                # Check if button area was clicked
                if grid_height + button_padding <= y <= window_size - button_padding:
                    # Start button
                    if 0 <= x <= (window_size // 2) - button_padding:
                        if target_box_set and start_box_set:
                            begin_search = True
                            continue
                    # Reset button
                    if (window_size // 2) - button_padding < x <= window_size - button_padding:
                        reset_grid()
                        start_box_set = False
                        target_box_set = False
                        continue

                # Left-click for setting start or wall
                if event.button == 1 and y < grid_height:
                    if not start_box_set and not grid[i][j].wall:
                        start_box = grid[i][j]
                        start_box.start = True
                        start_box.visited = True
                        queue.append(start_box)
                        start_box_set = True
                    else:
                        grid[i][j].wall = True  # Set walls

                # Right-click for setting the target
                elif event.button == 3 and not target_box_set and y < grid_height:
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True

            # Pathfinding process
            if begin_search:
                if queue and searching:
                    current_box = queue.pop(0)
                    current_box.visited = True
                    if current_box == target_box:  # Target found
                        searching = False
                        while current_box.prior is not None:  # Trace path back to start
                            path.append(current_box.prior)
                            current_box = current_box.prior
                    else:
                        for neighbour in current_box.neighbours:
                            if not neighbour.queued and not neighbour.wall and not neighbour.visited:
                                neighbour.queued = True
                                neighbour.prior = current_box
                                queue.append(neighbour)
                else:
                    if searching:
                        pygame.quit()
                        Tk().wm_withdraw()  # Hide Tkinter root window
                        messagebox.showinfo("Path Not Found", "No Path This Time — Try Again! 😎")
                        pygame.init()
                        create_window()
                        create_grid()
                        searching = False

        # Draw and update the grid and buttons in the window
        window.fill((30, 30, 30))
        draw_buttons()

        # Draw each box based on its state
        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (70, 70, 70))
                if box.queued:
                    box.draw(window, (255, 100, 100))
                if box.visited:
                    box.draw(window, (100, 255, 100))
                if box in path:
                    box.draw(window, (70, 130, 180))
                if box.start:
                    box.draw(window, (100, 255, 255))
                if box.wall:
                    box.draw(window, (50, 50, 50))
                if box.target:
                    box.draw(window, (255, 220, 50))

        pygame.display.flip()  # Refresh the display

main()
