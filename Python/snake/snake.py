#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import random
pygame.init()

XSIZE_WIN = 1000
YSIZE_WIN = 1000

fps = 60
clock = pygame.time.Clock()


win = pygame.display.set_mode((XSIZE_WIN,YSIZE_WIN))
pygame.display.set_caption('Path Finder')

GAME_RUN = True
MARGIN = 1

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

NROW = 50
NCOLUMS = 50

WIDTH = XSIZE_WIN // NCOLUMS
HEIGHT = YSIZE_WIN // NROW

grid = [[0]*NCOLUMS for n in range(NROW)]

#grid[24][10] = 2

snake = [[NROW//2,NCOLUMS//2],[NROW//2+1,NCOLUMS//2],[NROW//2+2,NCOLUMS//2]]
#for coord in snake:
	#print(coord)

searchpaths = [[snake[0]]]

foodpath = []

direction = 2

points = 0

def affichage():
	#print("affichage")
	gridcolumn = 0
	gridrow = 0

	for coord in snake:
		grid[coord[0]][coord[1]] = 1

	for row in grid:
		for col in row:
			color = WHITE
			if col == 0:
				color = (0,0,0)
			if col == 1:
				color = (0,255,0)
			if col == 2:
				color = (255,0,0)
			if col == 3:
				color = (0,0,255)
			if col == 4:
				color = (255,255,0)
			pygame.draw.rect(win, (color), (WIDTH * gridcolumn, HEIGHT * gridrow, WIDTH, HEIGHT))
			pygame.draw.rect(win,(BLACK), (WIDTH * gridcolumn, HEIGHT * gridrow, WIDTH, MARGIN))
			pygame.draw.rect(win, (BLACK), (WIDTH * gridcolumn, HEIGHT * gridrow, MARGIN, HEIGHT))
			gridcolumn = gridcolumn + 1
		gridrow = gridrow + 1
		gridcolumn = 0
	gridrow = 0
	#UPDATE SURFACE
	pygame.display.update()

def createFood():
	while 1:
		x = random.randint(0,NROW-1)
		y = random.randint(0,NCOLUMS-1)
		

		if (grid[x][y] == 0):
			break

	grid[x][y] = 2
	#print("MIAM"*100)
	global points
	points += 1
	print(points)
	#print("FOOD IS ON :")
	#print([x,y])
	#global searchpaths
	#print(searchpaths)
	#searchpaths = [[snake[0]]]
	#print(searchpaths)
	#print(foodpath)
	#foodpath = []
	#print(foodpath)
	affichage()

def search2():
	#print("-+/\\+-"*100)
	#print("searching...")
	#print("snake")
	#print(snake)
	#print("searchpaths")
	#print(searchpaths)

	global searchpaths
	#print(searchpaths)
	searchpaths = [[snake[0]]]
	
	for path in searchpaths:
		#n=50
		#print("*"*n)
		#print("*"*n)
		#print("*"*n)
		#pygame.time.delay(1000)
		#print("avant :")
		#print(path)
		#print(path[-1][0])
		#print(searchpaths)
		row = path[-1][0]
		col = path[-1][1]
		#print("row=", row, ", col=", col)

		#recherche si l'objectif est à coté
		if row > 0:
			if grid[row-1][col] == 2:
				path.append([row-1, col])
				#print("return")
				#print(path)
				clearSearch()
				return path
		if row < NROW-1:
			if grid[row+1][col] == 2:
				path.append([row+1, col])
				#print("return")
				#print(path)
				clearSearch()
				return path
		if col > 0:
			if grid[row][col-1] == 2:
				path.append([row, col-1])
				#print("return")
				#print(path)
				clearSearch()
				return path
		if col < NCOLUMS-1:
			if grid[row][col+1] == 2:
				path.append([row, col+1])
				#print("return")
				#print(path)
				clearSearch()
				return path

		#Fait avancer de 1
		if row > 0:
			if grid[row-1][col] == 0:
				grid[row-1][col] = 3
				path_ = path[:]
				path_.append([row-1, col])
				searchpaths.append(path_)
		if row < NROW-1:
			if grid[row+1][col] == 0:
				grid[row+1][col] = 3
				path_ = path[:]
				path_.append([row+1, col])
				searchpaths.append(path_)
		if col > 0:
			if grid[row][col-1] == 0:
				grid[row][col-1] = 3
				path_ = path[:]
				path_.append([row, col-1])
				searchpaths.append(path_)
		if col < NCOLUMS-1:
			if grid[row][col+1] == 0:
				grid[row][col+1] = 3
				path_ = path[:]
				path_.append([row, col+1])
				searchpaths.append(path_)

		#supprime l'ancien chemin
		#print("apres :")
		#print(path)
		del path

		#print(searchpaths)
	#print("return nothing")
	#affichage()
	longestPath = []
	for path in searchpaths:
		if len(path) > len(longestPath):
			longestPath = path
			#print(longestPath)
	clearSearch()
	#print(longestPath[:2])
	return longestPath[:2]


def clearSearch():
	for row in range(len(grid)):
		for col in range(len(grid[row])):
			if grid[row][col]  == 3 or grid[row][col] == 4:
				grid[row][col] = 0

def gotofood():

	#print("gotofood")
	#print(foodpath)
	#print("snake")
	#print(snake)
	#print("difrow")
	difrow = snake[0][0] - foodpath[0][0]
	#print(snake[0][0])
	#print(foodpath[0][0])
	#print(difrow)

	difcol = snake[0][1] - foodpath[0][1]
	#print(snake[0][1])
	#print(foodpath[0][1])
	#print(difcol)

	global direction

	if difrow < 0 and direction != 2:
		direction = 4
	elif difrow > 0 and direction != 4:
		direction = 2
	elif difcol < 0 and direction != 1:
		direction = 3
	elif difcol > 0 and direction != 3:
		direction = 1

	#print("direction=")
	#print(direction)

	#print(foodpath[0])
	del foodpath[0]
	#print("end gotofood")

def avancer():
	#print("avancer")
	if direction == 1: #aller à gauche
		if snake[0][1] > 0:
			if grid[snake[0][0]][snake[0][1]-1] == 2:
				snake.insert(0, [snake[0][0], snake[0][1]-1])
				createFood()
			elif grid[snake[0][0]][snake[0][1]-1] == 0:
				snake.insert(0, [snake[0][0], snake[0][1]-1])
				grid[snake[-1][0]][snake[-1][1]] = 0
				del snake[-1]
			else:
				return 0
		else:
			return 0

	if direction == 2: #aller en haut
		if snake[1][0] > 0:
			if grid[snake[0][0]-1][snake[0][1]] == 2:
				snake.insert(0, [snake[0][0]-1, snake[0][1]])
				createFood()
			elif grid[snake[0][0]-1][snake[0][1]] == 0:
				snake.insert(0, [snake[0][0]-1, snake[0][1]])
				grid[snake[-1][0]][snake[-1][1]] = 0
				del snake[-1]
			else:
				return 0
		else:
			return 0

	if direction == 3: #aller à droite
		if snake[0][1] < NCOLUMS-1:
			if grid[snake[0][0]][snake[0][1]+1] == 2:
				snake.insert(0, [snake[0][0], snake[0][1]+1])
				createFood()
			elif grid[snake[0][0]][snake[0][1]+1] == 0:
				snake.insert(0, [snake[0][0], snake[0][1]+1])
				grid[snake[-1][0]][snake[-1][1]] = 0
				del snake[-1]
			else:
				return 0
		else:
			return 0

	if direction == 4: #aller en bas
		if snake[1][0] < NROW-1:
			if grid[snake[0][0]+1][snake[0][1]] == 2:
				snake.insert(0, [snake[0][0]+1, snake[0][1]])
				createFood()
			elif grid[snake[0][0]+1][snake[0][1]] == 0:
				snake.insert(0, [snake[0][0]+1, snake[0][1]])
				grid[snake[-1][0]][snake[-1][1]] = 0
				del snake[-1]
			else:
				return 0
		else:
			return 0


createFood()
affichage()


#search2()


#pygame.time.delay(10000)
#for i in range(100):
while GAME_RUN:
	"""
	while search2() == None:
		print("while...")
		print(searchpaths)
		print("end while.")
		continue
	"""
	#print(len(searchpaths))
	#print(searchpaths)
	if len(foodpath) == 0:#T
		foodpath = search2()[1:]#T
		"""
		if foodpath != None:
			for pt in foodpath:
				if grid[pt[0]][pt[1]] != 2:
					grid[pt[0]][pt[1]] = 4
			affichage()
			pygame.time.delay(100)
			clearSearch()
		"""
		if foodpath == []:#T
			GAME_RUN = 0#T
			break#T
	
	gotofood()#T

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME_RUN = False

		elif event.type == pygame.KEYDOWN:
			#print("event")
			if event.key == pygame.K_LEFT and (direction != 3):
				#print("left")
				direction = 1
			elif event.key == pygame.K_UP and (direction != 4):
				#print("up")
				direction = 2
			elif event.key == pygame.K_RIGHT and (direction != 1):
				#print("right")
				direction = 3
			elif event.key == pygame.K_DOWN and (direction != 2):
				#print("down")
				direction = 4

	#if (pygame.time.get_ticks() - time) > NCOLUMS*4:
	
	if avancer() == 0:
		GAME_RUN = 0

	
		# direction = random.randint(1,4)
		# affichage()
		#print("tour")
		# clock.tick(len(snake))
		# clock.tick(1)
		# pygame.time.delay(200)
affichage()
print("dead")

GAME_RUN = True
while GAME_RUN:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME_RUN = False
