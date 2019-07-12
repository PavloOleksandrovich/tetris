import pygame
import random
import pickle
from Network import Network
import Main 

block_size = 25 
rows = 20 
colls = 20

play_width = rows * block_size 
play_height = colls * block_size 

state = 'waiting'

window_width = 1000 
window_height = 800 

top_left_x = (window_width - play_width) // 2
top_left_y = window_height - play_height - 70 

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

class Piece:
    def __init__(self,x,y,shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(shape_colors)
        self.rotation = 0

def draw_game_over(window):
    ''' draw label game over at the center of screen '''

    #load fonts
    pygame.font.init()

    white_color = (255,255,255)

    #create font
    font = pygame.font.SysFont('comicsans',60)
    #create label
    label = font.render('Game over.Press any key...',1,white_color)
    #draw label
    window.blit(label,(window_width / 2 - label.get_width() / 2,window_height / 2 - label.get_height()))

def fall(shape,grid):
    ''' descend the shape to the bottom '''

    while check_free_space(shape,grid):
        shape.y += 1

    return shape.y - 1

def check_free_space(shape,grid):
    ''' This function returns True shape does not collide border or another shape '''

    #get all free spaces from grid
    accepted_pos = [[(j,i) for j in range(rows // 2) 
        if grid[i][j] == (0,0,0)] for i in range(colls)]

    #convert from 2d list to 1d list 
    accepted_pos = [j for i in accepted_pos for j in i]

    #convert shape to positions
    positions = convert_shape_to_position(shape)

    #check if there are free space
    for pos in positions:
        if pos not in accepted_pos and pos[1] >= 0:
            #return False if there is occupied space
            return False

    return True

def convert_shape_to_position(shape):
    ''' convert from shape to coordinates '''

    position = [] 

    #get current type of shape form
    form = shape.shape[shape.rotation % len(shape.shape)]

    #get shape height
    shape_height = len(form)

    #convert to coordinate
    for i , line in enumerate(form):
        row = list(line)
        for j , column in enumerate(row):
            if column == '0':
                position.append((shape.x + j,shape.y + i))

    ''' normalize coordinates 
    x - 1 for centralizing on grid , y - height of shape because we want 
    the shape to appear behind the grid and gradually descend by one block'''
    for i in range(len(position)):
        position[i] = (position[i][0] - 1,position[i][1] - shape_height)

    return position

def create_new_shape():
    ''' create random shape '''

    shape = random.choice(shapes)
    
    return Piece((rows - rows // 2) // 2,0,shape)

def create_grid(positions = {},friend_positions={}):
    ''' create grid with filled positions '''

    #create grid
    grid = [[(0,0,0) for _ in range(rows)] for _ in range(colls)]

    #fill player positions
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in positions:
                grid[i][j] = positions[(j,i)]

    #fill friend positions
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in friend_positions:
                grid[i][j+10] = friend_positions[(j,i)]

    return grid

def draw_next_shape(window,shape,friend_shape):
    #load fonts
    pygame.font.init()

    white_color = (255,255,255)

    #create font
    font = pygame.font.SysFont('comicsans',30)
    #create label
    label = font.render('Next shape',1,white_color)


    form = shape.shape[shape.rotation % len(shape.shape)] 

    #start coordinates
    start_x =  100 
    start_y = window_height / 2 - 50

    #draw shape
    for i , line in enumerate(form):
        row = list(line)
        for j , column in enumerate(row):
            if column == '0':
                pygame.draw.rect(window,shape.color,
                (start_x + j * block_size,start_y + i * block_size,
                block_size,block_size))
                pygame.draw.rect(window,(128,128,128),
                (start_x + j * block_size,start_y + i * block_size,
                block_size,block_size),2)

    #draw label
    window.blit(label,(start_x - 10,start_y - 50))

    #start coordinates
    start_x = top_left_x + play_width + 50 
    start_y = window_height / 2 - 100

    form = friend_shape.shape[
        friend_shape.rotation % len(friend_shape.shape)] 

    #draw shape
    for i , line in enumerate(form):
        row = list(line)
        for j , column in enumerate(row):
            if column == '0':
                pygame.draw.rect(window,friend_shape.color,
                    (start_x + j * block_size,start_y + i * block_size,block_size,block_size))
                pygame.draw.rect(window,(128,128,128),
                    (start_x + j * block_size,start_y + i * block_size,block_size,block_size),2)
    #draw label
    window.blit(label,(start_x - 20,start_y - 50))

def draw_grid_lines(window):
    ''' This function draws grey grid lines '''

    #silver color
    silver_color = (128,128,128)
    #red color
    red_color = (255,0,0)

    #draw grid squares 
    for i in range(colls):
        for j in range(rows):
            pygame.draw.rect(window,silver_color,
            (j * block_size + top_left_x,i * block_size + top_left_y,
            block_size,block_size),1)

    #draw split line
    pygame.draw.line(window,red_color,
    (rows / 2 * block_size + top_left_x,top_left_y),
    (rows / 2 * block_size + top_left_x,colls * block_size + top_left_y),4)

def draw_grid_border(window):
    ''' draw red border around grid '''

    #border parameters
    red_color = (255,0,0)
    rect = (top_left_x,top_left_y,play_width,play_height)
    border_width = 4

    #draw border
    pygame.draw.rect(window,red_color,rect,border_width)

def draw_grid(window,grid):
    ''' draw grid '''

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            rect = (top_left_x + j * block_size,
            top_left_y + i * block_size,block_size,block_size)
            color = grid[i][j]
            pygame.draw.rect(window,color,rect)

def draw_score(window,score):
    ''' draw common score '''

    #load fonts
    pygame.font.init()

    white_color = (255,255,255)

    #start position
    start_x = top_left_x + play_width + 95
    start_y = window_height / 2 - 100

    #create font
    font = pygame.font.SysFont('comicsans',60)
    #create label
    label = font.render('Score: ' + str(score),1,white_color)
    #draw label
    window.blit(label,(window_width / 2 - label.get_width() / 2,100))

def draw_window(window,grid,player_shape,friend_shape,score):
    ''' draw all components '''

    global state

    #clear window
    window.fill((0,0,0)) 

    draw_grid(window,grid)

    draw_grid_lines(window)

    draw_grid_border(window)

    draw_next_shape(window,player_shape,friend_shape)

    draw_score(window,score)

    if state == 'game_over':
        draw_game_over(window)

    pygame.display.update()

def draw_waiting(window):
    #clear window
    window.fill((0,0,0)) 

    #load fonts
    pygame.font.init()

    white_color = (255,255,255)

    #create font
    font = pygame.font.SysFont('comicsans',60)
    #create label
    label = font.render('Waiting for players',1,white_color)
    #draw label
    window.blit(label,(window_width / 2 - label.get_width() / 2,window_height / 2 - label.get_height()))

    pygame.display.update()

def client(window = None):
    global state 

    #create window
    window = pygame.display.set_mode((window_width,window_height))

    net = Network()

    #filled positions
    positions = {}

    #do need create new shape
    new_shape = False

    #connect to server , receive shape and next shape
    data = net.connect() 

    #current player shape
    player_shape = data[0]

    #next shape
    next_shape = data[1] 

    #friend shape
    friend_shape = None

    #friend filled positions 
    friend_positions = {} 

    #friend next shape
    friend_next_shape = None

    #score
    score = 0

    #friend score
    friend_score = 0

    #how often we descend our shape
    fall_speed = 0.5 

    ''' when this variable will reach time as fall speed 
    we will descend our shape at one position '''
    fall_time = 0

    #create clock we need it to count elapsed time
    clock = pygame.time.Clock()

    while True:

        if state == 'waiting':

            #handling events
            for event in pygame.event.get():
                    
                #quit game
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()

            draw_waiting(window)

            state = net.send_object("")

        if state == 'play':

            ''' send shape to server and receive friend shape from server '''
            friend_shape = net.send_object(player_shape)

            ''' send positions to server and receive 
                friend positions from server '''

            net.client.send(pickle.dumps(positions))

            data = pickle.loads(net.client.recv(8192))

            positions= data[0]
            grid = data[1]
            state = data[2]

            ''' send score to server and receive 
                friend score from server '''

            total_score = net.send_object(score)

            ''' send next shape to server and receive 
                friend next shape from server '''

            friend_next_shape = net.send_object(next_shape)

            ''' update_time - elapsed time since last update 
                clock.tick - determinate fps '''

            update_time = clock.tick(60)

            #update fall time
            fall_time += update_time

            #move shape down
            if fall_time / 1000 > fall_speed:
                player_shape.y += 1 
                fall_time = 0

                ''' if shape collide border or another shape 
                return shape to previus previous and create new shape '''
                if not check_free_space(player_shape,grid):
                    player_shape.y -= 1

                    new_shape = True

            #get pressed keys
            keys = pygame.key.get_pressed()
            
            #handling events
            for event in pygame.event.get():
                    
                #quit game
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()


                #handling down keys 
                if event.type == pygame.KEYDOWN:

                    #move left 
                    if event.key == pygame.K_LEFT:
                        player_shape.x -= 1

                        '''if shape collide border or another shape 
                        return shape to previus previous and create new shape '''
                        if not check_free_space(player_shape,grid):
                            player_shape.x += 1

                    #move right
                    if event.key == pygame.K_RIGHT:
                        player_shape.x += 1

                        '''if shape collide border or another shape 
                        return shape to previus previous and create new shape '''
                        if not check_free_space(player_shape,grid):
                            player_shape.x -= 1

                    #rotate
                    if event.key == pygame.K_UP:
                        player_shape.rotation += 1

                        '''if shape collide border or another shape 
                        return shape to previus previous and create new shape '''
                        if not check_free_space(player_shape,grid):
                            player_shape.rotation -= 1

                    #fall shape 
                    if event.key == pygame.K_SPACE:
                        player_shape.y = fall(player_shape,grid)
                        pass

            #descend player shape
            if keys[pygame.K_DOWN]:
                player_shape.y += 1 
                if not check_free_space(player_shape,grid):
                    player_shape.y -= 1
                        
            player_convert_positions = convert_shape_to_position(player_shape)
            friend_convert_positions = convert_shape_to_position(friend_shape)

            #add player shape to grid
            for i in range(len(player_convert_positions)):
                x , y = player_convert_positions[i]
                    
                if y >= 0:
                    grid[y][x] = player_shape.color

            #add friend shape to grid
            for i in range(len(friend_convert_positions)):
                x , y = friend_convert_positions[i]
                    
                if y >= 0:
                    grid[y][x + 10] = friend_shape.color

            #create new shape
            if new_shape:

                #add current player shape to grid
                for pos in player_convert_positions:
                    p = (pos[0],pos[1])
                    positions[p] = player_shape.color

                new_shape = False

                player_shape = next_shape 

                next_shape = create_new_shape() 

                score += 10

            #draw all components
            draw_window(window,grid,next_shape,friend_next_shape,
                total_score)

        if state == 'game_over':

            #handling events
            for event in pygame.event.get():
                    
                #quit game
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()

                #handling down keys 
                if event.type == pygame.KEYDOWN:
                    Main.menu(window)

if __name__ == '__main__':
    client()