import os
import logging
import argparse
import pytorch_transformers

from taboo import judger, formatter, ruler, checker

os.system("clear")
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--attacker_host', default="127.0.0.1", help="The host address of attacker.")
    parser.add_argument('--attacker_port', default=10086, help="The port of attacker")
    parser.add_argument('--defender_host', default="127.0.0.1", help="The host address of defender.")
    parser.add_argument('--defender_port', default=10087, help="The port of defender")
    args = parser.parse_args()

    judger = judger.TabooJudger({}, args.attacker_host, int(args.attacker_port), args.defender_host,
                                int(args.defender_port))
    word_list = ["apple", "peach", "ubuntu", "windows", "hello", "what", "fuck"]
    judger.select_word(word_list)

    judger.play_game(checker.TabooEnglishChecker(), formatter.TabooStupidFormatter(), ruler.TabooStupidRuler(),
                     word_list)
