from aws_cdk import App, Stack
from aws_cdk import aws_lambda as _lambda
from aws_cdk.aws_iam import PolicyStatement
from constructs import Construct


class MyLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        lambda_function = _lambda.Function(
            self, "CloudFrontInvalidationFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_handler.handler",
            code=_lambda.Code.from_asset("path/to/your/lambda/code"),
        )

        lambda_function.add_to_role_policy(
            PolicyStatement(
                actions=["cloudfront:CreateInvalidation"],
                resources=["*"],
            )
        )

app = App()
MyLambdaStack(app, "MyLambdaStack")
app.synth()
