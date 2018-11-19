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
score = 0
health = 3
level = 0


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


def swarmer_bullet_player_collision():
    global score
    global health
    for swarmer in swarmers:
        if swarmer.touches(player):
            health -= 1
            swarmers.remove(swarmer)
        for projectile in projectiles:
            if projectile.touches(swarmer):
                swarmers.remove(swarmer)
                projectiles.remove(projectile)
                score += 1


def player_ui():
    score_counter = gamebox.from_text(camera.x+300, camera.y-250, fontsize=36, text="Score: " + str(score),
                                      color="white", bold=True)
    health_counter = gamebox.from_text(camera.x-300, camera.y-250, fontsize=36, text="Health: " + str(health),
                                       color="white", bold=True)
    camera.draw(score_counter)
    camera.draw(health_counter)


def welcome_screen(keys):
    global level
    welcome_message = gamebox.from_text(camera.x, camera.y-250, fontsize=36, text="Welcome to \"Insert Game Name "
                                                                                  "Here\"", color="white")
    begin_message = gamebox.from_text(camera.x, camera.y-2, fontsize=36, text="Press Space to Begin", color="white")
    camera.draw(welcome_message)
    camera.draw(begin_message)
    if pygame.K_SPACE in keys:
        level += 1


def tick(keys):
    global level
    if level == 0:
        welcome_screen(keys)
    if level == 1:
        camera.clear("black")
        shooting(keys)
        friction()
        swarmer_start()
        swarmer_bullet_player_collision()
        player_ui()
        camera.draw(player)
        player_movement(keys)
    camera.display()


gamebox.timer_loop(30, tick)
