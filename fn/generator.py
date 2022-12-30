import json
from abc import abstractmethod
from enum import Enum, unique
from hashlib import sha256
from jwcrypto import jwk


class Keys:
    _keys: jwk.JWK

    def __init__(self, keys: jwk.JWK) -> None:
        self._keys = keys

    def as_dict(self) -> dict:
        return {
            "private_key": self._keys.export_private(as_dict=True),
            "public_key": self._keys.export_public(as_dict=True),
            "private_public_pair": self._keys.export(as_dict=True)
        }

    def as_json(self) -> str:
        return json.dumps(self.as_dict())


class KeyGenerator:

    def __init__(self) -> None:
        pass

    def generate_keys(self) -> Keys:
        keys = self._create_keys()
        pub_key = keys.export_public()
        kid = sha256(pub_key.encode("utf-8")).hexdigest()
        keys.update(kid=kid)
        return Keys(keys=keys)

    @abstractmethod
    def _create_keys(self) -> jwk.JWK:
        pass


@unique
class SupportedRSAKeySizesEnum(Enum):
    RSA_1024 = 1024
    RSA_2048 = 2048
    RSA_4096 = 4096

    @staticmethod
    def is_valid_key_size(key_size: int):
        return key_size in [member.value for member in SupportedRSAKeySizesEnum.__members__.values()]


class RSAKeyGenerator(KeyGenerator):
    _key_size: int

    def __init__(self, key_size: int = 4096) -> None:
        if not SupportedRSAKeySizesEnum.is_valid_key_size(key_size):
            raise AttributeError(f"Unsupported RSA key size: {key_size}, must be 1024, 2048 or 4096!")
        self._key_size = key_size

    def _create_keys(self) -> jwk.JWK:
        return jwk.JWK.generate(kty="RSA", size=self._key_size)


@unique
class SupportedCrvEnum(Enum):
    P_256 = "P-256"
    P_384 = "P-384"
    P_521 = "P-521"

    def __repr__(self):
        return self.value


class ECKeyGenerator(KeyGenerator):
    _crv: str

    def __init__(self, crv: SupportedCrvEnum = SupportedCrvEnum.P_521):
        self._crv = crv.value

    def _create_keys(self) -> jwk.JWK:
        return jwk.JWK.generate(kty="EC", crv=self._crv)


def generate_keys(kty: str, params: str) -> Keys:
    if "RSA" == kty:
        _generator = RSAKeyGenerator(key_size=int(params)) if params else RSAKeyGenerator()
    elif "EC" == kty:
        _generator = ECKeyGenerator(crv=SupportedCrvEnum(params)) if params else ECKeyGenerator()
    else:
        raise AttributeError("kty must be either RSA or EC!")
    return _generator.generate_keys()


def generate_keys_as_json(kty: str, params: str):
    return generate_keys(kty=kty, params=params).as_json()


def generate_keys_as_dict(kty: str, params: str):
    return generate_keys(kty=kty, params=params).as_dict()
