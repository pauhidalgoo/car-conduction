import math
from constants import *
import pygame
car_image = pygame.image.load('./Assets/car_image.png')


class Car:
    def __init__(self, x, y):
        self.image = car_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = START_SPEED
        self.angle = 90
        self.center = [x, y]
        self.distance_traveled = 0
        self.last_checkpoint = -1

    def move(self):
        rad = math.radians(self.angle)
        self.center[0] += self.speed * math.cos(rad)
        self.center[1] -= self.speed * math.sin(rad)
        self.rect = self.image.get_rect(center=self.center)
        self.distance_traveled += self.speed

    def rotate(self, direction):
        if direction == 'left':
            self.angle += 5
        elif direction == 'right':
            self.angle -= 5
        elif direction == 'none':
            self.angle = self.angle

    def check_collision(self, background):
        if (self.center[0] < 0 or self.center[0] >= WIDTH or 
            self.center[1] < 0 or self.center[1] >= HEIGHT):
            return False
        pixel_color = background.get_at(self.rect.center)
        if pixel_color == BLACK:
            self.speed = 3
            return 3
        elif pixel_color == GREEN:
            self.speed = 2
            return 6
        elif pixel_color == PURPLE:
            return False
        else:
            self.speed = START_SPEED
        return True
    
    def check_checkpoint(self):
        for i, (cx, cy) in enumerate(CHECKPOINTS):
            if self.last_checkpoint < i and math.hypot(self.center[0] - cx, self.center[1] - cy) < CHECKPOINT_RADIUS:
                self.last_checkpoint = i
                return True
        return False

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)