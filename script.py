import os
import csv
from time import time, sleep
from random import random, choice
from importlib import reload

import mathlib
import gate


def update():
    reload(mathlib)
    reload(gate)


def game(data):
    quoto = 100
    base = 0
    ts = 0
    change_hands = 0
    side = "buy"

    while True:
        try:
            close = float(data[ts][4])
        except IndexError:
            break

        if close == 0:
            pass
        else:
            if side == "buy":
                base = quoto / close * 0.998
                side = "sell"
            else:
                quoto = base * close * 0.998
                side = "buy"
                change_hands += 1

        ts += choice(range(100))

    return (quoto, change_hands)


def simulate(gi):
    quoto = []
    change_hands = []

    filename = choice(list(gi.db["klines"].keys()))
    data = gi.db["klines"][filename]

    for i in range(100):
        result = game(data)
        quoto.append(result[0])
        change_hands.append(result[1])

    print(
        "%-24s%-8.2f%-d"
        % (filename, sum(quoto) / len(quoto), sum(change_hands) / len(change_hands))
    )


def main(gi):

    while True:

        for i in gi.vf_klines.contents:
            if i not in gi.vf_klines.anchor.keys():
                gi.vf_klines.load_file(i)

        simulate(gi)
        sleep(0.5)
