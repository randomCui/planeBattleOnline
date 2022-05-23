import pickle
import socket
import threading
import time

from base.config import window_height, ip, port
from base.game import Game
from base.player import Player2, Player3


def client_thread(connection, game_id, player_id, game_state):
    if game_state[game_id] != 'running':
        game_state[game_id] = 'running'

    player_attr = pickle.loads(connection.recv(2048 * 10))
    player_attr['basic_setting']['x'] = 100
    player_attr['basic_setting']['y'] = window_height - 100
    if player_attr['basic_setting']['texture_name'] == 'YELLOW_SPACE_SHIP':
        player = Player2(basic_setting=player_attr['basic_setting'],
                         inertia_setting=player_attr['inertia_setting'],
                         plane_setting=player_attr['plane_setting'],
                         player_setting=player_attr['player_setting'],
                         )
    elif player_attr['basic_setting']['texture_name'] == 'BLUE_SPACE_SHIP':
        player = Player3(basic_setting=player_attr['basic_setting'],
                         inertia_setting=player_attr['inertia_setting'],
                         plane_setting=player_attr['plane_setting'],
                         player_setting=player_attr['player_setting'],
                         )
    connection.send(pickle.dumps(
        (player_id, player)
    ))

    game_semaphore[game_id].acquire()
    games[game_id].players[player_id] = player
    game_semaphore[game_id].release()

    current_game = games[game_id]
    current_player = current_game.players[player_id]
    while True:
        try:
            data = pickle.loads(connection.recv(2048 * 10))
            if current_player.state != 'dead':
                current_player.set_pos(data['pos'])

                if data['bullet'] is not None:
                    current_player.want_to_shoot = data['bullet']
                if current_game.pause_owner == '' or current_game.pause_owner == player_id:
                    if data['pause']:
                        current_game.pause_owner = player_id
                        current_game.state = 'pause'
                        game_state[game_id] = 'idle'
                    else:
                        current_game.state = 'running'
                        game_state[game_id] = 'running'
                        current_game.pause_owner = ''

                if data['restart'] == True:
                    games[game_id] = Game(game_id)

            all_dead = True
            for id, player in current_game.players.items():
                if player.state == 'alive':
                    all_dead = False
                    break
            if all_dead:
                current_game.state = 'lose'

            connection.send(pickle.dumps(current_game))
            if not data:
                break
        except EOFError as end:
            game_semaphore[game_id].acquire()
            del current_game.players[player_id]
            game_semaphore[game_id].release()
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
            game_semaphore[game_id].acquire()
            games[game_id].update()
            # time.sleep(0.005)
            game_semaphore[game_id].release()
        elif game_state[game_id] == 'idle':
            games[game_id].recover_from_pause = True
            time.sleep(0.2)
        elif game_state[game_id] == 'win' or game_state[game_id] == 'lose':
            time.sleep(1)
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
            game_semaphore[game_id] = threading.Semaphore(1)
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
    game_semaphore = {}

    listen_thread = threading.Thread(target=acceptation_thread)
    listen_thread.setDaemon(True)
    listen_thread.start()

    time.sleep(0.3)
    while True:
        if input('>> ') == 'q':
            break
