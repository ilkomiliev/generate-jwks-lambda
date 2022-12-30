import unittest
from fn import generator


class AllTests(unittest.TestCase):

    def test_rsa(self):
        _generator = generator.RSAKeyGenerator()
        _keys = _generator.generate_keys()
        print(_keys.as_dict())
        self.assertEqual(_keys.as_dict()["private_key"]["kty"], "RSA")

    def test_rsa_2048(self):
        _generator = generator.RSAKeyGenerator(key_size=2048)
        _keys = _generator.generate_keys()
        print(_keys.as_dict())
        print(_keys.as_json())
        self.assertEqual(_keys.as_dict()["private_key"]["kty"], "RSA")

    def test_ec(self):
        _generator = generator.ECKeyGenerator()
        _keys = _generator.generate_keys()
        print(_keys.as_dict())
        self.assertEqual(_keys.as_dict()["private_key"]["kty"], "EC")
        self.assertEqual(_keys.as_dict()["private_key"]["crv"], generator.SupportedCrvEnum.P_521.value)

    def test_ec_P_256(self):
        _generator = generator.ECKeyGenerator(crv=generator.SupportedCrvEnum.P_256)
        _keys = _generator.generate_keys()
        print(_keys.as_dict())
        self.assertEqual(_keys.as_dict()["private_key"]["kty"], "EC")
        self.assertEqual(_keys.as_dict()["private_key"]["crv"], generator.SupportedCrvEnum.P_256.value)

    def test_in(self):
        print(generator.SupportedRSAKeySizesEnum.is_valid_key_size("1024"))
