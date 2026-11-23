"""Pure, testable number guessing game logic."""
import random

LEVELS = {"Easy": (1, 50, 10), "Medium": (1, 100, 8), "Hard": (1, 200, 7)}

class GuessingGame:
    def __init__(self, level="Easy", secret=None):
        self.reset(level, secret)

    def reset(self, level="Easy", secret=None):
        if level not in LEVELS:
            raise ValueError("Unknown difficulty")
        self.level = level
        self.low, self.high, self.max_attempts = LEVELS[level]
        if secret is not None and not self.low <= secret <= self.high:
            raise ValueError("Secret outside range")
        self.secret = secret if secret is not None else random.randint(self.low, self.high)
        self.attempts = 0
        self.finished = False
        self.won = False

    @property
    def remaining(self):
        return self.max_attempts - self.attempts

    def guess(self, value):
        if self.finished:
            return "Game over. Start a new game."
        try:
            number = int(value.strip())
        except (ValueError, AttributeError):
            return "Enter a whole number."
        if not self.low <= number <= self.high:
            return f"Enter a number from {self.low} to {self.high}."
        self.attempts += 1
        if number == self.secret:
            self.finished = self.won = True
            unit = "guess" if self.attempts == 1 else "guesses"
            return f"Correct! You won in {self.attempts} {unit}."
        if self.remaining == 0:
            self.finished = True
            return f"No attempts left. The number was {self.secret}."
        return f"Try higher! ({self.remaining} left)" if number < self.secret else f"Try lower! ({self.remaining} left)"

    def score(self):
        return self.remaining * 10 + 20 if self.won else 0
