#!/usr/bin/env python3
from pathlib import Path
import argparse


SPECIAL_CHARACTERS = ["'", '"', "(", ",", ")", " ", "="]


def main():
    parser = argparse.ArgumentParser(
        description="This script takes the config parameters from "
        "settings.py and makes a .env with them."
    )
    parser.add_argument(
        "settings_path", help="Your path to settings.py from your root directory."
    )
    path = parser.parse_args().settings_path
    root_dir = Path(__file__).resolve()
    for i in range(0, 7):
        root_dir = root_dir.parent
    environment = read_settings(path, root_dir)
    write_file(environment, root_dir)


def write_file(environment, root_dir):
    file = open(f"{root_dir}/.env", "w")
    file.write(environment)


def read_settings(settings_file, root_dir):
    environment = ""
    file = open(f"{root_dir}/{settings_file}", "r")
    content = file.read()
    index = 0

    while index < len(content):
        current_word = get_word(index, content)
        if not current_word:
            break
        index += len(current_word)
        while content[index] in SPECIAL_CHARACTERS:
            index += 1
        if current_word not in ["config", "cast"]:
            continue
        parameter = get_word(index, content)
        if current_word == "config":
            environment += f"\n{parameter}" if len(environment) != 0 else f"{parameter}"
        else:
            if parameter == "Csv":
                parameter = "list"
            environment += f": {parameter}"
        while content[index] in SPECIAL_CHARACTERS:
            index += 1

    return environment


def get_word(current_character: int, content: str) -> str | None:
    word = ""
    if current_character == len(content) - 1:
        return None
    while (
        current_character < len(content) - 1
        and content[current_character] not in SPECIAL_CHARACTERS
    ):
        word += content[current_character]
        current_character += 1

    return word


main()
