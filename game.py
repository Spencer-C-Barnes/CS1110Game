# Spencer Barnes and William Brinkley (wjb6kcr)

import gamebox
import pygame
import random

# Define Variables
camera = gamebox.Camera(800, 600)
player = gamebox.from_color(50, 50, "blue", 15, 15)
projectiles = []
swarmers = []
power_up_1s = []
power_up_2s = []
shooters = []
konami_code = []
refresh = 45
player_speed = 5
num_swarmers = 10
swarmer_speed = 2
score = 0
health = 3
level = 0
cool_down_count = 0
cool_down_count_2 = 0
cool_down_count_3 = 18
cool_down_count_4 = 0
num_shooters = 10
shooter_speed = 2


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
    global cool_down_count_2
    cool_down_count_2 += 1
    if cool_down_count_2 % 60 == 0 and num_swarmers > 0:
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


def shooter_start():
    #FINISH IMPLEMENTING AND BUG TESTING
    global num_shooters
    global shooter_speed
    global cool_down_count_3
    cool_down_count_3 += 1
    if cool_down_count_3 % 60 == 0 and num_shooters > 0:
        shooter_form = gamebox.from_color(random.randint(10, 790), random.randint(10, 550), "dark red", 15, 15)
        num_shooters -= 1
        swarmers.append(shooter_form)
    for shooter in shooters:
        camera.draw(shooter)
        if player.x < shooter.x:
            shooter.x -= shooter_speed
        elif player.x > shooter.x:
            shooter.x += shooter_speed
        if player.y < shooter.y:
            shooter.y -= shooter_speed
        elif player.y > shooter.y:
            shooter.y += shooter_speed
        if random.randint(1, 50) == 25:
            bullet_form = gamebox.from_color(shooter.x, shooter.y, "orange", 7, 7)
            camera.draw(bullet_form)


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
    global level
    global num_swarmers
    score_counter = gamebox.from_text(camera.x+300, camera.y-250, fontsize=36, text="Score: " + str(score),
                                      color="white", bold=True)
    health_counter = gamebox.from_text(camera.x-300, camera.y-250, fontsize=36, text="Health: " + str(health),
                                       color="white", bold=True)
    if num_swarmers == 0 and len(swarmers) == 0:
        level += 1
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


def player_endgame():
    global health
    global level
    if health == 0:
        level = 10


def endgame_screen():
    global level
    global score
    welcome_message = gamebox.from_text(camera.x, camera.y - 250, fontsize=36, text="Game Over!", color="white")
    begin_message = gamebox.from_text(camera.x, camera.y - 2, fontsize=36, text="Your score was: "+str(score), color="white")
    camera.draw(welcome_message)
    camera.draw(begin_message)


def level_2_start(keys):
    global level
    global num_swarmers
    global swarmer_speed
    global power_up_1s
    global power_up_2s
    level_message = gamebox.from_text(camera.x, camera.y - 250, fontsize=36, text="Level 2", color="white")
    begin_message = gamebox.from_text(camera.x, camera.y - 2, fontsize=36, text="Press Space to Begin", color="white")
    camera.draw(level_message)
    camera.draw(begin_message)
    power_up_1s = []
    power_up_2s = []
    if pygame.K_SPACE in keys:
        level += 1
        num_swarmers = 25
        swarmer_speed = 4


def level_3_start(keys):
    global level
    global num_swarmers
    global power_up_1s
    global power_up_2s
    level_message = gamebox.from_text(camera.x, camera.y - 250, fontsize=36, text="Level 3", color="white")
    begin_message = gamebox.from_text(camera.x, camera.y - 2, fontsize=36, text="Press Space to Begin", color="white")
    camera.draw(level_message)
    camera.draw(begin_message)
    power_up_1s = []
    power_up_2s = []
    if pygame.K_SPACE in keys:
        level += 1
        num_swarmers = 10


def power_up_1():
    global refresh
    if random.randint(1, 400) == 25:
        power_up_1_form = gamebox.from_color(random.randint(10, 790), random.randint(10, 550), "yellow", 15, 15)
        power_up_1s.append(power_up_1_form)
    for power_up_1 in power_up_1s:
        camera.draw(power_up_1)
        if player.touches(power_up_1):
            power_up_1s.remove(power_up_1)
            if refresh > 10:
                refresh -= 5


