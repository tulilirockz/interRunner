import pytest
import rerun.cmd_line


@pytest.fixture(scope="session")
def cmd_instance():
    return rerun.cmd_line.Commands()
