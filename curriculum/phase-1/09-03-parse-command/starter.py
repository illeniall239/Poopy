from typing import Literal, TypedDict, Union

Direction = Literal["up", "down", "left", "right"]


class Move(TypedDict):
    type: Literal["move"]
    direction: Direction
    steps: int


class Say(TypedDict):
    type: Literal["say"]
    message: str


class Quit(TypedDict):
    type: Literal["quit"]


class ParseError(TypedDict):
    type: Literal["error"]
    message: str


Command = Union[Move, Say, Quit]


def parse_command(input: str) -> Union[Command, ParseError]:
    """Parse "move <dir> <steps>", "say <words>" or "quit" into a command dict, or an error dict."""
    raise NotImplementedError
