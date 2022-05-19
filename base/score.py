import csv
import os.path
import datetime

csv_path = os.path.join('..', 'leader_board.csv')


def add_score(player):
    with open(csv_path, 'a') as fd:
        waiter = csv.writer(fd)
        row = [player.nickname, player.score, datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")]
        waiter.writerow(row)


def read_leader_board():
    data = []
    with open(csv_path, 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            data.append(row)
    return data


def rank(score):
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
