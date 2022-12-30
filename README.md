# JWK Generator

This project can be used to generate RSA or EC asymmetric key pairs as specified by the JWK. It uses 
the [jwcrypto](https://github.com/latchset/jwcrypto) library.
Currently, the following formats are supported:

- RSA with 1024, 2048 and 4096 bits private key lengths
- EC with P-256, P-384 and P-521 crv sizes

The output is an JSON object with the following structure:

```json
{
  "private_key": {
    "kty": "EC",
    "crv": "P-256",
    "x": "yHLTSVOSrT9JhY8aQOsSEetWue8sppFDJzIVW_He0gc",
    "y": "aZ_33v9b66Rpwr0oPE7CotPVlp0r17MHbmrA83madbc",
    "d": "r4d3rJ84yfZ2Wd5_VSPJ4_9V7GX1lLs6fBbXe0wOq44",
    "kid": "304406413d22a763ebdd4cbfe8d54029d26842a5a49e38d4f201e6597ecc3533"
  },
  "public_key": {
    "kty": "EC",
    "kid": "304406413d22a763ebdd4cbfe8d54029d26842a5a49e38d4f201e6597ecc3533",
    "crv": "P-256",
    "x": "yHLTSVOSrT9JhY8aQOsSEetWue8sppFDJzIVW_He0gc",
    "y": "aZ_33v9b66Rpwr0oPE7CotPVlp0r17MHbmrA83madbc"
  },
  "private_public_pair": {
    "kty": "EC",
    "crv": "P-256",
    "x": "yHLTSVOSrT9JhY8aQOsSEetWue8sppFDJzIVW_He0gc",
    "y": "aZ_33v9b66Rpwr0oPE7CotPVlp0r17MHbmrA83madbc",
    "d": "r4d3rJ84yfZ2Wd5_VSPJ4_9V7GX1lLs6fBbXe0wOq44",
    "kid": "304406413d22a763ebdd4cbfe8d54029d26842a5a49e38d4f201e6597ecc3533"
  }
}
```

The key id (`kid`) is generated as SHA256 over the public key.

## Development

The project uses AWS SAM for building the lambda function within a container. After this is done the real provisioning is accomplished by AWS CDK application. 

### Project structure

- cdk folder contains the AWS CDK stacks for the IaS provisioning
- fn folder contains the JWK key generator and the lambda handler

### AWS SAM

Installation instruction fo AWS SAM installation can be found [here](https://aws.amazon.com/serverless/sam/).
The [template.yaml](template.yaml) file in the main project folder contains instruction for packaging the 
lambda function with its dependencies. It uses the [requirements.txt](./fn/requirements.txt) file from the `fn` folder. 
The lambda function can be built with:

```sam build --use-container```

> This requires working Docker installation!

The above command can be extended with environment variables for example to 
customise the build environment for enterprise setups with internal pypi repos:

`sam build --use-container -e PIP_INDEX_URL=https://artifactory.internal/pypi/simple`

For local tests local invocation can be used with events from the 
tests/unit folder, i.e.

`sam local invoke -e tests/unit/event_proxy.json`

>The deployment of the lambda function is NOT done by SAM!

### AWS CDK 

Installation instructions for AWS CDK can be found [here](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html#getting_started_install).
As python is used for development a virtual environment is used - see python specific setup 
instructions [here](https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-python.html).
See also the auto-generated [README_cdk.md](./README_cdk.md) file. The project dependencies are controlled with the top-level [requirements.txt](requirements.txt) file.

After the venv is set up and sourced the deployment stack can be synthesized with:

`cdk synth`

For deployment the following command can be used:

`cdk deploy --require-approval never`

> Ensure that the lambda function is built BEFORE executing the deployment!

> --require-approval is optional and used to avoid confirmation of the execution of privileged actions

On successful deployment the URL for the API Gateway access will be outputed in the `Outputs` section:
```
Outputs:
GenerateJwksLambdaStack.jwkgenapiEndpointFE9F2455 = https://c71z2qxamg.execute-api.us-east-1.amazonaws.com/prod/
Stack ARN:
arn:aws:cloudformation:us-east-1:123456789012:stack/GenerateJwksLambdaStack/105115a0-883f-11ed-8c21-0e429b5bf1fb
```

If you open the URL in the browser Usage page will be shown for the possible calls.
The same page is shown under the `/help` or `/usage` endpoints.

### Clean Up

Use `cdk destroy` to clean up the provisioned resources.