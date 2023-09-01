import aws_cdk
import aws_cdk as cdk
from aws_cdk import (Stack,
aws_s3 as s3,
aws_ssm as ssm,
RemovalPolicy
)
from constructs import Construct

class S3Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        env_name = self.node.try_get_context("env")
        account_id = cdk.Aws.ACCOUNT_ID
        lambda_bucket = s3.Bucket(self, 'weight-calculator',
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            bucket_name=account_id+'-'+env_name+'-Weight-Calculator',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,

        )
        cdk.CfnOutput(self,"s3-front-export",
                          value=lambda_bucket.bucket_name,
                          export_name="Calculator-bucket")