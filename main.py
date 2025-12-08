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
    "lives": 3,
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
    "circleRadius": min(boxWidth, boxHeight) // 2 + 70,
    "shootCooldown": 30,
    "shootTimer": 0,
    "bullets": [],
    "phase": 1,
    "transforming": False,
    "spinAngle": 0,
    "spinSpeed": 20,
    "state": "circling",
    "chargeTimer": 0,
    "dashSpeed": 15,
    "dashTarget": (0, 0)
}

gameOver = False
gameWon = False

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("Sprite/background.webp").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
pygame.display.set_caption("Bullet Hell Game")
clock = pygame.time.Clock()

playerImg = pygame.image.load("Sprite/Cursor.png").convert_alpha()
playerImg = pygame.transform.scale(playerImg, (player["width"], player["height"]))

bulletImg = pygame.image.load("Sprite/Pink_Laser.webp").convert_alpha()
bulletImg = pygame.transform.scale(bulletImg, (8, 8))

eye = [
    pygame.image.load("Sprite/Eye_of_Cthulhu_(Phase_1)_(1).png").convert_alpha(),
    pygame.image.load("Sprite/Eye_of_Cthulhu_(Phase_1)_(2).png").convert_alpha(),
    pygame.image.load("Sprite/Eye_of_Cthulhu_(Phase_1)_(3).png").convert_alpha()
]

eye_phase2 = [
    pygame.image.load("Sprite/Eye_of_Cthulhu_(Phase_2)_(1).png").convert_alpha(),
    pygame.image.load("Sprite/Eye_of_Cthulhu_(Phase_2)_(2).png").convert_alpha(),
    pygame.image.load("Sprite/Eye_of_Cthulhu_(Phase_2)_(3).png").convert_alpha()
]

boss["frames"] = eye

boss["width"] = eye[0].get_width()
boss["height"] = eye[0].get_height()

servant = [
    pygame.image.load("Sprite/Servant_of_Cthulhu_1.png").convert_alpha(),
    pygame.image.load("Sprite/Servant_of_Cthulhu_2.png").convert_alpha()
]
servant = [pygame.transform.scale(img, (15, 15)) for img in servant]
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
        length = math.hypot(dx, dy)
        dx = (dx / length) * player["speed"]
        dy = (dy / length) * player["speed"]

    player["shootTimer"] += 1

    if keys[pygame.K_SPACE] and player["shootTimer"] >= player["shootCooldown"]:
        mouseX, mouseY = pygame.mouse.get_pos()

        playerX = player["posX"] + player["width"] // 2
        playerY = player["posY"] + player["height"] // 2

        directionX = mouseX - playerX
        directionY = mouseY - playerY
        distance = math.hypot(directionX, directionY)

        if distance != 0:
            vx = (directionX / distance) * 10
            vy = (directionY / distance) * 10
        else:
            vx = 0
            vy = -10

        player["bullets"].append({
            "x": playerX,
            "y": playerY,
            "vx": vx,
            "vy": vy
        })

        player["shootTimer"] = 0

    return dx, dy

def updatePlayer(player, dx, dy):
    player["posX"] = max(boxX, min(boxX + boxWidth - player["width"], player["posX"] + dx))
    player["posY"] = max(boxY, min(boxY + boxHeight - player["height"], player["posY"] + dy))

def updateBoss(boss, player):
    if boss["hp"] <= 15 and boss["phase"] == 1 and not boss["transforming"]:
        boss["transforming"] = True
        boss["spinAngle"] = 0
        boss["frameCounter"] = 0
        return
    
    if boss["transforming"]:
        boss["frameCounter"] += 1
        if boss["frameCounter"] >= boss["animSpeed"]:
            boss["frameCounter"] = 0
            boss["frameIndex"] = (boss["frameIndex"] + 1) % len(boss["frames"])

        boss["spinAngle"] += boss["spinSpeed"]

        if boss["spinAngle"] >= 720:
            boss["transforming"] = False
            boss["phase"] = 2
            boss["spinAngle"] = 0

            boss["frames"] = eye_phase2
            boss["width"] = eye_phase2[0].get_width()
            boss["height"] = eye_phase2[0].get_height()

            boss["shootCooldown"] = 15
            boss["circleSpeed"] = 0.04
        return

    boss["frameCounter"] += 1

    if boss["frameCounter"] >= boss["animSpeed"]:
        boss["frameCounter"] = 0
        boss["frameIndex"] = (boss["frameIndex"] + 1) % len(boss["frames"])
        
    if boss["phase"] == 2:
        if boss["state"] == "circling":
            boss["circleAngle"] += boss["circleSpeed"]
            boss["posX"] = circleCenterX + math.cos(boss["circleAngle"]) * boss["circleRadius"] - boss["width"] // 2
            boss["posY"] = circleCenterY + math.sin(boss["circleAngle"]) * boss["circleRadius"] - boss["height"] // 2

            if pygame.time.get_ticks() % 180 == 0:
                boss["state"] = "charging"
                boss["chargeTimer"] = 0

        elif boss["state"] == "charging":
            boss["chargeTimer"] += 1
            if boss["chargeTimer"] >= FRAMES * 1:
                oppositeAngle = (boss["circleAngle"] + math.pi) % (2 * math.pi)
                boss["dashTarget"] = (
                    circleCenterX + math.cos(oppositeAngle) * boss["circleRadius"] - boss["width"] // 2,
                    circleCenterY + math.sin(oppositeAngle) * boss["circleRadius"] - boss["height"] // 2
                    )
                boss["state"] = "dashing"

        elif boss["state"] == "dashing":
            dx = boss["dashTarget"][0] - boss["posX"]
            dy = boss["dashTarget"][1] - boss["posY"]
            dist = math.hypot(dx, dy)
            if dist != 0:
                boss["posX"] += (dx / dist) * boss["dashSpeed"]
                boss["posY"] += (dy / dist) * boss["dashSpeed"]
            
            if dist < boss["dashSpeed"]:
                boss["circleAngle"] = math.atan2(
                    boss["posY"] + boss["height"]/2 - circleCenterY,
                    boss["posX"] + boss["width"]/2 - circleCenterX
                    )
                boss["state"] = "circling"

        elif boss["state"] == "returning":
            dx = circleCenterX - boss["posX"]
            dy = circleCenterY - boss["posY"]
            dist = math.hypot(dx, dy)
            if dist != 0:
                boss["posX"] += (dx / dist) * boss["dashSpeed"]
                boss["posY"] += (dy / dist) * boss["dashSpeed"]

            if dist < boss["dashSpeed"]:
                boss["state"] = "circling"
    else:
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
            "angle": 0,
            "spinSpeed": 5,
            "frame": 0,
            "count": 0
        })


        boss["shootTimer"] = 0

