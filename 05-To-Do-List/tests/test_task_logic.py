import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from task_logic import TaskStore
class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory(); self.addCleanup(self.tmp.cleanup); self.s=TaskStore(Path(self.tmp.name)/'tasks.json')
    def test_add_reload(self):
        self.s.put('Study','High','2026-12-01'); self.assertEqual(TaskStore(self.s.path).tasks[0]['title'],'Study')
    def test_edit(self):
        self.s.put('A'); self.s.put('B',task_id=self.s.tasks[0]['id']); self.assertEqual(len(self.s.tasks),1); self.assertEqual(self.s.tasks[0]['title'],'B')
    def test_toggle_filter(self):
        self.s.put('Study'); self.s.toggle(self.s.tasks[0]['id']); self.assertEqual(len(self.s.filtered('study','Completed')),1)
    def test_delete(self):
        self.s.put('A'); self.s.delete(self.s.tasks[0]['id']); self.assertEqual(self.s.tasks,[])
    def test_invalid(self):
        with self.assertRaises(ValueError): self.s.put(' ')
        with self.assertRaises(ValueError): self.s.put('A',due='bad')
