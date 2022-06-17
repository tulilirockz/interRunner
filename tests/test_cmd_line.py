from rerun.cmd_line import Commands
from typing import Callable, TypeVar, Union
import pytest


@pytest.mark.parametrize("test_input,expected", [
    ('amongus', '*** Unknown syntax: amongus\n'),
    ('aaaaaaaaaa', '*** Unknown syntax: aaaaaaaaaa\n'),
    ('', ''),
])
def test_cmderr(capsys, test_input, expected):
    c = Commands()
    c.onecmd(test_input)
    err = capsys.readouterr()[1]
    assert err == expected


@pytest.mark.parametrize("test_stack,times,expected_stack", [
    (["echo"], 1, []),
    (["echo", 'hello', 'world'], '1', ['echo', 'hello']),
    (["echo", 'hello', 'world'], '3', []),
])
def test_cmdpop(test_stack: list[str], times: Union[str, int], expected_stack: list[str]) -> None:
    c = Commands()
    c.setArgv(test_stack)
    c.do_pop(times)
    assert c._arg_stack == expected_stack


def test_cmdpop_except(capsys) -> None:
    c = Commands()
    c.setArgv(["echo", "hello", "world"])
    c.do_pop("hi")
    assert capsys.readouterr()[1] == "hi could not be interpreted as a number\n"


@pytest.mark.parametrize("test_stack, additional_str, expected_stack", [
    (['echo hello'], 'world', ['echo hello', 'world']),
    (['echo'], 'hello world', ['echo', 'hello', 'world']),
    (['echo'], 'hiihhi hi hi hi', ['echo', 'hiihhi', 'hi', 'hi', 'hi']),
]
)
def test_cmdpush(test_stack: list[str], additional_str: str, expected_stack: list[str]) -> None:
    c = Commands()
    c.setArgv(test_stack)
    c.do_push(additional_str)
    assert c._arg_stack == expected_stack


def test_prompt() -> None:
    c = Commands()
    c.setArgv(["echo", "hello", "world"])
    c.prompt = "[ " + " ".join(["echo", "hello", 'world']) + " ]" + " >>> "
    c.onecmd("pop 2")
    c.postcmd(False, '')
    assert c.prompt == "[ echo ] >>> "
    c.onecmd("push hihi hi")
    c.postcmd(False, '')
    assert c.prompt == "[ echo hihi hi ] >>> "
    c.onecmd("pop")
    c.postcmd(False, '')
    assert c.prompt == "[ echo hihi ] >>> "


def test_exit() -> None:
    with pytest.raises(SystemExit):
        Commands().do_exit("")

    with pytest.raises(SystemExit):
        Commands().do_EOF("")
