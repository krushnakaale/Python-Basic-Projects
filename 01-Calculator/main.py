"""Cross-platform calculator using Kivy."""
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from calculator_logic import calculate

BG = (0.07, 0.09, 0.13, 1)
PANEL = (0.12, 0.15, 0.20, 1)
KEY = (0.20, 0.24, 0.30, 1)
ACCENT = (0.22, 0.46, 0.94, 1)
TEXT = (0.96, 0.97, 0.99, 1)
MUTED = (0.68, 0.74, 0.81, 1)


class CalculatorApp(App):
    title = 'Python Calculator'

    def build(self):
        Window.clearcolor = BG
        Window.size = (380, 650)
        self.expression = ''
        self.history = []
        self.history_visible = False
        root = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12))
        header = BoxLayout(size_hint_y=None, height=dp(44))
        header.add_widget(Label(text='CALCULATOR', bold=True, font_size='19sp', color=TEXT, halign='left'))
        history_btn = self.button('History', PANEL, font_size='15sp')
        history_btn.size_hint_x = .32
        history_btn.bind(on_release=lambda *_: self.toggle_history())
        header.add_widget(history_btn)
        root.add_widget(header)

        display = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(122), padding=dp(14), spacing=dp(5))
        with display.canvas.before:
            Color(*PANEL)
            rect = RoundedRectangle(pos=display.pos, size=display.size, radius=[dp(12)])
        display.bind(pos=lambda inst, *_: setattr(rect, 'pos', inst.pos),
                     size=lambda inst, *_: setattr(rect, 'size', inst.size))
        self.expression_label = Label(text='0', color=MUTED, font_size='20sp', halign='right', valign='middle', shorten=True)
        self.result_label = Label(text='0', color=TEXT, font_size='34sp', bold=True, halign='right', valign='middle', shorten=True)
        for label in (self.expression_label, self.result_label):
            label.bind(size=lambda inst, *_: setattr(inst, 'text_size', inst.size))
            display.add_widget(label)
        root.add_widget(display)

        self.history_panel = ScrollView(size_hint_y=None, height=0, opacity=0)
        self.history_label = Label(text='No calculations yet', color=MUTED, size_hint_y=None, halign='right', valign='top', font_size='14sp')
        self.history_label.bind(texture_size=lambda inst, size: setattr(inst, 'height', max(dp(100), size[1] + dp(20))))
        self.history_label.bind(width=lambda inst, *_: setattr(inst, 'text_size', (inst.width - dp(12), None)))
        self.history_panel.add_widget(self.history_label)
        root.add_widget(self.history_panel)

        keys = [
            ['AC', '⌫', '(', ')'],
            ['7', '8', '9', '÷'],
            ['4', '5', '6', '×'],
            ['1', '2', '3', '−'],
            ['%', '0', '.', '+'],
            ['√', 'x²', '=', 'C'],
        ]
        grid = GridLayout(cols=4, spacing=dp(8))
        for row in keys:
            for key in row:
                color = ACCENT if key == '=' else ((0.54, 0.23, 0.25, 1) if key in ('AC', 'C') else KEY)
                btn = self.button(key, color)
                btn.bind(on_release=lambda _, k=key: self.press(k))
                grid.add_widget(btn)
        root.add_widget(grid)
        Window.bind(on_key_down=self.on_key_down)
        return root

    def button(self, label, color, font_size='23sp'):
        return Button(text=label, background_normal='', background_color=color,
                      color=TEXT, font_size=font_size, bold=True)

    def press(self, key):
        if key in ('AC', 'C'):
            self.expression = ''
            self.result_label.text = '0'
        elif key == '⌫':
            self.expression = self.expression[:-1]
        elif key == '=':
            try:
                result = calculate(self.expression)
                self.history.append(f'{self.expression} = {result}')
                self.history = self.history[-20:]
                self.history_label.text = '\n'.join(reversed(self.history))
                self.result_label.text = result
                self.expression = result
            except ValueError as exc:
                self.result_label.text = str(exc)
        elif key == '√':
            self.expression = f'sqrt({self.expression or "0"})'
        elif key == 'x²':
            self.expression = f'({self.expression or "0"})**2'
        else:
            self.expression += key
        self.expression_label.text = self.expression or '0'

    def toggle_history(self):
        self.history_visible = not self.history_visible
        self.history_panel.height = dp(120) if self.history_visible else 0
        self.history_panel.opacity = 1 if self.history_visible else 0

    def on_key_down(self, _window, keycode, _scancode, text, modifiers):
        if keycode in (13, 271):
            self.press('=')
        elif keycode == 8:
            self.press('⌫')
        elif keycode == 27:
            self.press('AC')
        elif text in '0123456789.+-*/()%':
            self.press({'*': '×', '/': '÷', '-': '−'}.get(text, text))
        return False


if __name__ == '__main__':
    CalculatorApp().run()
