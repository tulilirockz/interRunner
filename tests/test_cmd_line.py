from typing import Union, List
import pytest


@pytest.mark.parametrize("test_input,expected", [
    ("CRITICAL", 50),
    ("ERROR", 40),
    ("WARNING", 30),
    ("INFO", 20),
    ("DEBUG", 10),
    ("NOTSET", 0),
    ("amongus", 100),
    ("", 100),
    (10, 10),
    (20, 20),
    (3, 3),
])
def test_verbosity(cmd_instance, test_input, expected):
    cmd_instance.setVerbosity(test_input)
    assert cmd_instance._verbosity == expected


@pytest.mark.parametrize("test_input,expected", [
    ('amongus', 'amongus is not a valid command\n'),
    ('aaaaaaaaaa', 'aaaaaaaaaa is not a valid command\n'),
    ('', 'aaaaaaaaaa is not a valid command\n'),
])
def test_cmderr(capsys, cmd_instance, test_input, expected):
    cmd_instance.setVerbosity("NOTSET").setLogOnly(False) \
        .onecmd(test_input)
    out, err = capsys.readouterr()
    assert out == ""
    assert err == expected


@ pytest.mark.parametrize("test_stack,times,expected_stack", [
    (["echo"], 1, []),
    (["echo", 'hello', 'world'], '1', ['echo', 'hello']),
    (["echo", 'hello', 'world'], '3', []),
])
def test_cmdpop(cmd_instance, test_stack: List[str], times: Union[str, int], expected_stack: List[str]) -> None:
    cmd_instance.setArgv(test_stack) \
        .do_pop(times)
    assert cmd_instance._arg_stack == expected_stack


def test_cmdpop_except(capsys, cmd_instance) -> None:
    cmd_instance.setArgv(["echo", "hello", "world"]) \
        .do_pop("hi")
    assert capsys.readouterr()[1] == "hi could not be interpreted as a number\n"


@ pytest.mark.parametrize("test_stack, additional_str, expected_stack", [
    (['echo hello'], 'world', ['echo hello', 'world']),
    (['echo'], 'hello world', ['echo', 'hello', 'world']),
    (['echo'], 'hiihhi hi hi hi', ['echo', 'hiihhi', 'hi', 'hi', 'hi']),
]
)
def test_cmdpush(cmd_instance, test_stack: List[str], additional_str: str, expected_stack: List[str]) -> None:
    cmd_instance.setArgv(test_stack) \
        .do_push(additional_str)
    assert cmd_instance._arg_stack == expected_stack


def test_prompt(cmd_instance) -> None:
    cmd_instance.setLogOnly(True)
    cmd_instance.setArgv(["echo", "hello", "world"])
    cmd_instance.prompt = "[ " + " ".join(["echo", "hello", 'world']) + " ]" + " >>> "
    cmd_instance.onecmd("pop 2")
    cmd_instance.postcmd(False, '')
    assert cmd_instance.prompt == "[ echo ] >>> "
    cmd_instance.onecmd("push hihi hi")
    cmd_instance.postcmd(False, '')
    assert cmd_instance.prompt == "[ echo hihi hi ] >>> "
    cmd_instance.onecmd("pop")
    cmd_instance.postcmd(False, '')
    assert cmd_instance.prompt == "[ echo hihi ] >>> "


def test_exit(cmd_instance) -> None:
    with pytest.raises(SystemExit):
        cmd_instance.do_exit("")

    with pytest.raises(SystemExit):
        cmd_instance.do_EOF("")
