from copy import deepcopy
from os import system
from time import time
from game import game
import sys
from draws import unit_width
from pacman import Pacman


def run():
    start_matrix = list(map(lambda line: list(
        map(lambda x: int(x), line[:-1])), open("level.txt", "r")))
    results = []
    pacman = Pacman(
        1, 1, unit_width, deepcopy(start_matrix), {
            "width": len(start_matrix[0]),
            "height": len(start_matrix),
            "numTraining": 1000
        })
    for i in range(10000):
        toQuit, result, player = game(start_matrix, pacman)
        if toQuit:
            break

        log_file = open('./logs/'+str(player.general_record_time)+'-l-'+str(player.params['width'])+'-m-'+str(
            player.params['height'])+'-x-'+str(player.params['num_training'])+'.log', 'a')
        
        log_file.write("Iteration %4d: steps: %5d, total steps: %5d, time: %4f, reward (points): %12f, epsilon: %10f," %
                       (player.numeps, player.local_cnt, player.cnt, time()-player.s, player.ep_rew, player.params['eps']))
        log_file.write(" Q-parameter: %10f, winner: %r \n" % (
            (max(player.Q_global, default=float('nan')), result[1])))

        sys.stdout.write("Iteration %4d: steps: %5d, total steps: %5d, time: %4f, reward (points): %12f, epsilon: %10f," %
                       (player.numeps, player.local_cnt, player.cnt, time()-player.s, player.ep_rew, player.params['eps']))
        sys.stdout.write(" Q-parameter: %10f, winner: %r \n" % (
            (max(player.Q_global, default=float('nan')), result[1])))

        sys.stdout.flush()
        results.append(result)
        pacman.reset()

    scores = [result[0] for result in results]
    wins = [result[1] for result in results]
    win_rate = wins.count(True) / float(len(wins))
    print(('Average Score:', sum(scores) / float(len(scores))))
    print(('Scores:       ', ', '.join([str(score) for score in scores])))
    print(('Win Rate:      %d/%d (%.2f)' %
           (wins.count(True), len(wins), win_rate)))
    print(('Record:       ', ', '.join(
        [['Loss', 'Win'][int(w)] for w in wins])))


run()
