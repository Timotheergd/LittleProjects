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

NROW = 4
NCOLUMS = 4

WIDTH = XSIZE_WIN // NCOLUMS
HEIGHT = YSIZE_WIN // NROW

def check_full():
	for i in range(NCOLUMS):
		for j in range(NROW):
			if grid[i][j] == 0:
				return False
	return True

def check_end(g):
	for i in range(NCOLUMS):
		for j in range(NROW):
			try:
				if g[i][j] == g[i+1][j]:
					print("return false check endi+1" + " " + str(i) + " " + str(j))
					print(str(g[i][j]) + " " + str(g[i+1][j]))
					return False
			except:
				print("ecxept")
				pass
			try:
				if g[i][j] == g[i-1][j] and not i == 0:
					print("return false check endi-1" + " " + str(i) + " " + str(j))
					print(str(g[i][j]) + " " + str(g[i-1][j]))
					return False
			except:
				print("ecxept")
				pass
			try:
				if g[i][j] == g[i][j+1]:
					print("return false check endj+1" + " " + str(i) + " " + str(j))
					print(str(g[i][j]) + " " + str(g[i][j+1]))
					return False
			except:
				print("ecxept")
				pass
			try:
				if g[i][j] == g[i][j-1] and not j == 0:
					print("return false check endj-1" + " " + str(i) + " " + str(j))
					print(str(g[i][j]) + " " + str(g[i][j-1]))
					return False
			except:
				print("ecxept")
				pass
	print("return true check end")
	return True


def add_num():
	print('add')
	placed = False

	if check_full():
		print("full")
		placed = True

	
	while placed == False:
		x = random.randint(0,NROW-1)
		y = random.randint(0,NCOLUMS-1)

		if (grid[x][y] == 0):
			if random.randint(0, 10) < 1:
				grid[x][y] = 4
			else:
				grid[x][y] = 2
			placed = True
			
# global grid
grid = [[0]*NCOLUMS for n in range(NROW)]
oldgrid = [[0]*NCOLUMS for n in range(NROW)]

# grid[0][3] = 0
# grid[1][3] = 8
# grid[2][3] = 4
# grid[3][3] = 4

# grid[0][0] = 2
# grid[0][1] = 8
# grid[0][2] = 4

# initialisation by placing 2 random cases
add_num()
add_num()

def eq_grid(g1, g2):
	try:
		for i in range(len(g1)):
			for j in range(len(g1[0])):
				if not g1[i][j] == g2[i][j]:
					print("eq return false")
					return False
	except:
		print("EQ RETURN FALSE BUT IN EXCEPT")
		return False
	print("eq return true")
	return True

