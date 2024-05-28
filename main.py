import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define constants
SCREEN_WIDTH = int(input("width: "))
SCREEN_HEIGHT = int(input("height: "))
BRICK_WIDTH = int(input("tile width: "))
BRICK_HEIGHT = int(input("tile height: "))
BRICK_GAP = int(input("tile gap: "))

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker - Level Editor")

# Define a class for bricks
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.value = 1
        self.update_color()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update_color(self):
        if self.value == 1:
            self.image.fill(RED)
        elif self.value == 2:
            self.image.fill(GREEN)
        elif self.value == 3:
            self.image.fill(BLUE)

# Function to create level data from drawn bricks
def create_level_data(bricks):
    level_data = []
    rows = SCREEN_HEIGHT // (BRICK_HEIGHT + BRICK_GAP)
    cols = SCREEN_WIDTH // (BRICK_WIDTH + BRICK_GAP)
    for row in range(rows):
        row_data = []
        for col in range(cols):
            brick_found = False
            for brick in bricks:
                if brick.rect.collidepoint(col * (BRICK_WIDTH + BRICK_GAP), row * (BRICK_HEIGHT + BRICK_GAP)):
                    row_data.append(brick.value)
                    brick_found = True
                    break
            if not brick_found:
                row_data.append(0)
        level_data.append(row_data)
    return level_data

# Function to draw grid lines
def draw_grid():
    for x in range(0, SCREEN_WIDTH, BRICK_WIDTH + BRICK_GAP):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BRICK_HEIGHT + BRICK_GAP):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))

# Main game loop
drawing_bricks = pygame.sprite.Group()
drawing = False
increase_value = False
bricks_increased = {}  # Dictionary to keep track of bricks whose values have been increased
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                brick = Brick(event.pos[0] // (BRICK_WIDTH + BRICK_GAP) * (BRICK_WIDTH + BRICK_GAP),
                              event.pos[1] // (BRICK_HEIGHT + BRICK_GAP) * (BRICK_HEIGHT + BRICK_GAP))
                drawing_bricks.add(brick)
            elif event.button == 3:  # Right click to remove bricks
                for brick in drawing_bricks:
                    if brick.rect.collidepoint(event.pos):
                        drawing_bricks.remove(brick)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                brick = Brick(event.pos[0] // (BRICK_WIDTH + BRICK_GAP) * (BRICK_WIDTH + BRICK_GAP),
                              event.pos[1] // (BRICK_HEIGHT + BRICK_GAP) * (BRICK_HEIGHT + BRICK_GAP))
                drawing_bricks.add(brick)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                level_data = create_level_data(drawing_bricks)
                # Convert square brackets to curly brackets
                level_data_str = str(level_data).replace('[', '{').replace(']', '}')
                print(level_data_str)
            elif event.key == pygame.K_r:
                increase_value = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                increase_value = False
                bricks_increased.clear()  # Clear the dictionary when the key is released

    # Increase brick value while R is held down
    if increase_value:
        for brick in drawing_bricks:
            if brick.rect.collidepoint(pygame.mouse.get_pos()):
                if brick not in bricks_increased:
                    brick.value = min(brick.value + 1, 3)
                    brick.update_color()
                    bricks_increased[brick] = True

    # Draw the background and grid
    screen.fill(WHITE)
    draw_grid()

    # Draw the bricks
    drawing_bricks.draw(screen)

    pygame.display.flip()
