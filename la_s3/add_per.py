import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_ssm as ssm,
    aws_cloudfront as cf,
    aws_s3_notifications as s3n,
    aws_cloudfront_origins as origins


)
from constructs import Construct
from aws_cdk.aws_iam import PolicyStatement


class Addaccess(Stack):
    def __init__(self, scope: Construct, construct_id: str,    **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        env_name = self.node.try_get_context("env")
        account_id = cdk.Aws.ACCOUNT_ID


        s3_arn = ssm.StringParameter.from_string_parameter_name(
            self,
            "s3-arn",
            string_parameter_name=f"{env_name}-weight-calculator")

        web_bucket = s3.Bucket.from_bucket_arn(self, "web-bucket", s3_arn.string_value)

        lambda_arn_parameter = ssm.StringParameter.from_string_parameter_name(
            self,
            "lambdaFunctionArn",
            string_parameter_name="Lambda_arn"
        ).string_value

        distribution_id = ssm.StringParameter.from_string_parameter_name(
            self,
            "distribution_id",
            string_parameter_name=f"/{env_name}/app-distribution-id"
        ).string_value


        lambda_function = _lambda.Function.from_function_arn(
            self,
            "LambdaFunction",
            lambda_arn_parameter
        )

        lambda_function.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["cloudfront:CreateInvalidation"],
            resources=[f"arn:aws:cloudfront::{account_id}:distribution/{distribution_id}"]
        ))











        # distribution_id= cf.Distribution.from_distribution_attributes()









