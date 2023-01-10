import argparse
from fn import generator


def main():
    _parser = argparse.ArgumentParser()
    _parser.add_argument("kty", help="Key type: must be RSA or EC")
    _parser.add_argument(
        "-params",
        required=False,
        help="Additional parameters, specific to the provided kty. For RSA this is the "
             "length of the private key and must be one of 1024, 2048, 4096 (default). "
             "For EC this is the crv type and must be one of P-256, P384 or P-521 (default)"
    )
    _parser.add_argument(
        "-output",
        choices=["json", "dict"],
        default="json",
        help="The type of the output - either json (default) or python dict"
    )
    _args = _parser.parse_args()
    try:
        _keys = generator.generate_keys_as_dict(kty=_args.kty, params=_args.params) \
            if _args.output and _args.output == "dict" \
            else generator.generate_keys_as_json(kty=_args.kty, params=_args.params)
        print(_keys)
    except Exception as e:
        print(e)


if __name__  == "__main__":
    main()
