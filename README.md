# Galaxy Dodge 

### description:

space shooter game instructions below:

### instructions



**_1_**. load the project

**_2_**. Dodge the rockets coming

**_3_**. if you want to spacebar to shoot down the enemies

**_4_**. try to get the highest score

**_5_**. **(keys to control)** **left arrow** to move player left and **right arrow** to move player right.

and have fun!


***DISCLAIMER***

shooting gives you 5 points


### code
if you want see code it is below:
```py

import pygame
import random
import sys

# 1. Initialize Pygame subsystems
pygame.init()
pygame.mixer.init()
pygame.font.init()

# 2. Set Up Game Window
WIDTH, HEIGHT = 1004, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Galaxy Dodge')

# Game Constants & Settings
PLAYER_WIDTH, PLAYER_HEIGHT = 105, 105
PLAYER_SPEED = 10
ENEMY_WIDTH, ENEMY_HEIGHT = 60, 60
ENEMY_SPEED = 7    
ENEMY_SPAWN_DELAY = 20    
SCROLL_SPEED = 2  

# Bullet Constants
BULLET_WIDTH, BULLET_HEIGHT = 8, 20
BULLET_SPEED = 12
FIRE_COOLDOWN = 15  # Frames between shots

# Colors
WHITE = (255, 255, 255)
RED = (255, 50, 50)
YELLOW = (255, 235, 0)
ORANGE_RED = (255, 69, 0)
LASER_GREEN = (0, 255, 100)

# 3. Load and Scale Game Assets
bg = pygame.transform.scale(pygame.image.load('STARS.png'), (WIDTH, HEIGHT))

player_img = pygame.image.load('SS.png')
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

enemy_img = pygame.image.load('enemey.png')
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))

# Audio Setup
pygame.mixer.music.load('bg_music.wav')
kaboom_sound = pygame.mixer.Sound('kaboom.wav')
laser_sound = pygame.mixer.Sound('laser.wav')  

# Typography Setup
game_over_font = pygame.font.SysFont('Arial', 80, bold=True)
restart_font = pygame.font.SysFont('Arial', 30, bold=False)
score_font = pygame.font.SysFont('Arial', 36, bold=True)

def draw_player(player):
    screen.blit(player_img, player.topleft)

def draw_enemies(enemies):
    for enemy in enemies:
        screen.blit(enemy_img, enemy.topleft)

def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, LASER_GREEN, bullet)

def draw_score(score):
    score_surface = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, (20, 20))

def draw_particles(particles):
    for particle in particles:
        t = particle['life_progress']
        r = int(YELLOW[0] + (ORANGE_RED[0] - YELLOW[0]) * t)
        g = int(YELLOW[1] + (ORANGE_RED[1] - YELLOW[1]) * t)
        b = int(YELLOW[2] + (ORANGE_RED[2] - YELLOW[2]) * t)
        color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
                
        pygame.draw.circle(screen, color, (int(particle['x']), int(particle['y'])), int(particle['size']))

def main():
    clock = pygame.time.Clock()
        
    while True: # Main Application Wrapper
        player = pygame.Rect(WIDTH // 2, HEIGHT - PLAYER_HEIGHT - 20, PLAYER_WIDTH, PLAYER_HEIGHT)
        enemies = []
        bullets = []       
        particles = []     
        spawn_counter = 0
        fire_counter = 0   
        score = 0
        bg_y = 0  
                
        pygame.mixer.music.play(-1)
        running = True
        died_by_collision = False
                
        # --- Primary Gameplay Loop ---
        while running:
            # Event Polling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Input & Movement
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and player.x > 0:
                player.x -= PLAYER_SPEED
            if key[pygame.K_RIGHT] and player.x < WIDTH - PLAYER_WIDTH:
                player.x += PLAYER_SPEED
            
            # Shooting Input & Cooldown
            if fire_counter > 0:
                fire_counter -= 1  
                
            if key[pygame.K_SPACE] and fire_counter == 0:
                bullet_x = player.x + (PLAYER_WIDTH // 2) - (BULLET_WIDTH // 2)
                bullet_y = player.y
                new_bullet = pygame.Rect(bullet_x, bullet_y, BULLET_WIDTH, BULLET_HEIGHT)
                bullets.append(new_bullet)
                fire_counter = FIRE_COOLDOWN  
                laser_sound.play()  

            # Entity Spawning
            spawn_counter += 1
            if spawn_counter >= ENEMY_SPAWN_DELAY:
                enemy_x = random.randint(0, WIDTH - ENEMY_WIDTH)
                new_enemy = pygame.Rect(enemy_x, -ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT)
                enemies.append(new_enemy)
                spawn_counter = 0

            # Bullet Physics & Bounds
            for bullet in bullets[:]:
                bullet.y -= BULLET_SPEED
                if bullet.y < -BULLET_HEIGHT:
                    bullets.remove(bullet)

            # Physics, Bounds, and Collisions
            for enemy in enemies[:]:
                enemy.y += ENEMY_SPEED
                                
                # Enemy rocket plume particles
                for _ in range(4):
                    start_size = random.uniform(7, 11)
                    particles.append({
                        'x': enemy.x + random.randint(18, ENEMY_WIDTH - 18),
                        'y': enemy.y,
                        'vx': random.uniform(-0.2, 0.2),
                        'vy': random.uniform(-1.5, -0.5), 
                        'size': start_size,
                        'max_size': start_size,
                        'life_progress': 0.0 
                    })                                
                
                # Bullet-Enemy Collisions 
                enemy_destroyed = False
                for bullet in bullets[:]:
                    if bullet.colliderect(enemy):
                        kaboom_sound.play()
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        score += 5  
                        enemy_destroyed = True
                        break  
                
                if enemy_destroyed:
                    continue  

                # Player collision check
                player_hitbox = player.inflate(-25, -25)
                enemy_hitbox = enemy.inflate(-25, -25)
                
                if player_hitbox.colliderect(enemy_hitbox):
                    pygame.mixer.music.stop()
                    kaboom_sound.play()
                    died_by_collision = True
                    running = False

                if enemy.y > HEIGHT:
                    enemies.remove(enemy)
                    score += 1

            # Update Particles
            for particle in particles[:]:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['size'] -= 0.55                                  
                if particle['size'] <= 0:
                    particles.remove(particle)
                else:
                    particle['life_progress'] = 1.0 - (particle['size'] / particle['max_size'])

            # Update Background Position
            bg_y += SCROLL_SPEED
            if bg_y >= HEIGHT:
                bg_y = 0  

            # Game Rendering Pipeline
            screen.blit(bg, (0, bg_y))
            screen.blit(bg, (0, bg_y - HEIGHT))
                        
            draw_particles(particles)
            draw_bullets(bullets)  
            
            draw_player(player)
            draw_enemies(enemies)
            draw_score(score)
                        
            pygame.display.flip()
            clock.tick(60)

        # --- Post-Collision Game Over Loop ---
        if died_by_collision:
            start_time = pygame.time.get_ticks()
            waiting_for_input = True
            
            while waiting_for_input:
                if pygame.time.get_ticks() - start_time > 3000:
                    pygame.quit()
                    sys.exit()
                                    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            waiting_for_input = False
                            died_by_collision = False
                            break

                screen.blit(bg, (0, bg_y))
                screen.blit(bg, (0, bg_y - HEIGHT))
                                
                draw_particles(particles)
                draw_bullets(bullets)
                draw_player(player)
                draw_enemies(enemies)
                draw_score(score)

                go_surface = game_over_font.render('GAME OVER', True, RED)
                go_rect = go_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))                                
                restart_surface = restart_font.render("Press 'R' to Restart or Wait to Quit", True, WHITE)
                restart_rect = restart_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))                                
                
                screen.blit(go_surface, go_rect)
                screen.blit(restart_surface, restart_rect)                                
                pygame.display.flip()
                clock.tick(60)

if __name__ == "__main__":
    main()

```





