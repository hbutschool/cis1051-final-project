import pygame

# https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/creating-pygame-window/

WIDTH = 800
HEIGHT = 800
running = True

screen = pygame.display.set_mode(((WIDTH, HEIGHT)))
screen.fill((255, 255, 255))  # background (plain color, note: how to set as image?)

pygame.display.set_caption("hello world")
pygame.display.flip()

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
