#python chess game
import pygame
import random
"""
MUST RUN PIP INSTALL PYGAME FOR THIS TO WORK
"""


#We ran into an issue where the png files for the pieces randomly corrupt and screws up everything, if that happens
#Please be aware of you are unable to run pychess.py . Thank you <3

"""
Original rationale was to build the game in pygame and display it as a web app using the Django framework
We realized that would basically be impossible/extremely annoying to implement so we dropped that idea
and continued with just PyGame
We used this repo for reference for a lot of the design patterns but did not copy/paste and a lot of the code is ours
https://github.com/plemaster01/pygameChess
https://www.youtube.com/watch?v=X-e0jk4I938&t=2235s
"""

pygame.init()
WIDTH = 800
HEIGTH = 1000
screen = pygame.display.set_mode([WIDTH, HEIGTH])
timer = pygame.time.Clock()                  #These are all of the different settings for the game UI
fps=60
pygame.display.set_caption("Chess Game CIS 434 Project")
text=pygame.font.Font('freesansbold.ttf', 48)
winner=''
#game images and placement
w_pieces = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
w_locations = [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)]
b_pieces = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
b_locations = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]
w_taken = []
b_taken = []
#turn order is white starts at 0, white selects a piece is at 1, black starts at 2, and black selects a piece is at 3
turn_order = 0
selection = 1000
valid_movement = []
#load images
b_queen = pygame.image.load('./black pieces/blackqueen.png')
b_queen = pygame.transform.scale(b_queen, (90,90))
b_king = pygame.image.load('./black pieces/blackking.png')
b_king = pygame.transform.scale(b_king, (90,90))
b_bishop = pygame.image.load('./black pieces/blackbishop.png')
b_bishop = pygame.transform.scale(b_bishop, (90,90))
b_knight = pygame.image.load('./black pieces/blackknight.png')
b_knight = pygame.transform.scale(b_knight, (90,90))
b_pawn = pygame.image.load('./black pieces/black pawn.png')
b_pawn = pygame.transform.scale(b_pawn, (70,70))               #Assets
b_rook = pygame.image.load('./black pieces/blackrook.png')
b_rook = pygame.transform.scale(b_rook, (90,90))
w_queen = pygame.image.load('./white pieces/whitequeen.png')
w_queen = pygame.transform.scale(w_queen, (90,90))
w_king = pygame.image.load('./white pieces/whiteking.png')
w_king = pygame.transform.scale(w_king, (90,90))
w_bishop = pygame.image.load('./white pieces/whitebishop.png')
w_bishop = pygame.transform.scale(w_bishop, (90,90))
w_knight = pygame.image.load('./white pieces/whiteknight.png')
w_knight = pygame.transform.scale(w_knight, (90,90))
w_pawn = pygame.image.load('./white pieces/whitepawn.png')
w_pawn = pygame.transform.scale(w_pawn, (70,70))
w_rook = pygame.image.load('./white pieces/whiterook.png')
w_rook = pygame.transform.scale(w_rook, (90,90))
w_images = [w_pawn, w_knight, w_bishop, w_rook, w_queen, w_king]
b_images = [b_pawn, b_knight, b_bishop, b_rook, b_queen, b_king]
piece_list = ['pawn','knight','bishop','rook','queen','king']

#function to find options of pieces
def check_options(pieces, locations, turn):
   moves=[]
   moves_list=[]
   for i in range(len(pieces)):
      location = locations[i]
      piece=pieces[i]
      if piece=='pawn':
         moves=check_pawn(location, turn)
      elif piece=='knight':
         moves=check_knight(location, turn)
      elif piece=='bishop':
         moves=check_bishop(location, turn)
      elif piece=='rook':
         moves=check_rook(location, turn)
      elif piece=='queen':
         moves=check_queen(location, turn)
      else:
         moves=check_king(location, turn)
      moves_list.append(moves)
   return moves_list
#drawing pieces to the board
def draw_pieces():
   for i in range(len(b_pieces)):
      index= piece_list.index(b_pieces[i])
      if b_pieces[i]=='pawn':
         screen.blit(b_pawn, (b_locations[i][0]*100+15,b_locations[i][1]*100+15))
      else:
         screen.blit(b_images[index], (b_locations[i][0]*100+5,b_locations[i][1]*100+5))
      if turn_order>=2:
         if selection == i:
            pygame.draw.rect(screen, 'brown', [b_locations[i][0]*100+1, b_locations[i][1]*100+1, 100, 100], 3)
   for i in range(len(w_pieces)):
      index= piece_list.index(w_pieces[i])
      if w_pieces[i]=='pawn':
         screen.blit(w_pawn, (w_locations[i][0]*100+15,w_locations[i][1]*100+15))
      else:
         screen.blit(w_images[index], (w_locations[i][0]*100+5,w_locations[i][1]*100+5))
      if turn_order<2:
         if selection==i:
            pygame.draw.rect(screen, 'purple', [w_locations[i][0]*100+1, w_locations[i][1]*100+1, 100, 100], 3)
