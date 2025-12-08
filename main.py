import pygame
import math

WIDTH = 800
HEIGHT = 800
FRAMES = 60
running = True

boxWidth = int(WIDTH * 0.60)
boxHeight = int(HEIGHT * 0.60)
boxX = (WIDTH - boxWidth) // 2
boxY = (HEIGHT - boxHeight) // 2

circleCenterX = boxX + boxWidth // 2
circleCenterY = boxY + boxHeight // 2

player = {
    "width": 50,
    "height": 50,
    "posX": WIDTH // 2,
    "posY": HEIGHT - 100,
    "speed": 7,
    "hearts": 3,
    "lives": 10,
    "shootCooldown": 15,
    "shootTimer": 0,
    "bullets": []
}

boss = {
    "width": 80,
    "height": 80,
    "posX": WIDTH // 2,
    "posY": 100,
    "hp": 30,
    "frameIndex": 0,
    "frameCounter": 0,
    "animSpeed": 15,
    "circleAngle": 0,
    "circleSpeed": 0.02,
    "circleRadius": min(boxWidth, boxHeight) // 2 + 50,
    "shootCooldown": 30,
    "shootTimer": 0,
    "bullets": []
}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bullet Hell Game")
clock = pygame.time.Clock()

eye = [
    pygame.image.load("Sprite/Eye_of_Cthulhu_(Phase_1)_(1).png").convert_alpha(),
    pygame.image.load("Sprite/Eye_of_Cthulhu_(Phase_1)_(2).png").convert_alpha(),
    pygame.image.load("Sprite/Eye_of_Cthulhu_(Phase_1)_(3).png").convert_alpha()
]
eye = [pygame.transform.scale(frame, (boss["width"], boss["height"])) for frame in eye]
boss["frames"] = eye

servant = [
    pygame.image.load("Sprite/Servant_of_Cthulhu_1.png").convert_alpha(),
    pygame.image.load("Sprite/Servant_of_Cthulhu_2.png").convert_alpha()
]
servant = [pygame.transform.scale(img, (10, 10)) for img in servant]
servant = [pygame.transform.rotate(img, 90) for img in servant]

heartImg = pygame.image.load("Sprite/Heart.png").convert_alpha()
heartImg = pygame.transform.scale(heartImg, (20, 20))

livesImg = pygame.image.load("Sprite/Life_Fruit.png").convert_alpha()
livesImg = pygame.transform.scale(livesImg, (20, 20))

def inputHandler(player):
    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if keys[pygame.K_w]:
        dy -= player["speed"]
    if keys[pygame.K_s]:
        dy += player["speed"]
    if keys[pygame.K_a]:
        dx -= player["speed"]
    if keys[pygame.K_d]:
        dx += player["speed"]

    if dx != 0 or dy != 0:
        length = (dx ** 2 + dy ** 2) ** 0.5
        dx = (dx / length) * player["speed"]
        dy = (dy / length) * player["speed"]

    player["shootTimer"] += 1

    if keys[pygame.K_SPACE] and player["shootTimer"] >= player["shootCooldown"]:
        player["bullets"].append({
            "x": player["posX"] + player["width"] // 2 - 4,
            "y": player["posY"],
            "speed": 7
        })

        player["shootTimer"] = 0

    return dx, dy

def updatePlayer(player, dx, dy):
    player["posX"] = max(boxX, min(boxX + boxWidth - player["width"], player["posX"] + dx))
    player["posY"] = max(boxY, min(boxY + boxHeight - player["height"], player["posY"] + dy))

