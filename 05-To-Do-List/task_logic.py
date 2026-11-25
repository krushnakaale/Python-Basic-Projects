import json
from pathlib import Path
from datetime import date
from uuid import uuid4

class TaskStore:
    def __init__(self, path):
        self.path = Path(path)
        self.tasks = json.loads(self.path.read_text(encoding='utf-8')) if self.path.exists() else []
    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix('.tmp')
        tmp.write_text(json.dumps(self.tasks, indent=2, ensure_ascii=False), encoding='utf-8')
        tmp.replace(self.path)
    def put(self, title, priority='Medium', due='', task_id=None):
        title = title.strip()
        if not title: raise ValueError('Enter a task title.')
        if priority not in ('High','Medium','Low'): raise ValueError('Invalid priority.')
        if due: due = date.fromisoformat(due).isoformat()
        task = next((t for t in self.tasks if t['id']==task_id), None)
        if task is None:
            task = {'id': uuid4().hex, 'done': False}
            self.tasks.append(task)
        task.update(title=title, priority=priority, due=due)
        self.save()
    def toggle(self, task_id):
        for t in self.tasks:
            if t['id']==task_id: t['done']=not t['done']
        self.save()
    def delete(self, task_id):
        self.tasks = [t for t in self.tasks if t['id']!=task_id]
        self.save()
    def filtered(self, query='', status='All'):
        return [t for t in self.tasks if query.casefold() in t['title'].casefold() and (status=='All' or t['done']==(status=='Completed'))]
