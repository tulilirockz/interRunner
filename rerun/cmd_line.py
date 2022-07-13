import subprocess
import sys
import logging
from cmd import Cmd
from typing import Optional, Union, Final, Dict, List


class Commands(Cmd):
    def setVerbosity(self, verbosity: Union[str, int] = 100):
        LEVELS: Final[Dict[str, int]] = {
            'NOTSET': 0, 'DEBUG': 10,
            'INFO': 20, 'WARNING': 30,
            'ERROR': 40, 'CRITICAL': 50
        }

        try:
            verbosity = int(verbosity)
        except ValueError:
            None

        if type(verbosity) is str:
            self._verbosity = LEVELS.get(verbosity, 100)
            logging.getLogger().setLevel(self._verbosity)  # no logging by default
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
        fullstk: List[str] = []
        fullstk.extend(self._arg_stack)
        fullstk.extend(line.split(" "))
        if not self._log_only:
            try:
                subprocess.run(fullstk)
            except FileNotFoundError:
                if self._verbosity <= 50:
                    print(f"{line} is not a valid command", file=sys.stderr)
                else:
                    logging.critical(f"{line} is not a valid command")

    def do_EOF(self, arg: Optional[str]) -> None:
        "Exits the program"
        return self.do_exit(arg)

    @staticmethod
    def do_exit(arg: Optional[str]) -> None:
        "Exits the program"
        arg = None
        raise SystemExit(arg)

    def do_help(self, arg: str) -> Optional[bool]:
        """Shows this help"""
        return super().do_help(arg)

    def do_push(self, arg: str) -> None:
        """Pushes the first argument to the argument stack"""
        self._arg_stack.extend(arg.split(" "))

    def do_pop(self, arg: Union[str, int]) -> Optional[int]:
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

    logging.basicConfig(format="", stream=sys.stderr)
    _arg_stack: List[str] = []
    _verbosity: int = 0
    _log_only: bool = False
