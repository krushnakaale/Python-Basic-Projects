import unittest
from clock_logic import duration, clock
class Tests(unittest.TestCase):
    def test_zero(self): self.assertEqual(duration(0),'00:00:00')
    def test_hours(self): self.assertEqual(duration(3661),'01:01:01')
    def test_negative(self): self.assertEqual(duration(-1),'00:00:00')
    def test_world(self): self.assertRegex(clock('Asia/Tokyo'),r'^\d{2}:\d{2}:\d{2}$')
    def test_twelve(self): self.assertRegex(clock('Asia/Kolkata',True),r'(AM|PM)$')
