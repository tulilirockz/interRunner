#!/usr/bin/env python3
import subprocess
import sys
from rerun.cmd import Commands
from typing import Final, Literal, Sequence


def main(argv: list[str] = sys.argv, /) -> int:
    if len(argv) <= 1:
        print("No arguments were specified", file=sys.stderr)
        return 1
    argv.pop(0)  # Pops this program's path from this list

    # [MAIN] >> Optional![sub_command] [sub_arguments]
    SUB_COMMAND_INDEX: Literal[0] = 0
    # Basically just a singleton for all these thingies
    BORG: Final[Commands] = Commands(argv)

    while True:
        BORG.setInput(input("[ " + " ".join(argv) + " ]" + " >>> ").split(" "))
        INPUT_COPY: Sequence[str] = BORG.getInput()
        SUB_COMMAND: str = INPUT_COPY[SUB_COMMAND_INDEX]

        if "exit" in INPUT_COPY:
            return 0

        if not BORG.checkValid(SUB_COMMAND):
            BORG._arg_stack.extend(INPUT_COPY)
        else:
            BORG._user_input.pop(0)  # Pops the subcommand
            print(BORG._user_input, SUB_COMMAND)
            BORG.runCommand(SUB_COMMAND)
            if len(INPUT_COPY):
                BORG._arg_stack.pop(SUB_COMMAND_INDEX)
            continue

        try:
            subprocess.run(BORG._arg_stack)
        except FileNotFoundError as e:
            print(f"ERROR: Command not found!\n{e}")

        # Pop everything that the user inputted
        BORG.pop(len(INPUT_COPY))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
