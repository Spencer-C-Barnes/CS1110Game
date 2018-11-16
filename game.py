# Spencer Barnes

import gamebox
import pygame

# Define Camera and Player
camera = gamebox.Camera(800, 600)
player = player = gamebox.from_color(50, 50, "blue", 15, 15)

def player_movement(keys):
    if

def tick(keys):
    camera.display()

gamebox.timer_loop(30, tick)
