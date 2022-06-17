from typing import Optional, Union
from cmd import Cmd
# import subprocess
# import logging
import sys


class Commands(Cmd):
    def setArgv(self, argv: list[str]) -> None:
        self._arg_stack = argv

    def postcmd(self, stop: bool, line: str) -> bool:
        self.prompt = "[ " + " ".join(self._arg_stack) + " ]" + " >>> "
        # logging.log(logging.INFO, self.cmdqueue)
        return super().postcmd(stop, line)

    def default(self, line: str) -> None:
        return print(f"*** Unknown syntax: {line}", file=sys.stderr)

    @staticmethod
    def do_EOF(arg: Optional[str]) -> int:
        "Exits the program"
        raise SystemExit()

    @staticmethod
    def do_exit(arg: Optional[str]) -> int:
        "Exits the program"
        raise SystemExit()

    def do_help(self, arg: str) -> bool | None:
        """Shows this help"""
        return super().do_help(arg)

    def do_push(self, arg: str) -> None:
        """Pushes the first argument to the argument stack"""
        self._arg_stack.extend(arg.split(" "))

    def do_pop(self, arg: Union[str, int]) -> int | None:
        """Pops the first argument from the argument stack"""
        times: int = 1
        try:
            if arg:
                times = int(arg)
        except ValueError:
            print(f"{arg} could not be interpreted as a number", file=sys.stderr)

        if len(self._arg_stack) >= 1:
            for _ in range(times):
                self._arg_stack.pop()
        return None

    _arg_stack: list[str] = []
