import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_ssm as ssm,
    aws_cloudfront as cf,
    aws_s3_notifications as s3n,


)
from constructs import Construct
from aws_cdk.aws_iam import PolicyStatement


class Addaccess(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        env_name = self.node.try_get_context("env")

        s3_arn = ssm.StringParameter.from_string_parameter_name(
            self,
            "s3-arn",
            string_parameter_name=f"{env_name}-weight-calculator")

        web_bucket = s3.Bucket.from_bucket_arn(self, "web-bucket", s3_arn.string_value)

        lambda_arn_parameter = ssm.StringParameter.from_string_parameter_name(
            self,
            "lambdaFunctionArn",
            string_parameter_name="Lambda_arn"
        )

        destrinution_id_ssm = ssm.StringParameter.from_string_parameter_name(
            self,
            "distribution_id",
            string_parameter_name=f"/{env_name}/app-distribution-id"
        ).string_value


        lambda_function = _lambda.Function.from_function_arn(
            self,
            "LambdaFunction",
            lambda_arn_parameter.string_value
        )

        cloudfront_distribution_arn = f"arn:aws:cloudfront::{self.account}:distribution/{destrinution_id_ssm}"
        print(cloudfront_distribution_arn)

        lambda_function.add_to_role_policy(iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["cloudfront:CreateInvalidation"],
                resources=[cloudfront_distribution_arn],
            )
        )





        lambda_function.add_to_role_policy(
            PolicyStatement(effect=iam.Effect.ALLOW,
                            actions=["s3:GetObject", "s3:PutObject"],
                            resources=[f"{web_bucket.bucket_arn}/*"] ))



        lambda_function.add_permission(
            's3-service-principal',
            principal=iam.ServicePrincipal('s3.amazonaws.com'),
            # action='lambda:InvokeFunction',
            source_arn=web_bucket.bucket_arn,
        )

        web_bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.LambdaDestination(lambda_function))



        # distribution_id= cf.Distribution.from_distribution_attributes()









