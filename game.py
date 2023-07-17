import pygame
import os
import sys
pygame.font.init()
pygame.init()
pygame.display.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My game")

BLUE = (0,100,0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (169,169,169)
WHITE = (255, 255, 255)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

BLACK_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BLACK_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'Shooter1.png'))
BLACK_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLACK_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'Shooter2.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 0)

def draw_window(red, black, red_bullets, black_bullets, red_health, black_health):
    WIN.fill((BLUE))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    red_health_text = HEALTH_FONT.render("Élet: " + str(red_health), 1, WHITE)
    black_health_text = HEALTH_FONT.render("Élet: " + str(black_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(black_health_text, (10, 10))
    
    WIN.blit(BLACK_SPACESHIP, (black.x, black.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in black_bullets:
        pygame.draw.rect(WIN, GREY, bullet)
    
    pygame.display.update()
    
def black_movement(keys_pressed, black):
    if keys_pressed[pygame.K_a] and black.x - VEL > 0: # Left
        black.x -= VEL
    if keys_pressed[pygame.K_d] and black.x + VEL + black.width < BORDER.x: # Right
        black.x += VEL
    if keys_pressed[pygame.K_s] and black.y + VEL + black.height < HEIGHT - 15: # Down
        black.y += VEL
    if keys_pressed[pygame.K_w] and black.y - VEL > 0: # Up
        black.y -= VEL

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # Left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # Right
        red.x += VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: # Down
        red.y += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # Up
        red.y -= VEL

def handle_bullets(black_bullets, red_bullets, black, red):
    for bullet in black_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            black_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            black_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if black.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLACK_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    black = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    black_bullets = []
    red_bullets = []

    black_health = 10
    red_health = 10
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(black_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(black.x + black.width, black.y + black.height//2 - 2, 10, 5)
                    black_bullets.append(bullet)
                
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
            
            if event.type == RED_HIT:
                red_health -= 1

            if event.type == BLACK_HIT:
                black_health -= 1
    
        winner_text = ""
        if red_health <= 0:
            winner_text = "Fekete Nyert!!"

        if black_health <= 0:
            winner_text = "Piros Nyert!!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        black_movement(keys_pressed, black)
        red_movement(keys_pressed, red)
        
        handle_bullets(black_bullets, red_bullets, black, red)

        draw_window(red, black, red_bullets, black_bullets, red_health, black_health)
    
    main()

if __name__ == "__main__":
    main()
