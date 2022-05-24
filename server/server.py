import pickle
import socket
import threading
import time

from base.config import window_height, ip, port
from base.game import Game
from base.player import Player2, Player3


def client_thread(connection, game_id, player_id):
    """
    用于响应每个客户端的线程，线程工作就是接收客户端数据，再将每局游戏的状态返回客户端

    :param connection: 和客户端的连接
    :param game_id: 该客户端对应的游戏id
    :param player_id: 该玩家对应的id
    :return:
    """

    # 从客户端传来的玩家对象设置
    player_attr = pickle.loads(connection.recv(2048 * 10))
    # 初始化出生点
    player_attr['basic_setting']['x'] = 200
    player_attr['basic_setting']['y'] = window_height - 100

    # 根据传入的设置参数生成对应的飞机对象
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

    # 将初始化的游戏对象发送回客户端保存
    connection.send(pickle.dumps(
        (player_id, player)
    ))

    # 为了防止多个线程同时对字典进行修改导致程序崩溃，这里要使用到锁
    game_semaphore[game_id].acquire()
    # 将玩家对象加入到游戏中
    games[game_id].players[player_id] = player
    # 释放锁
    game_semaphore[game_id].release()

    # 初始化一些short cut，方便使用
    current_game = games[game_id]
    current_player = current_game.players[player_id]

    # 开始进行游戏接收响应循环
    while True:
        try:
            # 接收客户端发送过来的数据
            data = pickle.loads(connection.recv(2048 * 10))
            # 如果当前玩家还没有死，就响应他的操作
            if current_player.state != 'dead':
                # 改变对象位置
                current_player.set_pos(data['pos'])

                # 如果发射子弹控制信号不为空
                if data['bullet'] is not None:
                    # 设置Game对象中的玩家的发射状态为真，具体是否发射还需要看发射的冷却时间
                    current_player.want_to_shoot = data['bullet']
                # 下面处理暂停请求
                # 如果目前没有人提出暂停请求 或是 提出暂停的玩家需要取消暂停
                if current_game.pause_owner == '' or current_game.pause_owner == player_id:
                    # 如果是提出暂停
                    if data['pause']:
                        # 记录提出暂停的玩家id
                        current_game.pause_owner = player_id
                        # 设置游戏状态为暂停
                        current_game.state = 'pause'
                    else:
                        # 恢复游戏运行状态
                        current_game.state = 'running'
                        # 清空提出暂停的玩家记录
                        current_game.pause_owner = ''

            # 如果玩家提出重新开始
            if data['restart'] == True:
                # 首先防止其他线程在修改游戏数据时进入造成崩溃
                game_semaphore[game_id].acquire()
                # 直接重建一个新的Game对象
                games[game_id] = Game(game_id)
                # 重开也要暂停游戏
                games[game_id].state = 'pause'
                # 根据之前传入的数据重新生成一个新的对象
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
                # 将这个玩家对象重新加入游戏的玩家列表
                games[game_id].players[player_id] = player

                # 更新两个short cut
                current_player = games[game_id].players[player_id]
                current_game = games[game_id]

                # 释放锁
                game_semaphore[game_id].release()

            # 将本局游戏数据发送回客户端
            connection.send(pickle.dumps(current_game))

            # 如果回传的数据为空，就退出应答循环
            if not data:
                break
        # 如果客户端断开连接，就将其对应的游戏对象移除游戏，并且关闭连接
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
        # 如果本局游戏中已经没有玩家
        if len(current_game.players) == 0:
            # 将状态设置为stopped，提醒游戏更新线程退出
            games[game_id].state = 'stopped'
            print("Closing Game", game_id)
            print('there are %d games current running on the server' % (len(games)))
    except Exception as e:
        print(e)
    connection.close()


def game_thread(games, game_id):
    """
    游戏更新线程，用于不断更新本局游戏

    :param games: 游戏中所有的game对象
    :param game_id: 线程负责的游戏id
    :return:
    """
    while True:
        # 如果游戏状态为正常运行
        if games[game_id].state == 'running':
            game_semaphore[game_id].acquire()
            # 更新游戏状态
            games[game_id].update()
            # time.sleep(0.005)
            game_semaphore[game_id].release()
        # 如果游戏状态为暂停
        elif games[game_id].state == 'pause':
            # 设置一个标志位，用于之后从暂停恢复到运行状态的判断
            # 暂停状态下不更新游戏状态
            games[game_id].recover_from_pause = True
            time.sleep(0.2)
        # 如果游戏赢了或输了，那么就不更新游戏
        elif games[game_id].state == 'win' or games[game_id].state == 'lose':
            time.sleep(1)
        # 如果游戏已经停止运行，那么就将本局游戏从所有游戏中移除，并且停止负责本局游戏更新的线程
        elif games[game_id].state == 'stopped':
            del games[game_id]
            break


def init_server(server, port):
    """
    初始化服务器监听端口

    :param server: 服务器地址
    :param port: 服务器端口
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)
    s.listen(3)
    return s


def acceptation_thread():
    """
    初始化服务器的监听线程，负责分配每局游戏的更新线程，将不同的玩家分配到不同的游戏中

    :param server: 服务器地址
    :param port: 服务器端口
    :return:
    """
    # 保存应答线程的数组
    service_threading = []
    # 保存游戏更新线程的数组
    game_threading = []

    # 初始化服务器socket
    s = init_server(ip, port)
    print("Waiting for a connection, Server Started")
    global game_id
    while True:
        # 获取连接之后的连接和地址
        conn, address = s.accept()
        print("Connected to:", address)

        # 目前只是局域网联机，暂不考虑动态分配id的情况
        game_id = 'default'
        # 如果目前还没有本局游戏，那么就新建一个游戏对象
        if game_id not in games:
            # 新建游戏对象
            print("Creating a new game...")
            games[game_id] = Game(game_id)
            # 将游戏初始状态置为暂停
            games[game_id].state = 'pause'
            # 创建游戏对象锁
            game_semaphore[game_id] = threading.Semaphore(1)

            # 开始一个游戏更新线程
            temp = threading.Thread(target=game_thread, args=(games, game_id))
            temp.setDaemon(True)
            temp.start()
            game_threading.append(temp)

        # 将该晚间添加进游戏中
        print("Adding player %s in game %s" % (address[1], game_id))

        # 开始一个应答线程
        temp = threading.Thread(target=client_thread, args=(conn, game_id, address[1]))
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

    # 开始监听线程
    listen_thread = threading.Thread(target=acceptation_thread)
    listen_thread.setDaemon(True)
    listen_thread.start()

    time.sleep(0.3)
    # 保留一个输入，防止程序退出，并且提供一个能够安全退出的选项
    while True:
        if input('>> ') == 'q':
            break
