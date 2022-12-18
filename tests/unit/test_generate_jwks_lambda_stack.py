import aws_cdk as core
import aws_cdk.assertions as assertions

from generate_jwks_lambda.generate_jwks_lambda_stack import GenerateJwksLambdaStack

# example tests. To run these tests, uncomment this file along with the example
# resource in generate_jwks_lambda/generate_jwks_lambda_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = GenerateJwksLambdaStack(app, "generate-jwks-lambda")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
