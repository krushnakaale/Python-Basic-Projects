"""Professional, modern Kivy UI for the Number Guessing Game."""
import json
import os
from pathlib import Path

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from game_logic import GuessingGame, LEVELS

# Modern mobile / desktop window size & deep dark background
Window.size = (440, 720)
Window.clearcolor = (0.05, 0.07, 0.11, 1)


class ModernCard(BoxLayout):
    """Container card with rounded corners and subtle border."""
    def __init__(self, bg_color=(0.09, 0.12, 0.18, 1), border_color=(0.16, 0.22, 0.33, 1),
                 radius=14, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.border_color = border_color
        self.radius = radius
        with self.canvas.before:
            self.border_c = Color(*border_color)
            self.border_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(radius)])
            self.bg_c = Color(*bg_color)
            self.bg_rect = RoundedRectangle(
                pos=(self.x + dp(1), self.y + dp(1)),
                size=(max(0, self.width - dp(2)), max(0, self.height - dp(2))),
                radius=[dp(radius - 1)]
            )
        self.bind(pos=self._update_shape, size=self._update_shape)

    def _update_shape(self, *args):
        self.border_rect.pos = self.pos
        self.border_rect.size = self.size
        self.bg_rect.pos = (self.x + dp(1), self.y + dp(1))
        self.bg_rect.size = (max(0, self.width - dp(2)), max(0, self.height - dp(2)))

    def set_card_color(self, bg_color, border_color=None):
        self.bg_c.rgba = bg_color
        if border_color:
            self.border_c.rgba = border_color


class ModernButton(Button):
    """Styled rounded button with hover/press reaction."""
    def __init__(self, bg_color=(0.23, 0.51, 0.96, 1), radius=10, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.base_color = bg_color
        self.radius = radius
        with self.canvas.before:
            self.btn_color = Color(*bg_color)
            self.btn_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(radius)])
        self.bind(pos=self._update_rect, size=self._update_rect, state=self._on_state)

    def _update_rect(self, *args):
        self.btn_rect.pos = self.pos
        self.btn_rect.size = self.size

    def _on_state(self, instance, value):
        if value == "down":
            self.btn_color.rgba = [max(0, c * 0.8) for c in self.base_color[:3]] + [self.base_color[3]]
        else:
            self.btn_color.rgba = self.base_color

    def set_bg_color(self, color):
        self.base_color = color
        self.btn_color.rgba = color


