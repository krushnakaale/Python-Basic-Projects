"""Pure game rules, independent of the graphical interface."""
import random
from dataclasses import dataclass, field

CHOICES = ('Rock', 'Paper', 'Scissors')
BEATS = {'Rock': 'Scissors', 'Paper': 'Rock', 'Scissors': 'Paper'}


def decide(player, computer):
    if player not in CHOICES or computer not in CHOICES:
        raise ValueError('Invalid choice')
    if player == computer:
        return 'draw'
    return 'win' if BEATS[player] == computer else 'loss'


@dataclass
class Game:
    best_of: int = 3
    wins: int = 0
    losses: int = 0
    draws: int = 0
    history: list = field(default_factory=list)
    finished: bool = False

    @property
    def target(self):
        return self.best_of // 2 + 1

    def play(self, player, computer=None):
        if self.finished:
            raise RuntimeError('Match has finished')
        computer = computer if computer is not None else random.choice(CHOICES)
        result = decide(player, computer)
        if result == 'win':
            self.wins += 1
        elif result == 'loss':
            self.losses += 1
        else:
            self.draws += 1
        self.history.insert(0, {'player': player, 'computer': computer, 'result': result})
        self.finished = self.wins >= self.target or self.losses >= self.target
        return result, computer
