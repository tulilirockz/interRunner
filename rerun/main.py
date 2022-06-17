#!/usr/bin/env python3
import sys
from rerun.cmd_line import Commands
from typing import Final
# Logging e Argparse!


def main(argv: list[str] = sys.argv, /) -> int:
    if len(argv) <= 1:
        print("No arguments were specified", file=sys.stderr)
        return 1
    argv.pop(0)  # Pops this program's path from this list

    CMD_LINE: Final[Commands] = Commands(completekey="tab")
    CMD_LINE.setArgv(argv)
    CMD_LINE.prompt = "[ " + " ".join(argv) + " ]" + " >>> "
    CMD_LINE.cmdloop("Rerun 1.0.0\nType help for more information, and exit or ^D for exiting.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
