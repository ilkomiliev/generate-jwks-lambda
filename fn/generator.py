import json
from abc import abstractmethod
from hashlib import sha256
from jwcrypto import jwk

RSA_PRIVATE_KEY_SIZES = [1024, 2048, 4096]
EC_CRV_ALGOS = ["P-256", "P-384", "P-521"]


class Keys:
    _keys: jwk.JWK

    def __init__(self, keys: jwk.JWK) -> None:
        self._keys = keys

    def as_dict(self) -> dict:
        """Represents the given JWK as python dict object.

        :return: dict with the following structure:
            "private_key": object, containing the private key,
            "public_key": object, containing the public key,
            "private_public_pair": object, containing the public-private key pair
        """
        return {
            "private_key": self._keys.export_private(as_dict=True),
            "public_key": self._keys.export_public(as_dict=True),
            "private_public_pair": self._keys.export(as_dict=True)
        }

    def as_json(self) -> str:
        """Returns JSON representation of the JWK object

        :return: JSON object with the following structure:
            "private_key": object, containing the private key,
            "public_key": object, containing the public key,
            "private_public_pair": object, containing the public-private key pair
        """
        return json.dumps(self.as_dict())


class KeyGenerator:

    def generate_keys(self) -> Keys:
        """Generates the key pair, the kid is set to SHA256 hash of the public key

        :return: Keys object with the JWK
        """
        keys = self._create_keys()
        pub_key = keys.export_public()
        kid = sha256(pub_key.encode("utf-8")).hexdigest()
        keys.update(kid=kid)
        return Keys(keys=keys)

    @abstractmethod
    def _create_keys(self) -> jwk.JWK:
        pass


class RSAKeyGenerator(KeyGenerator):
    _key_size: int

    def __init__(self, key_size: int = 4096) -> None:
        """RSA key pair generator

        :param key_size: the size of the private key
        """
        if key_size not in RSA_PRIVATE_KEY_SIZES:
            raise AttributeError(f"Unsupported RSA key size: {key_size}, must be one of {RSA_PRIVATE_KEY_SIZES}!")
        self._key_size = key_size

    def _create_keys(self) -> jwk.JWK:
        return jwk.JWK.generate(kty="RSA", size=self._key_size)


class ECKeyGenerator(KeyGenerator):
    _crv: str

    def __init__(self, crv: str = "P-521"):
        """EC key pair generator

        :param crv: the crv algorithm
        """
        if crv not in EC_CRV_ALGOS:
            raise AttributeError(f"Unsupported EC crv: {crv}, must be one of {EC_CRV_ALGOS}!")
        self._crv = crv

    def _create_keys(self) -> jwk.JWK:
        return jwk.JWK.generate(kty="EC", crv=self._crv)


def generate_keys(kty: str, params: str) -> Keys:
    if "RSA" == kty:
        _generator = RSAKeyGenerator(key_size=int(params)) if params else RSAKeyGenerator()
    elif "EC" == kty:
        _generator = ECKeyGenerator(crv=params) if params else ECKeyGenerator()
    else:
        raise AttributeError("kty must be either RSA or EC!")
    return _generator.generate_keys()


def generate_keys_as_json(kty: str, params: str) -> str:
    return generate_keys(kty=kty, params=params).as_json()


def generate_keys_as_dict(kty: str, params: str) -> dict:
    return generate_keys(kty=kty, params=params).as_dict()
