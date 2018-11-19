# Spencer Barnes and William Brinkley (wjb6kcr)

import gamebox
import pygame
import random

# Define Variables
camera = gamebox.Camera(800, 600)
player = gamebox.from_color(50, 50, "blue", 15, 15)
projectiles = []
swarmers = []
cool_down_count = 0
refresh = 45
player_speed = 5
num_swarmers = 10
swarmer_speed = 2


def player_movement(keys):
    global player_speed
    if pygame.K_a in keys:
        player.xspeed = -player_speed
    if pygame.K_d in keys:
        player.xspeed = player_speed
    if pygame.K_w in keys:
        player.yspeed = -player_speed
    if pygame.K_s in keys:
        player.yspeed = player_speed
    player.move_speed()


def shooting(keys):
    global cool_down_count
    global refresh
    cool_down_count += 1
    if (pygame.K_UP in keys or pygame.K_DOWN in keys or pygame.K_LEFT in keys or pygame.K_RIGHT in keys) and \
            cool_down_count > refresh:
        projectile_form = gamebox.from_color(player.x, player.y, "green", 15, 15)
        cool_down_count = 0
        if pygame.K_UP in keys:
            projectile_form.yspeed = -10
        if pygame.K_DOWN in keys:
            projectile_form.yspeed = 10
        if pygame.K_LEFT in keys:
            projectile_form.xspeed = -10
        if pygame.K_RIGHT in keys:
            projectile_form.xspeed = 10
        projectiles.append(projectile_form)
    for projectile in projectiles:
        camera.draw(projectile)
        projectile.move_speed()
        if projectile.x == camera.x+400 or projectile.x == camera.x-400 or projectile.y == camera.y+300 or projectile.y\
                == camera.y-300:
            projectiles.remove(projectile)


def friction():
    if player.xspeed > 0:
        player.xspeed -= 1
    if player.xspeed < 0:
        player.xspeed += 1
    if player.yspeed > 0:
        player.yspeed -= 1
    if player.yspeed < 0:
        player.yspeed += 1


def swarmer_start():
    global num_swarmers
    global swarmer_speed
    if cool_down_count % 60 == 0 and num_swarmers > 0:
        swarmer_form = gamebox.from_color(random.randint(10, 790), random.randint(10, 550), "red", 15, 15)
        num_swarmers -= 1
        swarmers.append(swarmer_form)
    for swarmer in swarmers:  # Swarmer code by Craig Dill
        camera.draw(swarmer)
        if player.x < swarmer.x:
            swarmer.x -= swarmer_speed
        elif player.x > swarmer.x:
            swarmer.x += swarmer_speed
        if player.y < swarmer.y:
            swarmer.y -= swarmer_speed
        elif player.y > swarmer.y:
            swarmer.y += swarmer_speed


def tick(keys):
    camera.clear("black")
    shooting(keys)
    friction()
    swarmer_start()
    camera.draw(player)
    player_movement(keys)
    camera.display()


gamebox.timer_loop(30, tick)
