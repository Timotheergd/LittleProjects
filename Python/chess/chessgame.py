import pygame
from pygame import display
from pygame import mouse
from menu import *
import datetime
from Tree import *

class Game():

    def __init__(self):
        pygame.init()

        # Menu
        self.running = True
        self.playing = False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.MOUSE_KEY = False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1000, 1000
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), display=0)
        self.font_name = 'Little_Comet_Bubling.otf'
        self.BLACK, self.WHITE, self.GREEN = (0, 0, 0), (255, 255, 255), (0, 255, 0)
        self.main_menu = MainMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

        # Chess Game

        self.mouse_posxy = (0, 0)
        self.mouse_pos = (0, 0)
        self.is_piece_selected = False
        self.selected_piece_pos = (0,0)
        self.move=[]
        self.can_en_passant = False
        self.last_move_pos = (0, 0)
        self.choose = False
        self.w_king_has_move, self.w_left_rook_has_move, self.w_right_rook_has_move = False, False, False
        self.b_king_has_move, self.b_left_rook_has_move, self.b_right_rook_has_move = False, False, False
        self.can_castling = False
        self.turn = 'white'
        self.checking_end = False
        self.finding_best_move = False
        self.depth = 1
        self.depth_case = []

        # creating the start grid 
        self.grid = [[0]*8 for i in range(8)]
        for i in range(0, 8):
            self.grid[i][1] = ('black', 'pawn')
            self.grid[i][6] = ('white', 'pawn')
            if i==0 or i==7:
                self.grid[i][0] = ('black', 'rook')
                self.grid[i][7] = ('white', 'rook')
            if i==1 or i==6:
                self.grid[i][0] = ('black', 'knight')
                self.grid[i][7] = ('white', 'knight')
            if i==2 or i==5:
                self.grid[i][0] = ('black', 'bishop')
                self.grid[i][7] = ('white', 'bishop')
            if i==3:
                self.grid[i][0] = ('black', 'queen')
                self.grid[i][7] = ('white', 'queen')
            if i==4:
                self.grid[i][0] = ('black', 'king')
                self.grid[i][7] = ('white', 'king')
                
        # import images and scale them
        self.board = pygame.transform.scale(pygame.image.load('textures/board.png'), (800, 800))

        self.black_rook = pygame.transform.scale(pygame.image.load('textures/black_rook.png'), (70, 70))
        self.black_pawn = pygame.transform.scale(pygame.image.load('textures/black_pawn.png'), (70, 70))
        self.black_king = pygame.transform.scale(pygame.image.load('textures/black_king.png'), (70, 70))
        self.black_queen = pygame.transform.scale(pygame.image.load('textures/black_queen.png'), (70, 70))
        self.black_bishop = pygame.transform.scale(pygame.image.load('textures/black_bishop.png'), (70, 70))
        self.black_knight = pygame.transform.scale(pygame.image.load('textures/black_knight.png'), (70, 70))

        self.white_rook = pygame.transform.scale(pygame.image.load('textures/white_rook.png'), (70, 70))
        self.white_pawn = pygame.transform.scale(pygame.image.load('textures/white_pawn.png'), (70, 70))
        self.white_king = pygame.transform.scale(pygame.image.load('textures/white_king.png'), (70, 70))
        self.white_queen = pygame.transform.scale(pygame.image.load('textures/white_queen.png'), (70, 70))
        self.white_bishop = pygame.transform.scale(pygame.image.load('textures/white_bishop.png'), (70, 70))
        self.white_knight = pygame.transform.scale(pygame.image.load('textures/white_knight.png'), (70, 70))

        self.white_rook_choose = pygame.transform.scale(pygame.image.load('textures/white_rook.png'), (140, 140))
        self.white_queen_choose = pygame.transform.scale(pygame.image.load('textures/white_queen.png'), (140, 140))
        self.white_bishop_choose = pygame.transform.scale(pygame.image.load('textures/white_bishop.png'), (140, 140))
        self.white_knight_choose = pygame.transform.scale(pygame.image.load('textures/white_knight.png'), (140, 140))
           
    def game_loop(self):
        while self.playing:
            self.check_events()
            self.display.fill(self.BLACK)
            self.window.blit(self.display, (0, 0))
            if self.turn == 'black':
                print("bot moving...")
                self.selectpiece()
            elif self.MOUSE_KEY:
                if self.is_piece_selected:
                    self.movepiece()
                else:
                    self.selectpiece()
            self.display_game()

            pygame.display.update()
            self.rest_keys()

    def movepiece(self, grid=None, play_pos=None, selected_piece_pos=None, testing=False):
        # print("m", grid, play_pos, selected_piece_pos)
        if not grid:
            grid=list(self.grid)
        if not play_pos:
            play_pos = self.mouse_pos
        if not selected_piece_pos:
            selected_piece_pos = self.selected_piece_pos

        self.is_piece_selected = False
        if play_pos in self.move or self.turn == 'black':
            grid[play_pos[0]][play_pos[1]], grid[selected_piece_pos[0]][selected_piece_pos[1]] = grid[selected_piece_pos[0]][selected_piece_pos[1]], 0
            # print("grid move !")
            # for l in grid:
            #     print(l)

            # En passant
            if grid[play_pos[0]][play_pos[1]][1] == 'pawn' and (selected_piece_pos[1]-play_pos[1] == 2 or selected_piece_pos[1]-play_pos[1] == -2): # if a pawn has move 2 cases
                self.can_en_passant = True # able en passant
                self.last_move_pos = play_pos

            if self.can_en_passant and grid[play_pos[0]][play_pos[1]][1] == 'pawn' and not selected_piece_pos[0]-play_pos[0] == 0: # destroy eatten piece en passant
                if grid[play_pos[0]][play_pos[1]][0] == 'white': 
                    grid[play_pos[0]][play_pos[1]+1] = 0
                else:
                    grid[play_pos[0]][play_pos[1]-1] = 0
                self.can_en_passant = False

            # check castling piece move
            if not testing:
                if play_pos[0] == 0 and play_pos[1] == 7:
                    self.w_left_rook_has_move = True
                if play_pos[0] == 7 and play_pos[1] == 7:
                    self.w_right_rook_has_move = True
                if play_pos[0] == 0 and play_pos[1] == 0:
                    self.b_left_rook_has_move = True
                if play_pos[0] == 7 and play_pos[1] == 0:
                    self.b_right_rook_has_move = True

                if grid[play_pos[0]][play_pos[1]][0] == 'white':
                    if grid[play_pos[0]][play_pos[1]][1] == 'rook':
                        if play_pos[0] == 0:
                            self.w_left_rook_has_move = True
                        elif play_pos[0] == 7:
                            self.w_right_rook_has_move = True
                    elif grid[play_pos[0]][play_pos[1]][1] == 'king':
                        self.w_king_has_move = True
                else:
                    if grid[play_pos[0]][play_pos[1]][1] == 'rook':
                        if play_pos[0] == 0:
                            self.b_left_rook_has_move = True
                        elif play_pos[0] == 7:
                            self.b_right_rook_has_move = True
                    elif grid[play_pos[0]][play_pos[1]][1] == 'king':
                        self.b_king_has_move = True

            # Casteling
            if grid[play_pos[0]][play_pos[1]][1] == 'king':
                if grid[play_pos[0]][play_pos[1]][0] == 'white': 
                    if selected_piece_pos[0]-play_pos[0] == 2 :
                        grid[3][7], grid[0][7] = grid[0][7], 0
                    elif selected_piece_pos[0]-play_pos[0] == -2:
                        grid[5][7], grid[7][7] = grid[7][7], 0
                else:
                    if selected_piece_pos[0]-play_pos[0] == 2 :
                        grid[3][0], grid[0][0] = grid[0][0], 0
                    elif selected_piece_pos[0]-play_pos[0] == -2:
                        grid[5][0], grid[0][0] = grid[0][0], 0

            # Pawn to end
            if not testing and grid[play_pos[0]][play_pos[1]][1] == 'pawn':
                if grid[play_pos[0]][play_pos[1]][0] == 'white' and play_pos[1] == 0:
                    self.choose_pawn_to_piece('white')
                elif play_pos[1] == 7:
                    self.choose_pawn_to_piece('black')
        
            # print("change color ??", testing)
            if not testing:
                print("change color !!")
                # print("points of ", self.turn, " = ", self.points(self.turn))
                if self.turn == 'white':
                    self.turn = 'black'
                else:
                    self.turn = 'white'
                # print("points of ", self.turn, " = ", self.points(self.turn))

            
        if not testing:
            self.move = [] # reset the moves

        return grid

    def choose_pawn_to_piece(self, color):
        self.choose = True
        # print("make your choice")
        self.last_move_pos = self.mouse_pos
        while self.choose:
            self.check_events()
            if self.MOUSE_KEY:
                if self.mouse_pos[1]>2 and self.mouse_pos[1]<5 and self.mouse_pos[0]>=0 and self.mouse_pos[0]<8:
                    if self.mouse_pos[0]>=0 and self.mouse_pos[0]<2:
                        #choose knight
                        self.grid[self.last_move_pos[0]][self.last_move_pos[1]] = (color, 'knight')
                    elif self.mouse_pos[0]>=2 and self.mouse_pos[0]<4:
                        #choose bishop
                        self.grid[self.last_move_pos[0]][self.last_move_pos[1]] = (color, 'bishop')
                    elif self.mouse_pos[0]>=4 and self.mouse_pos[0]<6:
                        #choose rook
                        self.grid[self.last_move_pos[0]][self.last_move_pos[1]] = (color, 'rook')
                    elif self.mouse_pos[0]>=6 and self.mouse_pos[0]<8:
                        #choose queen
                        self.grid[self.last_move_pos[0]][self.last_move_pos[1]] = (color, 'queen')
                    self.choose=False
                    
            self.display_game()
            pygame.display.update()
            self.rest_keys()

    def selectpiece(self, pos=None, grid=None, testing=False):
        if not pos:
            pos = self.mouse_pos
        if not grid:
            grid = list(self.grid)

        # Check possible move for the selected piece
        if pos[0] >= 0 and pos[0] < 8 and pos[1] >= 0 and pos[1] < 8 and (not grid[pos[0]][pos[1]] == 0):

            if not self.finding_best_move and self.turn == 'black': #grid[pos[0]][pos[1]][0] == 'black':
                #self.turn = "black" # ?????????????????
                print("bot moving... selecting piece")

                self.depth_case=[]
                print("before findallmoves")
                self.find_all_moves('black')
                best_move = self.choose_best_move()
                print(best_move)
                self.move = best_move
                print("BEFORE MOVE")
                self.movepiece(play_pos=best_move[1], selected_piece_pos=best_move[0])
                # for e in self.grid:
                #     print(e)
                print("end of selecting bot move")
                print(f"{self.turn=}")
                return
            # check who's turn is it
            if not testing and not grid[pos[0]][pos[1]][0] == self.turn:
                # print(grid[pos[0]][pos[1]][0])
                # print("MAUVAISE COULEUR !!")
                return
                #pass
            

            if grid[pos[0]][pos[1]][1] == 'pawn':
                # print("pawn")

                if grid[pos[0]][pos[1]][0] == 'white':
                    # print("white")
                    if grid[pos[0]][pos[1]-1] == 0: # move 1
                        self.move.append((pos[0],pos[1]-1))
                    if pos[1] == 6 and grid[pos[0]][pos[1]-1] == 0 and grid[pos[0]][pos[1]-2] == 0: # move 2
                        self.move.append((pos[0],pos[1]-2))
                    if pos[0]>0 and not grid[pos[0]-1][pos[1]-1] == 0 and not grid[pos[0]][pos[1]][0] == grid[pos[0]-1][pos[1]-1][0]: # eat left
                        self.move.append((pos[0]-1,pos[1]-1))
                    if pos[0]<7 and not grid[pos[0]+1][pos[1]-1] == 0 and not grid[pos[0]][pos[1]][0] == grid[pos[0]+1][pos[1]-1][0]: # eat right
                        self.move.append((pos[0]+1,pos[1]-1))
                    if self.can_en_passant and pos[1] == 3: # En passant
                        if pos[0]+1 == self.last_move_pos[0]:
                            self.move.append((pos[0]+1,pos[1]-1)) # right
                        if pos[0]-1 == self.last_move_pos[0]:
                            self.move.append((pos[0]-1,pos[1]-1)) # left
                    
                elif grid[pos[0]][pos[1]][0] == 'black':
                    # print("black")
                    if grid[pos[0]][pos[1]+1] == 0: # move 1
                        self.move.append((pos[0],pos[1]+1))
                    if pos[1] == 1 and grid[pos[0]][pos[1]+1] == 0 and grid[pos[0]][pos[1]+2] == 0: #move 2
                        self.move.append((pos[0],pos[1]+2))
                    if pos[0]>0 and not grid[pos[0]-1][pos[1]+1] == 0 and not grid[pos[0]][pos[1]][0] == grid[pos[0]-1][pos[1]+1][0]: # eat left
                        self.move.append((pos[0]-1,pos[1]+1))
                    if pos[0]<7 and not grid[pos[0]+1][pos[1]+1] == 0 and not grid[pos[0]][pos[1]][0] == grid[pos[0]+1][pos[1]+1][0]: # eat right
                        self.move.append((pos[0]+1,pos[1]+1))
                    if self.can_en_passant and pos[1] == 4: # En passant
                        if pos[0]+1 == self.last_move_pos[0]:
                            self.move.append((pos[0]+1,pos[1]+1)) # right
                        if pos[0]-1 == self.last_move_pos[0]:
                            self.move.append((pos[0]-1,pos[1]+1)) # left

            elif grid[pos[0]][pos[1]][1] == 'king':
                # print("king")
                # look straight right
                if pos[0]<7:
                    if not self.check_check(pos[0]+1,pos[1], grid[pos[0]][pos[1]][0]):
                        if grid[pos[0]+1][pos[1]] == 0:
                            self.move.append((pos[0]+1,pos[1]))
                        else:
                            if not grid[pos[0]][pos[1]][0] == grid[pos[0]+1][pos[1]][0]:
                                self.move.append((pos[0]+1,pos[1]))
                
                # look straight left
                if pos[0]>0:
                    if not self.check_check(pos[0]-1,pos[1], grid[pos[0]][pos[1]][0]):
                        if grid[pos[0]-1][pos[1]] == 0:
                            self.move.append((pos[0]-1,pos[1]))
                        else:
                            if not grid[pos[0]][pos[1]][0] == grid[pos[0]-1][pos[1]][0]:
                                self.move.append((pos[0]-1,pos[1]))
                
                # look straight down
                if pos[1]<7:
                    if not self.check_check(pos[0],pos[1]+1, grid[pos[0]][pos[1]][0]):
                        if grid[pos[0]][pos[1]+1] == 0:
                            self.move.append((pos[0],pos[1]+1))
                        else:
                            if not grid[pos[0]][pos[1]][0] == grid[pos[0]][pos[1]+1][0]:
                                self.move.append((pos[0],pos[1]+1))
                
                # look straight up
                if pos[1]>0:
                    if not self.check_check(pos[0],pos[1]-1, grid[pos[0]][pos[1]][0]):
                        if grid[pos[0]][pos[1]-1] == 0:
                            self.move.append((pos[0],pos[1]-1))
                        else:
                            if not grid[pos[0]][pos[1]][0] == grid[pos[0]][pos[1]-1][0]:
                                self.move.append((pos[0],pos[1]-1))
                    
                # look diagonal right down
                if pos[0]<7 and pos[1]<7:
                    if not self.check_check(pos[0]+1,pos[1]+1, grid[pos[0]][pos[1]][0]):
                        if grid[pos[0]+1][pos[1]+1] == 0:
                            self.move.append((pos[0]+1,pos[1]+1))
                        else:
                            if not grid[pos[0]][pos[1]][0] == grid[pos[0]+1][pos[1]+1][0]:
                                self.move.append((pos[0]+1,pos[1]+1))
                    
                # look diagonal left up
                if pos[0]>0 and pos[1]>0:
                    if not self.check_check(pos[0]-1,pos[1]-1, grid[pos[0]][pos[1]][0]):
                        if grid[pos[0]-1][pos[1]-1] == 0:
                            self.move.append((pos[0]-1,pos[1]-1))
                        else:
                            if not grid[pos[0]][pos[1]][0] == grid[pos[0]-1][pos[1]-1][0]:
                                self.move.append((pos[0]-1,pos[1]-1))
                    
                # look diagonal right up
                if pos[0]<7 and pos[1]>0:
                    if not self.check_check(pos[0]+1,pos[1]-1, grid[pos[0]][pos[1]][0]):
                        if grid[pos[0]+1][pos[1]-1] == 0:
                            self.move.append((pos[0]+1,pos[1]-1))
                        else:
                            if not grid[pos[0]][pos[1]][0] == grid[pos[0]+1][pos[1]-1][0]:
                                self.move.append((pos[0]+1,pos[1]-1))
                    
                # look diagonal left down
                if pos[0]>0 and pos[1]<7:
                    if not self.check_check(pos[0]-1,pos[1]+1, grid[pos[0]][pos[1]][0]):
                        if grid[pos[0]-1][pos[1]+1] == 0:
                            self.move.append((pos[0]-1,pos[1]+1))
                        else:
                            if not grid[pos[0]][pos[1]][0] == grid[pos[0]-1][pos[1]+1][0]:
                                self.move.append((pos[0]-1,pos[1]+1))

                castlingmove = self.check_castling(grid[pos[0]][pos[1]][0])
                if len(castlingmove):
                    self.move += castlingmove
                    
            elif grid[pos[0]][pos[1]][1] == 'queen':
                # print("queen")

                # rook
                for i in range(1, 8-pos[0]): # look straight right
                    if grid[pos[0]+i][pos[1]] == 0:
                        self.move.append((pos[0]+i,pos[1]))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]+i][pos[1]][0]:
                            self.move.append((pos[0]+i,pos[1]))
                        break
                for i in range(1, pos[0]+1): # look straight left
                    if grid[pos[0]-i][pos[1]] == 0:
                        self.move.append((pos[0]-i,pos[1]))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]-i][pos[1]][0]:
                            self.move.append((pos[0]-i,pos[1]))
                        break

                for i in range(1, 8-pos[1]): # look straight down
                    if grid[pos[0]][pos[1]+i] == 0:
                        self.move.append((pos[0],pos[1]+i))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]][pos[1]+i][0]:
                            self.move.append((pos[0],pos[1]+i))
                        break
                for i in range(1, pos[1]+1): # look straight up
                    if grid[pos[0]][pos[1]-i] == 0:
                        self.move.append((pos[0],pos[1]-i))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]][pos[1]-i][0]:
                            self.move.append((pos[0],pos[1]-i))
                        break
                
                # bishop
                for i in range(1, min(8-pos[0], 8-pos[1])): # look diagonal right down
                    if grid[pos[0]+i][pos[1]+i] == 0:
                        self.move.append((pos[0]+i,pos[1]+i))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]+i][pos[1]+i][0]:
                            self.move.append((pos[0]+i,pos[1]+i))
                        break
                for i in range(1, min(pos[0]+1, pos[1]+1)): # look diagonal left up
                    if grid[pos[0]-i][pos[1]-i] == 0:
                        self.move.append((pos[0]-i,pos[1]-i))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]-i][pos[1]-i][0]:
                            self.move.append((pos[0]-i,pos[1]-i))
                        break
                for i in range(1, min(8-pos[0], pos[1]+1)): # look diagonal right up
                    if grid[pos[0]+i][pos[1]-i] == 0:
                        self.move.append((pos[0]+i,pos[1]-i))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]+i][pos[1]-i][0]:
                            self.move.append((pos[0]+i,pos[1]-i))
                        break
                for i in range(1, min(pos[0]+1, 8-pos[1])): # look diagonal left down
                    if grid[pos[0]-i][pos[1]+i] == 0:
                        self.move.append((pos[0]-i,pos[1]+i))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]-i][pos[1]+i][0]:
                            self.move.append((pos[0]-i,pos[1]+i))
                        break
                
            elif grid[pos[0]][pos[1]][1] == 'rook':
                # print("rook")

                for i in range(1, 8-pos[0]): # look straight right
                    if grid[pos[0]+i][pos[1]] == 0:
                        self.move.append((pos[0]+i,pos[1]))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]+i][pos[1]][0]:
                            self.move.append((pos[0]+i,pos[1]))
                        break
                for i in range(1, pos[0]+1): # look straight left
                    if grid[pos[0]-i][pos[1]] == 0:
                        self.move.append((pos[0]-i,pos[1]))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]-i][pos[1]][0]:
                            self.move.append((pos[0]-i,pos[1]))
                        break
                for i in range(1, 8-pos[1]): # look straight down
                    if grid[pos[0]][pos[1]+i] == 0:
                        self.move.append((pos[0],pos[1]+i))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]][pos[1]+i][0]:
                            self.move.append((pos[0],pos[1]+i))
                        break
                for i in range(1, pos[1]+1): # look straight up
                    if grid[pos[0]][pos[1]-i] == 0:
                        self.move.append((pos[0],pos[1]-i))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]][pos[1]-i][0]:
                            self.move.append((pos[0],pos[1]-i))
                        break

            elif grid[pos[0]][pos[1]][1] == 'knight': # pas sur sur les commentaires
                # print("knight")

                if pos[0]<7 and pos[1]>1:
                    if grid[pos[0]+1][pos[1]-2] == 0: # diagonal right up up
                        self.move.append((pos[0]+1,pos[1]-2))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]+1][pos[1]-2][0]:
                            self.move.append((pos[0]+1,pos[1]-2))

                if pos[0]<6 and pos[1]>0:
                    if grid[pos[0]+2][pos[1]-1] == 0: # diagonal right up right
                        self.move.append((pos[0]+2,pos[1]-1))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]+2][pos[1]-1][0]:
                            self.move.append((pos[0]+2,pos[1]-1))

                if pos[0]<6 and pos[1]<7:
                    if grid[pos[0]+2][pos[1]+1] == 0: # diagonal right down right
                        self.move.append((pos[0]+2,pos[1]+1))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]+2][pos[1]+1][0]:
                            self.move.append((pos[0]+2,pos[1]+1))

                if pos[0]<7 and pos[1]<6:
                    if grid[pos[0]+1][pos[1]+2] == 0: # diagonal right down down
                        self.move.append((pos[0]+1,pos[1]+2))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]+1][pos[1]+2][0]:
                            self.move.append((pos[0]+1,pos[1]+2))
                
                if pos[0]>0 and pos[1]>1:
                    if grid[pos[0]-1][pos[1]-2] == 0: # diagonal right up up
                        self.move.append((pos[0]-1,pos[1]-2))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]-1][pos[1]-2][0]:
                            self.move.append((pos[0]-1,pos[1]-2))

                if pos[0]>1 and pos[1]>0:
                    if grid[pos[0]-2][pos[1]-1] == 0: # diagonal right up right
                        self.move.append((pos[0]-2,pos[1]-1))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]-2][pos[1]-1][0]:
                            self.move.append((pos[0]-2,pos[1]-1))

                if pos[0]>1 and pos[1]<7:
                    if grid[pos[0]-2][pos[1]+1] == 0: # diagonal right down right
                        self.move.append((pos[0]-2,pos[1]+1))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]-2][pos[1]+1][0]:
                            self.move.append((pos[0]-2,pos[1]+1))

                if pos[0]>0 and pos[1]<6:
                    if grid[pos[0]-1][pos[1]+2] == 0: # diagonal right down down
                        self.move.append((pos[0]-1,pos[1]+2))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]-1][pos[1]+2][0]:
                            self.move.append((pos[0]-1,pos[1]+2))

            elif grid[pos[0]][pos[1]][1] == 'bishop':
                # print("bishop")
                
                for i in range(1, min(8-pos[0], 8-pos[1])): # look diagonal right down
                    if grid[pos[0]+i][pos[1]+i] == 0:
                        self.move.append((pos[0]+i,pos[1]+i))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]+i][pos[1]+i][0]:
                            self.move.append((pos[0]+i,pos[1]+i))
                        break
                for i in range(1, min(pos[0]+1, pos[1]+1)): # look diagonal left up
                    if grid[pos[0]-i][pos[1]-i] == 0:
                        self.move.append((pos[0]-i,pos[1]-i))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]-i][pos[1]-i][0]:
                            self.move.append((pos[0]-i,pos[1]-i))
                        break
                for i in range(1, min(8-pos[0], pos[1]+1)): # look diagonal right up
                    if grid[pos[0]+i][pos[1]-i] == 0:
                        self.move.append((pos[0]+i,pos[1]-i))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]+i][pos[1]-i][0]:
                            self.move.append((pos[0]+i,pos[1]-i))
                        break
                for i in range(1, min(pos[0]+1, 8-pos[1])): # look diagonal left down
                    if grid[pos[0]-i][pos[1]+i] == 0:
                        self.move.append((pos[0]-i,pos[1]+i))
                    else:
                        if not grid[pos[0]][pos[1]][0] == grid[pos[0]-i][pos[1]+i][0]:
                            self.move.append((pos[0]-i,pos[1]+i))
                        break
    
            self.is_piece_selected = True
            self.selected_piece_pos = (pos[0],pos[1])
            print("return select before self.playable=", self.selected_piece_pos, self.move)
            self.move = self.playable_move(self.move, grid[pos[0]][pos[1]][0], grid)
            print("return select after self.playable=", self.selected_piece_pos, self.move)
            if not self.checking_end and self.move == []:
                self.check_end(grid[pos[0]][pos[1]][0])
            # print(f"{grid[pos[0]][pos[1]][0]=}")
            
            print("return select=", self.move)
            return self.move

    def check_check(self, x, y, color, grid=None):
        if not grid:
            grid = list(self.grid)
        # straight
        for i in range(1, 8-x): # look straight right
            if not grid[x+i][y] == 0 and not x-i == x:
                if grid[x+i][y][1] == 'king' and color == grid[x+i][y][0]:
                    continue
                if not color == grid[x+i][y][0]:
                    if grid[x+i][y][1] == 'rook' or grid[x+i][y][1] == 'queen':
                        return True
                    elif not grid[x+1][y] == 0 and grid[x+1][y][1] == 'king':
                        return True
                break
        for i in range(1, x+1): # look straight left
            if not grid[x-i][y] == 0:
                if grid[x-i][y][1] == 'king' and color == grid[x-i][y][0]:
                    continue
                if not color == grid[x-i][y][0]:
                    if grid[x-i][y][1] == 'rook' or grid[x-i][y][1] == 'queen':
                        return True
                    elif not grid[x-1][y] == 0 and grid[x-1][y][1] == 'king':
                        return True
                break
        for i in range(1, 8-y): # look straight down
            if not grid[x][y+i] == 0:
                if grid[x][y+i][1] == 'king' and color == grid[x][y+i][0]:
                    continue
                if not color == grid[x][y+i][0]:
                    if grid[x][y+i][1] == 'rook' or grid[x][y+i][1] == 'queen':
                        return True
                    elif not grid[x][y+1] == 0 and grid[x][y+i][1] == 'king':
                        return True
                break
        for i in range(1, y+1): # look straight up
            if not grid[x][y-i] == 0:
                if grid[x][y-i][1] == 'king' and color == grid[x][y-i][0]:
                    continue
                if not color == grid[x][y-i][0]:
                    if grid[x][y-i][1] == 'rook' or grid[x][y-i][1] == 'queen':
                        return True
                    elif not grid[x][y-1] == 0 and grid[x][y-i][1] == 'king':
                        return True
                break
        
        # diagonal
        for i in range(1, min(8-x, 8-y)): # look diagonal right down
            if not grid[x+i][y+i] == 0:
                if grid[x+i][y+i][1] == 'king' and color == grid[x+i][y+i][0]:
                    continue
                if not color == grid[x+i][y+i][0]:
                    if grid[x+i][y+i][1] == 'bishop' or grid[x+i][y+i][1] == 'queen':
                        return True
                    elif not grid[x+1][y+1] == 0 and (grid[x+1][y+1][1] == 'king' or (grid[x+1][y+1][1] == 'pawn' and color == 'black')):
                        return True
                break
        for i in range(1, min(x+1, y+1)): # look diagonal left up
            if not grid[x-i][y-i] == 0:
                if grid[x-i][y-i][1] == 'king' and color == grid[x-i][y-i][0]:
                    continue
                if not color == grid[x-i][y-i][0]:
                    if grid[x-i][y-i][1] == 'bishop' or grid[x-i][y-i][1] == 'queen':
                        return True
                    elif not grid[x-1][y-1] == 0 and (grid[x-1][y-1][1] == 'king' or (grid[x-1][y-1][1] == 'pawn' and color == 'white')):
                        return True
                break
        for i in range(1, min(8-x, y+1)): # look diagonal right up
            if not grid[x+i][y-i] == 0:
                if grid[x+i][y-i][1] == 'king' and color == grid[x+i][y-i][0]:
                    continue
                if not color == grid[x+i][y-i][0]:
                    if grid[x+i][y-i][1] == 'bishop' or grid[x+i][y-i][1] == 'queen':
                        return True
                    elif not grid[x+1][y-1] == 0 and (grid[x+1][y-1][1] == 'king' or (grid[x+1][y-1][1] == 'pawn' and color == 'white')):
                        return True
                break
        for i in range(1, min(x+1, 8-y)): # look diagonal left down
            if not grid[x-i][y+i] == 0:
                if grid[x-i][y+i][1] == 'king' and color == grid[x-i][y+i][0]:
                    continue
                if not color == grid[x-i][y+i][0]:
                    if grid[x-i][y+i][1] == 'bishop' or grid[x-i][y+i][1] == 'queen':
                        return True
                    elif not grid[x-1][y+1] == 0 and (grid[x-1][y+1][1] == 'king' or (grid[x-1][y+1][1] == 'pawn' and color == 'black')):
                        return True
                break

        #knight
        if x<7 and y>1:
            if not grid[x+1][y-2] == 0: # diagonal right up up
                if not color == grid[x+1][y-2][0]:
                    if grid[x+1][y-2][1] == 'knight':
                        return True

        if x<6 and y>0:
            if not grid[x+2][y-1] == 0: # diagonal right up up
                if not color == grid[x+2][y-1][0]:
                    if grid[x+2][y-1][1] == 'knight':
                        return True

        if x<6 and y<7:
            if not grid[x+2][y+1] == 0: # diagonal right up up
                if not color == grid[x+2][y+1][0]:
                    if grid[x+2][y+1][1] == 'knight':
                        return True

        if x<7 and y<6:
            if not grid[x+1][y+2] == 0: # diagonal right up up
                if not color == grid[x+1][y+2][0]:
                    if grid[x+1][y+2][1] == 'knight':
                        return True
        
        if x>0 and y>1:
            if not grid[x-1][y-2] == 0: # diagonal right up up
                if not color == grid[x-1][y-2][0]:
                    if grid[x-1][y-2][1] == 'knight':
                        return True

        if x>1 and y>0:
            if not grid[x-2][y-1] == 0: # diagonal right up up
                if not color == grid[x-2][y-1][0]:
                    if grid[x-2][y-1][1] == 'knight':
                        return True

        if x>1 and y<7:
            if not grid[x-2][y+1] == 0: # diagonal right up up
                if not color == grid[x-2][y+1][0]:
                    if grid[x-2][y+1][1] == 'knight':
                        return True

        if x>0 and y<6:
            if not grid[x-1][y+2] == 0: # diagonal right up up
                if not color == grid[x-1][y+2][0]:
                    if grid[x-1][y+2][1] == 'knight':
                        return True
        return False
           
    def check_castling(self, color):
        move=[]
        if color == 'white':
            if not self.w_king_has_move and not self.check_check(4, 7, color) and not self.w_left_rook_has_move and self.grid[1][7] == 0 and not self.check_check(1,7, color) and self.grid[2][7] == 0 and not self.check_check(2,7, color) and self.grid[3][7] == 0 and not self.check_check(3,7, color):
                move.append((2, 7))
            if not self.w_king_has_move and not self.check_check(4, 7, color) and not self.w_right_rook_has_move and self.grid [5][7] == 0 and not self.check_check(5,7, color) and self.grid[6][7] == 0 and not self.check_check(6,7, color):
                move.append((6, 7))
        else:
            if not self.b_king_has_move and not self.check_check(4, 0, color) and not self.b_left_rook_has_move and self.grid[1][0] == 0 and not self.check_check(1,0, color) and self.grid[2][0] == 0 and not self.check_check(2,0, color) and self.grid[3][0] == 0 and not self.check_check(3,0, color):
                move.append((2, 0))
            if not self.b_king_has_move and not self.check_check(4, 0, color) and not self.b_right_rook_has_move and self.grid [5][0] == 0 and not self.check_check(5,0, color) and self.grid[6][0] == 0 and not self.check_check(6,0, color):
                move.append((6, 0))
        return move
    
    def check_end(self, color):
        self.checking_end = True
        move = []
        king_pos = (0,0)
        grid = [[0]*8 for i in range(8)]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                grid[i][j] = self.grid[i][j]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if not self.grid[i][j] == 0 and self.grid[i][j][0] == color:
                    move.append(self.selectpiece((i,j)))
                    if self.grid[i][j][1] == 'king':
                        king_pos = (i,j)
        if move == []:
            if self.check_check(king_pos[0], king_pos[1], color):
                print("ECHEC ET MAT !!! "*50)
            else:
                print("PAT !!! "*50)
        self.move = []
        self.checking_end = False
        
    def playable_move(self, move, color, original_grid=None):
        selected_piece_pos = self.selected_piece_pos
        if not original_grid:
            original_grid=list(self.grid)
        playablemove=[]
        king_pos = (0,0)
        for mv in move:
            testgrid = [[0]*8 for i in range(8)]
            for i in range(len(original_grid)):
                for j in range(len(original_grid[i])):
                    testgrid[i][j] = original_grid[i][j]
            self.is_piece_selected = True
            selected_piece_pos = (self.selected_piece_pos[0],self.selected_piece_pos[1])
            # print("grid playablemove ")
            # for l in testgrid:
            #     print(l)
            self.movepiece(testgrid, mv, selected_piece_pos, True)

            for i in range(len(testgrid)):
                for j in range(len(testgrid[0])):
                    if not testgrid[i][j] == 0 and testgrid[i][j][1] == 'king' and color == testgrid[i][j][0]:
                        king_pos = (i,j)
            if not self.check_check(king_pos[0], king_pos[1], self.turn, testgrid):
                playablemove.append(mv)
        self.is_piece_selected = True
        return playablemove

    def display_game(self):
        self.window.blit(self.board, (100, 100))

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if not self.grid[i][j]==0:
                    if self.grid[i][j][0] == 'white':
                        if self.grid[i][j][1] == 'pawn':
                            self.window.blit(self.white_pawn, (115+i*100, 115+j*100))
                        elif self.grid[i][j][1] == 'king':
                            self.window.blit(self.white_king, (115+i*100, 115+j*100))
                        elif self.grid[i][j][1] == 'queen':
                            self.window.blit(self.white_queen, (115+i*100, 115+j*100))
                        elif self.grid[i][j][1] == 'rook':
                            self.window.blit(self.white_rook, (115+i*100, 115+j*100))
                        elif self.grid[i][j][1] == 'knight':
                            self.window.blit(self.white_knight, (115+i*100, 115+j*100))
                        elif self.grid[i][j][1] == 'bishop':
                            self.window.blit(self.white_bishop, (115+i*100, 115+j*100))
                    else:
                        if self.grid[i][j][1] == 'pawn':
                            self.window.blit(self.black_pawn, (115+i*100, 115+j*100))
                        elif self.grid[i][j][1] == 'king':
                            self.window.blit(self.black_king, (115+i*100, 115+j*100))
                        elif self.grid[i][j][1] == 'queen':
                            self.window.blit(self.black_queen, (115+i*100, 115+j*100))
                        elif self.grid[i][j][1] == 'rook':
                            self.window.blit(self.black_rook, (115+i*100, 115+j*100))
                        elif self.grid[i][j][1] == 'knight':
                            self.window.blit(self.black_knight, (115+i*100, 115+j*100))
                        elif self.grid[i][j][1] == 'bishop':
                            self.window.blit(self.black_bishop, (115+i*100, 115+j*100))

        for i in range(len(self.move)):
            pygame.draw.circle(self.window, (0,255,0,128), ((self.move[i][0]*100)+150, (self.move[i][1]*100)+150), 20)

        if self.choose:
            pygame.draw.rect(self.window, self.BLACK, pygame.Rect(100, 300, 800, 300))
            #self.draw_text("Make your choice :", 100, 500, 300)
            self.window.blit(self.white_knight_choose, (130, 430))
            self.window.blit(self.white_bishop_choose, (330, 430))
            self.window.blit(self.white_rook_choose, (530, 430))
            self.window.blit(self.white_queen_choose, (730, 430))
            
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.MOUSE_KEY = True
                    self.mouse_posxy = pygame.mouse.get_pos()
                    self.mouse_pos = ((self.mouse_posxy[0]-100)//100, (self.mouse_posxy[1]-100)//100)

    def points(self, color, grid=None):
        if not grid:
            grid = self.grid
        w_points=0
        b_points=0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if not grid[i][j] == 0:
                    if grid[i][j][1] == 'pawn':
                        if grid[i][j][0] == 'white':
                            w_points +=1
                        else:
                            b_points +=1
                    elif grid[i][j][1] == 'bishop' or grid[i][j][1] == 'knight':
                        if grid[i][j][0] == 'white':
                            w_points +=3
                        else:
                            b_points +=3
                    elif grid[i][j][1] == 'rook':
                        if grid[i][j][0] == 'white':
                            w_points +=5
                        else:
                            b_points +=5
                    elif grid[i][j][1] == 'queen':
                        if grid[i][j][0] == 'white':
                            w_points +=9
                        else:
                            b_points +=9
        return w_points-b_points

    def find_all_moves(self, color, grid=None, previous_moves=[], depth=None):
        print("BEGIN FING BEST MOVE", depth)
        if depth == None:
            depth = self.depth
            print("first depth =", depth)
        elif depth <= 0:
            print("EEEEEEEENNNNNNNNNDDDDDD" + str(previous_moves), str(self.points(color, grid)))
            return (previous_moves, self.points(self.turn,grid), self.turn)
        
        # print("DEBUT FIND BEST MOVE")
        self.finding_best_move = True
        selected_piece = []
        move = []

        if not grid:
            grid = [[0]*8 for i in range(8)]
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    grid[i][j] = self.grid[i][j]

        testgrid = [[0]*8 for i in range(8)]
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                testgrid[i][j] = grid[i][j]
        
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if not grid[i][j] == 0 and grid[i][j][0] == color:
                    u = self.selectpiece((i,j), grid, True)
                    print(f"{u=}")
                    move += u
                    while len(selected_piece) < len(move):
                        selected_piece += [(i,j)]
                    self.move=[]
        
        # pour chaque mv, tester et voir le nb de points
        # print("BEFORE")
        # print(f"{depth=}")
        print("     " + f"{move=}")
        print(f"{selected_piece=}")
        # print(f"{len(move)=}, {len(selected_piece)=}")
        # for i in testgrid:
        #     print(i)
        # print("AFTER")
        for i in range(len(move)):
            self.move = move
            # print(move)
            # print(i)
            # print(f"{move[i]=}")
            # print(str(datetime.datetime.now()))

            #reinit testgrid
            for ii in range(len(grid)):
                for j in range(len(grid[ii])):
                    testgrid[ii][j] = grid[ii][j]

            testgrid = self.movepiece(testgrid, move[i], selected_piece[i], True).copy()
            self.move=[]
            # for t in testgrid:
            #     print(t)
            # print(self.points(color, testgrid))
            print("before recurtion")
            print(f"{self.depth_case=}")
            self.depth_case.append(self.find_all_moves(self.change_color(color), testgrid, previous_moves+[(selected_piece[i], move[i])], depth-1))
            #depth = depth-1
            # print("*"*50)
            # print("*"*50)
            # print("*"*50)
        self.finding_best_move = False  
        # print(f"{move=}")
        # print(f"{len(move)=}")
        # for e in move:
        #     print(e)
        #return move

    def choose_best_move(self):
        print("begin choose best move")
        print(f"{len(self.depth_case)=}")
        f = open("moves.txt", "w")
        f.write(str(self.depth_case))
        f.close()
        base = Tree(None, [[(None)],[(None)]])
        tree_moves = base.copy()
        mother = tree_moves
        for i in range(len(self.depth_case)):
            if self.depth_case[i] == None:
                continue
            self.create_tree_moves(self.depth_case[i], mother)
        # tree_moves.print()
        
        best_move = tree_moves.max(1).read_tree_up(self.depth-1).move
        
        return best_move

    def create_tree_moves(self, coups, mother):
        if len(coups[0]) == 0:
            return
        child_num=-1
        add=1
        for i in range(len(mother.children)):
            child_num+=1
            if Tree(mother, coups[0][0]) == mother.children[i]:
                add=0
                break
        if add==1:
            mother.add_child(coups[0][0], coups[1])
            child_num+=1
        del coups[0][0]
        self.create_tree_moves(coups, mother.children[child_num])

    def change_color(self, color):
        if color == 'white':
            return 'black'
        else:
            return 'white'

    def rest_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.MOUSE_KEY = False, False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)