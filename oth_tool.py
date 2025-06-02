#!/usr/bin/env python3

from blackboard import Blackboard

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('command')
parser.add_argument('-m', '--markdown', help='Save the blackboard to FILE', metavar='FILE', type=str)

args = parser.parse_args()

def main() -> None:
    if args.command in ('blackboard', 'black', 'bl', 'b'):
        blackboard = Blackboard('https://informatik-mathematik.oth-regensburg.de/schwarzes-brett')
        blackboard.scrape()

        if args.markdown != None:
            with open(args.markdown, 'w') as f:
                f.write(blackboard.to_markdown_str())
        else:
            print(blackboard)
    else:
        parser.exit(1,parser.format_help())

if __name__ == "__main__":
    main()
    #url = 'https://informatik-mathematik.oth-regensburg.de/schwarzes-brett'
    #blackboard = Blackboard(url)
    #blackboard.scrape()
    #print(blackboard)
