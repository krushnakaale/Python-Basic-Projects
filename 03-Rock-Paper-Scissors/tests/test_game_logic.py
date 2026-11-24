import unittest
from game_logic import Game, decide

class TestRules(unittest.TestCase):
    def test_win_loss_draw(self):
        self.assertEqual(decide('Rock', 'Scissors'), 'win')
        self.assertEqual(decide('Rock', 'Paper'), 'loss')
        self.assertEqual(decide('Rock', 'Rock'), 'draw')

    def test_invalid_choice(self):
        with self.assertRaises(ValueError):
            decide('Fire', 'Paper')

    def test_match_completion(self):
        game = Game(best_of=3)
        game.play('Rock', 'Scissors')
        self.assertFalse(game.finished)
        game.play('Rock', 'Scissors')
        self.assertTrue(game.finished)
        with self.assertRaises(RuntimeError):
            game.play('Rock', 'Paper')

    def test_draw_does_not_count_as_win(self):
        game = Game()
        game.play('Rock', 'Rock')
        self.assertEqual((game.wins, game.losses, game.draws), (0, 0, 1))

if __name__ == '__main__':
    unittest.main()
