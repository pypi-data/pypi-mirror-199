from argparse import ArgumentParser
from typing import Callable

def main():
    parser: ArgumentParser = create_parser()
    subparser = parser.add_subparsers(title="command", description="command description")
    cmd1 = subparser.add_parser("hello",help="Say hi.")
    cmd1.set_defaults(func=hello_world)
    cmd1.add_argument("-n", help="Type your name")
    args = parser.parse_args()
    args.func(vars(args))

def create_parser(parser: Callable=ArgumentParser):
    return parser({
            "prog": "how-to-cmd-line-tool",
            "description": "this is description",
    })

def hello_world(args):
    name = args.get("n")
    word = 'World!'
    if name is not None:
        word = word.replace('!', f', {name}!')
    print(word)

    
    