import pygame
import sys
import time
from constants import *

pygame.init()

background = pygame.image.load('./Assets/background.png')
car_image = pygame.image.load('./Assets/car_image.png')
car_rect = car_image.get_rect(center=START_POSITION)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("F1 Circuit Game")

car_speed = START_SPEED
car_angle = 90
start_time = None
lap_completed = False

def blit_rotate_center(surf, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    surf.blit(rotated_image, new_rect.topleft)
    return new_rect

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        car_rect.y -= car_speed
        car_angle = 0
    if keys[pygame.K_s]:
        car_rect.y += car_speed
        car_angle = 180
    if keys[pygame.K_a]:
        car_rect.x -= car_speed
        car_angle = 90
    if keys[pygame.K_d]:
        car_rect.x += car_speed
        car_angle = 270

    background_pixel_color = background.get_at(car_rect.center)
    if background_pixel_color == BLACK:
        car_speed = 3
    elif background_pixel_color == GREEN:
        car_speed = 2
    elif background_pixel_color == GREEN_END:
        lap_time = time.time() - start_time
        print(f'Lap completed in {lap_time:.2f} seconds')
        lap_completed = False  # Reset for next lap
        time.sleep(1)
        running = False
    elif background_pixel_color == PURPLE:
        car_rect.center = START_POSITION
        car_speed = START_SPEED
    else:
        car_speed = START_SPEED

    if not lap_completed and background_pixel_color == GREEN:
        lap_completed = True
        start_time = time.time()

    screen.blit(background, (0, 0))
    car_rect = blit_rotate_center(screen, car_image, car_rect.topleft, car_angle)

    pygame.display.flip()

pygame.quit()
sys.exit()
