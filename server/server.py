import socket
import threading
import pickle
from game import Game
from base.player import Player
from client.config import window_width,window_height


def client_thread(connection, game_id):
    global idCount
    player_attr = pickle.loads(connection.recv(2048*10))
    width=player_attr['size'][0]
    height = player_attr['size'][1]
    player = Player(100,
                    window_height-100,
                    width,
                    height,
                    player_attr
                    )
    connection.sendall(pickle.dumps(player))
    reply = []
    while True:
        try:
            data = pickle.loads(connection.recv(2048*10))
            if game_id in games:
                game = games[game_id]
            else:
                break

            if not data:
                break
            else:
                if data == "reset":
                    game.resetWent()
                elif data != "get":
                    game.play(player_id, data)

                connection.sendall(pickle.dumps(game))

        except:
            break

    print("Lost connection")
    try:
        del games[game_id]
        print("Closing Game", game_id)
    except:
        pass
    idCount -= 1
    connection.close()


def init_server(server, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)
    s.listen(3)
    return s


if __name__=='__main__':
    server = "localhost"
    port = 5556

    s = init_server(server,port)
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
        game_id = 1
        games[game_id] = Game(game_id)
        print("Creating a new game...")
        threading.Thread(target=client_thread,args=(conn,game_id)).start()