def power_up_2():
    global player_speed
    if random.randint(1, 400) == 25:
        power_up_2_form = gamebox.from_color(random.randint(10, 790), random.randint(10, 550), "purple", 15, 15)
        power_up_2s.append(power_up_2_form)
    for power_up_2 in power_up_2s:
        camera.draw(power_up_2)
        if player.touches(power_up_2):
            power_up_2s.remove(power_up_2)
            if player_speed < 15:
                player_speed += 1


def konami_code_func(keys):
    global konami_code
    global refresh
    global health
    global cool_down_count_4
    cool_down_count_4 += 1
    if pygame.K_UP in keys and "UP" not in konami_code and cool_down_count_4 > 5:
        konami_code.append("UP")
        cool_down_count_4 = 0
    if pygame.K_UP in keys and "UP2" not in konami_code and cool_down_count_4 > 5:
        konami_code.append("UP2")
        cool_down_count_4 = 0
    if pygame.K_DOWN in keys and "DOWN" not in konami_code and cool_down_count_4 > 5:
        konami_code.append("DOWN")
        cool_down_count_4 = 0
    if pygame.K_DOWN in keys and "DOWN2" not in konami_code and cool_down_count_4 > 5:
        konami_code.append("DOWN2")
        cool_down_count_4 = 0
    if pygame.K_LEFT in keys and "LEFT" not in konami_code and cool_down_count_4 > 5:
        konami_code.append("LEFT")
        cool_down_count_4 = 0
    if pygame.K_RIGHT in keys and "RIGHT" not in konami_code and cool_down_count_4 > 5:
        konami_code.append("RIGHT")
        cool_down_count_4 = 0
    if pygame.K_LEFT in keys and "LEFT2" not in konami_code and cool_down_count_4 > 5:
        konami_code.append("LEFT2")
        cool_down_count_4 = 0
    if pygame.K_RIGHT in keys and "RIGHT2" not in konami_code and cool_down_count_4 > 5:
        konami_code.append("RIGHT2")
        cool_down_count_4 = 0
    if pygame.K_b in keys and "B" not in konami_code and cool_down_count_4 > 5:
        konami_code.append("B")
        cool_down_count_4 = 0
    if pygame.K_a in keys and "A" not in konami_code and cool_down_count_4 > 5:
        konami_code.append("A")
        cool_down_count_4 = 0
    if pygame.K_RETURN in keys and "START" not in konami_code and cool_down_count_4 > 5:
        konami_code.append("START")
        cool_down_count_4 = 0
    if konami_code == ["UP", "UP2", "DOWN", "DOWN2", "LEFT", "RIGHT", "LEFT2", "RIGHT2", "B", "A", "START"]:
        refresh = 1
        health = 99


def winning_screen():
    global level
    level_message = gamebox.from_text(camera.x, camera.y - 250, fontsize=36, text="Congratulations! You won!",
                                      color="white")
    camera.draw(level_message)


def tick(keys):
    global level
    camera.clear("black")
    if level == 0:
        welcome_screen(keys)
        konami_code_func(keys)
    if level == 1:
        shooting(keys)
        friction()
        swarmer_start()
        swarmer_bullet_player_collision()
        player_ui()
        power_up_1()
        power_up_2()
        camera.draw(player)
        player_movement(keys)
        player_endgame()
    if level == 2:
        level_2_start(keys)
    if level == 3:
        shooting(keys)
        friction()
        swarmer_start()
        swarmer_bullet_player_collision()
        player_ui()
        power_up_1()
        power_up_2()
        camera.draw(player)
        player_movement(keys)
        player_endgame()
    if level == 4:
        level_3_start(keys)
    if level == 5:
        shooting(keys)
        friction()
        swarmer_start()
        shooter_start()
        swarmer_bullet_player_collision()
        player_ui()
        power_up_1()
        power_up_2()
        camera.draw(player)
        player_movement(keys)
        player_endgame()
    if level == 6:
        winning_screen()
    if level == 10:
        endgame_screen()
    camera.display()


gamebox.timer_loop(30, tick)
