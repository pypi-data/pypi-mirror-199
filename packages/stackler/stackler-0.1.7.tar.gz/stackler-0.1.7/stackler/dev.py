"""
Dev utils for Stackler
"""

import os
import sys
import subprocess
from uuid import uuid4
import typer
from git import Repo
from termcolor import colored

REPO_PATH = os.getcwd()

app = typer.Typer()


@app.command()
def generate_commits(count: int = 3):
    """Generates commits by count."""
    repo = Repo(REPO_PATH)
    for i in range(1, count + 1):
        path = get_path_with_idx(i)
        write_file(path, i)
        repo.git.add(path)
        repo.index.commit(f"commit {i}/{count}")


@app.command()
def simulate_output(exit_code: int = 0):
    """Simulates two outputs, one goes to stdout, the other goes to stderr"""
    regular_output = """stdout:
    line 1
    line 2
    """
    error_ouput = """stderr:
    line 1
    line 2
    """
    print(regular_output)
    print(colored(error_ouput, 'red'), file=sys.stderr)
    sys.exit(exit_code)


@app.command()
def popen_test():
    """Test popen"""
    p = subprocess.Popen("vim")
    print(p.poll())
    return p


def get_path_with_idx(idx: int) -> str:
    """Get the new file path by index"""
    return fr"{REPO_PATH}/{str(uuid4())[:8]}_test_file_{idx}.txt"


def write_file(path: str, idx: int):
    """Write file by index"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"test file {idx}")


if __name__ == "__main__":
    app()
