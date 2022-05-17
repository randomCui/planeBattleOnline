import pickle
import socket
import threading
import time

from base.config import window_height, ip, port
from base.game import Game
from base.player import Player


def client_thread(connection, game_id, player_id, game_state):
    if game_state[game_id] != 'running':
        game_state[game_id] = 'running'

    player_attr = pickle.loads(connection.recv(2048*10))
    player_attr['basic_setting']['x'] = 100
    player_attr['basic_setting']['y'] = window_height - 100
    player = Player(basic_setting=player_attr['basic_setting'],
                    inertia_setting=player_attr['inertia_setting'],
                    plane_setting=player_attr['plane_setting'],
                    player_setting=player_attr['player_setting'],
                    )

    connection.send(pickle.dumps(
        (player_id, player)
    ))
    games[game_id].players[player_id] = player
    current_game = games[game_id]
    current_player = current_game.players[player_id]
    while True:
        try:
            data = pickle.loads(connection.recv(2048 * 10))
            current_player.set_pos(data['pos'])
            if data['bullet'] is not None:
                current_player.want_to_shoot = data['bullet']
            connection.send(pickle.dumps(current_game))
            if not data:
                break
        except EOFError as end:
            del current_game.players[player_id]
            connection.close()
            break

        except Exception as e:
            raise e

    print("Lost connection")
    print("game %s has %d players" % (game_id, len(current_game.players)))
    print(current_game.players)

    try:
        if len(current_game.players) == 0:
            game_state[game_id] = 'stopped'
            del games[game_id]
            print("Closing Game", game_id)
            print('there are %d games current running on the server' % (len(games)))
    except Exception as e:
        print(e)
    connection.close()


def game_thread(game_state, games, game_id):
    while True:
        if game_state[game_id] == 'running':
            games[game_id].update()
            # time.sleep(0.005)
        elif game_state[game_id] == 'idle':
            time.sleep(0.1)
        elif game_state[game_id] == 'stopped':
            break


def init_server(server, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)
    s.listen(3)
    return s


def acceptation_thread():
    service_threading = []
    game_threading = []
    game_state = {}

    s = init_server(ip, port)
    print("Waiting for a connection, Server Started")
    global game_id
    while True:
        conn, address = s.accept()
        print("Connected to:", address)

        game_id = 'default'
        if game_id not in games:
            print("Creating a new game...")
            games[game_id] = Game(game_id)
            game_state[game_id] = 'idle'
            temp = threading.Thread(target=game_thread, args=(game_state, games, game_id))
            temp.setDaemon(True)
            temp.start()
            game_threading.append(temp)
        print("Adding player %s in game %s" % (address[1], game_id))

        temp = threading.Thread(target=client_thread, args=(conn, game_id, address[1], game_state))
        temp.setDaemon(True)
        temp.start()
        service_threading.append(temp)


if __name__ == '__main__':
    idCount = 0
    game_id = 0

    # 服务器的所有网络连接
    connected = set()

    # 服务器正在运行的所有游戏房间字典
    games = {}

    listen_thread = threading.Thread(target=acceptation_thread)
    listen_thread.setDaemon(True)
    listen_thread.start()

    time.sleep(0.3)
    while True:
        pass
        if input('>> ') == 'q':
            break
