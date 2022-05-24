import csv
import datetime
import os.path

csv_path = os.path.join('..', 'leader_board.csv')


def add_score(player):
    """
    将对应的玩家成绩添加到积分榜中

    :param player: 胜利的游戏玩家
    :return:
    """
    with open(csv_path, 'a') as fd:
        waiter = csv.writer(fd)
        row = [player.nickname, player.game_score, datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")]
        waiter.writerow(row)


def read_leader_board() -> list:
    """
    读取游戏积分榜

    :return: 返回保存排行榜所有玩家的列表
    """
    data = []
    with open(csv_path, 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            data.append(row)
    return data


def rank(score):
    """
    返回给定的分数在积分榜中的排名

    :param score: 给定的分数
    :return: 排名
    """
    data = []
    with open(csv_path, 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            data.append(row)
    score_list = []
    for row in data:
        score_list.append(row)
    score_list.sort(reverse=True)
    counter = 0
    for old_score in score_list:
        counter += 1
        if old_score < score:
            return counter

    return len(score_list) + 1
