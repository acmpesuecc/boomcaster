import pygame
import math
import random
from collections import deque

wall_texture_path = 'wall.png'
floor_texture_path = 'floor.png'
sky_texture_path = 'sky.png'

# world = [
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
#     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
#     [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
#     [1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
#     [1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# ]

def generate_world(width, height, doomguy_pos):
   
    world = [[1 for _ in range(width)] for _ in range(height)]

    for x in range(width):
        world[0][x] = 1 
        world[height - 1][x] = 1
    for y in range(height):
        world[y][0] = 1  
        world[y][width - 1] = 1 
        
    doomguy_x, doomguy_y = int(doomguy_pos[0]), int(doomguy_pos[1])
    world[doomguy_y][doomguy_x] = 0 

    def fill(x, y):
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and world[ny][nx] == 1:
                world[y + dy // 2][x + dx // 2] = 0
                world[ny][nx] = 0 
                fill(nx, ny)
    
    fill(doomguy_x, doomguy_y)
    return world

def place_destination(world):
    width = len(world[0])
    height = len(world)
    
    while True:
        dest_x = random.randint(1, width - 2)
        dest_y = random.randint(1, height - 2)
        if world[dest_y][dest_x] == 0: 
            return (dest_x, dest_y)
        
def reached_destination(doomguy_pos, destination):
    return math.isclose(doomguy_pos[0], destination[0], abs_tol=1) and math.isclose(doomguy_pos[1], destination[1], abs_tol=1)


doomguy_pos = 1.5, 3
doomguy_vector = 0
doomguy_speed = 2
doomguy_sens = 2
fov = math.pi / 3
scale = 1600 // 600

world = generate_world(6,5,doomguy_pos)
destination = place_destination(world)

walls = {}
for l, row in enumerate(world):
    for n, value in enumerate(row):
        if value:
            walls[(n, l)] = value

print(world, destination)


def lighting(screen, doomguy_pos, doomguy_vector):
    ox, oy = doomguy_pos
    x_map, y_map = int(ox), int(oy)

    main_vector = doomguy_vector - (math.pi / 3) / 2 + 0.1
    for ray in range(800):
        sin_a = math.sin(main_vector)
        cos_a = math.cos(main_vector)

        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(20):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor in walls:
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(20):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert in walls:
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        if depth_vert < depth_hor:
            depth = depth_vert
        else:
            depth = depth_hor

        depth *= math.cos(doomguy_vector - main_vector)

        proj_height = 800 / math.tan((math.pi / 3) / 2) / (depth + 0.0001)

        color = [255 / (1 + depth ** 5 * 0.00002)] * 3
        pygame.draw.rect(screen, color, (ray * scale, 540 - proj_height // 2, scale, proj_height))

        main_vector += (math.pi / 3) / 800


doomguy_x, doomguy_y = doomguy_pos
doomguy_vector = doomguy_vector


def check_wall_collision(x, y):
    return (int(x), int(y)) not in walls


pygame.init()
screen = pygame.display.set_mode((1600, 1080))
clock = pygame.time.Clock()
dt = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            pygame.quit()

    sin_a = math.sin(doomguy_vector)
    cos_a = math.cos(doomguy_vector)
    dx, dy = 0, 0
    speed = doomguy_speed * dt
    speed_sin = speed * sin_a
    speed_cos = speed * cos_a

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        dx += speed_cos
        dy += speed_sin
    if keys[pygame.K_s]:
        dx += -speed_cos
        dy += -speed_sin
    if keys[pygame.K_a]:
        dx += speed_sin
        dy += -speed_cos
    if keys[pygame.K_d]:
        dx += -speed_sin
        dy += speed_cos

    if check_wall_collision(doomguy_x + dx, doomguy_y):
        doomguy_x += dx
    if check_wall_collision(doomguy_x, doomguy_y + dy):
        doomguy_y += dy
        
    doomguy_pos = doomguy_x, doomguy_y
    
    if reached_destination(doomguy_pos, destination):
        
        world = generate_world(16, 11, doomguy_pos)
        destination = place_destination(world)
        print(world, destination)
        walls = {}
        for l, row in enumerate(world):
            for n, value in enumerate(row):
                if value:
                    walls[(n, l)] = value

    if keys[pygame.K_LEFT]:
        doomguy_vector -= doomguy_sens * dt
    if keys[pygame.K_RIGHT]:
        doomguy_vector += doomguy_sens * dt
    doomguy_vector %= math.tau

    screen.fill((0, 0, 0))

    floor_texture = pygame.image.load(floor_texture_path).convert()
    floor_texture = pygame.transform.scale(floor_texture, (scale, scale))
    for y in range(540, 1080, scale):
        for x in range(0, 1600, scale):
            screen.blit(floor_texture, (x, y))

    sky_texture = pygame.image.load(sky_texture_path).convert()
    sky_texture = pygame.transform.scale(sky_texture, (1600, 540))
    screen.blit(sky_texture, (0, 0))

    wall_texture = pygame.image.load(wall_texture_path).convert()
    wall_texture = pygame.transform.scale(wall_texture, (scale, scale))
    for (x, y) in walls:
        screen.blit(wall_texture, (x * scale, y * scale))
    lighting(screen, (doomguy_x, doomguy_y), doomguy_vector)

    pygame.display.flip()
    dt = clock.tick(60) / 1000.0