#drawing the chess board
def draw_board():
   for i in range(32):
      column =i % 4
      row = i // 4
      if row % 2 == 0:
         pygame.draw.rect(screen, 'dark gray', [600 - (column*200), row*100, 100, 100])
      else:
         pygame.draw.rect(screen, 'dark gray', [700 - (column*200), row*100, 100, 100])
      pygame.draw.rect(screen, 'light blue', [0, 800, 800, 200])
      pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 200], 10)
      status_text = ['White: Select a Piece to move', 'White: Select its destination', 'Black: Select a Piece to move', 'Black: Select its destination']
      screen.blit(text.render(status_text[turn_order], True, 'black'), (20, 875))
      for i in range(9):
         pygame.draw.line(screen, 'white', (0, 100*i), (800, 100*i), 2)
         pygame.draw.line(screen, 'white', (100*i,0), (100*i,800),2)
#game over
def draw_game_over():
   pygame.draw.rect(screen,'dark blue',[75, 200, 650, 150])
   screen.blit(text.render(f'{winner} won the game!',True,'light blue'), (150, 240))
#check pawn movement
def check_pawn(position, color):
   moves=[]
   if color == 'white':
      if (position[0], position[1]-1) not in w_locations and (position[0], position[1]-1) not in b_locations and position[1]>0:
         moves.append((position[0], position[1]-1))
      if (position[0], position[1]-2) not in w_locations and (position[0], position[1]-2) not in b_locations and position[1]==6:
         moves.append((position[0], position[1]-2))
      if (position[0]+1, position[1]-1) in b_locations:
         moves.append((position[0]+1, position[1]-1))
      if (position[0]-1, position[1]-1) in b_locations:
         moves.append((position[0]-1, position[1]-1))
   else:
      if (position[0], position[1]+1) not in b_locations and (position[0], position[1]+1) not in w_locations and position[1]<7:
         moves.append((position[0], position[1]+1))
      if (position[0], position[1]+2) not in b_locations and (position[0], position[1]+2) not in w_locations and position[1]==1:
         moves.append((position[0], position[1]+2))
      if (position[0]+1, position[1]+1) in w_locations:
         moves.append((position[0]+1, position[1]+1))
      if (position[0]-1, position[1]+1) in w_locations:
         moves.append((position[0]-1, position[1]+1))
   return moves
#check knight movement
def check_knight(position, color):
   moves=[]
   if color=='black':
      friendly=b_locations
   else:
      friendly=w_locations
   move_to=[(1, 2), (-1, 2), (-1, -2), (1, -2), (-2, 1), (-2,-1), (2,-1), (2,1)]
   for i in range(8):
      movement=(position[0]+move_to[i][0], position[1]+move_to[i][1])
      if movement not in friendly and 0<=movement[0]<=7 and 0<=movement[1]<=7:
         moves.append(movement)
   return moves
#check bishop movement
def check_bishop(position, color):
   moves=[]
   if color=='black':
      enemy=w_locations
      friendly=b_locations
   else:
      enemy=b_locations
      friendly=w_locations
   for i in range(4): #check diagonal directions
      path=True
      length=1
      if i==0:
         x=1
         y=1
      elif i==1:
         x=1
         y=-1
      elif i==2:
         x=-1
         y=1
      else:
         x=-1
         y=-1
      while path:
         if (position[0]+(length*x),position[1]+(length*y)) not in friendly and 0<=position[0]+(length*x)<=7 and 0<=position[1]+(length*y)<=7:
            moves.append((position[0]+(length*x),position[1]+(length*y)))
            if (position[0]+(length*x),position[1]+(length*y)) in enemy:
               path=False
            length+=1
         else:
            path=False
   return moves
#check rook movement
def check_rook(position, color):
   moves=[]
   if color== 'white':
      friendly=w_locations
      enemy=b_locations
   else:
      friendly=b_locations
      enemy=w_locations
   for i in range(4): #check cardinal directions
      path=True
      length=1
      if i==0:
         x=0
         y=1
      elif i==1:
         x=0
         y=-1
      elif i==2:
         x=1
         y=0
      else:
         x=-1
         y=0
      while path:
         if (position[0]+(length*x), position[1]+(length*y)) not in friendly and 0<=position[0]+(length*x)<=7 and 0<=position[1]+(length*y)<=7:
            moves.append((position[0]+(length*x), position[1]+(length*y)))
            if (position[0]+(length*x), position[1]+(length*y)) in enemy:
               path=False
            length+=1
         else:
            path=False
   return moves
