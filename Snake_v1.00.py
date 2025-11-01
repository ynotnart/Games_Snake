

# Snake_game_v1.00
#
#
# Source: Deepseek
# Created: 10/31/2025
# Tony Tran

# Features
# Auto-play: The snake automatically navigates toward food while avoiding obstacles
# OR
# Manual play: You play the game.

# Retro Background: Classic grid-based design with a dark background

# Controls Summary:
# Arrow Keys: Move snake (manual mode only)

# A: Toggle between auto-play and manual play

# R: Restart game (when game over)

# ESC: Quit game

# Power-ups:

# Speed Boost (Blue): Increases snake speed

# Slow Down (Purple): Decreases snake speed

# Double Points (Yellow): Doubles growth and points when collecting food

# Score Keeper: Tracks and displays the current score

# Time Tracker: Shows how long the game has been running

# Visual Enhancements:

# Gradient-colored snake body

# Snake eyes that follow direction

# Shine effects on food

# Power-up symbols and timers


# How to Play
# The game runs automatically

# Press 'R' to restart after game over

# Press 'ESC' to quit

##########


import pygame
import random
import time
import numpy as np
from collections import deque

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
DARK_GREEN = (0, 100, 0)
GRAY = (40, 40, 40)
CYAN = (0, 255, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.grow_pending = 2  # Start with length 3
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Check for collision with self
        if new_position in self.positions[1:]:
            return False  # Game over
            
        self.positions.insert(0, new_position)
        
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()
            
        return True
    
    def grow(self, amount=1):
        self.grow_pending += amount
        self.score += 10 * amount
        
    def change_direction(self, direction):
        # Prevent 180-degree turns
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            # Draw snake body with gradient color
            color_ratio = i / max(len(self.positions), 1)
            r = int(GREEN[0] * (1 - color_ratio) + DARK_GREEN[0] * color_ratio)
            g = int(GREEN[1] * (1 - color_ratio) + DARK_GREEN[1] * color_ratio)
            b = int(GREEN[2] * (1 - color_ratio) + DARK_GREEN[2] * color_ratio)
            color = (r, g, b)
            
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)
            
            # Draw eyes on the head
            if i == 0:
                # Determine eye positions based on direction
                if self.direction == RIGHT:
                    left_eye = (p[0] * GRID_SIZE + GRID_SIZE - 5, p[1] * GRID_SIZE + 5)
                    right_eye = (p[0] * GRID_SIZE + GRID_SIZE - 5, p[1] * GRID_SIZE + GRID_SIZE - 5)
                elif self.direction == LEFT:
                    left_eye = (p[0] * GRID_SIZE + 5, p[1] * GRID_SIZE + 5)
                    right_eye = (p[0] * GRID_SIZE + 5, p[1] * GRID_SIZE + GRID_SIZE - 5)
                elif self.direction == UP:
                    left_eye = (p[0] * GRID_SIZE + 5, p[1] * GRID_SIZE + 5)
                    right_eye = (p[0] * GRID_SIZE + GRID_SIZE - 5, p[1] * GRID_SIZE + 5)
                else:  # DOWN
                    left_eye = (p[0] * GRID_SIZE + 5, p[1] * GRID_SIZE + GRID_SIZE - 5)
                    right_eye = (p[0] * GRID_SIZE + GRID_SIZE - 5, p[1] * GRID_SIZE + GRID_SIZE - 5)
                
                pygame.draw.circle(surface, WHITE, left_eye, 3)
                pygame.draw.circle(surface, WHITE, right_eye, 3)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)
        
        # Draw a shine effect
        shine_rect = pygame.Rect((self.position[0] * GRID_SIZE + 4, self.position[1] * GRID_SIZE + 4), 
                                (GRID_SIZE // 3, GRID_SIZE // 3))
        pygame.draw.ellipse(surface, (255, 200, 200), shine_rect)

class PowerUp(Food):
    def __init__(self, power_type):
        super().__init__()
        self.power_type = power_type
        self.active_time = 0
        self.duration = 5 * FPS  # 5 seconds
        
        if power_type == "speed":
            self.color = BLUE
        elif power_type == "slow":
            self.color = PURPLE
        elif power_type == "double":
            self.color = YELLOW
            
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)
        
        # Draw a symbol based on power type
        font = pygame.font.SysFont('Arial', 12, bold=True)
        if self.power_type == "speed":
            text = font.render("S", True, WHITE)
        elif self.power_type == "slow":
            text = font.render("L", True, WHITE)
        elif self.power_type == "double":
            text = font.render("2X", True, WHITE)
            
        text_rect = text.get_rect(center=(self.position[0] * GRID_SIZE + GRID_SIZE // 2, 
                                         self.position[1] * GRID_SIZE + GRID_SIZE // 2))
        surface.blit(text, text_rect)

class AutoPlayer:
    def __init__(self, snake, food):
        self.snake = snake
        self.food = food
        
    def get_next_move(self):
        head = self.snake.get_head_position()
        food_pos = self.food.position
        
        # Simple pathfinding: try to move towards food
        # First, check if moving horizontally gets us closer
        if head[0] < food_pos[0] and RIGHT != self.get_opposite_direction(self.snake.direction):
            return RIGHT
        elif head[0] > food_pos[0] and LEFT != self.get_opposite_direction(self.snake.direction):
            return LEFT
        # Then check vertical movement
        elif head[1] < food_pos[1] and DOWN != self.get_opposite_direction(self.snake.direction):
            return DOWN
        elif head[1] > food_pos[1] and UP != self.get_opposite_direction(self.snake.direction):
            return UP
        
        # If direct path is blocked, try to avoid walls and self
        return self.avoid_obstacles()
    
    def get_opposite_direction(self, direction):
        return (-direction[0], -direction[1])
    
    def avoid_obstacles(self):
        head = self.snake.get_head_position()
        possible_directions = [UP, DOWN, LEFT, RIGHT]
        
        # Remove opposite direction to prevent 180-degree turns
        opposite = self.get_opposite_direction(self.snake.direction)
        if opposite in possible_directions:
            possible_directions.remove(opposite)
            
        # Remove directions that would cause collision
        safe_directions = []
        for direction in possible_directions:
            new_x = (head[0] + direction[0]) % GRID_WIDTH
            new_y = (head[1] + direction[1]) % GRID_HEIGHT
            new_position = (new_x, new_y)
            
            if new_position not in self.snake.positions[1:]:
                safe_directions.append(direction)
                
        if safe_directions:
            return random.choice(safe_directions)
        else:
            # If no safe direction, just continue current direction
            return self.snake.direction

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GRAY, rect, 1)

def draw_retro_background(surface):
    # Draw a simple retro-style background
    surface.fill(BLACK)
    
    # Draw grid lines
    draw_grid(surface)
    
    # Draw a border
    pygame.draw.rect(surface, WHITE, (0, 0, WIDTH, HEIGHT), 2)

def draw_score_time(surface, score, elapsed_time, active_power_ups, auto_play):
    # Draw score and time at the top
    font = pygame.font.SysFont('Arial', 20, bold=True)
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))
    
    time_text = font.render(f"Time: {int(elapsed_time)}s", True, WHITE)
    surface.blit(time_text, (WIDTH - 120, 10))
    
    # Draw game mode
    mode_color = CYAN if auto_play else YELLOW
    mode_text = font.render(f"Mode: {'AUTO' if auto_play else 'HUMAN'}", True, mode_color)
    surface.blit(mode_text, (WIDTH // 2 - 60, 10))
    
    # Draw active power-ups
    if active_power_ups:
        power_text = font.render("Active: ", True, WHITE)
        surface.blit(power_text, (WIDTH // 2 - 100, 35))
        
        x_offset = WIDTH // 2 - 40
        for power_type, time_left in active_power_ups.items():
            color = BLUE if power_type == "speed" else PURPLE if power_type == "slow" else YELLOW
            power_rect = pygame.Rect(x_offset, 37, 15, 15)
            pygame.draw.rect(surface, color, power_rect)
            pygame.draw.rect(surface, WHITE, power_rect, 1)
            
            time_font = pygame.font.SysFont('Arial', 10)
            time_left_text = time_font.render(str(int(time_left/FPS)), True, WHITE)
            surface.blit(time_left_text, (x_offset + 18, 39))
            
            x_offset += 40

def draw_controls(surface):
    font = pygame.font.SysFont('Arial', 14)
    controls = [
        "CONTROLS:",
        "Arrow Keys - Move Snake",
        "A - Toggle Auto/Manual",
        "R - Restart Game",
        "ESC - Quit"
    ]
    
    for i, text in enumerate(controls):
        control_text = font.render(text, True, WHITE)
        surface.blit(control_text, (10, HEIGHT - 100 + i * 20))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Retro Snake - Toggle Auto/Manual Play")
    clock = pygame.time.Clock()
    
    snake = Snake()
    food = Food()
    auto_player = AutoPlayer(snake, food)
    
    # Power-up management
    power_ups = []
    active_power_ups = {}  # {power_type: time_left}
    power_up_spawn_timer = 0
    power_up_spawn_interval = 10 * FPS  # Spawn a power-up every 10 seconds
    
    # Game state
    game_over = False
    auto_play = True  # Start with auto-play enabled
    start_time = time.time()
    current_fps = FPS
    
    while True:
        elapsed_time = time.time() - start_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    # Reset game
                    snake.reset()
                    food.randomize_position()
                    power_ups.clear()
                    active_power_ups.clear()
                    game_over = False
                    start_time = time.time()
                    current_fps = FPS
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                elif event.key == pygame.K_a and not game_over:
                    # Toggle auto-play
                    auto_play = not auto_play
                elif not auto_play and not game_over:
                    # Human controls
                    if event.key == pygame.K_UP:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(RIGHT)
        
        if not game_over:
            # Auto-player logic
            if auto_play:
                next_direction = auto_player.get_next_move()
                snake.change_direction(next_direction)
            
            # Update snake
            if not snake.update():
                game_over = True
                
            # Check for food collision
            if snake.get_head_position() == food.position:
                snake.grow()
                food.randomize_position()
                # Make sure food doesn't spawn on snake
                while food.position in snake.positions:
                    food.randomize_position()
                    
            # Power-up spawning
            power_up_spawn_timer += 1
            if power_up_spawn_timer >= power_up_spawn_interval and len(power_ups) < 2:
                power_type = random.choice(["speed", "slow", "double"])
                new_power_up = PowerUp(power_type)
                new_power_up.randomize_position()
                # Make sure power-up doesn't spawn on snake or food
                while new_power_up.position in snake.positions or new_power_up.position == food.position:
                    new_power_up.randomize_position()
                power_ups.append(new_power_up)
                power_up_spawn_timer = 0
                
            # Check for power-up collisions
            for power_up in power_ups[:]:
                if snake.get_head_position() == power_up.position:
                    active_power_ups[power_up.power_type] = power_up.duration
                    power_ups.remove(power_up)
                    
                    # Apply power-up effects
                    if power_up.power_type == "speed":
                        current_fps = FPS * 1.5
                    elif power_up.power_type == "slow":
                        current_fps = FPS * 0.7
                    elif power_up.power_type == "double":
                        snake.grow(2)  # Double points and growth
                        
            # Update active power-ups
            for power_type in list(active_power_ups.keys()):
                active_power_ups[power_type] -= 1
                if active_power_ups[power_type] <= 0:
                    del active_power_ups[power_type]
                    # Reset effects when power-up expires
                    if power_type == "speed" or power_type == "slow":
                        current_fps = FPS
                        
        # Drawing
        draw_retro_background(screen)
        
        # Draw food
        food.draw(screen)
        
        # Draw power-ups
        for power_up in power_ups:
            power_up.draw(screen)
            
        # Draw snake
        snake.draw(screen)
        
        # Draw score, time, and mode
        draw_score_time(screen, snake.score, elapsed_time, active_power_ups, auto_play)
        
        # Draw controls
        draw_controls(screen)
        
        # Draw game over message
        if game_over:
            font = pygame.font.SysFont('Arial', 36, bold=True)
            game_over_text = font.render("GAME OVER", True, RED)
            restart_text = font.render("Press R to Restart", True, WHITE)
            
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))
        
        pygame.display.update()
        clock.tick(current_fps)

if __name__ == "__main__":
    main()
