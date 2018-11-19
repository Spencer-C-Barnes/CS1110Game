# Spencer Barnes and William Brinkley (wjb6kcr)

import gamebox
import pygame

# Define Camera and Player
camera = gamebox.Camera(800, 600)
player = gamebox.from_color(50, 50, "blue", 15, 15)


def player_movement(keys):
    if pygame.K_a in keys:
        player.xspeed = 5


def tick(keys):
    camera.display()


gamebox.timer_loop(30, tick)
