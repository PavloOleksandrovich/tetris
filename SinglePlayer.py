import pygame
import random
from Main import menu
from enum import Enum

#block width and block height 
block_size = 30 
#amount of rows
rows = 10 
#amount of colls 
colls = 20

#grid size
play_width = rows * block_size 
play_height = colls * block_size 

#window size
window_width = 800
window_height = 800 

#start grid x position
top_left_x = (window_width - play_width) // 2  
#start grid y position
top_left_y = window_height - play_height - 100 

#SHAPES 

I = [['0000'],

     ['0',
      '0',
      '0',
      '0']]

O = [['00',
      '00',]]

J = [['0..',
      '000'],

     ['00',
      '0.',
      '0.'],

     ['000',
      '..0'],

     ['.0',
      '.0',
      '00']]

L = [['..0',
      '000'],

     ['0.',
      '0.',
      '00'],

     ['000',
      '0..'],

     ['00',
      '.0',
      '.0']]

T = [['.0.',
      '000'],

     ['0.',
      '00',
      '0.'],

     ['000',
      '.0.'],

     ['.0',
      '00',
      '.0']]

S = [['.00',
      '00.'],

     ['0.',
      '00',
      '.0']]

Z = [['00.',
      '.00'],

     ['.0',
      '00',
      '0.']]

shapes = [I,O,J,L,T,S,Z]
#colors
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 0, 255), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

#enum game state
class State(Enum):
    play = 'play'
    pause = 'pause'
    game_over = 'game_over'

class Piece:
    def __init__(self,x,y,shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(shape_colors)
        self.rotation = 0

def fall(shape,grid):
    ''' lower the block to the bottom '''

    while check_free_space(shape,grid):
        shape.y += 1

    return shape.y - 1

def check_game_over(positions):
    ''' if some block has reached the upper limit return True else return False '''

    for pos in positions:
        x , y = pos

        if y == 0:
            return True 

    return False 

def check_free_space(shape,grid):
    ''' This function returns True shape does not collide border or another shape '''

    #get all free spaces from grid
    accepted_pos = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]

    #convert from 2d list to 1d list 
    accepted_pos = [j for i in accepted_pos for j in i]

    #convert current shape to coordinates
    form = convert_shape_to_position(shape)

    #check coordinates 
    for pos in form:
        if pos not in accepted_pos and pos[1] >= 0:
            return False

    return True

def convert_shape_to_position(shape):
    ''' convert shape to coordinates '''

    position = [] 

    #get a shape type
    form = shape.shape[shape.rotation % len(shape.shape)]

    #get a height of shape 
    shape_height = len(form)

    #convert shape to coordinates
    for i , line in enumerate(form):
        row = list(line)
        for j , column in enumerate(row):
            if column == '0':
                position.append((shape.x + j,shape.y + i))

    for i in range(len(position)):
        position[i] = (position[i][0] - 1,position[i][1] - shape_height)

    return position

