# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from typing import Literal, Optional, TypedDict, Union

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


def error(message: str) -> ParseError:
    return {"type": "error", "message": message}


def to_direction(word: str) -> Optional[Direction]:
    lower = word.lower()
    if lower in ("up", "down", "left", "right"):
        return lower
    return None


def to_steps(word: str) -> Optional[int]:
    if not word.isdecimal():
        return None
    steps = int(word)
    return steps if steps >= 1 else None


def parse_command(input: str) -> Union[Command, ParseError]:
    words = input.split()
    if len(words) == 0:
        return error("Empty command")

    name = words[0].lower()
    if name == "quit":
        return {"type": "quit"} if len(words) == 1 else error("quit takes no arguments")
    if name == "say":
        if len(words) < 2:
            return error("say needs a message")
        return {"type": "say", "message": " ".join(words[1:])}
    if name == "move":
        if len(words) != 3:
            return error("Usage: move <direction> <steps>")
        direction = to_direction(words[1])
        if direction is None:
            return error(f'Unknown direction "{words[1]}"')
        steps = to_steps(words[2])
        if steps is None:
            return error(f'Steps must be a whole number of at least 1, got "{words[2]}"')
        return {"type": "move", "direction": direction, "steps": steps}
    return error(f'Unknown command "{words[0]}"')