#check queen movement
def check_queen(position, color):
   moves=[]
   if color== 'white':
      friendly=w_locations
      enemy=b_locations
   else:
      friendly=b_locations
      enemy=w_locations
   for i in range(8): #check all directions
      path=True
      length=1
      if i==0:
         x=0
         y=1
      elif i==1:
         x=0
         y=-1
      elif i==2:
         x=1
         y=0
      elif i==3:
         x=-1
         y=0
      elif i==4:
         x=1
         y=1
      elif i==5:
         x=1
         y=-1
      elif i==6:
         x=-1
         y=1
      else:
         x=-1
         y=-1
      while path:
         if (position[0]+(length*x), position[1]+(length*y)) not in friendly and 0<=position[0]+(length*x)<=7 and 0<=position[1]+(length*y)<=7:
            moves.append((position[0]+(length*x), position[1]+(length*y)))
            if (position[0]+(length*x), position[1]+(length*y)) in enemy:
               path=False
            length+=1
         else:
            path=False
   return moves
#check king movement
def check_king(position, color):
   moves=[]
   if color== 'white':
      friendly=w_locations
      enemy=b_locations
   else:
      friendly=b_locations
      enemy=w_locations
   move_to=[(1, 1), (-1, 1), (-1, -1), (1, -1), (0, 1), (-1,0), (0,-1), (1,0)]
   for i in range(8): #check all directions
      movement=(position[0]+move_to[i][0], position[1]+move_to[i][1])
      if movement not in friendly and 0<=movement[0]<=7 and 0<=movement[1]<=7:
         moves.append(movement)
   return moves
#draw and verify king is in check
def draw_check():
   if turn_order < 2:
      if 'king' in w_pieces:
       king_index=w_pieces.index('king')
       king_location=w_locations[king_index]
       for i in range(len(b_options)):
         if king_location in b_options[i]:
            pygame.draw.rect(screen,'dark red',[w_locations[king_index][0] * 100 + 1, w_locations[king_index][1] * 100 + 1, 100, 100], 5)
   else:
      if 'king' in b_pieces:
       king_index=b_pieces.index('king')
       king_location=b_locations[king_index]
       for i in range(len(w_options)):
         if king_location in w_options[i]:
            pygame.draw.rect(screen,'dark red',[b_locations[king_index][0] * 100 + 1, b_locations[king_index][1] * 100 + 1, 100, 100], 5)
#check valid moves of piece
def check_valid():
   if turn_order<2:
      options_list = w_options
   else:
      options_list = b_options
   valid_options=options_list[selection]
   return valid_options
#draw valid movement
def draw_valid(moves):
   if turn_order<2:
      color='purple'
   else:
      color='brown'
   for i in range(len(moves)):
      pygame.draw.circle(screen, color, (moves[i][0]*100+50,moves[i][1]*100+50), 15)




#main
w_options=check_options(w_pieces, w_locations, 'white')
b_options=check_options(b_pieces, b_locations, 'black')
run = True
while run: #Main game runs in this loop
    timer.tick(fps)
    screen.fill('tan')
    draw_board()     #Different functions to create the UI of the game
    draw_pieces()
    draw_check()
    if selection != 1000:
       valid_movement=check_valid()
       draw_valid(valid_movement)
    #events
    for event in pygame.event.get():
       if event.type==pygame.QUIT:
        run = False
       if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
          x=event.pos[0] // 100
          y=event.pos[1] // 100
          clicked=(x,y)
          #white turn
          if turn_order <2:
             if clicked in w_locations:
                selection = w_locations.index(clicked)
                if turn_order == 0:
                   turn_order = 1
             if clicked in valid_movement and selection != 1000:
                w_locations[selection] = clicked
                if clicked in b_locations:
                   b_piece = b_locations.index(clicked)
                   w_taken.append(b_pieces[b_piece])
                   if b_pieces[b_piece] == 'king':
                      winner = 'white'
                   b_pieces.pop(b_piece)
                   b_locations.pop(b_piece)
                b_options = check_options(b_pieces, b_locations, 'black')
                w_options = check_options(w_pieces, w_locations, 'white')
                turn_order = 3
                selection = 1000
                valid_movement = []
          #black turn
          if turn_order >=2:
             while clicked not in valid_movement:
                try:
                   piece_to_move = random.sample(b_locations, 1)[0]
                   selection = b_locations.index(piece_to_move)
                   valid_movement = check_valid()
                   clicked = random.sample(valid_movement, 1)[0]
                except:
                   pass
             if clicked in valid_movement and selection != 1000:
                b_locations[selection] = clicked
                if clicked in w_locations:
                   w_piece = w_locations.index(clicked)
                   b_taken.append(w_pieces[w_piece])
                   if w_pieces[w_piece] == 'king':
                      winner = 'black'
                   w_pieces.pop(w_piece)
                   w_locations.pop(w_piece)
                w_options = check_options(w_pieces, w_locations, 'white')
                b_options = check_options(b_pieces, b_locations, 'black')
                turn_order = 0
                selection = 1000
                valid_movement = []
    if winner!='':
       game_over=True
       draw_game_over()
    pygame.display.flip()
pygame.QUIT()