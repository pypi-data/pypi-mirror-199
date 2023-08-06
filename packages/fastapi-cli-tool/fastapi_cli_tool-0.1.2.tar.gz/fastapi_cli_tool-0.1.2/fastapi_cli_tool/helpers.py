import re
from typing import TypeVar

import questionary
import requests
import typer

EnumType = TypeVar("EnumType")


custom_style_fancy = questionary.Style(
    [
        ("qmark", "fg:#FDFF33 bold"),  # token in front of the question
        ("question", "fg:#33FFE9 bold"),  # question text
        ("answer", "fg:#01C100 bold"),  # submitted answer text behind the question
        ("pointer", "fg:#019E00 bold"),  # pointer used in select and checkbox prompts
        (
            "highlighted",
            "fg:#019E00 bold",
        ),  # pointed-at choice in select and checkbox prompts
        ("selected", "fg:#019E00"),  # style for a selected item of a checkbox
        ("separator", "fg:#cc5454"),  # separator in lists
        ("instruction", ""),  # user instructions for select, rawselect, checkbox
        ("text", ""),  # plain text
        (
            "disabled",
            "fg:#858585 italic",
        ),  # disabled choices for select and checkbox prompts
    ]
)


def camel_to_snake(text: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()


def question(question: str, choices: EnumType) -> questionary.Question:
    prompt = camel_to_snake(choices.__name__).replace("_", " ")  # type: ignore
    return questionary.select(question, choices=list(choices), style=custom_style_fancy)


def question_input(text: str, default: str = "") -> questionary.Question:
    return questionary.text(text, default=default, style=custom_style_fancy)


def binary_question(option: str) -> questionary.Question:
    return questionary.confirm(
        f"Do you want {option}?", default=False, style=custom_style_fancy
    )


def get_package_version(package_name) -> str:
    try:
        response = requests.get(f"https://pypi.python.org/pypi/{package_name}/json")
        data = response.json()
        return data["info"]["version"]
    except Exception as e:
        print(e)
        return "*"
