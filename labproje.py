import pygame
import random
import math

# Başlat
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sapanla Balon Vurma")
clock = pygame.time.Clock()

# Renkler
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GREY = (100, 100, 100)

# Sapan konumu ve açı
sling_pos = (width // 2, height - 50)
angle = 90  # Yukarı
power = 12  # Taşın gücü

# Taşlar ve balonlar
stones = []
balloons = []
score = 0
font = pygame.font.SysFont("Arial", 28)

def create_balloon():
    x = random.randint(50, width - 50)
    y = height + 50
    speed = random.randint(2, 4)
    return {"x": x, "y": y, "r": 25, "speed": speed}

def fire_stone():
    rad = math.radians(angle)
    vx = power * math.cos(rad)
    vy = -power * math.sin(rad)
    stones.append({"x": sling_pos[0], "y": sling_pos[1], "vx": vx, "vy": vy})

running = True
spawn_timer = 0

while running:
    screen.fill(WHITE)

    # Etkinlikler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Tuşlar
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and angle < 160:
        angle += 1
    if keys[pygame.K_RIGHT] and angle > 20:
        angle -= 1
    if keys[pygame.K_SPACE]:
        if len(stones) < 10:  # Aynı anda çok taş olmasın
            fire_stone()

    # Taşları güncelle
    for stone in stones:
        stone["x"] += stone["vx"]
        stone["y"] += stone["vy"]
        stone["vy"] += 0.3  # Yerçekimi
        pygame.draw.circle(screen, GREY, (int(stone["x"]), int(stone["y"])), 6)

    stones = [s for s in stones if 0 < s["x"] < width and 0 < s["y"] < height]

    # Balonları üret ve çiz
    spawn_timer += 1
    if spawn_timer > 50:
        balloons.append(create_balloon())
        spawn_timer = 0

    for balloon in balloons:
        balloon["y"] -= balloon["speed"]
        pygame.draw.circle(screen, RED, (balloon["x"], balloon["y"]), balloon["r"])

    balloons = [b for b in balloons if b["y"] > -50]

    # Çarpışma kontrolü
    for stone in stones:
        for balloon in balloons:
            dist = ((stone["x"] - balloon["x"])**2 + (stone["y"] - balloon["y"])**2)**0.5
            if dist < balloon["r"]:
                if stone in stones: stones.remove(stone)
                if balloon in balloons: balloons.remove(balloon)
                score += 1
                break

    # Sapanı çiz
    sling_length = 40
    rad = math.radians(angle)
    end_x = sling_pos[0] + sling_length * math.cos(rad)
    end_y = sling_pos[1] - sling_length * math.sin(rad)

    pygame.draw.line(screen, BROWN, sling_pos, (end_x, end_y), 6)
    pygame.draw.circle(screen, BROWN, sling_pos, 10)

    # Skor
    text = font.render(f"Skor: {score}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
