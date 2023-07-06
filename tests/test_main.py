"""Test cases for the maze module."""
import pytest
from click.testing import CliRunner

from ec_maze import maze


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(maze.main)
    assert result.exit_code == 0
