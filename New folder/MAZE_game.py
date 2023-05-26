
#commite
import pygame
import sys
import random

# Define constants for the maze elements
WALL = '#'
START = 'S'
SPACE = ' '
EXIT = 'E'

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set the width and height of the screen (in pixels)
screen_width = 840  # Increased to accommodate the additional column
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])

# Set the title of the window
pygame.display.set_caption('Maze Game')

# Set the font for the text
font = pygame.font.Font(None, 36)

# Get the size of a maze cell
cell_width = 40
cell_height = 40

# Calculate the number of cells in the maze
num_cells_x = screen_width // cell_width
num_cells_y = screen_height // cell_height

# Define the player class
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface([cell_width, cell_height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * cell_width
        self.rect.y = pos[1] * cell_height

    def update(self, dx, dy):
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        if new_x % cell_width == 0 and new_y % cell_height == 0:
            column = new_x // cell_width
            row = new_y // cell_height

            if 0 <= row < num_cells_y and 0 <= column < num_cells_x:
                if maze[row][column] != WALL:
                    self.rect.x = new_x
                    self.rect.y = new_y

                    if column == num_cells_x - 1:
                        global game_won
                        game_won = True

# Define the wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface([cell_width, cell_height])
        self.image.fill(BLACK)  # Changed color to black
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * cell_width
        self.rect.y = pos[1] * cell_height

# Define the exit class
class Exit(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface([cell_width, cell_height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * cell_width
        self.rect.y = pos[1] * cell_height

# Generate a random maze
def generate_maze():
    maze = [[WALL] * (num_cells_x - 1) + [EXIT] for _ in range(num_cells_y)]
    stack = []
    start_pos = (1, 1)
    stack.append(start_pos)
    maze[start_pos[1]][start_pos[0]] = SPACE

    while stack:
        current_cell = stack[-1]
        x, y = current_cell
        neighbors = [(x, y-2), (x, y+2), (x-2, y), (x+2, y)]
        unvisited_neighbors = []

        for neighbor in neighbors:
            nx, ny = neighbor
            if nx >= 0 and nx < num_cells_x and ny >= 0 and ny < num_cells_y and maze[ny][nx] == WALL:
                unvisited_neighbors.append(neighbor)

        if unvisited_neighbors:
            next_cell = random.choice(unvisited_neighbors)
            nx, ny = next_cell
            maze[ny][nx] = SPACE
            maze[y + (ny-y)//2][x + (nx-x)//2] = SPACE
            stack.append(next_cell)
        else:
            stack.pop()

    return maze

# Create sprite groups
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()

# Generate maze
maze = generate_maze()

# Create wall and exit sprites
for i, row in enumerate(maze):
    for j, cell in enumerate(row):
        if cell == WALL:
            wall = Wall((j, i))
            all_sprites.add(wall)
            walls.add(wall)
        elif cell == EXIT:
            exit = Exit((j, i))
            all_sprites.add(exit)

# Create player sprite
player = Player((1, 1))
all_sprites.add(player)

# Set the clock for the game
clock = pygame.time.Clock()

# Game loop
game_over = False
game_won = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Get the keyboard input
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx = -cell_width
    elif keys[pygame.K_RIGHT]:
        dx = cell_width
    elif keys[pygame.K_UP]:
        dy = -cell_height
    elif keys[pygame.K_DOWN]:
        dy = cell_height

    # Update the player
    player.update(dx, dy)

    # Clear the screen
    screen.fill(WHITE)

    # Draw the maze
    all_sprites.draw(screen)

    # Check if the player reached the exit
    if game_won:
        game_over = True

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(100)

# Display win message
if game_won:
    text = font.render('Congratulations! You reached the exit!', True, RED)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

# Quit the game
pygame.quit()
sys.exit()
