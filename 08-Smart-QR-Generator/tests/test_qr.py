import unittest
from qr_logic import payload, generate
class Tests(unittest.TestCase):
    def test_text(self): self.assertEqual(payload('Text','hello'),'hello')
    def test_url(self):
        with self.assertRaises(ValueError): payload('Website','example.com')
    def test_email(self): self.assertEqual(payload('Email','a@example.com'),'mailto:a@example.com')
    def test_phone(self): self.assertEqual(payload('Phone','+91 1234567890'),'tel:+911234567890')
    def test_wifi(self): self.assertEqual(payload('Wi-Fi','a;b','pass'),'WIFI:T:WPA;S:a\\;b;P:pass;;')
    def test_image(self): self.assertEqual(generate('hello').size,(512,512))
    def test_color(self):
        with self.assertRaises(ValueError): generate('hello',color='#ffffff')
