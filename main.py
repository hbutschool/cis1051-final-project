from re import S
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
playerSpeed = 7
playerHearts = 3
playerLives = 10

boxWidth = int(WIDTH * 0.60)
boxHeight = int(HEIGHT * 0.60)
boxX = (WIDTH - boxWidth) // 2
boxY = (HEIGHT - boxHeight) // 2

bossWidth = 80
bossHeight = 80
bossX = (WIDTH - bossWidth) // 2
bossY = 100
bossSpeed = 10
bossDirection = 1 # 1 = right, -1 = left

eye1 = [
    pygame.image.load("Sprite/Eye_of_Cthulhu_(Phase_1)_(1).png").convert_alpha(),
    pygame.image.load("Sprite/Eye_of_Cthulhu_(Phase_1)_(2).png").convert_alpha(),
    pygame.image.load("Sprite/Eye_of_Cthulhu_(Phase_1)_(3).png").convert_alpha(),]


eye1 = [pygame.transform.scale(i, (bossWidth, bossHeight)) for i in eye1]

bossFrameIndex = 0
bossAnimationSpeed = 20 # higher num, slower animation
bossFrameCounter = 0

bullets = []
bulletWidth = 10
bulletHeight = 10
bulletAmount = 0 
bulletCooldown = 30 # how many frames for ONE bullet
bulletSpeed = 3

while running == True:
    screen.fill((255, 255, 255)) # IMPORTANT, redraws / update background???

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    dx = 0
    dy = 0

    if keys[pygame.K_w]:
        dy -= playerSpeed
    if keys[pygame.K_s]:
        dy += playerSpeed
    if keys[pygame.K_a]:
        dx -= playerSpeed
    if keys[pygame.K_d]:
        dx += playerSpeed

    if dx != 0 or dy != 0:
         length = (dx**2 + dy**2) ** 0.5
         dx = (dx / length) * playerSpeed
         dy = (dy / length) * playerSpeed

    playerX += dx
    playerY += dy

    bossX += bossSpeed * bossDirection

    bossFrameCounter += 1
    if bossFrameCounter >= bossAnimationSpeed:
        bossFrameCounter = 0
        bossFrameIndex = (bossFrameIndex + 1) % len(eye1)

    if (bossX <= 0) or (bossX + bossWidth >= WIDTH):
            bossDirection *= -1
    
    bulletAmount += 1 # shoots one bullet

    if bulletAmount >= bulletCooldown:
        bullets.append({"x": bossX + bossWidth // 2 - bulletWidth // 2, "y": bossY, "speed": bulletSpeed})
        bulletAmount = 0 # stop shooting

    for bullet in bullets:
         bullet["y"] += bullet["speed"]
         pygame.draw.rect(screen, (255, 0, 0), (bullet["x"], bullet["y"], bulletWidth, bulletHeight))

         playerRect = pygame.Rect(playerX, playerY, playerWidth, playerHeight)
         bulletRect = pygame.Rect(bullet["x"], bullet["y"], bulletWidth, bulletHeight)

         if playerRect.colliderect(bulletRect):
              playerHearts -= 1
        
              bullets.remove(bullet)

              if playerHearts <= 0:
                  playerLives -= 1

                  if playerLives <= 0:
                       print("GAME OVER")

                       running = False
                  else:
                       playerHearts = 3
                       

    # make sure player stay inside the window
    playerX = max(boxX, min(boxX + boxWidth - playerWidth, playerX))
    playerY = max(boxY, min(boxY + boxHeight - playerHeight, playerY))

    pygame.draw.rect(screen, (200, 200, 200), (boxX, boxY, boxWidth, boxHeight), 10) # box
    pygame.draw.rect(screen, (0, 0, 255), (playerX, playerY, playerWidth, playerHeight)) # player
    screen.blit(eye1[bossFrameIndex], (bossX, bossY)) # boss

    for i in range(playerHearts):
         pygame.draw.rect(screen, (255, 0, 0), (10 + i * 30, 10, 20, 20)) # scuffed way to display hearts lol (dont change numbers)

    for i in range(playerLives):
         pygame.draw.rect(screen, (0, 255, 0), (10 + i * 25, 40, 20, 20)) # ^ same with lives (dont change numbers)

    pygame.display.flip()
    clock.tick(FRAMES)
