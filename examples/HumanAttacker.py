import os
import logging
import argparse

from taboo.attacker import TabooAttacker
from taboo.util import END_CODE_SET

os.system("clear")
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--host', default="127.0.0.1", help="The host address of attacker.")
parser.add_argument('--port', default=10086, help="The port of attacker.")
args = parser.parse_args()

attacker = TabooAttacker(args.host, int(args.port))


def initilization():
    pass


def select_word(word_list):
    print("Type your selection (id, from 0 to %d): " % len(word_list))
    idx = int(input().strip())
    attacker.select_word(idx)


def attack():
    while True:
        print("Type your sentence: ", end='')
        sent = input().strip()
        data = attacker.attack(sent)

        if data["code"] in END_CODE_SET:
            break


if __name__ == "__main__":
    initilization()
    select_word(attacker.word_list)
    attack()
