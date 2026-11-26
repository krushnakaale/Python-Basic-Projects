import unittest
from quiz_logic import Quiz,BANK
class Tests(unittest.TestCase):
    def test_categories(self):
        for cat in BANK: self.assertEqual(len(Quiz(cat).questions),5)
    def test_correct(self):
        q=Quiz('Python'); self.assertTrue(q.answer(q.current[2])); self.assertEqual(q.score,1)
    def test_timeout(self):
        q=Quiz('Python'); self.assertFalse(q.answer(-1)); self.assertEqual(q.score,0)
    def test_duplicate(self):
        q=Quiz('Python'); q.answer(q.current[2]); self.assertIsNone(q.answer(q.current[2])); self.assertEqual(q.score,1)
    def test_finish(self):
        q=Quiz('Python')
        for i in range(5):
            q.answer(q.current[2]); self.assertEqual(q.advance(),i<4)
        self.assertEqual(q.score,5)
if __name__=='__main__': unittest.main()
