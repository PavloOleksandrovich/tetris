import socket
import pickle
import os
from _thread import *
from SinglePlayer import Piece , I , O , J , L , T , S , Z , shapes , shape_colors
from Client import create_new_shape

def get_ip_address():
    ''' return ip address of local network '''

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

#data for connection
ip = '192.168.1.7' #get_ip_address()
port = 5555

game_state = 'waiting'

rows = 20 
colls = 20

#player index 
currentPlayer = 0

score_rows = 0
player_shapes = [None,None]
player_positions = [{},{}]
player_scores = [0,0]
player_next_shapes = [None,None]
send_to_player_flags = [True,True]

def create_grid(positions = {},positions2 = {}):
    ''' fill grid '''

    grid = [[(0,0,0) for _ in range(rows)] for _ in range(colls)]

    #fill positions player 1
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in positions:
                grid[i][j] = positions[(j,i)]

    #fill positions player 2
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in positions2:
                grid[i][j+10] = positions2[(j,i)]

    return grid

def clear_rows(grid,positions,positions2):
    ''' This function clears filled rows '''

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

            for j in range(len(row)):
                try:
                    del positions2[(j,i)]
                except:
                    continue


    if flag:

        for i in range(index - 1,-1,-1):
            for j in range(rows):
                if (j,i) in positions:
                    color = positions[(j,i)]
                    del positions[(j,i)]
                    positions[(j,i + height)] = color

        for i in range(index - 1,-1,-1):
            for j in range(rows):
                if (j,i) in positions2:
                    color = positions2[(j,i)]
                    del positions2[(j,i)]
                    positions2[(j,i + height)] = color

    return height * 400 

def threaded_client(conn, player,addr):
    ''' player thread '''

    conn.send(pickle.dumps([player_shapes[player],player_next_shapes[player]]))

    #grid = None 
    global score_rows
    global game_state

    conn.recv(8192)

    while game_state == 'waiting':

        if player == 1:

            game_state = 'play'

    reply = pickle.dumps(game_state)

    conn.send(reply)

    while True:

        #receive and send current shapes
        try:
            shape = pickle.loads(conn.recv(8192))
            player_shapes[player] = shape 
        except:
            break

        if player == 0:
            reply = pickle.dumps(player_shapes[1])
        elif player == 1:
            reply = pickle.dumps(player_shapes[0])
        
        try:
            conn.send(reply)
        except:
            break


        #receive and send positions 

        try:
            positions = pickle.loads(conn.recv(8192))

            if send_to_player_flags[player] == True:
                player_positions[player] = positions 

                if player == 0:
                    grid = create_grid(player_positions[0],player_positions[1])
                else:
                    grid = create_grid(player_positions[1],player_positions[0])

                score_last_rows = clear_rows(grid,player_positions[0],player_positions[1]) 
                score_rows += score_last_rows

                if score_last_rows != 0:
                    if player == 0:
                        send_to_player_flags[1] = False
                    if player == 1:
                        send_to_player_flags[0] = False
            else:
                send_to_player_flags[player] = True

        except:
            break

        for pos in positions:
            x , y = pos

            if y == 0:
                game_state = 'game_over'


        reply = pickle.dumps([player_positions[player],grid,game_state])

        try:
            conn.send(reply)
        except:
            break


        #receive and send scores 
        try:
            score = pickle.loads(conn.recv(8192))
            player_scores[player] = score 
        except:
            break

        reply = pickle.dumps(score_rows + player_scores[0] + player_scores[1])
        
        try:
            conn.send(reply)
        except:
            break

        #receive and send next shapes 
        try:
            next_shape = pickle.loads(conn.recv(8192))
            player_next_shapes[player] = next_shape 
        except:
            break

        if player == 0:
            reply = pickle.dumps(player_next_shapes[1])
        elif player == 1:
            reply = pickle.dumps(player_next_shapes[0])
        
        try:
            conn.send(reply)
        except:
            break

    conn.close()

    print("Disconnected",addr)


def main():
    global currentPlayer

    #create shapes for players 
    player_shapes[0] = create_new_shape()
    player_shapes[1] = create_new_shape()

    player_shapes[0].y -= 1

    #create next shapes for players 
    player_next_shapes[0] = create_new_shape()
    player_next_shapes[1] = create_new_shape()

    #create socket
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #tell system to do not use socket after we close server
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #bind server to ip and to port
    try:
        sock.bind((ip,port))
    except socket.error as e:
        quit()

    #open port and take a queue of two client 
    sock.listen(2)

    print('Sever started.Waiting for a connection...')

    while True:

        #get connection with client
        try:
            conn, addr = sock.accept()
        except:
            print()
            print('Server closed.')
            quit()

        print("Connected to:",addr)

        #start new player thread 
        start_new_thread(threaded_client, (conn, currentPlayer,addr))

        currentPlayer += 1 

if __name__ == '__main__':
    main()
