import pygame
import neat
import time
import os
import random
import math
from constants import *

# Initialize Pygame
pygame.init()


# Load images
background = pygame.image.load('./Assets/background.png')
car_image = pygame.image.load('./Assets/car_image.png')

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("F1 Circuit Game")

# Car class to handle the car properties and actions
class Car:
    def __init__(self, x, y):
        self.image = car_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = START_SPEED
        self.angle = 0
        self.center = [x, y]
        self.distance_traveled = 0

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

    def check_collision(self, background):
        if (self.center[0] < 0 or self.center[0] >= WIDTH or 
            self.center[1] < 0 or self.center[1] >= HEIGHT):
            return False
        pixel_color = background.get_at(self.rect.center)
        if pixel_color == BLACK:
            self.speed = 3
        elif pixel_color == GREEN:
            self.speed = 2
        elif pixel_color == PURPLE:
            return False
        else:
            self.speed = START_SPEED
        return True

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)

# Function to run the NEAT algorithm
def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(eval_genomes, 50)
    print('\nBest genome:\n{!s}'.format(winner))

# Function to evaluate the genomes
def eval_genomes(genomes, config):
    nets = []
    cars = []
    ge = []

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        cars.append(Car(START_POSITION[0], START_POSITION[1]))
        genome.fitness = 0
        ge.append(genome)

    clock = pygame.time.Clock()
    run = True
    start_time = time.time()

    while run and len(cars) > 0:
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        if current_time - start_time > 30:  # Check if 30 seconds have passed
            run = False

        for i, car in enumerate(cars):
            car.move()
            if not car.check_collision(background):
                ge[i].fitness -= 10
                cars.pop(i)
                nets.pop(i)
                ge.pop(i)
                continue

            output = nets[i].activate((car.rect.centerx, car.rect.centery, car.angle, car.speed))
            if output[0] > 0.5:
                car.rotate('left')
            elif output[1] > 0.5:
                car.rotate('right')

            ge[i].fitness = car.distance_traveled

        screen.blit(background, (0, 0))
        for car in cars:
            car.draw(screen)
        pygame.display.flip()
        clock.tick(30)

# NEAT configuration
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    run_neat(config)
