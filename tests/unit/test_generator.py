import unittest
from fn import generator


class AllTests(unittest.TestCase):

    def test_rsa(self):
        _generator = generator.RSAKeyGenerator()
        _keys = _generator.generate_keys()
        self.assertEqual(_keys.as_dict()["private_key"]["kty"], "RSA")

    def test_rsa_2048(self):
        _generator = generator.RSAKeyGenerator(key_size=2048)
        _keys = _generator.generate_keys()
        self.assertEqual(_keys.as_dict()["private_key"]["kty"], "RSA")

    def test_rsa_invalid_key_size(self):
        self.assertRaises(AttributeError, generator.RSAKeyGenerator, 2000)

    def test_ec(self):
        _generator = generator.ECKeyGenerator()
        _keys = _generator.generate_keys()
        self.assertEqual(_keys.as_dict()["private_key"]["kty"], "EC")
        self.assertEqual(_keys.as_dict()["private_key"]["crv"], "P-521")

    def test_ec_P_256(self):
        _generator = generator.ECKeyGenerator(crv="P-256")
        _keys = _generator.generate_keys()
        self.assertEqual(_keys.as_dict()["private_key"]["kty"], "EC")
        self.assertEqual(_keys.as_dict()["private_key"]["crv"], "P-256")

    def test_ec_invalid_crv(self):
        self.assertRaises(AttributeError, generator.ECKeyGenerator, "wow")
