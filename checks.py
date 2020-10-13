from __future__ import annotations

import sys
from argparse import ArgumentParser
from subprocess import CalledProcessError, check_output
from typing import List

IGNORE_PATHS: List[str] = [
    "./*/migrations",
]


def filter_files(find_command: str) -> List[str]:
    """
    Execute the `find_command` filtering the paths from `IGNORE_PATHS`

    Args:
        find_command (str): Command to find files

    Returns:
        List[str]: All files found
    """

    if IGNORE_PATHS:
        find_command = "{find} | grep -vE '{additional}'".format(
            find=find_command, additional="' | grep -v '".join(IGNORE_PATHS)
        )

    print(f"Finding files with the following command:  {find_command}")

    output: str = check_output(find_command, shell=True).decode(sys.stdout.encoding)
    files: List[str] = [str(path) for path in output.split("\n") if path]

    return files


def find_files_all() -> List[str]:
    """
    Find all the python files in the repository.

    Will filter out the paths present at `IGNORE_PATHS`.

    Returns:
        List[str]: Paths to the python files in the repository
    """

    find_command = "find . | grep '.py$'"
    return filter_files(find_command)


def find_files_since_commit(commit: str) -> List[str]:
    """
    Find all the python files in the repository modified since the `commit`.

    Will filter out the paths present at `IGNORE_PATHS`.

    Returns:
        List[str]: Paths to the python files in the repository
    """
    find_command = f"git diff --name-only {commit} HEAD | grep '.py$'"

    try:
        return filter_files(find_command)

    except CalledProcessError:
        # If there is no diff, it returns status code 1
        return []


def type_checks(paths_to_check: List[str]) -> bool:
    """
    Run typing checks using mypy on the supplied list of files

    Args:
        paths (List[str]): List of paths to check with mypy

    Returns:
        bool: True if it failed the checks, False otherwise
    """
    from os import system

    if not paths_to_check:
        print("No files found to check")
        return True

    command = "mypy --strict {paths}".format(paths=" ".join(paths_to_check))

    print(f"Checking types with the following command:  {command}")
    result = system(command)
    return bool(result)


if __name__ == "__main__":

    argparser = ArgumentParser()
    argparser.add_argument(
        "--typing",
        default=False,
        action="store_true",
        help="Check typing across the repository",
    )
    argparser.add_argument(
        "--since",
        type=str,
        help="Check since this commit hash. See git diff for more information.",
    )
    args = argparser.parse_args()
    results: List[bool] = []

    if args.since:
        files = find_files_since_commit(args.since)
    else:
        files = find_files_all()

    if args.typing:
        results.append(type_checks(files))

    if any(results):
        exit(-1)
