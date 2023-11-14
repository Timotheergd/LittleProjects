#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import random
pygame.init()

XSIZE_WIN = 1000
YSIZE_WIN = 1000

win = pygame.display.set_mode((XSIZE_WIN,YSIZE_WIN))
pygame.display.set_caption('Path Finder')
#board = pygame.image.load('/home/timothee/Bureau/goomba.png')
#pygame.draw.rect(win, (243, 235, 215), (0, 0, 900, 900))
pygame.display.update()
#board = pygame.transform.scale(board, (900,900))
GAME_RUN = True
MARGIN = 1
pawn_x = -60
pawn_y = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
NROW = 100
NCOLUMS = 100
#grid = [ [1]*XROW for n in range(XCOLUMS)]
#grid = [[0]*NCOLUMS for n in range(NROW)]
#grid[NCOLUMS//2][NROW//2] = -1
WIDTH = XSIZE_WIN // NCOLUMS
HEIGHT = YSIZE_WIN // NROW
print("WIDTH = ", WIDTH)
print("HEIGHT = ", HEIGHT)

gridcolumn = 0
gridrow = 0
find = 0
coord = None

searchgrid = [[0]*NCOLUMS for n in range(NROW)]
searchgrid[20][20] = 1

for n in range(30):
	searchgrid[5][n+10] = 4
	searchgrid[n+5][10] = 4
	searchgrid[35][n+10] = 4
	searchgrid[n+5][40] = 4

#searchgrid[31][40] = 0
searchgrid[6][10] = 0

#searchgrid[NROW-10][NCOLUMS-10] = 5
searchgrid[21][NCOLUMS-21] = 5

searchpaths = []
#searchpaths = [[[0,1], [1,1]], [[2,5],[3,5]]]
for row in range(len(searchgrid)):
		for col in range(len(searchgrid[row])):
			if searchgrid[row][col]  == 1:
				searchpaths.append([[row, col]])





print(len(searchgrid))

def affichage():
	print("affichage")
	gridcolumn = 0
	gridrow = 0

	for row in searchgrid:
		for col in row:
			color = WHITE
			if col == 1:
				color = (255,0,0)
			if col == 2:
				color = (255,255,0)
			if col == 3:
				color = (0,255,0)
			if col == 4:
				color = (0,0,0)
			if col == 5:
				color = (255,0,255)
			pygame.draw.rect(win, (color), (WIDTH * gridcolumn, HEIGHT * gridrow, WIDTH, HEIGHT))
			pygame.draw.rect(win,(BLACK), (WIDTH * gridcolumn, HEIGHT * gridrow, WIDTH, MARGIN))
			pygame.draw.rect(win, (BLACK), (WIDTH * gridcolumn, HEIGHT * gridrow, MARGIN, HEIGHT))
			gridcolumn = gridcolumn + 1
		gridrow = gridrow + 1
		gridcolumn = 0
	gridrow = 0
	#UPDATE SURFACE
	pygame.display.update()


def search():
	"""
	nbDone = 0

	for row in range(len(searchgrid)):
		for col in range(len(searchgrid[row])):
			if searchgrid[row][col] == 0:
				nbDone +=1
				print(nbDone)
	if nbDone == 0:
		pygame.time.delay(5000)
		GAME_RUN = False
	"""

	for row in range(len(searchgrid)):
		for col in range(len(searchgrid[row])):
			if searchgrid[row][col]  == 2:
				searchgrid[row][col] = 3

	for row in range(len(searchgrid)):
		for col in range(len(searchgrid[row])):
			if searchgrid[row][col]  == 1:
				searchgrid[row][col] = 2


	for row in range(len(searchgrid)):
		for col in range(len(searchgrid[row])):
			if searchgrid[row][col] == 2:



				if searchgrid[row][col-1] == 5:
					return (row, col-1)
				if searchgrid[row][col-1] == 0 and col > 0:					
					searchgrid[row][col-1] = 1

				if row < NROW-1:
					if searchgrid[row+1][col] == 5:
						return (row+1, col)
					if searchgrid[row+1][col] == 0:
						searchgrid[row+1][col] = 1

				if col < NCOLUMS-1:
					if searchgrid[row][col+1] == 5:
						return (row, col+1)
					if searchgrid[row][col+1] == 0:
						searchgrid[row][col+1] = 1

				if searchgrid[row-1][col] == 5:
					return (row-1, col)
				if searchgrid[row-1][col] == 0 and row > 0:
					searchgrid[row-1][col] = 1


