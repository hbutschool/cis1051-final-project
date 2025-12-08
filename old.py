import math
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

heartImg = pygame.image.load("Sprite/Heart.png").convert_alpha()
heartImg = pygame.transform.scale(heartImg, (20, 20))

livesImg = pygame.image.load("Sprite/Life_Fruit.png").convert_alpha()
livesImg = pygame.transform.scale(livesImg, (20, 20))
                                  
boxWidth = int(WIDTH * 0.60)
boxHeight = int(HEIGHT * 0.60)
boxX = (WIDTH - boxWidth) // 2
boxY = (HEIGHT - boxHeight) // 2

circleCenterX = boxX + boxWidth // 2
circleCenterY = boxY + boxHeight // 2
circleRadius = min(boxWidth, boxHeight) // 2 + 50
circleAngle = 0
circleSpeed = 0.02

bossWidth = 80
bossHeight = 80
bossX = (WIDTH - bossWidth) // 2
bossY = 100
bossSpeed = 10
bossDirection = 1 # 1 = right, -1 = left
bossHp = 30

eye1 = [
    pygame.image.load("Sprite/Eye_of_Cthulhu_(Phase_1)_(1).png").convert_alpha(),
    pygame.image.load("Sprite/Eye_of_Cthulhu_(Phase_1)_(2).png").convert_alpha(),
    pygame.image.load("Sprite/Eye_of_Cthulhu_(Phase_1)_(3).png").convert_alpha(),]

eye1 = [pygame.transform.scale(frame, (bossWidth, bossHeight)) for frame in eye1]

bossFrameIndex = 0
bossAnimationSpeed = 15 # higher num, slower animation
bossFrameCounter = 0

bullets = []
bulletWidth = 10
bulletHeight = 10
bulletAmount = 0 
bulletCooldown = 30 # how many frames for ONE bullet
bulletSpeed = 3

Servant = [
    pygame.image.load("Sprite/Servant_of_Cthulhu_1.png").convert_alpha(),
    pygame.image.load("Sprite/Servant_of_Cthulhu_2.png").convert_alpha(),]

Servant = [pygame.transform.scale(img, (bulletWidth, bulletHeight)) for img in Servant]
Servant = [pygame.transform.rotate(img, 90) for img in Servant]

playerBullets = []
playerBulletWidth = 8
playerBulletHeight = 15
playerBulletSpeed = 7
playerShootCooldown = 15
playerShootTimer = 0

while running == True:
    screen.fill((255, 255, 255)) # IMPORTANT, redraws / update background???

    keys = pygame.key.get_pressed()

    playerShootTimer += 1

    if keys[pygame.K_SPACE] and playerShootTimer >= playerShootCooldown:
        playerBullets.append({
            "x": playerX + playerWidth // 2 - playerBulletWidth // 2,
            "y": playerY,
            "speed": playerBulletSpeed
        })

        playerShootTimer = 0


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
    # fixed diagonal going 41% faster
    if dx != 0 or dy != 0:
         length = (dx**2 + dy**2) ** 0.5
         dx = (dx / length) * playerSpeed
         dy = (dy / length) * playerSpeed

    playerX += dx
    playerY += dy

    bossFrameCounter += 1
    if bossFrameCounter >= bossAnimationSpeed:
        bossFrameCounter = 0
        bossFrameIndex = (bossFrameIndex + 1) % len(eye1)

    circleAngle += circleSpeed
    bossX = circleCenterX + math.cos(circleAngle) * circleRadius - bossWidth // 2
    bossY = circleCenterY + math.sin(circleAngle) * circleRadius - bossHeight // 2
    
    bulletAmount += 1 # shoots one bullet

    if bulletAmount >= bulletCooldown:
        dx = (playerX + playerWidth // 2) - (bossX + bossWidth // 2)
        dy = (playerY + playerHeight // 2) - (bossY + bossHeight // 2)
        distance = (dx ** 2 + dy ** 2) ** 0.5
        velocityX = (dx / distance) * bulletSpeed
        velocityY = (dy / distance) * bulletSpeed

        bullets.append({
            "x": bossX + bossWidth // 2 - bulletWidth // 2,
            "y": bossY,
            "vx": velocityX,
            "vy": velocityY,
            "frame": 0,
            "counter": 0,
        })
        bulletAmount = 0

    # make sure player stay inside the window
    playerX = max(boxX, min(boxX + boxWidth - playerWidth, playerX))
    playerY = max(boxY, min(boxY + boxHeight - playerHeight, playerY))

    bossRect = pygame.Rect(bossX, bossY, bossWidth, bossHeight)

    for bullet in playerBullets[:]:
        bullet["y"] -= bullet["speed"]
        pygame.draw.rect(screen, (0, 0, 0), (bullet["x"], bullet["y"], playerBulletWidth, playerBulletHeight))

        bossRect = pygame.Rect(bossX, bossY, bossWidth, bossHeight)
        bulletRect = pygame.Rect(bullet["x"], bullet["y"], playerBulletWidth, playerBulletHeight)

        if bossRect.colliderect(bulletRect):
            bossHp -= 1
            playerBullets.remove(bullet)

            continue

        if (bullet["x"] < boxX or bullet["x"] + playerBulletWidth > boxX + boxWidth or
            bullet["y"] < boxY or bullet["y"] + playerBulletHeight > boxY + boxHeight):
            playerBullets.remove(bullet)

            continue

    for bullet in bullets[:]:
        bullet["x"] += bullet["vx"]
        bullet["y"] += bullet["vy"]
        bullet["counter"] += 1
        if bullet["counter"] >= 5:
            bullet["counter"] = 0
            bullet["frame"] = (bullet["frame"] + 1) % len(Servant)

        angle = math.degrees(math.atan2(bullet["vy"], bullet["vx"]))
        currentFrame = Servant[bullet["frame"]]
        screen.blit(currentFrame, (bullet["x"], bullet["y"]))

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

        if bullet["y"] > HEIGHT:
            bullets.remove(bullet)

    barWidth = bossWidth
    barHeight = 10
    barRatio = bossHp / 30
    # health bar
    pygame.draw.rect(screen, (255, 0, 0), (bossX, bossY - 20, barWidth * barRatio, barHeight))
    pygame.draw.rect(screen, (0, 0, 0), (bossX, bossY - 20, barWidth, barHeight), 2)

    pygame.draw.rect(screen, (200, 200, 200), (boxX, boxY, boxWidth, boxHeight), 10) # box
    pygame.draw.rect(screen, (0, 0, 255), (playerX, playerY, playerWidth, playerHeight)) # player
    bossX = circleCenterX + math.cos(circleAngle) * circleRadius - bossWidth // 2
    bossY = circleCenterY + math.sin(circleAngle) * circleRadius - bossHeight // 2
    dx = circleCenterX - (bossX + bossWidth / 2)
    dy = circleCenterY - (bossY + bossHeight / 2)
    angle = math.degrees(math.atan2(dy, dx))
    rotatedBoss = pygame.transform.rotate(eye1[bossFrameIndex], -angle + 90)
    rotatedRect = rotatedBoss.get_rect(center=(bossX + bossWidth / 2, bossY + bossHeight / 2))
    screen.blit(rotatedBoss, rotatedRect.topleft) # boss ???

    for i in range(playerHearts):
         screen.blit(heartImg, (10 + i * 30, 10)) # scuffed way to display hearts lol (dont change numbers)

    for i in range(playerLives):
         screen.blit(livesImg, (10 + i * 25, 40)) # ^ same with lives (dont change numbers)

    pygame.display.flip()
    clock.tick(FRAMES)