def create_new_shape():
    ''' create new random shape '''

    return Piece(rows // 2,0,random.choice(shapes))

def create_grid(positions = {}):
    ''' create a grid filled with existing blocks '''

    #create empty grid
    grid = [[(0,0,0) for _ in range(rows)] for _ in range(colls)]

    #filled grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in positions:
                grid[i][j] = positions[(j,i)]

    return grid

def draw_grid_lines(window):
	''' draw grey grid lines '''

	silver_color = (128,128,128)

	for i in range(colls):
		for j in range(rows):
			pygame.draw.rect(window,silver_color,(j * block_size + top_left_x,i * block_size + top_left_y,block_size,block_size),1)

def draw_grid(window,grid):
    ''' draw grid '''

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            rect = (top_left_x + j * block_size,top_left_y + i * block_size,block_size,block_size)
            color = grid[i][j]
            pygame.draw.rect(window,color,rect)

def draw_grid_border(window):
    ''' draw border around grid '''

	#border parameters
    red_color = (255,0,0)
    rect = (top_left_x,top_left_y,play_width,play_height)
    border_width = 4

	#draw border
    pygame.draw.rect(window,red_color,rect,border_width)

def draw_main_title(window):
    ''' draw main title '''

    #load fonts
    pygame.font.init()

    white_color = (255,255,255)

    #create font
    font = pygame.font.SysFont('comicsans',60)
    #create label
    label = font.render('TETRIS',1,white_color)
    #draw label
    window.blit(label,(window_width / 2 - label.get_width() / 2,30))

def draw_pause(window):
    #load fonts
    pygame.font.init()

    white_color = (255,255,255)

    #create font
    font = pygame.font.SysFont('comicsans',60)
    #create label
    label = font.render('Pause',1,white_color)
    #draw label
    window.blit(label,(window_width / 2 - label.get_width() / 2,window_height / 2 - label.get_height()))

def draw_game_over(window):
    #load fonts
    pygame.font.init()

    white_color = (255,255,255)

    #create font
    font = pygame.font.SysFont('comicsans',60)
    #create label
    label = font.render('Game over.Press any key...',1,white_color)
    #draw label
    window.blit(label,(window_width / 2 - label.get_width() / 2,window_height / 2 - label.get_height()))

def draw_next_shape(window,shape):
    #load fonts
    pygame.font.init()

    white_color = (255,255,255)

    #create font
    font = pygame.font.SysFont('comicsans',30)
    #create label
    label = font.render('Next shape',1,white_color)

    form = shape.shape[shape.rotation % len(shape.shape)] 

    #start coordinates
    start_x = top_left_x + play_width + 100 
    start_y = window_height / 2 - 100

    #draw shape
    for i , line in enumerate(form):
        row = list(line)
        for j , column in enumerate(row):
            if column == '0':
                pygame.draw.rect(window,shape.color,
                    (start_x + j * block_size,start_y + i * block_size,block_size,block_size))
                pygame.draw.rect(window,(128,128,128),
                    (start_x + j * block_size,start_y + i * block_size,block_size,block_size),2)

    #draw label
    window.blit(label,(start_x - 20,start_y - 50))

def draw_score(window,score):
    #load fonts
    pygame.font.init()

    white_color = (255,255,255)

    start_x = top_left_x + play_width + 95
    start_y = window_height / 2 - 100

    #create font
    font = pygame.font.SysFont('comicsans',30)
    #create label
    label = font.render('Score:' + str(score),1,white_color)
    #draw label
    window.blit(label,(start_x,window_height / 2 + 50))

def clear_rows(grid,positions):
    ''' clear filled rows '''

    index = 0
    flag = False
    height = 0

    for i in range(len(grid) -1,-1,-1):
        row = grid[i]
        if (0,0,0) not in row:

            flag = True

            index = i
            height += 1

            for j in range(len(row)):
                try:
                    del positions[(j,i)]
                except:
                    continue

    if flag:
        for i in range(index - 1,-1,-1):
            for j in range(rows):
                if (j,i) in positions:
                    color = positions[(j,i)]
                    del positions[(j,i)]
                    positions[(j,i + height)] = color

    return height * 200  

def draw_window(window,grid,game_state,next_shape,score):
    window.fill((0,0,0)) 

    #draw main title 
    draw_main_title(window)

    #draw grid
    draw_grid(window,grid)

    #draw silver unfilled grid on grid
    draw_grid_lines(window)

    #draw border around grid
    draw_grid_border(window)

    #draw next shape on the right
    draw_next_shape(window,next_shape)

    #draw score
    draw_score(window,score)

    #draw label pause
    if game_state == State.pause:
        draw_pause(window)

    #draw label game over
    if game_state == State.game_over:
        draw_game_over(window)

    #update screen
    pygame.display.update()

def main(window):
    pygame.init() 

    #create window
    window = pygame.display.set_mode((window_width,window_height))

    #create grid
    grid = create_grid()

    positions = {}

    #define game state
    game_state = State.play

    new_shape = False

    #create current shape
    current_shape = create_new_shape()

    #create next shape
    next_shape = create_new_shape()

    score = 0
    
    #determinate fall speed
    fall_speed = 0.25

    fall_time = 0

    level_time = 0

    clock = pygame.time.Clock()

    while True:

        if game_state == State.play:

            #create grid with filled blocks
            grid = create_grid(positions)

            #get time since last update
            update_time = clock.tick(60)

            fall_time += update_time

            level_time += update_time

            #increase speed 
            if level_time / 1000 > 5:
                level_time = 0
                if fall_speed > 0.15:
                    fall_speed -= 0.005

            #move shape down
            if fall_time / 1000 > fall_speed:
                current_shape.y += 1 
                fall_time = 0

                #if shape collide border or another shape
                if not check_free_space(current_shape,grid):
                    current_shape.y -= 1
                    new_shape = True

            #get pressed keys
            keys = pygame.key.get_pressed()

        	#handling input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()

                if event.type == pygame.KEYDOWN:

                    #move left 
                    if event.key == pygame.K_LEFT:
                        current_shape.x -= 1
                        if not check_free_space(current_shape,grid):
                            current_shape.x += 1

                    #move right
                    if event.key == pygame.K_RIGHT:
                        current_shape.x += 1
                        if not check_free_space(current_shape,grid):
                            current_shape.x -= 1

                    #rotate
                    if event.key == pygame.K_UP:
                        current_shape.rotation += 1
                        if not check_free_space(current_shape,grid):
                            current_shape.rotation -= 1
                    
                    #fall shape
                    if event.key == pygame.K_SPACE:
                        current_shape.y = fall(current_shape,grid)

                    #pause
                    if event.key == pygame.K_p:
                        game_state = State.pause

            #speed up
            if keys[pygame.K_DOWN]:
                current_shape.y += 1 
                if not check_free_space(current_shape,grid):
                    current_shape.y -= 1

            #get position of current shape
            current_shape_position = convert_shape_to_position(current_shape)

            #add current shape to grid
            for i in range(len(current_shape_position)):
                x , y = current_shape_position[i]
                
                if y >= 0:
                  grid[y][x] = current_shape.color

            ''' create new shape , check if rows are filled , update score , define next shape '''
            if new_shape:
                for pos in current_shape_position:
                    p = (pos[0],pos[1])
                    positions[p] = current_shape.color

                new_shape = False
                current_shape = next_shape
                next_shape = create_new_shape()
                score += 10
                score += clear_rows(grid,positions)


            ''' if there are blocks at first row finish the game '''
            if check_game_over(positions):
                game_state = State.game_over

            #draw window
            draw_window(window,grid,game_state,next_shape,score)

        elif game_state == State.pause:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()
                
                if event.type == pygame.KEYDOWN:

                    #continue play
                    if event.key == pygame.K_p:
                        game_state = State.play

        elif game_state == State.game_over:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()

                #return to menu
                if event.type == pygame.KEYDOWN:
                    menu(window)
