from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.utils import platform
from password_logic import generate

KV = '''
#:import dp kivy.metrics.dp
<CleanButton@Button>:
    background_normal: ''
    background_color: .10,.22,.39,1
    size_hint_y: None
    height: dp(48)
<Ink@Label>:
    color: .10,.16,.25,1
    text_size: self.width, self.height
    halign: 'left'
    valign: 'middle'
BoxLayout:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: .96,.97,.99,1
        Rectangle:
            pos: self.pos
            size: self.size
    ScrollView:
        do_scroll_x: False
        BoxLayout:
            orientation: 'vertical'
            padding: dp(24)
            spacing: dp(12)
            size_hint_y: None
            height: self.minimum_height
            Ink:
                text: 'Password Generator'
                font_size: '25sp'
                bold: True
                size_hint_y: None
                height: dp(44)
            Ink:
                text: 'SECURITY / PYTHON PROJECT 04'
                font_size: '12sp'
                size_hint_y: None
                height: dp(26)
            TextInput:
                text: app.password
                readonly: True
                multiline: True
                font_size: '19sp'
                size_hint_y: None
                height: dp(110)
                padding: dp(12), dp(12)
            Ink:
                text: 'Length: ' + str(int(length.value))
                size_hint_y: None
                height: dp(28)
            Slider:
                id: length
                min: 8
                max: 128
                step: 1
                value: 16
                size_hint_y: None
                height: dp(40)
''' 
for key, label, active in [('upper','Uppercase letters',True),('lower','Lowercase letters',True),('digits','Numbers',True),('symbols','Special characters',True),('exclude','Exclude similar characters',False)]:
    KV += f'''            BoxLayout:
                size_hint_y: None
                height: dp(40)
                Ink:
                    text: '{label}'
                Switch:
                    id: {key}
                    active: {active}
                    size_hint_x: None
                    width: dp(70)
'''
KV += '''            Ink:
                text: app.strength
                size_hint_y: None
                height: dp(30)
            CleanButton:
                text: 'Generate password'
                on_release: app.create_password()
            CleanButton:
                text: 'Copy password'
                on_release: app.copy_password()
            Ink:
                text: app.status
                font_size: '13sp'
                size_hint_y: None
                height: dp(52)
'''

class PasswordApp(App):
    password = StringProperty('')
    strength = StringProperty('Strength estimate: —')
    status = StringProperty('Passwords are not saved by this app.')

    def build(self):
        self.title = 'Password Generator'
        if platform in ('win', 'linux', 'macosx'):
            Window.size = (460, 760)
        return Builder.load_string(KV)

    def on_start(self):
        self.create_password()

    def create_password(self):
        ids = self.root.ids
        try:
            self.password = generate(int(ids.length.value), *(ids[k].active for k in ('upper','lower','digits','symbols','exclude')))
        except ValueError as exc:
            self.status = str(exc)
            self.password = ''
            self.strength = 'Strength estimate: —'
            return
        n = len(self.password)
        types = sum(ids[k].active for k in ('upper','lower','digits','symbols'))
        self.strength = 'Strength estimate: ' + ('Strong' if n >= 16 and types >= 3 else 'Moderate' if n >= 12 else 'Basic')
        self.status = 'Generated locally. Use a unique password for each account.'

    def copy_password(self):
        if self.password:
            Clipboard.copy(self.password)
            self.status = 'Copied. Clipboard history may retain this password.'

if __name__ == '__main__':
    PasswordApp().run()
