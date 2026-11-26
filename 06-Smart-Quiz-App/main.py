import json
from pathlib import Path
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from quiz_logic import Quiz, BANK

NAVY=(.09,.18,.32,1)
BLUE=(.16,.34,.64,1)
GREEN=(.08,.45,.27,1)
RED=(.7,.18,.18,1)
Window.clearcolor=(.95,.97,.99,1)

class QuizApp(App):
    title='Smart Quiz'
    timer=None
    def build(self):
        self.path=Path(self.user_data_dir)/'scores.json'
        try:
            self.best=json.loads(self.path.read_text())
            if not isinstance(self.best,dict): self.best={}
        except (OSError,ValueError): self.best={}
        self.root_box=BoxLayout(orientation='vertical',padding=dp(20),spacing=dp(12))
        self.home()
        return self.root_box
    def label(self,text,size=18,height=48):
        w=Label(text=text,color=NAVY,font_size=dp(size),size_hint_y=None,height=dp(height),halign='center',valign='middle')
        w.bind(size=lambda obj,val:setattr(obj,'text_size',val))
        self.root_box.add_widget(w)
        return w
    def button(self,text,action,color=BLUE):
        b=Button(text=text,background_normal='',background_color=color,font_size=dp(17),size_hint_y=1)
        b.bind(on_release=lambda *_:action())
        self.root_box.add_widget(b)
        return b
    def stop_timer(self):
        if self.timer: self.timer.cancel(); self.timer=None
    def home(self):
        self.stop_timer(); self.root_box.clear_widgets()
        self.label('LEARNING / PROJECT 06',13,30)
        self.label('Smart Quiz',32,65)
        self.label('Choose a category to begin',18,50)
        for cat in BANK:
            self.button(f'{cat}  |  Best: {self.best.get(cat,0)}/5',lambda c=cat:self.start(c))
        self.label('5 questions • 20 seconds each',14,40)
    def start(self,cat):
        self.category=cat; self.quiz=Quiz(cat); self.show_question()
    def show_question(self):
        self.stop_timer(); self.root_box.clear_widgets()
        q=self.quiz; self.remaining=20
        self.label(f'{self.category}  |  Question {q.index+1}/{len(q.questions)}',15,35)
        self.status=self.label(f'Score: {q.score}  |  Time: 20s',16,35)
        self.root_box.add_widget(ProgressBar(max=len(q.questions),value=q.index+1,size_hint_y=None,height=dp(12)))
        self.label(q.current[0],21,90)
        self.answers=[self.button(option,lambda i=i:self.submit(i)) for i,option in enumerate(q.current[1])]
        self.feedback=self.label('',15,55)
        self.next_button=self.button('Next',self.next_question,NAVY); self.next_button.disabled=True
        self.button('Back to categories',self.home,NAVY)
        self.timer=Clock.schedule_interval(self.tick,1)
    def tick(self,dt):
        self.remaining-=1
        self.status.text=f'Score: {self.quiz.score}  |  Time: {self.remaining}s'
        if self.remaining<=0: self.submit(-1); return False
    def submit(self,i):
        result=self.quiz.answer(i)
        if result is None:return
        self.stop_timer()
        correct=self.quiz.current[2]
        for j,b in enumerate(self.answers):
            b.disabled=True
            b.background_disabled_normal=''
            b.background_color=GREEN if j==correct else RED if j==i else NAVY
        self.feedback.text='Correct!' if result else ('Time up! ' if i==-1 else 'Incorrect. ')+ 'Answer: '+self.quiz.current[1][correct]
        self.status.text=f'Score: {self.quiz.score}  |  Time: {self.remaining}s'
        self.next_button.disabled=False
    def next_question(self):
        if self.quiz.advance(): self.show_question()
        else:self.results()
    def results(self):
        self.root_box.clear_widgets(); score=self.quiz.score; total=len(self.quiz.questions)
        self.best[self.category]=max(score,self.best.get(self.category,0))
        try:
            self.path.parent.mkdir(parents=True,exist_ok=True); self.path.write_text(json.dumps(self.best))
        except OSError: pass
        self.label('Quiz complete',30,70)
        self.label(f'{score} / {total}',38,100)
        self.label(f'Accuracy: {score/total:.0%}  |  Best: {self.best[self.category]}',18,60)
        self.button('Play again',lambda:self.start(self.category))
        self.button('Choose category',self.home,NAVY)

if __name__=='__main__': QuizApp().run()
