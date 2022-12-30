from typing import Optional, Any

import generator


def _parse_event(event):
    _kty = event["queryStringParameters"]["kty"]
    _params: Optional[Any] = event["queryStringParameters"]["params"] if "params" in event[
        "queryStringParameters"].keys() else None
    return _kty, _params


def handle(event, context):
    print(f"event: {event}")
    try:
        _path: str = event["path"].lower()
        if "/help" == _path or "/usage" == _path or "/h" == _path or "/u" == _path:
            return _usage_response(event)
        if "/jwk" == _path:
            _kty, _params = _parse_event(event)
            print(f"kty, params: {_kty}, {_params}")
            return _normal_response(kty=_kty, params=_params)
        return _usage_response(event, 400)
    except Exception:
        return _usage_response(event, 400)


def _normal_response(kty: str, params: str):
    print("normal response")
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "isBase64Encoded": False,
        "body": generator.generate_keys_as_json(kty=kty, params=params)
    }


def _usage_response(event, status_code: int = 200):
    print(f"usage_response, code: {status_code}")
    _proto = event["headers"]["X-Forwarded-Proto"]
    _domain = event["requestContext"]["domainName"]
    _stage = event["requestContext"]["stage"]
    _fdn = f"{_proto}://{_domain}/{_stage}"
    return {
        "statusCode": status_code,
        "headers": {
            "Content-type": "text/plain"
        },
        "isBase64Encoded": False,
        "body": f'''
            Usage:
            \n
            curl {_fdn}/jwk?kty=kty[&params=params]
            \n
            where:
            \n
            kty: is one of RSA or EC for the type of the key pair
            \n
            params: is optional and depends on the type of the key pair as follow 
            \n
            For RSA keys it must be an integer determining the size of the private key, i.e. 1024, 2048, etc. 
            The default value is 4096.
            \n
            For EC type keys it is the crv value and must be one of P-256, P-384 or P-521. 
            The default value is P-521.
             \n
            Examples, using curl and jq:
            \n
            RSA with 4096: curl -s "{_fdn}/jwk?kty=RSA" | jq .
            \n
            RSA with 2048: curl -s "{_fdn}/jwk?kty=RSA&params=2048" | jq .
            \n
            EC with P-521: curl -s "{_fdn}/jwk?kty=EC" | jq .
            \n
            EC with P-256: curl -s "{_fdn}/jwk?kty=EC&params=P-256" | jq .
            \n
            Use {_fdn}/help or {_fdn}/usage to print this page.
        '''
    }
