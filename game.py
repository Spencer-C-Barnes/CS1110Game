# Spencer Barnes and William Brinkley (wjb6kcr)

import gamebox
import pygame

# Define Camera and Player
camera = gamebox.Camera(800, 600)
player = gamebox.from_color(50, 50, "blue", 15, 15)
projectiles = []


def player_movement(keys):
    if pygame.K_a in keys:
        player.xspeed = -5
    if pygame.K_d in keys:
        player.xspeed = 5
    if pygame.K_w in keys:
        player.yspeed = -5
    if pygame.K_s in keys:
        player.yspeed = 5
    player.move_speed()


def shooting(keys):
    if pygame.K_UP in keys or pygame.K_DOWN in keys or pygame.K_LEFT in keys or pygame.K_RIGHT in keys:
        projectile_form = gamebox.from_color(player.x, player.y, "green", 15, 15)
        if pygame.K_UP in keys:
            projectile_form.yspeed = -5
        if pygame.K_DOWN in keys:
            projectile_form.yspeed = 5
        if pygame.K_LEFT in keys:
            projectile_form.xspeed = -5
        if pygame.K_RIGHT in keys:
            projectile_form.xspeed = 5
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


def tick(keys):
    camera.clear("black")
    shooting(keys)
    friction()
    camera.draw(player)
    player_movement(keys)
    camera.display()


gamebox.timer_loop(30, tick)
