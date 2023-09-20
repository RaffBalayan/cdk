import aws_cdk
import aws_cdk as cdk
from aws_cdk import (Stack,
aws_s3 as s3,aws_iam as iam,
aws_ssm as ssm,
aws_cloudfront as cdn,
RemovalPolicy
)
from constructs import Construct
class S3Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        env_name = self.node.try_get_context("env")
        account_id = cdk.Aws.ACCOUNT_ID
        web_bucket = s3.Bucket(self, 'weight-calculator',
           access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            bucket_name=account_id+'-'+env_name+'-weight-calculator',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False

            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
            website_index_document='index.html',


        )
        cdn.OriginAccessIdentity(self,id="weghting-calculator-OAI")

        cdk.CfnOutput(self,"s3-front-export",
                          value=web_bucket.bucket_name,
                          export_name="Calculator-bucket")



