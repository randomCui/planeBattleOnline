import pickle
import socket
import threading

from base.game import Game
from base.player import Player
from client.config import window_height


def client_thread(connection, game_id, player_id):
    player_attr = pickle.loads(connection.recv(2048))
    width = player_attr['size'][0]
    height = player_attr['size'][1]
    player = Player(100,
                    window_height - 100,
                    width,
                    height,
                    player_attr
                    )

    connection.send(pickle.dumps(
        (player_id, player)
    ))
    games[game_id].players[player_id] = player
    current_game = games[game_id]
    current_player = current_game.players[player_id]
    while True:
        try:
            data = pickle.loads(connection.recv(2048))
            current_player.set_pos(data['pos'])
            connection.send(pickle.dumps(current_game))
            if not data:
                break
        except Exception as e:
            print(e)

    print("Lost connection")
    try:
        del games[game_id]
        print("Closing Game", game_id)
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
    server = "localhost"
    port = 5561

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
        idCount += 1
        game_id = 'default'
        if game_id not in games:
            games[game_id] = Game(game_id)
        print("Creating a new game...")
        threading.Thread(target=client_thread, args=(conn, game_id, address[1])).start()
