"""Rock Paper Scissors: cross-platform Kivy application."""
import json
from pathlib import Path
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from game_logic import Game, CHOICES

BG = (0.965, 0.975, 0.99, 1)
WHITE = (1, 1, 1, 1)
NAVY = (0.10, 0.16, 0.27, 1)
MUTED = (0.39, 0.45, 0.55, 1)
BLUE = (0.18, 0.36, 0.82, 1)
PALE = (0.90, 0.93, 0.98, 1)
GREEN = (0.12, 0.55, 0.38, 1)
RED = (0.75, 0.25, 0.28, 1)


def label(text, size=16, color=NAVY, bold=False, height=36):
    return Label(text=text, font_size=dp(size), color=color, bold=bold,
                 size_hint_y=None, height=dp(height), halign='center', valign='middle',
                 text_size=(None, None))


def button(text, callback, bg=BLUE, height=54):
    b = Button(text=text, background_normal='', background_color=bg,
               color=WHITE if bg != PALE else NAVY, bold=True, font_size=dp(16),
               size_hint_y=None, height=dp(height))
    b.bind(on_release=callback)
    return b


class Card(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=dp(16), spacing=dp(8), **kwargs)
        with self.canvas.before:
            Color(*WHITE)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *_):
        self.rect.pos = self.pos
        self.rect.size = self.size


class RPSApp(App):
    title = 'Rock Paper Scissors'

    def build(self):
        Window.clearcolor = BG
        Window.size = (420, 760)
        self.game = Game()
        self.stats_path = Path(self.user_data_dir) / 'stats.json'
        self.stats = self.load_stats()

        root = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12))
        root.add_widget(label('ROCK  •  PAPER  •  SCISSORS', 19, NAVY, True, 46))
        root.add_widget(label('A classic game, thoughtfully simple.', 13, MUTED, False, 28))

        settings = Card(size_hint_y=None, height=dp(90))
        row = BoxLayout(spacing=dp(12))
        row.add_widget(label('Match format', 15, NAVY, True))
        self.format = Spinner(text='Best of 3', values=('Best of 3', 'Best of 5', 'Best of 7'),
                              size_hint=(0.52, None), height=dp(44))
        self.format.bind(text=self.change_format)
        row.add_widget(self.format)
        settings.add_widget(row)
        root.add_widget(settings)

        score = Card(size_hint_y=None, height=dp(128))
        score.add_widget(label('CURRENT MATCH', 12, MUTED, True, 25))
        self.score_label = label('YOU  0    :    0  COMPUTER', 21, NAVY, True, 52)
        score.add_widget(self.score_label)
        self.round_label = label('First to 2 wins', 13, MUTED, False, 24)
        score.add_widget(self.round_label)
        root.add_widget(score)

        actions = Card(size_hint_y=None, height=dp(160))
        actions.add_widget(label('MAKE YOUR MOVE', 13, MUTED, True, 28))
        move_row = BoxLayout(spacing=dp(9))
        for choice in CHOICES:
            move_row.add_widget(button(choice.upper(), lambda _, c=choice: self.play(c), BLUE))
        actions.add_widget(move_row)
        self.feedback = label('Choose Rock, Paper or Scissors to begin.', 13, MUTED, False, 42)
        actions.add_widget(self.feedback)
        root.add_widget(actions)

        history_card = Card()
        history_card.add_widget(label('RECENT ROUNDS', 13, MUTED, True, 30))
        scroll = ScrollView(do_scroll_x=False)
        self.history_box = BoxLayout(orientation='vertical', spacing=dp(3), size_hint_y=None)
        self.history_box.bind(minimum_height=self.history_box.setter('height'))
        scroll.add_widget(self.history_box)
        history_card.add_widget(scroll)
        root.add_widget(history_card)

        self.total_label = label('', 12, MUTED, False, 28)
        root.add_widget(self.total_label)
        root.add_widget(button('NEW MATCH', self.new_match, PALE, 48))
        self.refresh()
        return root

    def load_stats(self):
        try:
            data = json.loads(self.stats_path.read_text(encoding='utf-8'))
            return {k: max(0, int(data.get(k, 0))) for k in ('won', 'lost')}
        except (OSError, ValueError, TypeError):
            return {'won': 0, 'lost': 0}

    def save_stats(self):
        try:
            self.stats_path.parent.mkdir(parents=True, exist_ok=True)
            self.stats_path.write_text(json.dumps(self.stats), encoding='utf-8')
        except OSError:
            pass  # The game remains playable if storage is unavailable.

    def change_format(self, _, value):
        self.game = Game(best_of=int(value[-1]))
        self.refresh()

    def new_match(self, *_):
        self.game = Game(best_of=int(self.format.text[-1]))
        self.refresh()

    def play(self, choice):
        if self.game.finished:
            self.feedback.text = 'Match finished. Select NEW MATCH to play again.'
            return
        result, computer = self.game.play(choice)
        descriptions = {'win': 'You win this round!', 'loss': 'Computer wins this round!', 'draw': 'It is a draw!'}
        self.feedback.text = f'You: {choice}  |  Computer: {computer}\n{descriptions[result]}'
        if self.game.finished:
            player_won = self.game.wins >= self.game.target
            self.stats['won' if player_won else 'lost'] += 1
            self.save_stats()
            self.feedback.text = ('MATCH WON! Great game.' if player_won else 'MATCH LOST. Try again!')
        self.refresh(keep_feedback=True)

    def refresh(self, keep_feedback=False):
        g = self.game
        self.score_label.text = f'YOU  {g.wins}    :    {g.losses}  COMPUTER'
        self.round_label.text = f'First to {g.target} wins  •  {g.draws} draws'
        if not keep_feedback:
            self.feedback.text = 'Choose Rock, Paper or Scissors to begin.'
        self.history_box.clear_widgets()
        if not g.history:
            self.history_box.add_widget(label('No rounds played yet.', 13, MUTED, False, 34))
        for index, round_data in enumerate(g.history[:15], 1):
            r = round_data
            entry = f"{index:02}   {r['player']} vs {r['computer']}   •   {r['result'].upper()}"
            self.history_box.add_widget(label(entry, 13, NAVY, False, 32))
        self.total_label.text = f"Lifetime matches  •  Won: {self.stats['won']}  |  Lost: {self.stats['lost']}"


if __name__ == '__main__':
    RPSApp().run()