def search2():
	#print("-+/\\+-"*100)
	for path in searchpaths:
		n=50
		#print("*"*n)
		#print("*"*n)
		#print("*"*n)
		#pygame.time.delay(1000)
		#print("avant :")
		#print(path[-1][0])
		#print(searchpaths)
		row = path[-1][0]
		col = path[-1][1]
		#print("row=", row, ", col=", col)

		#recherche si l'objectif est à coté
		if row > 0:
			if searchgrid[row-1][col] == 5:
				path.append([row, col])
				print("return")
				return path
		if row < NROW-1:
			if searchgrid[row+1][col] == 5:
				path.append([row, col])
				print("return")
				return path
		if col > 0:
			if searchgrid[row][col-1] == 5:
				path.append([row, col])
				print("return")
				return path
		if col < NCOLUMS-1:
			if searchgrid[row][col+1] == 5:
				path.append([row, col])
				print("return")
				return path

		#Fait avancer de 1
		if row > 0:
			if searchgrid[row-1][col] == 0:
				searchgrid[row-1][col] = 3
				path_ = path[:]
				path_.append([row-1, col])
				searchpaths.append(path_)
		if row < NROW-1:
			if searchgrid[row+1][col] == 0:
				searchgrid[row+1][col] = 3
				path_ = path[:]
				path_.append([row+1, col])
				searchpaths.append(path_)
		if col > 0:
			if searchgrid[row][col-1] == 0:
				searchgrid[row][col-1] = 3
				path_ = path[:]
				path_.append([row, col-1])
				searchpaths.append(path_)
		if col < NCOLUMS-1:
			if searchgrid[row][col+1] == 0:
				searchgrid[row][col+1] = 3
				path_ = path[:]
				path_.append([row, col+1])
				searchpaths.append(path_)

		#supprime l'ancien chemin
		#print("apres :")
		#print(path)
		del path

	# LIGNES A INDENTER OU DESINDENTER POUR AFFICHAGE PROGRESSIF OU
	#print(searchpaths)
	print("return nothing")
	affichage()
	return

	
affichage()
while GAME_RUN == True:
	#affichage()
	#pygame.time.delay(100)
	#affichage()
  	#GAME LOGIC
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME_RUN = False

		elif find == 2 and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
			print("init")
			gridcolumn = 0
			gridrow = 0
			find = 0
			coord = None

			searchgrid = [[0]*NCOLUMS for n in range(NROW)]
			
			
			for n in range(30):
				searchgrid[5][n+10] = 4
				searchgrid[n+5][10] = 4
				searchgrid[35][n+10] = 4
				searchgrid[n+5][40] = 4

			for n in range(NCOLUMS*15):
				searchgrid[random.randint(0,NROW-1)][random.randint(0,NCOLUMS-1)] = 4

			#print(searchgrid)
			#searchgrid[31][40] = 0
			
			for i in range(35):
				for j in range(4):
					searchgrid[j][i] = 0
			"""
			for i in range(9):
				for j in range(35):
					searchgrid[j][i] = 0
			"""

			searchgrid[6][8] = 0
			searchgrid[6][9] = 0
			searchgrid[6][10] = 0
			searchgrid[6][11] = 0
			searchgrid[6][12] = 0
			searchgrid[20][20] = 1

			searchgrid[NROW-10][NCOLUMS-10] = 5

			searchpaths = []
			#searchpaths = [[[0,1], [1,1]], [[2,5],[3,5]]]
			for row in range(len(searchgrid)):
					for col in range(len(searchgrid[row])):
						if searchgrid[row][col]  == 1:
							searchpaths.append([[row, col]])

			affichage()

			find = 0
			#print(searchgrid)

	
		elif event.type == pygame.MOUSEBUTTONDOWN:
			# User clicks the mouse. Get the position
			pos = pygame.mouse.get_pos()
			# Change the x/y screen coordinates to grid coordinates
			column = int(pos[0] // (WIDTH))
			row = int(pos[1] // (HEIGHT))
			# Set that location to one
			#pygame.draw.rect(win,(0,0,0), (WIDTH * column, HEIGHT * row, 1000, 1000))
			print("row=", row, ", col=", col)
			searchgrid[row][column] = 4
			#print(grid)
			print("Click ", pos, "Grid coordinates: ", row, column)
			affichage()
	
		
		


		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				find = not find
				"""for i in range(len(searchgrid)):
					for j in range(len(searchgrid[0])):
						searchgrid[i][j] = random.randint(0,2)"""

	
	if find == 1:

		coord = search2()


		affichage()


		if not coord == None:
			print("WIIIIIIIIIIIIIINNNNNNNNNNNNNNN")
			print(coord)

			for pt in coord:
				searchgrid[pt[0]][pt[1]] = 2


			affichage()
			#while not (event.type == pygame.MOUSEBUTTONDOWN ):#or event.type == pygame.KEYDOWN):
			find = 2
		else:
			find = 2

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_F5:
				find = 2
				
