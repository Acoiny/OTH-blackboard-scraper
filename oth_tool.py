#!/usr/bin/env python3

from blackboard import Blackboard
from mensaplan import Mensaplan

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('command')
parser.add_argument('-m', '--markdown', help='Save the blackboard to FILE', metavar='FILE', type=str)
parser.add_argument('-d', '--weekday', help='Only retrieves plan of DAY (mensaplan only)', metavar='DAY', type=str)
parser.add_argument('-w', '--calendar_week', help='Retrieves plan for calendar week WEEK (mensaplan only)', metavar='WEEK', type=int)

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
    elif args.command in ('mensaplan', 'mensa', 'me', 'm'):
        mensa = None
        if args.calendar_week:
            mensa = Mensaplan(args.calendar_week)
        else:
            mensa = Mensaplan()
        mensa.get()

        if args.markdown != None:
            with open(args.markdown, 'w') as f:
                f.write(mensa.to_markdown_str())
        else:
            if args.weekday != None:
                day = args.weekday.lower()
                if day in ('monday', 'montag', 'mo', 'm'):
                    print(mensa.stringify_day(0))
                elif day in ('tuesday', 'dienstag', 'tu', 'di'):
                    print(mensa.stringify_day(1))
                elif day in ('wednesday', 'mittwoch', 'wed', 'mi', 'w', 'm'):
                    print(mensa.stringify_day(2))
                elif day in ('thursday', 'donnerstag', 'th', 'do'):
                    print(mensa.stringify_day(3))
                elif day in ('friday', 'freitag', 'fr', 'f'):
                    print(mensa.stringify_day(4))
                else:
                    parser.exit(1, f'Invalid weekday "{args.weekday}"')
            else:
                print(mensa)
    else:
        parser.exit(1,parser.format_help())

if __name__ == "__main__":
    main()
    #url = 'https://informatik-mathematik.oth-regensburg.de/schwarzes-brett'
    #blackboard = Blackboard(url)
    #blackboard.scrape()
    #print(blackboard)
