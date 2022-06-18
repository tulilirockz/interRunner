#!/usr/bin/env python3
import sys
from rerun.cmd_line import Commands
from typing import Final, Optional
from argparse import ArgumentParser, Namespace


def split_args(args_list: list[str]) -> list[str]:
    total_list: list[str] = []
    for argstr in args_list:
        total_list.extend(argstr.split(" "))
    return total_list


def _arg_parser() -> ArgumentParser:
    PARSER: Final[ArgumentParser] = ArgumentParser(prog='rerun', allow_abbrev=True)

    PARSER.add_argument("argument_list",
                        metavar="ARG_LIST",
                        nargs="*",
                        help="Every argument supplied for rerunning")

    PARSER.add_argument("-l", "--log-only",
                        help="Doesn't execute any program, just logs everyting to stdout",
                        action="store_true")

    PARSER.add_argument('-v', '--verbosity',
                        help="Sets the verbosity level.\nAllowed verbosity levels are: CRITICAL (50), ERROR (40), WARNING (30), INFO (20), DEBUG(10) , NOTSET (0)",
                        default=100)

    return PARSER


def main(argv: Optional[list[str]] = sys.argv, /) -> int:
    PARSER: ArgumentParser = _arg_parser()
    ARGS: Final[Namespace] = PARSER.parse_args(argv)
    ARGS.argument_list.pop(0)  # Pops this program's path from this list
    ARGS.argument_list = split_args(ARGS.argument_list)
    if not ARGS.argument_list:
        PARSER.print_help()

    CMD_LINE: Final[Commands] = Commands(completekey="tab")
    CMD_LINE.prompt = "[ " + " ".join(ARGS.argument_list) + " ]" + " >>> "
    (
        CMD_LINE.setVerbosity(ARGS.verbosity)
                .setArgv(ARGS.argument_list)
                .setLogOnly(ARGS.log_only)
                .cmdloop("Rerun 1.0.0\nType help for more information, and exit or ^D for exiting.")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
