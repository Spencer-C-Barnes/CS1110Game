# Spencer Barnes (scb9ca) and William Brinkley (wjb6kcr)
# *** Character images and backgrounds are in progress. They are being drawn by William Brinkley ***

import gamebox
import pygame
import random

# Define Variables
camera = gamebox.Camera(800, 600)
player = gamebox.from_image(camera.x, camera.y, "CavmanFR1.png")
boss = gamebox.from_image(camera.x-400, camera.y-150, "Dill.png")
background = gamebox.from_image(camera.x, camera.y, "level_1.jpg")
projectiles = []
swarmers = []
power_up_1s = []
power_up_2s = []
shooters = []
konami_code = []
bullets = []
lasers = []
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
cool_down_count_5 = 0
num_shooters = 0
shooter_speed = 2
num_boss = 0
boss_speed = 5
boss_health = 0
scores_dict = {}


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
        projectile_form = gamebox.from_image(player.x, player.y, "Sabre.png")
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


def boss_start():
    global num_boss
    global boss_speed
    global player
    global boss
    global cool_down_count_5
    global boss_health
    global level
    global health
    global score
    cool_down_count_5 += 1
    if boss.touches(player):
        health -= 1
    if num_boss > 0:
        num_boss -= 1
        boss.xspeed = boss_speed
    if cool_down_count_5 > 160:
        boss.xspeed *= -1
        cool_down_count_5 = 0
    for projectile in projectiles:
        if projectile.touches(boss):
            boss_health -= 1
            projectiles.remove(projectile)
    if boss_health == 0:
        score += 30
    if random.randint(0, 25) == 5:
        laser_form = gamebox.from_text(boss.x, boss.y, fontsize=64, color="orange", text="BLAH")
        laser_form.rotate(-90)
        laser_form.yspeed = 7
        lasers.append(laser_form)
    for laser in lasers:
        if player.touches(laser):
            health -= 1
            lasers.remove(laser)
        camera.draw(laser)
        laser.move_speed()
    boss.move_speed()
    camera.draw(boss)


def swarmer_start():
    global num_swarmers
    global swarmer_speed
    global cool_down_count_2
    cool_down_count_2 += 1
    if cool_down_count_2 % 60 == 0 and num_swarmers > 0:
        swarmer_form = gamebox.from_image(random.randint(10, 790), random.randint(10, 550), "HokieFront2.png")
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
    global num_shooters
    global shooter_speed
    global cool_down_count_3
    global health
    global player
    cool_down_count_3 += 1
    if cool_down_count_3 % 60 == 0 and num_shooters > 0:
        shooter_form = gamebox.from_image(random.randint(10, 790), random.randint(10, 550), "HokieFront2.png")
        num_shooters -= 1
        shooters.append(shooter_form)
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
        if random.randint(1, 100) == 25:
            bullet_form = gamebox.from_image(shooter.x, shooter.y, "Feather.png")
            if player.x < shooter.x:
                bullet_form.xspeed -= shooter_speed*1.5
            elif player.x > shooter.x:
                bullet_form.xspeed += shooter_speed*1.5
            if player.y < shooter.y:
                bullet_form.yspeed -= shooter_speed*1.5
            elif player.y > shooter.y:
                bullet_form.yspeed += shooter_speed*1.5
            bullets.append(bullet_form)
    for bullet in bullets:
        bullet.move_speed()
        if bullet.touches(player):
            health -= 1
            bullets.remove(bullet)
        if bullet.x == camera.x + 400 or bullet.x == camera.x - 400 or bullet.y == camera.y + 300 or \
                bullet.y == camera.y - 300:
            bullets.remove(bullet)
        camera.draw(bullet)


def swarmer_bullet_player_collision():
    global score
    global health
    for swarmer in swarmers:
        if swarmer.touches(player):
            health -= 1
            swarmers.remove(swarmer)
        for projectile in projectiles:
            if projectile.touches(swarmer) and (swarmer in swarmers):
                swarmers.remove(swarmer)
                projectiles.remove(projectile)
                score += 1
    for shooter in shooters:
        if shooter.touches(player):
            health -= 1
            shooters.remove(shooter)
        for projectile in projectiles:
            if projectile.touches(shooter) and (shooter in shooters):
                shooters.remove(shooter)
                projectiles.remove(projectile)


def player_ui():
    global level
    global num_swarmers
    global num_shooters
    score_counter = gamebox.from_text(camera.x+300, camera.y-250, fontsize=36, text="Score: " + str(score),
                                      color="white", bold=True)
    health_counter = gamebox.from_text(camera.x-300, camera.y-250, fontsize=36, text="Health: " + str(health),
                                       color="white", bold=True)
    if num_swarmers == 0 and len(swarmers) == 0 and num_shooters == 0 and len(shooters) == 0 and num_boss == 0 \
            and boss_health == 0:
        level += 1
    camera.draw(score_counter)
    camera.draw(health_counter)


def welcome_screen(keys):
    global level
    welcome_message = gamebox.from_text(camera.x, camera.y-250, fontsize=36, text="Welcome to Cavalier Showdown",
                                        color="white")
    welcome_message_2 = gamebox.from_text(camera.x, camera.y - 200, fontsize=36,
                                          text="Created By: Spencer Barnes (scb9ca) & William Brinkley (wjb6kcr)",
                                          color="white")
    begin_message = gamebox.from_text(camera.x, camera.y+250, fontsize=36, text="Press Space to Begin", color="white")
    how_to_play = gamebox.from_image(camera.x, camera.y, 'how_to_play.jpg')
    camera.draw(welcome_message)
    camera.draw(welcome_message_2)
    camera.draw(begin_message)
    camera.draw(how_to_play)
    if pygame.K_SPACE in keys:
        level += 1


