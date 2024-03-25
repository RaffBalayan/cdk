import aws_cdk as cdk
from aws_cdk import aws_lambda as _lambda, aws_s3 as s3, Stack, aws_iam as iam, aws_s3_notifications as s3n, aws_ssm as ssm, aws_iam as iam
from constructs import Construct

import aws_cdk.aws_lambda_event_sources as eventsources


class S3BucketStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        env_name = self.node.try_get_context("env")
        account_id = cdk.Aws.ACCOUNT_ID

        web_bucket = s3.Bucket(
            self,
            'weight-calculator',
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            bucket_name=f"{account_id}-{env_name}-weight-calculator",
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
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                effect=iam.Effect.ALLOW,
                resources=[web_bucket.arn_for_objects("*")],
                principals=[iam.ArnPrincipal(arn="*")],
            )
        )

        # distribution_id = ssm.StringParameter.from_string_parameter_name(
        #     self,
        #     "distribution_id",
        #     string_parameter_name=f"/{env_name}/app-distribution-id"
        # ).string_value

        lambda_function = _lambda.Function(
            self, "CloudFrontInvalidationLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            function_name="CloudFrontInvalidationLambda",
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("Lambda/awsla.zip"),
            # environment={
            #     'cf_distribution_id': distribution_id
            # }
        )





        lambda_function.add_to_role_policy(
            iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                actions=["s3:GetObject", "s3:PutObject"],
                                resources=[f"{web_bucket.bucket_arn}/*"]))


        # lambda_function.role.add_to_principal_policy(iam.PolicyStatement(
        #     effect=iam.Effect.ALLOW,
        #     actions=["cloudfront:CreateInvalidation"],
        #     resources=[f"arn:aws:cloudfront::{account_id}:distribution/{distribution_id}"]
        # ))


        lambda_function.add_permission(
            's3-service-principal',
            principal=iam.ServicePrincipal('s3.amazonaws.com'),
            action='lambda:InvokeFunction',
            source_arn=web_bucket.bucket_arn,
        )






        web_bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.LambdaDestination(lambda_function))

        lambda_function.role.add_to_principal_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["ssm:GetParameter"],
            resources=[f"arn:aws:ssm:eu-central-1:{account_id}:parameter/{env_name}/app-distribution-id"]
        ))


        ssm.StringParameter(
            self,
            "bucket-arn",
            parameter_name=f"{env_name}-weight-calculator",
            string_value=web_bucket.bucket_arn,
        )

        ssm.StringParameter(self, "lambda_name", parameter_name="Lambda_arn",
                            string_value=lambda_function.function_arn)


