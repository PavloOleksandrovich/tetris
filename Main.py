import pygame
import os
import random
from enum import Enum
import SinglePlayer
import Client 

#window size
window_width = 600
window_height = 500

#enum choosed button 
class Choosed(Enum):
    single = 'single_palyer'
    multiplayer = 'multiplayer'
    quit = 'quit'

def draw_title(window):
    ''' draw title '''

    #load fonts
    pygame.font.init()

    white_color = (255,255,255)

    #create font
    font = pygame.font.SysFont('comicsans',60)
    #create label
    label = font.render('TETRIS',1,white_color)
    #draw label
    window.blit(label,(window_width / 2 - label.get_width() / 2,60))

def draw_options(window):
    ''' draw menu points '''

    #load fonts
    pygame.font.init()

    white_color = (255,255,255)

    #create font
    font = pygame.font.SysFont('comicsans',40)
    #font = pygame.font.Font(os.path.join('font','.ttf'), 40)

    #create label
    single_player_label = font.render('Single  player',1,white_color)
    #create label
    multiplayer_label = font.render('Multiplayer',1,white_color)
    #create label
    quit_label = font.render('Quit',1,white_color)

    #draw labels
    window.blit(single_player_label,(window_width / 2 - single_player_label.get_width() / 2,170))
    window.blit(multiplayer_label,(window_width / 2 - multiplayer_label.get_width() / 2,230))
    window.blit(quit_label,(window_width / 2 - quit_label.get_width() / 2,280))

def draw_button_frames(window,choose):
    ''' draw frames around menu points '''

    if choose == Choosed.single:
        r_w = 220
        rect = ((window_width - r_w) / 2,169,r_w,30)
    elif choose == Choosed.multiplayer:
        r_w = 160
        rect = ((window_width - r_w) / 2,229,r_w,30)
    elif choose == Choosed.quit:
        r_w = 70 
        rect = ((window_width - r_w) / 2,279,r_w,30)
    
    pygame.draw.rect(window,(128,128,128),rect,1)


def draw_menu(window,choose):
    window.fill((0,0,0)) 

    #draw title
    draw_title(window)

    #draw menu points
    draw_options(window)

    #draw frames around menu points
    draw_button_frames(window,choose)

    pygame.display.update()

def menu(window=None):
    pygame.init()

    #create window
    window = pygame.display.set_mode((window_width,window_height))

    pygame.display.set_caption('Tetris')

    #current button 
    choosed_string = Choosed.single

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                #switch buttons
                if event.key == pygame.K_DOWN:
                    if choosed_string == Choosed.single:
                        choosed_string = Choosed.multiplayer
                    elif choosed_string == Choosed.multiplayer:
                        choosed_string = Choosed.quit
                    elif choosed_string == Choosed.quit:
                        choosed_string = Choosed.single

                #switch buttons
                if event.key == pygame.K_UP:
                    if choosed_string == Choosed.single:
                        choosed_string = Choosed.quit
                    elif choosed_string == Choosed.multiplayer:
                        choosed_string = Choosed.single
                    elif choosed_string == Choosed.quit:
                        choosed_string = Choosed.multiplayer

                #execute button 
                if event.key == pygame.K_RETURN:
                    
                    if choosed_string == Choosed.single:
                        SinglePlayer.main(window)

                    if choosed_string == Choosed.multiplayer:
                        Client.client(window)

                    if choosed_string == Choosed.quit:
                        pygame.display.quit()
                        quit()

        #draw menu
        draw_menu(window,choosed_string)


if __name__ == '__main__':
    menu()