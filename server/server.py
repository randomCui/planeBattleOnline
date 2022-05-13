import pickle
import socket
import threading
import pygame

import game_logic

from base.game import Game
from base.player import Player
from base.texture import Texture
from client.config import window_height, ip, port

t = Texture()


def client_thread(connection, game_id, player_id):

    player_attr = pickle.loads(connection.recv(2048))
    player_attr['basic_setting']['x'] = 100
    player_attr['basic_setting']['y'] = window_height - 100

    player = Player(basic_setting=player_attr['basic_setting'],
                    inertia_setting=player_attr['inertia_setting'],
                    plane_setting=player_attr['plane_setting'],
                    )

    connection.send(pickle.dumps(
        (player_id, player)
    ))
    games[game_id].players[player_id] = player
    current_game = games[game_id]
    current_player = current_game.players[player_id]
    while True:
        try:
            data = pickle.loads(connection.recv(2048*10))
            current_player.set_pos(data['pos'])
            current_game.update()
            connection.send(pickle.dumps(current_game))
            if not data:
                break
        except EOFError as end:
            del current_game.players[player_id]
            connection.close()
            break
        except Exception as e:
            print(e)

    print("Lost connection")
    print("game %s has %d players" % (game_id,len(current_game.players)))
    print(current_game.players)
    try:

        if len(current_game.players) == 0:
            del games[game_id]
            print("Closing Game", game_id)
            print('there are %d games current running on the server' % (len(games)))
    except Exception as e:
        print(e)
    connection.close()


def init_server(server, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)
    s.listen(3)
    return s


if __name__ == '__main__':
    server = ip
    port = port

    s = init_server(server, port)
    print("Waiting for a connection, Server Started")

    # 服务器的所有网络连接
    connected = set()

    # 服务器正在运行的所有游戏房间字典
    games = {}

    idCount = 0
    game_id = 0

    while True:
        conn, address = s.accept()
        print("Connected to:", address)

        game_id = 'default'
        if game_id not in games:
            games[game_id] = Game(game_id)
            print("Creating a new game...")
        print("Adding player %s in game %s" % (address[1], game_id))
        threading.Thread(target=client_thread, args=(conn, game_id, address[1])).start()
