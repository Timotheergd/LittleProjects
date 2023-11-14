#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import pygame.freetype

import random
pygame.init()

XSIZE_WIN = 1000
YSIZE_WIN = 1000

fps = 600
clock = pygame.time.Clock()

MARGIN = 1

win = pygame.display.set_mode((XSIZE_WIN,YSIZE_WIN))
pygame.display.set_caption('Solitaire')

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

NROW = 7
NCOLUMS = 7

WIDTH = XSIZE_WIN // NCOLUMS
HEIGHT = YSIZE_WIN // NROW

points=32

save_game = []

bot_running = False
botmaxpoints = 2

grid = [[1]*NCOLUMS for n in range(NROW)]
for i in range(0,2):
    for j in range(0,2):
        for ii in range(0,2):
            for jj in range(0,2):
                grid[i*5+ii][j*5+jj] = -1
                grid[i*5+ii][j*5+jj] = -1
grid[3][3] = 0

def affichage_game():
    global bot_running
    
    print(grid)

    global selected
    gridcolumn = 0
    gridrow = 0

    for row in grid:
        for col in row:
            color = WHITE
            if col == -1:
                color = (0,0,0)
            elif col == 0:
                color = (100,100,100)
            elif col == 1:
                color = (0,255,0)
            elif col == 2:
                color = (255,0,0)
            elif col == 3:
                color = (100,255,0)
            
            pygame.draw.rect(win, (color), (WIDTH * gridrow, HEIGHT * gridcolumn, WIDTH, HEIGHT))
            pygame.draw.rect(win,(BLACK), (WIDTH * gridrow, HEIGHT * gridcolumn, WIDTH, MARGIN))
            pygame.draw.rect(win, (BLACK), (WIDTH * gridrow, HEIGHT * gridcolumn, MARGIN, HEIGHT))
            gridcolumn = gridcolumn + 1
        gridrow = gridrow + 1
        gridcolumn = 0
    gridrow = 0

    font = pygame.font.Font("Little Comet Bubling Demo Version.otf", XSIZE_WIN*6//100)
    text = font.render("Points : "+str(points), False, (255,255,0))
    win.blit(text, (XSIZE_WIN*3//4,10))

    if checkend() and not selected:
        print("checkend", checkend())
        print("slcted=", selected)
        gmov_font = pygame.font.Font("Little Comet Bubling Demo Version.otf", XSIZE_WIN*6//25)
        gmov_text = gmov_font.render("GAME OVER", False, (255,255,0))
        gmov_text_r = gmov_text.get_rect()
        win.blit(gmov_text, ((XSIZE_WIN-gmov_text_r.size[0])//2,(YSIZE_WIN-gmov_text_r.size[1])//2))
        
        c_font = pygame.font.Font("Little Comet Bubling Demo Version.otf", XSIZE_WIN//25)
        c_text = c_font.render("PRESS ANY KEY TO CONTINUE", False, (255,255,0))
        c_text_r = c_text.get_rect()
        win.blit(c_text, ((XSIZE_WIN-c_text_r.size[0])//2,(YSIZE_WIN-c_text_r.size[1]+250)//2))

        print(grid)
        print("points", points)
        pygame.display.update()

        print(f"{save_game=}")

        print(bot_running, points)

        end=True
        while end:
            #print("while true checkend")
            if (bot_running == True) and (points > botmaxpoints):
                end=False
                MENU_RUN = True
                print("HERE WE GO AGAIN"*20)
                bot_game()
            else:
                bot_running=False

            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN) or (event.type == pygame.MOUSEBUTTONDOWN):
                    print("BREAK"*20)
                    
                    end=False
                elif event.type == pygame.QUIT:
                    MENU_RUN = False
                    end=False
        menu()
    
    #UPDATE SURFACE
    pygame.display.update()

def checkend():
    gridi=0
    gridj=0
    n=points
    play=[]
    for gridi in range(len(grid)):
        for gridj in range(len(grid[gridi])):
            if grid[gridi][gridj] == 2:
                return False
            if grid[gridi][gridj] == 1:
                if gridi>1 and grid[gridi-1][gridj] == 1 and grid[gridi-2][gridj] == 0: # can play left
                    play.append((gridi-2,gridj))
                if gridi<5 and grid[gridi+1][gridj] == 1 and grid[gridi+2][gridj] == 0: # can play right
                    play.append((gridi+2,gridj))
                if gridj>1 and grid[gridi][gridj-1] == 1 and grid[gridi][gridj-2] == 0: # can play up
                    play.append((gridi,gridj-2))
                if gridj<5 and grid[gridi][gridj+1] == 1 and grid[gridi][gridj+2] == 0: # can play down
                    play.append((gridi,gridj+2))

    if not len(play):
        return True
    else:
        return False

def game():
    GAME_RUN = True

    running = False
    global selected
    selected=False
    selectedpos = (0,0)

    global points
    point = 32
    global grid
    grid = [[1]*NCOLUMS for n in range(NROW)]
    for i in range(0,2):
        for j in range(0,2):
            for ii in range(0,2):
                for jj in range(0,2):
                    grid[i*5+ii][j*5+jj] = -1
                    grid[i*5+ii][j*5+jj] = -1
    grid[3][3] = 0

    while GAME_RUN:

        affichage_game()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAME_RUN = False
                win.fill(pygame.Color("black"))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    

                    pospix = pygame.mouse.get_pos()
                    pos = (pospix[0]//WIDTH, pospix[1]//HEIGHT)

                    if not selected:
                        selectedpos = pos
                        play=[] # list of playable cases
                        if grid[pos[0]][pos[1]] == 1: #if therre is a ball
                            if pos[0]>1 and grid[pos[0]-1][pos[1]] == 1 and grid[pos[0]-2][pos[1]] == 0: # can play left
                                play.append((pos[0]-2,pos[1]))
                            if pos[0]<5 and grid[pos[0]+1][pos[1]] == 1 and grid[pos[0]+2][pos[1]] == 0: # can play right
                                play.append((pos[0]+2,pos[1]))
                            if pos[1]>1 and grid[pos[0]][pos[1]-1] == 1 and grid[pos[0]][pos[1]-2] == 0: # can play up
                                play.append((pos[0],pos[1]-2))
                            if pos[1]<5 and grid[pos[0]][pos[1]+1] == 1 and grid[pos[0]][pos[1]+2] == 0: # can play down
                                play.append((pos[0],pos[1]+2))
                            grid[pos[0]][pos[1]] = 2
                            for p in play:
                                grid[p[0]][p[1]] = 3
                            selected = True
                    else:
                        selected= False
                        for p in play:
                                grid[p[0]][p[1]] = 0
                        grid[selectedpos[0]][selectedpos[1]] = 1
                        if pos in play:
                            grid[selectedpos[0]][selectedpos[1]] = 0 # move the selected ball
                            grid[pos[0]][pos[1]] = 1 # to the next place
                            grid[(selectedpos[0]+pos[0])//2][(selectedpos[1]+pos[1])//2] = 0 # remove the ball in between
                            save_game.append((selectedpos, pos))
                            points-=1
                            
def bot_game():
    
    global bot_running
    bot_running = True

    while bot_running:
        GAME_RUN = True
        running = False
        global selected
        selected=False
        selectedpos = (0,0)

        save_game=[]

        coups=0

        global points
        points = 32
        global grid
        grid = [[1]*NCOLUMS for n in range(NROW)]
        for i in range(0,2):
            for j in range(0,2):
                for ii in range(0,2):
                    for jj in range(0,2):
                        grid[i*5+ii][j*5+jj] = -1
                        grid[i*5+ii][j*5+jj] = -1
        grid[3][3] = 0

        while GAME_RUN:
            coups+=1
            #affichage_game()
            if checkend() and not selected:
                if points <= 3:
                    print(points)
                if  points > botmaxpoints: # Si perdu
                    GAME_RUN = False
                else:                      # GAGNE !!!!
                    bot_running = False
                    print(save_game)
                    affichage_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GAME_RUN = False
                    win.fill(pygame.Color("black"))

            if not selected:
                while True:
                    pos = (random.randint(0,6), random.randint(0,6)) 
                    if grid[pos[0]][pos[1]] == 1:
                        break
                selectedpos = pos
                play=[] # list of playable cases
                if grid[pos[0]][pos[1]] == 1: #if therre is a ball
                    if pos[0]>1 and grid[pos[0]-1][pos[1]] == 1 and grid[pos[0]-2][pos[1]] == 0: # can play left
                        play.append((pos[0]-2,pos[1]))
                    if pos[0]<5 and grid[pos[0]+1][pos[1]] == 1 and grid[pos[0]+2][pos[1]] == 0: # can play right
                        play.append((pos[0]+2,pos[1]))
                    if pos[1]>1 and grid[pos[0]][pos[1]-1] == 1 and grid[pos[0]][pos[1]-2] == 0: # can play up
                        play.append((pos[0],pos[1]-2))
                    if pos[1]<5 and grid[pos[0]][pos[1]+1] == 1 and grid[pos[0]][pos[1]+2] == 0: # can play down
                        play.append((pos[0],pos[1]+2))
                    grid[pos[0]][pos[1]] = 2
                    for p in play:
                        grid[p[0]][p[1]] = 3
                    selected = True
            else:
                if len(play):
                    n=random.randint(0,len(play)-1)
                    pos=play[n]
                else:
                    pos=(0,0)
                selected= False
                for p in play:
                        grid[p[0]][p[1]] = 0
                grid[selectedpos[0]][selectedpos[1]] = 1
                if pos in play:
                    grid[selectedpos[0]][selectedpos[1]] = 0 # move the selected ball
                    grid[pos[0]][pos[1]] = 1 # to the nex place
                    grid[(selectedpos[0]+pos[0])//2][(selectedpos[1]+pos[1])//2] = 0 # remove the ball in between
                    points-=1
                    save_game.append((selectedpos, pos))
            #clock.tick(200)
    

def affichage_menu():
    
    global play_text_r
    global bot_text_r
    global quit_text_r

    title_font = pygame.font.Font("Little Comet Bubling Demo Version.otf", XSIZE_WIN*6//30)
    play_font = pygame.font.Font("Little Comet Bubling Demo Version.otf", XSIZE_WIN*6//50)
    bot_font = pygame.font.Font("Little Comet Bubling Demo Version.otf", XSIZE_WIN*6//50)
    quit_font = pygame.font.Font("Little Comet Bubling Demo Version.otf", XSIZE_WIN*6//50)

    title_text = title_font.render("Solitaire", False, (255,255,255))
    title_text_r = title_text.get_rect()
    win.blit(title_text, ((XSIZE_WIN-title_text_r.size[0])//2,50))

    play_text = play_font.render("Play", True, (255,255,255))
    pygame.display.update()
    play_text_r = play_text.get_rect()
    play_text_r.move_ip((XSIZE_WIN-play_text_r.size[0])//2,300)
    win.blit(play_text, ((XSIZE_WIN-play_text_r.size[0])//2,300))

    bot_text = bot_font.render("Bot", True, (255,255,255))
    pygame.display.update()
    bot_text_r = bot_text.get_rect()
    bot_text_r.move_ip((XSIZE_WIN-bot_text_r.size[0])//2,450)
    win.blit(bot_text, ((XSIZE_WIN-bot_text_r.size[0])//2,450))

    quit_text = quit_font.render("Quit", False, (255,255,255))
    quit_text_r = quit_text.get_rect()
    quit_text_r.move_ip((XSIZE_WIN-quit_text_r.size[0])//2,600)
    win.blit(quit_text, ((XSIZE_WIN-quit_text_r.size[0])//2,600))
    
    #UPDATE SURFACE
    pygame.display.update()

def menu():
    global play_text_r
    global bot_text_r
    global quit_text_r
    win.fill(pygame.Color("black"))
    MENU_RUN = True
    while MENU_RUN:
        affichage_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MENU_RUN = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # 1 == left button
                    if play_text_r.collidepoint(pygame.mouse.get_pos()):
                        game()
                    if bot_text_r.collidepoint(pygame.mouse.get_pos()):
                        bot_game()
                    if quit_text_r.collidepoint(pygame.mouse.get_pos()):
                        MENU_RUN = False
        #clock.tick(30)
menu()
