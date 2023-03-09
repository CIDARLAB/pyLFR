import subprocess


def test():
    """
    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest discover`
    """
    subprocess.run(["pytest", "-vv", "tests"])


def format():
    """
    Runs black and isort
    """
    subprocess.run(["isort", "."])
    subprocess.run(["black", "lfr"])
