import pygame
from colors import *

from interface import Field, UserInterface

WIDTH = 640
HEIGHT = 480
FPS = 30

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BASE_BACKGROUND_COLOR)

pygame.display.set_caption('Tic-tac-toe!')
clock = pygame.time.Clock()

field = Field(WIDTH, HEIGHT)
user_buttons = UserInterface(field)

system_online = True

while system_online:
    clock.tick(FPS)

    for event in pygame.event.get():
        position = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            system_online = False
        elif event.type == pygame.MOUSEBUTTONUP:
            field.process_click(position)
            user_buttons.process_button_up(position)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            user_buttons.process_button_down(position)

    field.update()
    field.draw(screen)

    user_buttons.update()
    user_buttons.draw(screen)

    pygame.display.flip()

pygame.quit()
