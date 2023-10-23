import subprocess


def test():
    """
    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest discover`
    """
    subprocess.run(["pytest", "-vv", "tests"], check=True)


def format():
    """
    Runs black and isort
    """
    subprocess.run(["isort", "."], check=True)
    subprocess.run(["black", "lfr"], check=True)


def static_analysis():
    """
    Runs mypy and flake8
    """
    subprocess.run(["mypy", "lfr"], check=True)
