import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tom and Jerry Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # Speed boost power-up
RED = (255, 0, 0)  # Slowdown power-up
BLACK = (0, 0, 0)

# Load images
tom_img = pygame.image.load("tom.png")  # Tom (Cat) image
jerry_img = pygame.image.load("jerry.png")  # Jerry (Mouse) image
cheese_img = pygame.image.load("cheese.png")  # Cheese image

# Resize images
mouse_size = 40
cat_size = 60
cheese_size = 30
power_up_size = 20

jerry_img = pygame.transform.scale(jerry_img, (mouse_size, mouse_size))
tom_img = pygame.transform.scale(tom_img, (cat_size, cat_size))
cheese_img = pygame.transform.scale(cheese_img, (cheese_size, cheese_size))

# Font setup
font = pygame.font.Font(None, 36)

def reset_game():
    global mouse_x, mouse_y, cat_x, cat_y, cheese_x, cheese_y, cat_speed, mouse_speed, score, power_ups, game_over
    
    # Initial positions
    mouse_x, mouse_y = WIDTH // 2, HEIGHT // 2
    cat_x, cat_y = random.randint(0, WIDTH - cat_size), random.randint(0, HEIGHT - cat_size)
    cheese_x, cheese_y = None, None
    power_ups = []  # Stores active power-ups
    
    # Speeds
    mouse_speed = 5
    cat_speed = 2  # Starts slow but increases with score
    
    # Score
    score = 0
    
    # Game state
    game_over = False

reset_game()

# Game loop flag
running = True
clock = pygame.time.Clock()

# Timers for auto cheese and power-up spawn
CHEESE_SPAWN_TIME = 3000  # 3 seconds
POWER_UP_SPAWN_TIME = 5000  # 5 seconds
last_cheese_spawn = pygame.time.get_ticks()
last_power_up_spawn = pygame.time.get_ticks()

while running:
    screen.fill(WHITE)  # Clear screen
    current_time = pygame.time.get_ticks()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()
    
    if not game_over:
        # Mouse movement (Arrow Keys)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            mouse_x -= mouse_speed
        if keys[pygame.K_RIGHT]:
            mouse_x += mouse_speed
        if keys[pygame.K_UP]:
            mouse_y -= mouse_speed
        if keys[pygame.K_DOWN]:
            mouse_y += mouse_speed

        # Collision boundary (Keep mouse inside the screen)
        mouse_x = max(0, min(WIDTH - mouse_size, mouse_x))
        mouse_y = max(0, min(HEIGHT - mouse_size, mouse_y))

        # AI for the cat (follows the mouse)
        if cat_x < mouse_x:
            cat_x += cat_speed
        if cat_x > mouse_x:
            cat_x -= cat_speed
        if cat_y < mouse_y:
            cat_y += cat_speed
        if cat_y > mouse_y:
            cat_y -= cat_speed

        # Auto-spawn cheese
        if cheese_x is None and (current_time - last_cheese_spawn > CHEESE_SPAWN_TIME):
            cheese_x, cheese_y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
            last_cheese_spawn = current_time

        # Auto-spawn power-ups randomly without a pattern
        if current_time - last_power_up_spawn > POWER_UP_SPAWN_TIME:
            power_ups.append({
                "x": random.randint(50, WIDTH - 50),
                "y": random.randint(50, HEIGHT - 50),
                "type": random.choice(["speed", "slowdown"])
            })
            last_power_up_spawn = current_time

        # Collision detection (Cat catches Mouse → Game Over)
        if abs(cat_x - mouse_x) < cat_size - 20 and abs(cat_y - mouse_y) < cat_size - 20:
            game_over = True

        # Cheese collection (Mouse eats Cheese → Score increases)
        if cheese_x is not None and cheese_y is not None:
            if abs(mouse_x - cheese_x) < cheese_size and abs(mouse_y - cheese_y) < cheese_size:
                score += 1  # Increase score
                cheese_x, cheese_y = None, None  # Remove cheese
                cat_speed += 0.5  # Increase cat speed

        # Power-up collection
        for power_up in power_ups[:]:  # Iterate over a copy to allow removal
            if abs(mouse_x - power_up["x"]) < power_up_size and abs(mouse_y - power_up["y"]) < power_up_size:
                if power_up["type"] == "speed":
                    mouse_speed += 2  # Speed boost
                elif power_up["type"] == "slowdown":
                    mouse_speed = max(2, mouse_speed - 2)  # Reduce speed but ensure minimum value
                power_ups.remove(power_up)  # Remove collected power-up

    # Draw Tom (Cat)
    screen.blit(tom_img, (cat_x, cat_y))
    # Draw Jerry (Mouse)
    screen.blit(jerry_img, (mouse_x, mouse_y))
    # Draw cheese (only if spawned)
    if cheese_x is not None and cheese_y is not None:
        screen.blit(cheese_img, (cheese_x, cheese_y))
    
    # Draw power-ups (Green = Speed Boost, Red = Slowdown)
    for power_up in power_ups:
        power_up_color = GREEN if power_up["type"] == "speed" else RED
        pygame.draw.rect(screen, power_up_color, (power_up["x"], power_up["y"], power_up_size, power_up_size))

    # Display Score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Display Game Over Message
    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
    
    # Refresh screen
    pygame.display.flip()
    clock.tick(30)  # Limit frame rate

pygame.quit()
