from aws_cdk import aws_lambda as _lambda
from aws_cdk import Stack
from constructs import Construct

class MyCdkStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Lambda function for CloudFront cache invalidation
        lambda_function = _lambda.Function(
            self, "CloudFrontInvalidationLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.asset("path/to/your/lambda/code")
        )
