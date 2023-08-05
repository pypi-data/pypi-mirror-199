import unittest
from ccipher import encrypt, decrypt, alphabet

class TestCaesarCipher(unittest.TestCase):
    def test_encrypt(self):
        self.assertEqual(encrypt(string=alphabet, key=1), "bcdefghijklmnopqrstuvwxyza")

    def test_decrypt(self):
        self.assertEqual(decrypt(string="xlmw mw e qiwweki xs fi higvctxih", key=4), "this is a message to be decrypted")

if __name__ == '__main__':
    unittest.main()