def playerBulletHandler(screen, player, boss):
    bossRect = pygame.Rect(boss["posX"], boss["posY"], boss["width"], boss["height"])

    for bullet in player["bullets"][:]:
        bullet["x"] += bullet["vx"]
        bullet["y"] += bullet["vy"]

        angle = -math.degrees(math.atan2(bullet["vy"], bullet["vx"]))
        rotatedBullet = pygame.transform.rotate(bulletImg, angle)
        rect = rotatedBullet.get_rect(center=(bullet["x"], bullet["y"]))
        screen.blit(rotatedBullet, rect.topleft)
        bulletRect = pygame.Rect(bullet["x"], bullet["y"], 8, 8)

        if bossRect.colliderect(bulletRect):
            boss["hp"] -= 1
            player["bullets"].remove(bullet)

            continue

        if (bullet["x"] < boxX or bullet["x"] > boxX + boxWidth or bullet["y"] < boxY or bullet["y"] > boxY + boxHeight):
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

        bullet["angle"] = (bullet["angle"] + bullet["spinSpeed"]) % 360
        frame = servantParam[0]
        rotated = pygame.transform.rotate(frame, bullet["angle"])
        rect = rotated.get_rect(center = (bullet["x"], bullet["y"]))
        screen.blit(rotated, rect.topleft)
        playerRect = pygame.Rect(player["posX"], player["posY"], player["width"], player["height"])
        bulletRect = pygame.Rect(bullet["x"], bullet["y"], 10, 10)

        for playerBullet in player["bullets"][:]:
            pRect = pygame.Rect(playerBullet["x"], playerBullet["y"], 8, 8)
            if pRect.colliderect(rect):
                player["bullets"].remove(playerBullet)
                boss["bullets"].remove(bullet)
                break

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
    screen.blit(background, (0, 0))
    mouseX, mouseY = pygame.mouse.get_pos()

    pygame.draw.rect(screen, (200,200,200), (boxX, boxY, boxWidth, boxHeight), 10)

    playerX = player["posX"] + player["width"] // 2
    playerY = player["posY"] + player["height"] // 2

    dx = mouseX - playerX
    dy = mouseY - playerY

    angle = -math.degrees(math.atan2(dy, dx)) - 90
    playerSurface = pygame.Surface((player["width"], player["height"]), pygame.SRCALPHA)
    pygame.draw.rect(playerSurface, (0, 0, 255), (0, 0, player["width"], player["height"]))
    rotatedPlayer = pygame.transform.rotate(playerImg, angle)
    rect = rotatedPlayer.get_rect(center=(playerX, playerY))
    screen.blit(rotatedPlayer, rect.topleft)

    dx = circleCenterX - (boss["posX"] + boss["width"] / 2)
    dy = circleCenterY - (boss["posY"] + boss["height"] / 2)

    angle = -math.degrees(math.atan2(dy, dx)) + 90
    frame = boss["frames"][boss["frameIndex"]]
    if boss["transforming"]:
        rotated = pygame.transform.rotate(frame, boss["spinAngle"])
    else:
        dx = circleCenterX - (boss["posX"] + boss["width"] / 2)
        dy = circleCenterY - (boss["posY"] + boss["height"] / 2)
        angle = -math.degrees(math.atan2(dy, dx)) + 90
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

    if gameWon:
        font = pygame.font.SysFont("Arial", 60)
        text = font.render("GG YOU WIN", True, (255, 255, 0))
        textRect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, textRect)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not gameOver:
        dx, dy = inputHandler(player)

        updatePlayer(player, dx, dy)
        updateBoss(boss, player)

        if boss["hp"] <= 0:
            gameWon = True
            gameOver = True

        draw(screen, player, boss)       
        playerBulletHandler(screen, player, boss)
        isPlayerAlive = bossBulletHandler(screen, boss, player, servant)

    if isPlayerAlive == False:
        print("GAME OVER")
        running = False

    pygame.display.flip()
    clock.tick(FRAMES)
