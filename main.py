import pygame as pg
import random
import os
import pickle

import pygame.draw

pg.init()

clock = pg.time.Clock()
fps = 30

red = (255, 0, 0)
yellow = (255, 200, 0)
purple = (255, 0, 255)
screen_width = 800
screen_height = 800
body = [(375, 375)]
cooldown = 6
score = 0
if os.path.exists('./highscore.dat'):
    highscore = pickle.load(open("highscore.dat", "rb"))
else:
    highscore = 0
food = False
game_started = True


screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Snake")

bg = pg.image.load("castleCenter.png").convert_alpha()
bg = pg.transform.scale(bg, (screen_width, screen_height))

score_font = pg.font.Font("Turok.ttf", 30)
pause_font = pg.font.Font("Turok.ttf", 80)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_rotated_text(text, font, text_col, x, y, rotation):
    img = font.render(text, True, text_col)
    img = pg.transform.rotate(img, rotation)
    screen.blit(img, (x, y))


def snake(xy, body, food_position, food, run, score, highscore, game_started):
    x = body[-1][0] + 50 * xy[0]
    y = body[-1][1] + 50 * xy[1]
    if x > 800:
        x -= 800
    if x < 0:
        x += 800
    if y > 800:
        y -= 800
    if y < 0:
        y += 800
    if (x, y) in body:
        pg.display.update()
        if score == highscore:
            pickle.dump(highscore, open("highscore.dat", "wb"))
        run = restart(run)
        score = 0
        game_started = True

    body.append((x, y))
    if food_position != body[-1]:
        body.pop(0)
        return body, food, run, score, highscore, game_started
    score += 1
    food = False
    return body, food, run, score,highscore, game_started


def make_food(body):
    food_x = random.randint(1, 16)
    food_y = random.randint(1, 16)
    food_position = (food_x * 50 - 25, food_y * 50 - 25)
    if food_position in body:
        food_position, food = make_food(body)
    food = True
    return food_position, food


def restart(run):
    game_lost = True
    draw_text("YOU LOST!", pause_font, yellow, 230, 250)
    draw_text("press r to restart", pause_font, yellow, 80, 400)
    pg.display.update()
    while game_lost:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                game_lost = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    game_lost = False
    return run


def start(xy, run):
    game_lost = True
    draw_text("< arrow left", score_font, yellow, 150, 350)
    draw_text("arrow right >", score_font, yellow, 430, 350)
    draw_rotated_text("arrow up >", score_font, yellow, 350, 195, 90)
    draw_rotated_text("arrow down >", score_font, yellow, 360, 420, 270)
    pygame.draw.circle(screen, red, (375, 375), 25)
    pg.display.update()
    body = [(375, 375)]
    while game_lost:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                game_lost = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    xy = [-1, 0]
                    game_lost = False
                if event.key == pg.K_RIGHT:
                    xy = [1, 0]
                    game_lost = False
                if event.key == pg.K_UP:
                    xy = [0, -1]
                    game_lost = False
                if event.key == pg.K_DOWN:
                    xy = [0, 1]
                    game_lost = False
    return xy, run, body


run = True
xy = [1, 0]

while run:
    screen.blit(bg, (0, 0))
    clock.tick(fps)
    cooldown -= 1
    if score > highscore:
        highscore = score

    if game_started:
        xy, run, body = start(xy, run)
        game_started = False
    draw_text(f"score: {score}", score_font, yellow, 20, 20)
    draw_text(f"highscore: {highscore}", score_font, yellow, 20, 50)
    if not food:
        food_position, food = make_food(body)

    key = pg.key.get_pressed()
    if key[pg.K_DOWN] and xy != [0, -1]:
        xy = [0, 1]
    if key[pg.K_UP] and xy != [0, 1]:
        xy = [0, -1]
    if key[pg.K_RIGHT] and xy != [-1, 0]:
        xy = [1, 0]
    if key[pg.K_LEFT] and xy != [1, 0]:
        xy = [-1, 0]

    if cooldown == 0:
        n, food, run, score, highscore, game_started = snake(xy, body, food_position, food, run, score, highscore, game_started)
        cooldown = 6
        color_change = 1
        for i in n:
            if color_change == 1:
                pygame.draw.circle(screen, red, i, 25)
                color_change *= -1
            else:
                pygame.draw.circle(screen, yellow, i, 25)
                color_change *= -1
        pygame.draw.circle(screen, purple, food_position, 10)
        pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False


pg.quit()