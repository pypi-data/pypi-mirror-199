import unittest
import ccipher

class TestCaesarCipher(unittest.TestCase):
    def test_encrypt(self):
        self.assertEqual(ccipher.encrypt(string=ccipher.alphabet, key=1), "bcdefghijklmnopqrstuvwxyza")

    def test_decrypt(self):
        self.assertEqual(ccipher.decrypt(string="xlmw mw e qiwweki xs fi higvctxih", key=4), "this is a message to be decrypted")

if __name__ == '__main__':
    unittest.main()
