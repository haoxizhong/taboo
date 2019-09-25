import os
import logging
import argparse

from taboo.defender import TabooDefender
from taboo.util import END_CODE_SET

os.system("clear")
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--host', default="127.0.0.1", help="The host address of attacker.")
parser.add_argument('--port', default=10087, help="The port of defender.")
args = parser.parse_args()

defender = TabooDefender(args.host, int(args.port))


def initilization():
    pass


def guess():
    word_list = defender.begin_guessing()

    print("Type your selection (id, from 0 to %d): " % len(word_list))
    idx = int(input().strip())
    defender.guess_word(idx)


def defend():
    while True:
        data = defender.receive_msg()
        if data["code"] in END_CODE_SET:
            break
        print("Type your sentence (type [GUESS] to guess the word): ", end='')
        sent = input().strip()
        if sent == "[GUESS]":
            guess()
            break

        defender.defend(sent)


if __name__ == "__main__":
    initilization()
    defend()