def affichage(grid):
	print("affichage")
	gridcolumn = 0
	gridrow = 0

	for i in range(NCOLUMS):
		for j in range(NROW):
			col = grid[j][i]
			# print(type(col))
			# print(col, gridcolumn, gridrow)
			# color = WHITE
			if col == 0:
				color = (0, 0, 0)
			elif col == 2:
				color = (0, 255, 0)
			elif col == 4:
				color = (0,255,204)
			elif col == 8:
				color = (0,153,255)
			elif col == 16:
				color = (255,51,204)
			elif col == 32:
				color = (255,80,80)
			elif col == 64:
				color = (255,204,0)
			elif col == 128:
				color = (153,255,51)
			elif col == 256:
				color = (0, 102, 0)
			elif col == 512:
				color = (0, 51, 102)
			elif col == 1024:
				color = (102, 0, 102)
			elif col == 2048:
				color = (128, 0, 0)
			elif col == 2048:
				color = (102, 51, 0)
			else:
				color = (200, 0, 200)
			
			pygame.draw.rect(win, (color), (WIDTH * gridcolumn, HEIGHT * gridrow, WIDTH, HEIGHT))
			pygame.draw.rect(win,(BLACK), (WIDTH * gridcolumn, HEIGHT * gridrow, WIDTH, MARGIN))
			pygame.draw.rect(win, (BLACK), (WIDTH * gridcolumn, HEIGHT * gridrow, MARGIN, HEIGHT))

			font = pygame.font.Font("Little Comet Bubling Demo Version.otf", XSIZE_WIN*15//100)
			text = font.render(str(col), False, (255,255,0))
			text_rec = text.get_rect(center=((XSIZE_WIN//8) + XSIZE_WIN*gridcolumn//4,(YSIZE_WIN//8) + YSIZE_WIN*gridrow//4))
			win.blit(text, text_rec)
		
			gridcolumn = gridcolumn + 1
		gridrow = gridrow + 1
		gridcolumn = 0
	gridrow = 0
	#UPDATE SURFACE
	pygame.display.update()

def aff_cons(g):
	print('\n')
	for i in range(NCOLUMS):
		for j in range(NROW):
			print(g[j][i], end='')
		print('')

def go_screen():
	print("END")
	GAME_RUN = False
	
	gmov_font = pygame.font.Font("Little Comet Bubling Demo Version.otf", XSIZE_WIN*6//25)
	gmov_text = gmov_font.render("GAME OVER", False, (255,255,255))
	gmov_text_r = gmov_text.get_rect()
	win.blit(gmov_text, ((XSIZE_WIN-gmov_text_r.size[0])//2,(YSIZE_WIN-gmov_text_r.size[1])//2))
	
	c_font = pygame.font.Font("Little Comet Bubling Demo Version.otf", XSIZE_WIN//25)
	c_text = c_font.render("PRESS ANY KEY TO CONTINUE", False, (255,255,255))
	c_text_r = c_text.get_rect()
	win.blit(c_text, ((XSIZE_WIN-c_text_r.size[0])//2,(YSIZE_WIN-c_text_r.size[1]+250)//2))

	pygame.display.update()

"""
grid :

  0,0   0,1   0,2 .. NCOLUMS
  1,0   1,1   1,2
  2,0   2,1   2,2
  :
  NROW
"""

def right2():
	

	for i in range(NROW):
		for j in range(NCOLUMS):
			oldgrid[i][j] = grid[i][j]
	i=0
	while i < NROW:
		xLastMerge = NCOLUMS
		# pygame.time.delay(500)
		j=NCOLUMS-2
		print('begin i')
		while j > -1:
			# pygame.time.delay(500)
			print('begin j')
			print(j)
			if grid[j][i] == 0:
				print('continue')
				j-=1
				print('j--')
				continue
			elif grid[j+1][i] == 0:
				print('decale')
				grid[j+1][i] = grid[j][i]
				grid[j][i] = 0
				j+=2
				if j == NCOLUMS:
					j-=1
					# print('break')
					# break
				print(str(j) + " _ 2")
				# print('xLastMerge=' + str(xLastMerge))
				# print('j+1=' + str(j+1))
			elif grid[j+1][i] == grid[j][i] and j+1 < xLastMerge: # merge
			#elif grid[j+1][i] == grid[j][i]: # merge
				xLastMerge = j+1
				# print('xLastMerge=' + str(xLastMerge))
				grid[j+1][i] = grid[j][i]*2
				grid[j][i] = 0
			j-=1
			print('j--')
		i+=1
		print('i++')
		print(i)

	print('fin right2')

	print("after while right")
	aff_cons(grid)

	if not eq_grid(grid, oldgrid):
		add_num()
		
		affichage(grid)
	elif check_end(grid):
		go_screen()


def left2():
	for i in range(NROW):
		for j in range(NCOLUMS):
			oldgrid[i][j] = grid[i][j]
	i=0
	while i < NROW:
		xLastMerge = -1
		j=1
		while j < NCOLUMS:
			if grid[j][i] == 0:
				j+=1
				continue
			elif grid[j-1][i] == 0:
				grid[j-1][i] = grid[j][i]
				grid[j][i] = 0
				j-=2
				if j == -1:
					j+=1
			elif grid[j-1][i] == grid[j][i] and j-1 > xLastMerge:
				xLastMerge = j-1
				grid[j-1][i] = grid[j][i]*2
				grid[j][i] = 0
			j+=1
		i+=1

	print("after while left")
	aff_cons(grid)

	if not eq_grid(grid, oldgrid):
		add_num()
		
		affichage(grid)
	elif check_end(grid):
		go_screen()
	

def down2():
	# oldgrid = grid[:]
	# oldgrid = [[0]*NCOLUMS for n in range(NROW)]
	for i in range(NROW):
		for j in range(NCOLUMS):
			oldgrid[i][j] = grid[i][j]

	aff_cons(oldgrid)
	print(id(grid))
	print(id(oldgrid))
	i=0
	while i < NCOLUMS:
		print("begin while i")
		yLastMerge = NROW
		j=NROW-2
		while j > -1:
			print("begin while j = " + str(j))
			if grid[i][j] == 0:
				j-=1
				print("continue")
				continue
			elif grid[i][j+1] == 0:
				grid[i][j+1] = grid[i][j]
				grid[i][j] = 0
				j+=2
				print("decxale")
				if j == NROW:
					j-=1
			elif grid[i][j+1] == grid[i][j] and j+1 < yLastMerge:
				yLastMerge = j+1
				grid[i][j+1] = grid[i][j]*2
				grid[i][j] = 0
				print("same")
			j-=1
			print("j--")
		i+=1
		print("i++")

	print("after while down")
	aff_cons(grid)
	print("old")
	aff_cons(oldgrid)

	if not eq_grid(grid, oldgrid):
		add_num()
		
		affichage(grid)
	elif check_end(grid):
		go_screen()
	

def up2():
	for i in range(NROW):
		for j in range(NCOLUMS):
			oldgrid[i][j] = grid[i][j]
	i=0
	while i < NCOLUMS:
		print("begin while i")
		yLastMerge = -1
		j=1
		while j < NROW:
			print("begin while j = " + str(j))
			if grid[i][j] == 0:
				j+=1
				print("continue")
				continue
			elif grid[i][j-1] == 0:
				grid[i][j-1] = grid[i][j]
				grid[i][j] = 0
				j-=2
				print("decxale")
				if j == -1:
					j+=1
			elif grid[i][j-1] == grid[i][j] and j-1 > yLastMerge:
				yLastMerge = j-1
				grid[i][j-1] = grid[i][j]*2
				grid[i][j] = 0
				print("same")
			j+=1
			print("j++")
		i+=1
		print("i++")

	print(" after while up")
	aff_cons(grid)

	if not eq_grid(grid, oldgrid):
		add_num()
		
		affichage(grid)
	elif check_end(grid):
		go_screen()




affichage(grid)
aff_cons(grid)

#pygame.time.delay(10000)
#for i in range(100):
while GAME_RUN:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME_RUN = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				#print("left")
				left2()
			elif event.key == pygame.K_UP:
				#print("up")
				up2()
			elif event.key == pygame.K_RIGHT:
				#print("right")
				right2()
			elif event.key == pygame.K_DOWN:
				#print("down")
				down2()


		#direction = random.randint(1,4)
		#affichage(grid)
		#print("tour")
		#clock.tick(len(snake))
		#clock.tick(100000)
		#pygame.time.delay(200)
# affichage(grid)
print("dead")

GAME_RUN = True
while GAME_RUN:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME_RUN = False