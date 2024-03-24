import aws_cdk as cdk
from aws_cdk import aws_lambda as _lambda,  Stack, aws_iam as iam, aws_ssm as ssm,aws_s3 as s3
from constructs import Construct
from aws_cdk.aws_iam import PolicyStatement
import aws_cdk.aws_lambda_event_sources as eventsources

class LambdaFunctionStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)


        # env_name = self.node.try_get_context("env")
        # destrinution_id = ssm.StringParameter.from_string_parameter_name(
        #     self,
        #     "distribution_id",
        #     string_parameter_name=f"/{env_name}/app-distribution-id"
        # )

        self.lambda_function = _lambda.Function(
            self, "CloudFrontInvalidationLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            function_name="CloudFrontInvalidationLambda",
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("Lambda/aswl.zip"),
        )
        #
        # self.lambda_function.add_to_role_policy(
        #     PolicyStatement(
        #         actions=["cloudfront:CreateInvalidation"],
        #         resources=[f"arn:aws:cloudfront:::distribution/{destrinution_id}"],
        #     )
        # )
        #
        # s3_arn = ssm.StringParameter.from_string_parameter_name(
        #     self,
        #     "s3-arn",
        #     string_parameter_name=f"{env_name}-weight-calculator").string_value
        #
        # self.lambda_function.add_permission(
        #     's3-service-principal',
        #     principal=iam.ServicePrincipal('s3.amazonaws.com'),
        #     source_arn=s3_arn
        # )
        #
        #
        #
               #
        # self.lambda_function.add_permission(
        #     's3-service-principal',
        #     principal=iam.ServicePrincipal('s3.amazonaws.com'),
        #     action='lambda:InvokeFunction',
        #     source_arn=web_bucket.bucket_arn,
        # )





        ssm.StringParameter(self,"lambda_name",parameter_name="Lambda_arn",string_value=self.lambda_function.function_arn)
