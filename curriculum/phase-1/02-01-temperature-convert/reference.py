# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import math


def celsius_to_fahrenheit(celsius: float) -> float:
    return math.floor((celsius * 9 / 5 + 32) * 10 + 0.5) / 10


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return math.floor((fahrenheit - 32) * 5 / 9 * 10 + 0.5) / 10
