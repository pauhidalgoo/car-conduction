import pygame
import neat
import time
import os
import random
import math
from constants import *
from car_class import Car
# Initialize Pygame
pygame.init()

# Load images
background = pygame.image.load('./Assets/background.png')

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("F1 Circuit Game")


def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(eval_genomes, 50)
    print('\nBest genome:\n{!s}'.format(winner))

def draw_checkpoints(screen, checkpoints):
    for (cx, cy) in checkpoints:
        pygame.draw.circle(screen, (255, 0, 0), (cx, cy), 10)

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Check if left mouse button clicked
                        print("Clicked at:", event.pos)
        if current_time - start_time > MAX_TIME:  # Check if 30 seconds have passed
            run = False

        for i, car in enumerate(cars):
            car.move()
            if not car.check_collision(background):
                ge[i].fitness -= 200
                cars.pop(i)
                nets.pop(i)
                ge.pop(i)
                continue

            output = nets[i].activate((car.rect.centerx, car.rect.centery, car.angle, car.speed))
            if output[0] > 0.5:
                if output[1] > 0.5:
                    car.rotate('none')
                car.rotate('left')
            elif output[1] > 0.5:
                car.rotate('right')
            if output[2] > 0.5:
                car.rotate('none')

            ge[i].fitness += 3
            ge[i].fitness -= car.check_collision(background)

            if car.check_checkpoint():
                ge[i].fitness += 100

        screen.blit(background, (0, 0))
        draw_checkpoints(screen, CHECKPOINTS)
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
