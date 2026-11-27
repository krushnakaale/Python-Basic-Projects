import json
import time
from pathlib import Path
from datetime import datetime
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from clock_logic import clock, duration

class DigitalClock(App):
    def build(self):
        self.title = 'Smart Digital Clock'
        self.path = Path(self.user_data_dir) / 'settings.json'
        try: self.settings = json.loads(self.path.read_text())
        except (OSError, ValueError): self.settings = {}
        self.elapsed = 0; self.started = None; self.deadline = None; self.remaining = 0; self.laps = []
        self.rootbox = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(8))
        self.nav = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(6))
        self.rootbox.add_widget(self.nav)
        for name in ('Clock','World','Stopwatch','Timer'):
            self.button(self.nav,name,lambda _, n=name:self.show(n))
        self.body = BoxLayout(orientation='vertical', spacing=dp(8)); self.rootbox.add_widget(self.body)
        self.show('Clock'); Clock.schedule_interval(self.tick, .15)
        return self.rootbox
    def button(self, parent, text, callback):
        b=Button(text=text, background_normal='', background_color=(.18,.34,.57,1), color=(1,1,1,1), size_hint_y=None,height=dp(44)); b.bind(on_release=callback); parent.add_widget(b); return b
    def label(self,text='',size=20):
        l=Label(text=text,font_size=dp(size),color=self.fg); self.body.add_widget(l); return l
    def save(self):
        self.path.parent.mkdir(parents=True,exist_ok=True); self.path.write_text(json.dumps(self.settings))
    def toggle(self,key):
        self.settings[key]=not self.settings.get(key,False); self.save(); self.show(self.page)
    def show(self,page):
        self.page=page; self.body.clear_widgets(); light=self.settings.get('light',False)
        Window.clearcolor=(.94,.96,.99,1) if light else (.06,.10,.18,1); self.fg=(.08,.15,.25,1) if light else (.92,.96,1,1)
        self.label('SMART DIGITAL CLOCK  /  '+page.upper(),15)
        self.display=self.label('',36 if page!='World' else 20)
        if page=='Clock':
            self.button(self.body,'Switch 12 / 24 hour format',lambda _:self.toggle('twelve'))
            self.button(self.body,'Switch light / dark theme',lambda _:self.toggle('light'))
        elif page=='Stopwatch':
            self.button(self.body,'Start / Pause',lambda _:self.stopwatch())
            self.button(self.body,'Record lap',lambda _:self.lap())
            self.button(self.body,'Reset',lambda _:self.reset())
            self.laplabel=self.label('',16)
        elif page=='Timer':
            self.entry=TextInput(hint_text='Duration in seconds (1–86400)',multiline=False,input_filter='int',size_hint_y=None,height=dp(44)); self.body.add_widget(self.entry)
            self.button(self.body,'Start timer',lambda _:self.timer())
            self.button(self.body,'Cancel timer',lambda _:self.cancel())
            self.status=self.label('',16)
        self.tick(0)
    def stopwatch(self):
        if self.started is None: self.started=time.monotonic()
        else: self.elapsed+=time.monotonic()-self.started; self.started=None
    def total(self): return self.elapsed+(time.monotonic()-self.started if self.started is not None else 0)
    def lap(self):
        if self.started is not None: self.laps.append(duration(self.total()))
    def reset(self): self.started=None; self.elapsed=0; self.laps=[]
    def timer(self):
        try:
            n=int(self.entry.text)
            if not 1<=n<=86400: raise ValueError
        except ValueError: self.status.text='Enter 1 to 86400 seconds'; return
        self.deadline=time.monotonic()+n; self.remaining=n; self.status.text='Timer running'
    def cancel(self): self.deadline=None; self.remaining=0; self.status.text='Timer cancelled'
    def tick(self,dt):
        import math
        if self.deadline is not None:
            self.remaining=max(0,math.ceil(self.deadline-time.monotonic()))
            if not self.remaining:
                self.deadline=None
                if self.page=='Timer': self.status.text='Time is up!'
        twelve=self.settings.get('twelve',False)
        if self.page=='Clock': self.display.text=clock('Asia/Kolkata',twelve)+'\n'+datetime.now(__import__('zoneinfo').ZoneInfo('Asia/Kolkata')).strftime('%A, %d %B %Y')
        elif self.page=='World': self.display.text='\n\n'.join(f'{name}   {clock(zone,twelve)}' for name,zone in [('India','Asia/Kolkata'),('London','Europe/London'),('New York','America/New_York'),('Tokyo','Asia/Tokyo'),('Dubai','Asia/Dubai')])
        elif self.page=='Stopwatch':
            self.display.text=duration(self.total()); self.laplabel.text='\n'.join(f'Lap {i+1}: {v}' for i,v in list(enumerate(self.laps))[-4:])
        else: self.display.text=duration(self.remaining)

if __name__=='__main__': DigitalClock().run()
