from aws_cdk import (
    # Duration,
    Stack,
    aws_apigateway as apigw,
    aws_lambda as lmbd, Duration
)
from constructs import Construct


class GenerateJwksLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        _fn = lmbd.Function(
            scope=self,
            id="JwkGeneratorFunction",
            code=lmbd.Code.from_asset(".aws-sam/build/JwkGeneratorFunction/"),
            runtime=lmbd.Runtime.PYTHON_3_9,
            handler="handler.handle",
            timeout=Duration.seconds(29),
            memory_size=256
        )

        apigw.LambdaRestApi(
            scope=self, id="jwkgenapi", rest_api_name="Jwk Generator", description="Generates JWK key", handler=_fn
        )