def player_endgame():
    global health
    global level
    if health == 0:
        level = -2


def endgame_screen():
    global level
    global score
    welcome_message = gamebox.from_text(camera.x, camera.y - 250, fontsize=36, text="Game Over!", color="white")
    begin_message = gamebox.from_text(camera.x, camera.y - 200, fontsize=36, text="Your score was: "+str(score), color="white")
    camera.draw(welcome_message)
    camera.draw(begin_message)


def level_2_start(keys):
    global level
    global num_swarmers
    global swarmer_speed
    global power_up_1s
    global power_up_2s
    global bullets
    global projectiles
    global background
    background = gamebox.from_image(camera.x, camera.y, "level_2.jpg")
    level_message = gamebox.from_text(camera.x, camera.y - 250, fontsize=36, text="Level 2", color="white")
    begin_message = gamebox.from_text(camera.x, camera.y - 2, fontsize=36, text="Press Space to Begin", color="white")
    camera.draw(level_message)
    camera.draw(begin_message)
    power_up_1s = []
    power_up_2s = []
    bullets = []
    projectiles = []
    if pygame.K_SPACE in keys:
        level += 1
        num_swarmers = 25
        swarmer_speed = 4


def level_3_start(keys):
    global level
    global num_swarmers
    global power_up_1s
    global power_up_2s
    global num_shooters
    global bullets
    global projectiles
    global background
    background = gamebox.from_image(camera.x, camera.y, "level_3.jpeg")
    level_message = gamebox.from_text(camera.x, camera.y - 250, fontsize=36, text="Level 3", color="white")
    begin_message = gamebox.from_text(camera.x, camera.y - 2, fontsize=36, text="Press Space to Begin", color="white")
    camera.draw(level_message)
    camera.draw(begin_message)
    power_up_1s = []
    power_up_2s = []
    bullets = []
    projectiles = []
    if pygame.K_SPACE in keys:
        level += 1
        num_swarmers = 10
        num_shooters = 10


def level_boss_start(keys):
    global level
    global power_up_1s
    global power_up_2s
    global bullets
    global projectiles
    global num_boss
    global background
    global boss_health
    background = gamebox.from_image(camera.x, camera.y, "level_4.jpg")
    level_message = gamebox.from_text(camera.x, camera.y - 250, fontsize=36, text="Level 4", color="white")
    begin_message = gamebox.from_text(camera.x, camera.y - 2, fontsize=36, text="Press Space to Begin", color="white")
    camera.draw(level_message)
    camera.draw(begin_message)
    power_up_1s = []
    power_up_2s = []
    bullets = []
    projectiles = []
    if pygame.K_SPACE in keys:
        level += 1
        num_boss = 1
        boss_health = 30


def power_up_1():
    global refresh
    if random.randint(1, 400) == 25:
        power_up_1_form = gamebox.from_color(random.randint(10, 790), random.randint(10, 550), "yellow", 15, 15)
        power_up_1s.append(power_up_1_form)
    for power_up_1 in power_up_1s:
        camera.draw(power_up_1)
        if player.touches(power_up_1):
            power_up_1s.remove(power_up_1)
            if refresh > 5:
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


def write_high_scores():
    global scores_dict
    global score
    global level
    sorting_list = []
    new_list = []
    file = open("scores.csv", "r")
    initials = input("Please enter your initials (3 Letters): ")
    scores_dict[score] = initials
    for line in file:
        name_score = line.strip().split(",")
        scores_dict[int(name_score[1])] = name_score[0]
    for value in scores_dict.keys():
        sorting_list.append(value)
        sorting_list.sort()
        sorting_list.reverse()
    for index in range(5):
        new_list.append(scores_dict[sorting_list[index]] + "," + str(sorting_list[index]) + "\n")
    file_2 = open("scores.csv", "w")
    file_2.writelines(new_list)
    level += 1


def read_high_scores():
    file = open("scores.csv")
    line_processed = []
    for line in file:
        line_processed.append(line.strip().split(","))
    for spacing in range(5):
        name_disp = gamebox.from_text(camera.x - 100, camera.y-100+50*spacing, line_processed[spacing][0], 36, "white")
        score_disp = gamebox.from_text(camera.x + 100, camera.y-100+50*spacing, line_processed[spacing][1], 36, "white")
        camera.draw(score_disp)
        camera.draw(name_disp)


def background_start():
    global background
    camera.draw(background)


def tick(keys):
    global level
    camera.clear("black")
    if level == -2:
        camera.draw(gamebox.from_text(camera.x, camera.y, "Please Input Initials into Console", 48, "black"))
        write_high_scores()
    if level == -1:
        endgame_screen()
        read_high_scores()
    if level == 0:
        welcome_screen(keys)
        konami_code_func(keys)
    if level == 1:
        background_start()
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
        background_start()
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
        background_start()
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
        level_boss_start(keys)
    if level == 7:
        background_start()
        shooting(keys)
        friction()
        boss_start()
        player_ui()
        power_up_1()
        power_up_2()
        camera.draw(player)
        player_movement(keys)
        player_endgame()
    if level == 8:
        write_high_scores()
    if level == 9:
        winning_screen()
        read_high_scores()
    camera.display()


gamebox.timer_loop(30, tick)
