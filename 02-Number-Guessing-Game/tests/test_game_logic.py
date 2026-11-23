import unittest
from game_logic import GuessingGame

class GameTests(unittest.TestCase):
    def test_hints_and_win(self):
        g = GuessingGame("Easy", secret=25)
        self.assertIn("higher", g.guess("10"))
        self.assertIn("lower", g.guess("40"))
        self.assertIn("Correct", g.guess("25"))
        self.assertTrue(g.won)
        self.assertGreater(g.score(), 0)

    def test_invalid_does_not_consume_attempt(self):
        g = GuessingGame(secret=10)
        g.guess("abc")
        g.guess("999")
        self.assertEqual(g.attempts, 0)

    def test_loss(self):
        g = GuessingGame("Hard", secret=200)
        for _ in range(g.max_attempts):
            g.guess("1")
        self.assertTrue(g.finished)
        self.assertFalse(g.won)
        self.assertEqual(g.score(), 0)

if __name__ == "__main__":
    unittest.main()