class GuessApp(App):
    title = "Number Guessing Game"

    def build(self):
        self.game = GuessingGame()
        self.history = []
        self.stats_file = self.get_stats_file()
        self.stats = self.load_stats()

        # Main scroll view
        scroll = ScrollView(do_scroll_x=False, bar_width=dp(4), bar_color=(0.3, 0.4, 0.6, 0.6))

        # Root content layout
        root = BoxLayout(
            orientation="vertical",
            padding=[dp(18), dp(16), dp(18), dp(20)],
            spacing=dp(14),
            size_hint_y=None
        )
        root.bind(minimum_height=root.setter("height"))
        scroll.add_widget(root)

        # 1. Header Section
        header_box = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(64), spacing=dp(4))
        title_lbl = Label(
            text="[b]NUMBER GUESSING[/b]",
            markup=True,
            font_size="22sp",
            color=(0.95, 0.97, 1.0, 1),
            size_hint_y=None,
            height=dp(34)
        )
        subtitle_lbl = Label(
            text="Crack the secret code in minimum attempts",
            font_size="13sp",
            color=(0.58, 0.64, 0.74, 1),
            size_hint_y=None,
            height=dp(20)
        )
        header_box.add_widget(title_lbl)
        header_box.add_widget(subtitle_lbl)
        root.add_widget(header_box)

        # 2. Difficulty Segmented Selector Card
        diff_card = ModernCard(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(112),
            bg_color=(0.08, 0.11, 0.17, 1),
            border_color=(0.14, 0.20, 0.30, 1)
        )
        diff_card_header = BoxLayout(size_hint_y=None, height=dp(22))
        diff_title = Label(
            text="[b]SELECT DIFFICULTY[/b]",
            markup=True,
            font_size="12sp",
            color=(0.60, 0.68, 0.80, 1),
            halign="left",
            size_hint_x=0.5
        )
        diff_title.bind(size=diff_title.setter("text_size"))
        self.diff_info = Label(
            text="Range: 1 – 50 • 10 Tries",
            font_size="12sp",
            color=(0.38, 0.70, 0.98, 1),
            halign="right",
            size_hint_x=0.5
        )
        self.diff_info.bind(size=self.diff_info.setter("text_size"))
        diff_card_header.add_widget(diff_title)
        diff_card_header.add_widget(self.diff_info)
        diff_card.add_widget(diff_card_header)

        # Buttons row
        diff_btn_row = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(42))
        self.diff_buttons = {}
        for level in ["Easy", "Medium", "Hard"]:
            btn = ModernButton(
                text=level,
                font_size="14sp",
                bold=True,
                bg_color=(0.23, 0.51, 0.96, 1) if level == "Easy" else (0.12, 0.16, 0.24, 1),
                radius=8
            )
            btn.bind(on_press=lambda inst, lvl=level: self.select_level(lvl))
            self.diff_buttons[level] = btn
            diff_btn_row.add_widget(btn)
        diff_card.add_widget(diff_btn_row)
        root.add_widget(diff_card)

        # 3. Status & Clue Card
        self.clue_card = ModernCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(125),
            bg_color=(0.09, 0.14, 0.23, 1),
            border_color=(0.20, 0.32, 0.52, 1)
        )
        self.clue_title = Label(
            text="[b]READY TO PLAY[/b]",
            markup=True,
            font_size="13sp",
            color=(0.38, 0.70, 0.98, 1),
            size_hint_y=None,
            height=dp(20)
        )
        self.clue_message = Label(
            text="Make your first guess below!",
            markup=True,
            font_size="17sp",
            bold=True,
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(48)
        )
        self.clue_message.bind(size=self.clue_message.setter("text_size"))

        self.attempts_badge = Label(
            text="Attempts left: 10 of 10",
            font_size="13sp",
            color=(0.70, 0.78, 0.90, 1),
            size_hint_y=None,
            height=dp(22)
        )
        self.clue_card.add_widget(self.clue_title)
        self.clue_card.add_widget(self.clue_message)
        self.clue_card.add_widget(self.attempts_badge)
        root.add_widget(self.clue_card)

        # 4. Input & Guess Action Card
        input_card = ModernCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
            size_hint_y=None,
            height=dp(170),
            bg_color=(0.08, 0.11, 0.17, 1),
            border_color=(0.14, 0.20, 0.30, 1)
        )

        input_wrapper = BoxLayout(size_hint_y=None, height=dp(52))
        # Note: Do NOT set focus=True at constructor time!
        # Initializing with focus=False allows FocusBehavior to cleanly bind keyboard on window start.
        self.entry = TextInput(
            hint_text="Enter your guess...",
            multiline=False,
            text_validate_unfocus=False,
            input_filter="int",
            font_size="22sp",
            halign="center",
            size_hint_y=None,
            height=dp(52),
            background_color=(0.14, 0.18, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.50, 0.58, 0.70, 1),
            cursor_color=(0.38, 0.70, 0.98, 1)
        )
        self.entry.bind(on_text_validate=lambda *_: self.submit())
        input_wrapper.add_widget(self.entry)
        input_card.add_widget(input_wrapper)

        # Primary Guess Button
        self.submit_btn = ModernButton(
            text="SUBMIT GUESS",
            font_size="15sp",
            bold=True,
            bg_color=(0.18, 0.48, 0.96, 1),
            size_hint_y=None,
            height=dp(48),
            radius=10
        )
        self.submit_btn.bind(on_press=lambda *_: self.submit())
        input_card.add_widget(self.submit_btn)

        # Secondary Action (New Game)
        new_game_btn = ModernButton(
            text="NEW GAME",
            font_size="13sp",
            bold=True,
            bg_color=(0.14, 0.18, 0.28, 1),
            size_hint_y=None,
            height=dp(38),
            radius=8
        )
        new_game_btn.bind(on_press=lambda *_: self.new_game())
        input_card.add_widget(new_game_btn)
        root.add_widget(input_card)

        # 5. History Tracker Card
        self.history_card = ModernCard(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(6),
            size_hint_y=None,
            height=dp(80),
            bg_color=(0.08, 0.11, 0.17, 1),
            border_color=(0.14, 0.20, 0.30, 1)
        )
        hist_title = Label(
            text="[b]ROUND GUESS HISTORY[/b]",
            markup=True,
            font_size="11sp",
            color=(0.50, 0.58, 0.70, 1),
            halign="left",
            size_hint_y=None,
            height=dp(18)
        )
        hist_title.bind(size=hist_title.setter("text_size"))
        self.history_label = Label(
            text="No guesses yet this round",
            font_size="13sp",
            color=(0.65, 0.72, 0.82, 1),
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(36)
        )
        self.history_label.bind(size=self.history_label.setter("text_size"))
        self.history_card.add_widget(hist_title)
        self.history_card.add_widget(self.history_label)
        root.add_widget(self.history_card)

        # 6. Statistics Dashboard Card
        stats_card = ModernCard(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(105),
            bg_color=(0.08, 0.11, 0.17, 1),
            border_color=(0.14, 0.20, 0.30, 1)
        )
        stats_title = Label(
            text="[b]CAREER STATS[/b]",
            markup=True,
            font_size="11sp",
            color=(0.50, 0.58, 0.70, 1),
            halign="left",
            size_hint_y=None,
            height=dp(16)
        )
        stats_title.bind(size=stats_title.setter("text_size"))
        stats_card.add_widget(stats_title)

        stats_row = GridLayout(cols=3, spacing=dp(8), size_hint_y=None, height=dp(56))

        def make_stat_box(title, value_ref):
            box = BoxLayout(orientation="vertical", padding=[dp(4), dp(4)], spacing=dp(2))
            val_lbl = Label(text="0", font_size="18sp", bold=True, color=(0.95, 0.97, 1, 1))
            t_lbl = Label(text=title, font_size="11sp", color=(0.55, 0.62, 0.72, 1))
            box.add_widget(val_lbl)
            box.add_widget(t_lbl)
            return box, val_lbl

        b1, self.stat_played = make_stat_box("PLAYED", "played")
        b2, self.stat_wins = make_stat_box("WINS", "wins")
        b3, self.stat_best = make_stat_box("BEST SCORE", "best")
        stats_row.add_widget(b1)
        stats_row.add_widget(b2)
        stats_row.add_widget(b3)
        stats_card.add_widget(stats_row)
        root.add_widget(stats_card)

        # 7. Sleek Footer
        footer = Label(
            text="Python Basic Projects • [b]Krushna Kale[/b]",
            markup=True,
            font_size="11sp",
            color=(0.40, 0.46, 0.56, 1),
            size_hint_y=None,
            height=dp(28)
        )
        root.add_widget(footer)

        self.refresh()
        return scroll

    def on_start(self):
        """Request focus once the window and event loop are fully initialized."""
        Clock.schedule_once(self._acquire_focus, 0.15)

    def _acquire_focus(self, *args):
        if hasattr(self, "entry") and self.entry:
            self.entry.focus = True

    def get_stats_file(self):
        """Robust location finder for stats.json."""
        try:
            if hasattr(self, "user_data_dir") and self.user_data_dir:
                p = Path(self.user_data_dir)
                p.mkdir(parents=True, exist_ok=True)
                return p / "stats.json"
        except (OSError, Exception):
            pass
        return Path(__file__).parent / "stats.json"

    def load_stats(self):
        try:
            if self.stats_file and self.stats_file.exists():
                data = json.loads(self.stats_file.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    return {
                        "played": max(0, int(data.get("played", 0))),
                        "wins": max(0, int(data.get("wins", 0))),
                        "best": max(0, int(data.get("best", 0)))
                    }
        except (OSError, ValueError, TypeError, OverflowError):
            pass
        return {"played": 0, "wins": 0, "best": 0}

    def save_stats(self):
        try:
            if self.stats_file:
                self.stats_file.parent.mkdir(parents=True, exist_ok=True)
                self.stats_file.write_text(json.dumps(self.stats, indent=2), encoding="utf-8")
        except OSError:
            pass

    def select_level(self, level):
        for lvl, btn in self.diff_buttons.items():
            if lvl == level:
                btn.set_bg_color((0.23, 0.51, 0.96, 1))
            else:
                btn.set_bg_color((0.12, 0.16, 0.24, 1))
        self.game.reset(level)
        self.history = []
        low, high, attempts = LEVELS[level]
        self.diff_info.text = f"Range: {low} – {high} • {attempts} Tries"
        self.entry.text = ""
        self.reset_clue_card("READY TO PLAY", f"Guess a number from {low} to {high}!", (0.09, 0.14, 0.23, 1), (0.20, 0.32, 0.52, 1))
        self.refresh()
        Clock.schedule_once(self._acquire_focus, 0.05)

    def reset_clue_card(self, title, message, bg, border):
        self.clue_title.text = f"[b]{title}[/b]"
        self.clue_message.text = message
        self.clue_card.set_card_color(bg, border)

    def refresh(self):
        self.diff_info.text = f"Range: {self.game.low} – {self.game.high} • {self.game.max_attempts} Tries"
        self.attempts_badge.text = f"Attempts remaining: {self.game.remaining} of {self.game.max_attempts}"
        self.stat_played.text = str(self.stats["played"])
        self.stat_wins.text = str(self.stats["wins"])
        self.stat_best.text = str(self.stats["best"])

        if self.history:
            recent = "   •   ".join(self.history[-4:])
            self.history_label.text = recent
        else:
            self.history_label.text = "No guesses yet this round"

    def new_game(self):
        self.select_level(self.game.level)
        Clock.schedule_once(self._acquire_focus, 0.05)

    def submit(self):
        val = self.entry.text.strip()
        if not val:
            Clock.schedule_once(self._acquire_focus, 0.05)
            return

        if self.game.finished:
            self.reset_clue_card("ROUND COMPLETE", "Click NEW GAME to play again!", (0.13, 0.11, 0.20, 1), (0.35, 0.25, 0.50, 1))
            Clock.schedule_once(self._acquire_focus, 0.05)
            return

        feedback = self.game.guess(val)
        self.entry.text = ""

        # Update clue styling based on outcome
        if self.game.won:
            self.reset_clue_card(
                "★ CONGRATULATIONS!",
                f"You guessed {self.game.secret} in {self.game.attempts} tries!",
                (0.06, 0.18, 0.12, 1),
                (0.12, 0.55, 0.35, 1)
            )
            self.clue_title.color = (0.20, 0.85, 0.50, 1)
            self.history.append(f"[color=33DD77]{val} (Correct!)[/color]")
            self.stats["played"] += 1
            self.stats["wins"] += 1
            self.stats["best"] = max(self.stats["best"], self.game.score())
            self.save_stats()
        elif self.game.finished:
            self.reset_clue_card(
                "✕ GAME OVER",
                f"Out of attempts! Secret number was {self.game.secret}",
                (0.20, 0.08, 0.09, 1),
                (0.58, 0.20, 0.22, 1)
            )
            self.clue_title.color = (0.95, 0.35, 0.35, 1)
            self.history.append(f"[color=EE5555]{val} (Last try)[/color]")
            self.stats["played"] += 1
            self.save_stats()
        elif "higher" in feedback:
            self.reset_clue_card(
                "▲ TRY HIGHER",
                f"{val} is too small! Go higher.",
                (0.18, 0.14, 0.06, 1),
                (0.55, 0.40, 0.15, 1)
            )
            self.clue_title.color = (0.98, 0.72, 0.20, 1)
            self.history.append(f"{val} (Too Low)")
        elif "lower" in feedback:
            self.reset_clue_card(
                "▼ TRY LOWER",
                f"{val} is too large! Go lower.",
                (0.06, 0.15, 0.20, 1),
                (0.15, 0.45, 0.58, 1)
            )
            self.clue_title.color = (0.25, 0.78, 0.95, 1)
            self.history.append(f"{val} (Too High)")
        else:
            self.reset_clue_card(
                "⚠ INVALID INPUT",
                feedback,
                (0.18, 0.10, 0.08, 1),
                (0.48, 0.25, 0.18, 1)
            )
            self.clue_title.color = (0.95, 0.50, 0.30, 1)

        self.refresh()
        Clock.schedule_once(self._acquire_focus, 0.05)


if __name__ == "__main__":
    GuessApp().run()
