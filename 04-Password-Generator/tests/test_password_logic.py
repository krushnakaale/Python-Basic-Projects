import unittest
import string
from password_logic import generate

class PasswordTests(unittest.TestCase):
    def test_length(self):
        self.assertEqual(len(generate(32)), 32)
    def test_groups(self):
        p = generate()
        for group in (string.ascii_uppercase,string.ascii_lowercase,string.digits,string.punctuation):
            self.assertTrue(any(c in group for c in p))
    def test_exclusion(self):
        self.assertFalse(set(generate(128, exclude=True)) & set('Il1O0o|'))
    def test_no_groups(self):
        with self.assertRaises(ValueError): generate(16,False,False,False,False)
    def test_invalid_length(self):
        with self.assertRaises(ValueError): generate(7)
    def test_digits_only(self):
        self.assertTrue(generate(16,False,False,True,False).isdigit())
