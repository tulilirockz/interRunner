import contextlib
import subprocess
import sys
import logging
from cmd import Cmd
from typing import Mapping, NoReturn, Union, List


class Commands(Cmd):
    def setVerbosity(self, verbosity: Union[str, Union[int, float]] = 100):
        LEVELS: Mapping[str, int] = {
            'NOTSET': 0, 'DEBUG': 10,
            'INFO': 20, 'WARNING': 30,
            'ERROR': 40, 'CRITICAL': 50
        }

        with contextlib.suppress(ValueError):
            verbosity = int(verbosity)

        if type(verbosity) is str:
            self._verbosity = LEVELS.get(verbosity, 100)
        elif type(verbosity) is int:
            self._verbosity = verbosity

        logging.getLogger().setLevel(self._verbosity)
        logging.info(f"Logging level set to {self._verbosity}")
        return self

    def setArgv(self, argv: List[str]) -> "Commands":
        self._arg_stack = argv
        logging.debug(f"Set arguments: {argv}")
        return self

    def setLogOnly(self, FLAG: bool) -> "Commands":
        self._log_only = FLAG
        logging.debug(f"Set log only: {self._log_only}")
        return self

    def postcmd(self, stop: bool, line: str) -> bool:
        self.prompt = "[ " + " ".join(self._arg_stack) + " ]" + " >>> "
        return super().postcmd(stop, line)

    def default(self, line: str) -> None:
        if self._log_only:
            return
        fullstk: List[str] = []
        fullstk.extend(self._arg_stack)
        fullstk.extend(line.split(" "))

        try:
            subprocess.run(fullstk)
        except FileNotFoundError:
            if self._verbosity <= 50:
                print(f"{line} is not a valid command", file=sys.stderr)

    @staticmethod
    def do_EOF(arg: str = "") -> NoReturn:
        "Exits the program"
        raise SystemExit()

    @staticmethod
    def do_exit(arg: str = "") -> NoReturn:
        "Exits the program"
        raise SystemExit()

    def do_push(self, arg: str) -> None:
        """Pushes the first argument to the argument stack"""
        self._arg_stack.extend(arg.split(" "))

    def do_pop(self, arg: Union[str, int]) -> None:
        """Pops the first argument from the argument stack"""
        try:
            arg = int(arg)
        except ValueError:
            logging.info(f'"{arg}" could not be interpreted as a number')
            arg = 1

        if len(self._arg_stack) >= 1:
            with contextlib.suppress(IndexError):
                for _ in range(arg):
                    self._arg_stack.pop()

    logging.basicConfig(format="", stream=sys.stderr)
    _arg_stack: List[str] = []
    _verbosity: int = 0
    _log_only: bool = False
