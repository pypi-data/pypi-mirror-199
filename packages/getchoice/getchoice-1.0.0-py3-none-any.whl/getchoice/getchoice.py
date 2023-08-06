import sys
from enum import Enum, auto
from typing import Optional, TypeVar

from getkey import getkey, keys
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText


class PromptAction(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    SELECT = auto()


T = TypeVar("T")


class ChoicePrinter:
    def __init__(
        self,
        normal_style: str = "skyblue",
        selected_style: str = "red bold",
        title_style: str = "skyblue bold underline",
        pointer: str = "*",
        show_numbers: bool = False,
    ) -> None:
        self.normal_style = normal_style
        self.selected_style = selected_style
        self.title_style = title_style
        self.pointer = pointer
        self.show_numbers = show_numbers

    def read_key(self) -> PromptAction:
        key = getkey()

        if key in (keys.DOWN, keys.J):
            return PromptAction.DOWN

        if key in (keys.UP, keys.K):
            return PromptAction.UP

        if key in (keys.SPACE, keys.ENTER):
            return PromptAction.SELECT

        return PromptAction.NONE

    def clear_lines(self, count: int):
        sys.stdout.write(f"\x1b[{count}F")

        sys.stdout.write("\r")

        sys.stdout.write("\x1b[0J")

    def hide_cursor(self):
        print("\033[?25l", end="")

    def show_cursor(self):
        print("\033[?25h", end="")

    def print_choices(
        self, choices: list[str], selected: int, title: Optional[str] = None
    ):
        assert 0 <= selected < len(choices)

        if title is not None:
            title_text = FormattedText([(self.title_style, title)])
            print_formatted_text(title_text)

        for i, text in enumerate(choices):
            this_style = self.normal_style
            prefix = " " * len(self.pointer)

            if i == selected:
                this_style = self.selected_style
                prefix = self.pointer

            num = f"{i + 1: <2}" if self.show_numbers else ""

            text = FormattedText([(this_style, f"{prefix}{num}{text}")])
            print_formatted_text(text)

    def getchoice(
        self,
        options: list[tuple[str, T | str]],
        title: Optional[str] = None,
    ) -> tuple[int, T | str]:
        selected: int = 0
        self.hide_cursor()

        additional_lines = 0
        if title is not None:
            additional_lines = len(title.split("\n"))

        self.print_choices([o[0] for o in options], selected=selected, title=title)

        user_input = self.read_key()
        while True:
            match user_input:
                case PromptAction.UP:
                    selected = max(selected - 1, 0)

                case PromptAction.DOWN:
                    selected = min(len(options) - 1, selected + 1)

                case PromptAction.SELECT:
                    _, item = options[selected]
                    self.show_cursor()
                    return (selected, item)

                case _:
                    continue

            self.clear_lines(len(options) + additional_lines)
            self.print_choices([o[0] for o in options], selected=selected, title=title)

            user_input = self.read_key()
