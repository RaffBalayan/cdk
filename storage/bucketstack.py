import aws_cdk as cdk
from aws_cdk import aws_lambda as _lambda, aws_s3 as s3, Stack, aws_iam as iam, aws_s3_notifications as s3n, aws_ssm as ssm
from constructs import Construct



class S3BucketStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        env_name = self.node.try_get_context("env")
        account_id = cdk.Aws.ACCOUNT_ID

        self.web_bucket = s3.Bucket(
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

        cdk.CfnOutput(self, "s3-export", value=self.web_bucket.bucket_name, export_name="Calculator-bucket")

        self.web_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                effect=iam.Effect.ALLOW,
                resources=[self.web_bucket.arn_for_objects("*")],
                principals=[iam.AnyPrincipal()],
            )
        )

        # lambda_arn_parameter = ssm.StringParameter.from_string_parameter_name(
        #     self,
        #     "lambdaFunctionArn",
        #     string_parameter_name="Lambda_arn"
        # )

        # lambda_function = _lambda.Function.from_function_arn(
        #     self,
        #     "LambdaFunction",
        #     lambda_arn_parameter.string_value
        # )


        # self.web_bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.LambdaDestination(lambda_function))


        ssm.StringParameter(
            self,
            "bucket-arn",
            parameter_name=f"{env_name}-weight-calculator",
            string_value=self.web_bucket.bucket_arn,
        )