def updateBoss(boss, player):
    boss["frameCounter"] += 1

    if boss["frameCounter"] >= boss["animSpeed"]:
        boss["frameCounter"] = 0
        boss["frameIndex"] = (boss["frameIndex"] + 1) % len(boss["frames"])

    boss["circleAngle"] += boss["circleSpeed"]
    boss["posX"] = circleCenterX + math.cos(boss["circleAngle"]) * boss["circleRadius"] - boss["width"] // 2
    boss["posY"] = circleCenterY + math.sin(boss["circleAngle"]) * boss["circleRadius"] - boss["height"] // 2

    boss["shootTimer"] += 1

    if boss["shootTimer"] >= boss["shootCooldown"]:
        dx = (player["posX"] + player["width"] // 2) - (boss["posX"] + boss["width"] // 2)
        dy = (player["posY"] + player["height"] // 2) - (boss["posY"] + boss["height"] // 2)

        dist = math.sqrt(dx * dx + dy * dy)
            
        vx = (dx / dist) * 3
        vy = (dy / dist) * 3

        boss["bullets"].append({
            "x": boss["posX"] + boss["width"] / 2,
            "y": boss["posY"],
            "vx": vx,
            "vy": vy,
            "frame": 0,
            "count": 0
        })

        boss["shootTimer"] = 0

def playerBulletHandler(screen, player, boss):
    bossRect = pygame.Rect(boss["posX"], boss["posY"], boss["width"], boss["height"])

    for bullet in player["bullets"][:]:
        bullet["y"] -= bullet["speed"]
        pygame.draw.rect(screen, (0,0,0), (bullet["x"], bullet["y"], 8, 15))
        bulletRect = pygame.Rect(bullet["x"], bullet["y"], 8, 15)

        if bossRect.colliderect(bulletRect):
            boss["hp"] -= 1
            player["bullets"].remove(bullet)

            continue
        if bullet["x"] < boxX or bullet["x"] + 8 > boxX + boxWidth or bullet["y"] < boxY or bullet["y"] + 15 > boxY + boxHeight:
            player["bullets"].remove(bullet)

            continue

def bossBulletHandler(screen, boss, player, servantParam):
    for bullet in boss["bullets"][:]:
        bullet["x"] += bullet["vx"]
        bullet["y"] += bullet["vy"]
        bullet["count"] += 1

        if bullet["count"] >= 5:
            bullet["count"] = 0
            bullet["frame"] = (bullet["frame"] + 1) % len(servantParam)

        pygame.draw.rect(screen, (255,0,255), (bullet["x"], bullet["y"], 10, 10))
        playerRect = pygame.Rect(player["posX"], player["posY"], player["width"], player["height"])
        bulletRect = pygame.Rect(bullet["x"], bullet["y"], 10, 10)

        if playerRect.colliderect(bulletRect):
            boss["bullets"].remove(bullet)
            player["hearts"] -= 1

            if player["hearts"] <= 0:
                player["lives"] -= 1
                player["hearts"] = 3

                if player["lives"] <= 0:
                    return False
                
        if bullet["y"] > HEIGHT:
            boss["bullets"].remove(bullet)

    return True

def draw(screen, player, boss):
    screen.fill((255,255,255))

    pygame.draw.rect(screen, (200,200,200), (boxX, boxY, boxWidth, boxHeight), 10)
    pygame.draw.rect(screen, (0,0,255), (player["posX"], player["posY"], player["width"], player["height"]))

    dx = circleCenterX - (boss["posX"] + boss["width"] / 2)
    dy = circleCenterY - (boss["posY"] + boss["height"] / 2)

    angle = -math.degrees(math.atan2(dy, dx)) + 90
    frame = boss["frames"][boss["frameIndex"]]
    rotated = pygame.transform.rotate(frame, angle)
    rect = rotated.get_rect(center=(boss["posX"] + boss["width"] / 2, boss["posY"] + boss["height"] / 2))
    screen.blit(rotated, rect.topleft)
    ratio = boss["hp"] / 30

    pygame.draw.rect(screen, (255,0,0), (boss["posX"], boss["posY"] - 20, boss["width"] * ratio, 10))
    pygame.draw.rect(screen, (0,0,0), (boss["posX"], boss["posY"] - 20, boss["width"], 10), 2)

    for i in range(player["hearts"]):
        screen.blit(heartImg, (10 + i * 30, 10))

    for i in range(player["lives"]):
        screen.blit(livesImg, (10 + i * 25, 40))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dx, dy = inputHandler(player)

    updatePlayer(player, dx, dy)
    updateBoss(boss, player)

    draw(screen, player, boss)

    playerBulletHandler(screen, player, boss)
    isPlayerAlive = bossBulletHandler(screen, boss, player, servant)

    if isPlayerAlive == False:
        print("GAME OVER")
        running = False

    pygame.display.flip()
    clock.tick(FRAMES)