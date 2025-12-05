import pygame

# https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/creating-pygame-window/

WIDTH = 800
HEIGHT = 800
FRAMES = 60
running = True

clock = pygame.time.Clock()
screen = pygame.display.set_mode(((WIDTH, HEIGHT)))
# screen.fill((255, 255, 255))  # background (plain color, note: how to set as image?)

pygame.display.set_caption("hello world")

playerWidth = 50
playerHeight = 50
playerX = WIDTH // 2 # initial x pos
playerY = HEIGHT - 100 # initial y pos
playerSpeed = 5

bossWidth = 80
bossHeight = 80
bossX =(WIDTH - bossWidth) // 2
bossY = 100
bossSpeed = 10
bossDirection = 1 # 1 = right, -1 = left

while running == True:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if keys[pygame.K_w]:
        playerY -= playerSpeed
    if keys[pygame.K_s]:
        playerY += playerSpeed
    if keys[pygame.K_a]:
        playerX -= playerSpeed
    if keys[pygame.K_d]:
        playerX += playerSpeed

    bossX += bossSpeed * bossDirection
    
    if (bossX <= 0) or (bossX + bossWidth >= WIDTH):
            bossDirection *= -1

    # make sure player stay inside the window
    playerX = max(0, min(WIDTH - playerWidth, playerX))
    playerY = max(0, min(HEIGHT - playerHeight, playerY))

    screen.fill((255, 255, 255)) # IMPORTANT, redraws / update background???
    pygame.draw.rect(screen, (0, 0, 255), (playerX, playerY, playerWidth, playerHeight))
    pygame.draw.rect(screen, (255, 0, 0), (bossX, bossY, bossWidth, bossHeight))

    pygame.display.flip()
    clock.tick(FRAMES)