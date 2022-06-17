from typing import Callable, Final, NoReturn, Union
import sys


class Commands():
    def __init__(self, argv, /, *, user_input: list[str] = []) -> None:
        self._arg_stack = argv
        self._user_input = user_input

    def setInput(self, user_input: list[str]) -> None:
        self._user_input = user_input

    def getInput(self, idx: int = -1, /) -> Union[list[str], str]:
        if idx != -1:
            try:
                return self._user_input[idx]
            except KeyError:
                print(f"Invalid key from user input was caught '{idx}' from {self._user_input}", file=sys.stderr)
        return self._user_input

    def checkValid(self, command: str) -> bool:
        return True if command in self._COMMAND_LIST else False

    def runCommand(self, command: str):
        self._COMMAND_LIST.get(command, self.none)(self)

    def none(self) -> NoReturn:
        ...

    def help(self) -> None:
        """Shows this help"""
        print(f"""
Available commands:
    help      {self.help.__doc__}
    exit      exits the program
    push      {self.push.__doc__}
    pop       {self.pop.__doc__}
            """)

    def push(self):
        """Pushes the first argument to the argument stack"""
        print(self._user_input)
        self._arg_stack.extend(self._user_input)

    def pop(self, times: int = 1):
        """Pops the first argument from the argument stack"""
        if len(self._arg_stack) >= 1:
            for x in range(times):
                self._arg_stack.pop()

    _COMMAND_LIST: Final[dict[str, Callable]] = {
        "help": help,
        "pop": pop,
        "push": push
    }
    _user_input: list[str]
    _arg_stack: list[str] = []
