import aws_cdk as cdk
from aws_cdk import aws_lambda as _lambda, aws_s3 as s3, Stack,aws_iam as iam,  aws_s3_notifications as s3n
from constructs import Construct
from aws_cdk.aws_iam import PolicyStatement

from aws_cdk.aws_lambda_event_sources import S3EventSource
import aws_cdk.aws_lambda_event_sources as eventsources
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_ssm as ssm
from aws_cdk.aws_cloudfront import IDistribution  # Assuming CloudFront is used elsewhere

class LambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, s3bucket: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # cal_bucket = ssm.StringParameter.from_string_parameter_name(self, "bucket_name",
        #                                                               string_parameter_name="web_bucket_name")

        # Define the Lambda function
        lambda_function = _lambda.Function(
            self, "CloudFrontInvalidationLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.lambda_handler",  # Ensure the handler matches your Lambda's file and function name
            code=_lambda.Code.from_asset("Lambda/aswl.zip"),
        )



        lambda_function.add_to_role_policy(
            PolicyStatement(
                actions=["cloudfront:CreateInvalidation"],
                resources=["arn:aws:cloudfront:::distribution/E1Q69E65H3UFSK"],
            )
        )

        lambda_function.add_permission(
            's3-service-principal',
            principal=iam.ServicePrincipal('s3.amazonaws.com')
        )

        env_name = self.node.try_get_context("env")
        account_id = cdk.Aws.ACCOUNT_ID

        web_bucket = s3.Bucket(
            self,
            'weight-calculator',
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            bucket_name=account_id + '-' + env_name + '-weight-calculator',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
            website_index_document='index.html',
        )

        cdk.CfnOutput(self, "s3-export", value=web_bucket.bucket_name, export_name="Calculator-bucket")

        web_bucket.add_to_resource_policy(
            permission=iam.PolicyStatement(
                actions=["s3:GetObject"],
                effect=iam.Effect.ALLOW,
                resources=[web_bucket.arn_for_objects(key_pattern="*")],
                principals=[iam.ArnPrincipal(arn="*")],
            )
        )

        web_bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.LambdaDestination(lambda_function))