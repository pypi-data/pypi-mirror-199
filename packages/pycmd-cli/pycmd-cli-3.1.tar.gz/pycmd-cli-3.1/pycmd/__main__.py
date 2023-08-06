# Command Handler
# This is the main script which handles all of the commands

import os
import sys
from pycmd.utils.pycmd import autocorrect
import msvcrt
import json
from colorama import Fore as fc, init
init(autoreset=True)

os.chdir(os.path.abspath(__file__ + "/../"))


def argparse(args: list):
    function = args[1] if not args[1].startswith("-") else ""
    parameter = ""
    flags = []
    for i in args[1:]:
        if i.startswith("--"):
            flags.append(i[1:])
        elif i.startswith("-"):
            flags.append(i)
        else:
            parameter = i if i != function else "."
        args.pop(args.index(i))

    return function, parameter, flags


def help(command: str):
    commands = open(f"json/commands.json", "r")
    commands = json.load(commands)
    for i in commands:

        if i["name"] == command:

            if "description" in i:
                print(" " * (2) + f'\n{fc.YELLOW}{i["description"]}\n')

            if "usage" in i:
                print(
                    " " * (2)
                    + f"{fc.GREEN}Usage:"
                    + " " * (15 - len("Usage:"))
                    + f'{fc.RESET}{i["usage"]}'
                )
            if "parameters" in i:
                print(
                    " " * (2)
                    + f"{fc.GREEN}Parameters:"
                    + " " * (15 - len("Parameters:"))
                    + f'{fc.RESET}{", ".join(i["parameters"])}'
                )
            if "flags" in i:
                print(
                    " " * (2)
                    + f"{fc.GREEN}Flags:"
                    + " " * (15 - len("Flags:"))
                    + f'{fc.RESET}{i["flags"]}'
                )
            if "example" in i:
                print(
                    " " * (2)
                    + f"{fc.GREEN}Example:"
                    + " " * (15 - len("Example:"))
                    + f'{fc.RESET}{i["example"]}'
                )


def execute(command: str, parameter: str, flags: list):

    if not command:
        os.system("python commands/help.py help " + " ".join(flags))
        return

    elif "-help" in flags or "-h" in flags:
        help(command)
        return

    elif command == "help":
        if parameter != ".":
            help(parameter)
        else:
            os.system("python commands/help.py")
        return

    if os.path.exists(f"commands/{command}.py"):
        os.system(f'python commands/{command}.py {parameter} {" ".join(flags)}')
        return

    else:
        corrected = autocorrect(command, os.listdir("commands"), 0.4)
        if corrected:
            # Removes the .py extension
            corrected = corrected[:-3]
            print(
                f'\nCommand {fc.LIGHTBLACK_EX}"{command}{fc.LIGHTBLACK_EX}"{fc.RESET} not found.\nDid you mean {fc.LIGHTBLACK_EX}"{fc.CYAN}{corrected}{fc.RESET}{fc.LIGHTBLACK_EX}"{fc.RESET}?'
            )
            print(
                f"{fc.LIGHTBLACK_EX}[{fc.GREEN}Y{fc.LIGHTBLACK_EX}/{fc.BLUE}n{fc.LIGHTBLACK_EX}]",
                end="\r",
            )
            response = msvcrt.getch()
            if response.lower() == b"y":
                print(fc.LIGHTGREEN_EX + "Yes  \n")
                execute(corrected, parameter, flags)
            else:
                print(f"Run {fc.CYAN}pycmd help{fc.RESET} for list of commands.")
        else:
            print(
                f'\nCommand {fc.LIGHTBLACK_EX}"{command}{fc.LIGHTBLACK_EX}"{fc.RESET} not found.'
            )
            print(f"Run {fc.CYAN}pycmd help{fc.RESET} for list of commands.")

        return


def main():

    if len(sys.argv) > 1:
        function, parameter, flags = argparse(sys.argv)
        try:
            execute(function, parameter, flags)
        except KeyboardInterrupt:
            pass

    else:
        os.system("python commands/help.py")