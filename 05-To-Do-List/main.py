from pathlib import Path
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from task_logic import TaskStore

NAVY=(.10,.18,.31,1); INK=(.12,.18,.27,1); MUTED=(.36,.42,.51,1); WHITE=(1,1,1,1); BLUE=(.15,.34,.68,1)
Window.clearcolor=(.94,.96,.98,1)
def panel(**kwargs):
    w=BoxLayout(**kwargs)
    with w.canvas.before:
        Color(*WHITE); r=RoundedRectangle(pos=w.pos,size=w.size,radius=[dp(12)])
    w.bind(pos=lambda *_: setattr(r,'pos',w.pos),size=lambda *_: setattr(r,'size',w.size))
    return w
def label(text='', size=15, color=INK, **kw):
    w=Label(text=text,font_size=dp(size),color=color,halign='left',valign='middle',**kw)
    w.bind(size=lambda *_: setattr(w,'text_size',w.size))
    return w
def button(text, callback, **kw):
    w=Button(text=text,background_normal='',background_color=NAVY,color=WHITE,**kw)
    w.bind(on_release=lambda *_: callback()); return w
class TodoApp(App):
    def build(self):
        self.title='Smart To-Do List'
        self.store=TaskStore(Path(self.user_data_dir)/'tasks.json')
        root=BoxLayout(orientation='vertical',padding=dp(16),spacing=dp(12))
        root.add_widget(label('WORKSPACE  /  TASKS',12,MUTED,size_hint_y=None,height=dp(24)))
        root.add_widget(label('My Tasks',30,size_hint_y=None,height=dp(48)))
        self.stats=label('',16,size_hint_y=None,height=dp(42)); root.add_widget(self.stats)
        self.progress=ProgressBar(max=100,size_hint_y=None,height=dp(12)); root.add_widget(self.progress)
        root.add_widget(button('+ New task',lambda:self.editor(),size_hint_y=None,height=dp(46)))
        bar=BoxLayout(size_hint_y=None,height=dp(44),spacing=dp(8))
        self.search=TextInput(hint_text='Search tasks',multiline=False,padding=[dp(10),dp(10)])
        self.status=Spinner(text='All',values=('All','Pending','Completed'),size_hint_x=.42,background_normal='',background_color=NAVY)
        bar.add_widget(self.search); bar.add_widget(self.status); root.add_widget(bar)
        scroll=ScrollView(); self.rows=GridLayout(cols=1,spacing=dp(10),size_hint_y=None); self.rows.bind(minimum_height=self.rows.setter('height')); scroll.add_widget(self.rows); root.add_widget(scroll)
        self.search.bind(text=lambda *_:self.refresh()); self.status.bind(text=lambda *_:self.refresh()); self.refresh(); return root
    def refresh(self):
        total=len(self.store.tasks); done=sum(t['done'] for t in self.store.tasks)
        self.stats.text=f'{total} Total   |   {total-done} Pending   |   {done} Done'; self.progress.value=100*done/total if total else 0
        self.rows.clear_widgets()
        tasks=self.store.filtered(self.search.text,self.status.text)
        if not tasks: self.rows.add_widget(label('No tasks to display.',15,MUTED,size_hint_y=None,height=dp(70)))
        for t in tasks:
            tid=t['id']; card=panel(orientation='vertical',padding=dp(12),spacing=dp(5),size_hint_y=None,height=dp(138))
            card.add_widget(label(t['title'],18)); card.add_widget(label(f"{t['priority']} priority  |  {t['due'] or 'No due date'}  |  {'Done' if t['done'] else 'Pending'}",12,MUTED))
            actions=BoxLayout(size_hint_y=None,height=dp(36),spacing=dp(6))
            actions.add_widget(button('Undo' if t['done'] else 'Done',lambda i=tid:self.change(i)))
            actions.add_widget(button('Edit',lambda task=t:self.editor(task)))
            actions.add_widget(button('Delete',lambda i=tid:self.confirm(i)))
            card.add_widget(actions); self.rows.add_widget(card)
    def change(self,i): self.store.toggle(i); self.refresh()
    def confirm(self,i):
        content=BoxLayout(orientation='vertical',padding=dp(12),spacing=dp(8)); p=Popup(title='Delete this task?',content=content,size_hint=(.85,None),height=dp(180))
        content.add_widget(button('Delete',lambda:(self.store.delete(i),p.dismiss(),self.refresh()))); content.add_widget(button('Cancel',p.dismiss)); p.open()
    def editor(self,t=None):
        t=t or {}; content=BoxLayout(orientation='vertical',padding=dp(12),spacing=dp(8)); p=Popup(title='Edit task' if t else 'New task',content=content,size_hint=(.9,None),height=dp(340))
        title=TextInput(text=t.get('title',''),hint_text='Task title',multiline=False); due=TextInput(text=t.get('due',''),hint_text='Due date (YYYY-MM-DD)',multiline=False); priority=Spinner(text=t.get('priority','Medium'),values=('High','Medium','Low')); error=label('',12,(.7,.15,.15,1))
        for w in (title,due,priority,error): content.add_widget(w)
        def save():
            try: self.store.put(title.text,priority.text,due.text.strip(),t.get('id'))
            except ValueError as e: error.text=str(e); return
            p.dismiss(); self.refresh()
        content.add_widget(button('Save task',save)); content.add_widget(button('Cancel',p.dismiss)); p.open()
if __name__=='__main__': TodoApp().run()
