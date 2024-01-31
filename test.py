import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_cloudfront as cdn,
    RemovalPolicy
)
from constructs import Construct

class S3Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        env_name = self.node.try_get_context("env")
        account_id = cdk.Aws.ACCOUNT_ID

        # Create S3 bucket
        web_bucket = s3.Bucket(self, 'weight-calculator',
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            bucket_name=account_id + '-' + env_name + '-weight-calculator',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
            website_index_document='index.html'
        )

        # Create Origin Access Identity for CloudFront
        oai = cdn.OriginAccessIdentity(self, id="weighting-calculator-OAI")

        # Create CloudFront distribution
        cdn_distribution = cdn.CloudFrontWebDistribution(self, "WebDistribution",
            origin_configs=[
                cdn.SourceConfiguration(
                    behaviors=[cdn.Behavior(is_default_behavior=True)],
                    s3_origin_source=cdn.S3OriginConfig(
                        s3_bucket_source=web_bucket,
                        origin_access_identity=oai
                    )
                )
            ],
            error_configurations=[
                cdn.CfnDistribution.CustomErrorResponseProperty(
                    error_code=400,
                    response_code=200,
                    response_page_path='/'
                )
            ]
        )

        # Output the S3 bucket name
        cdk.CfnOutput(self, "S3BucketExport",
            value=web_bucket.bucket_name,
            export_name="CalculatorBucket")

        # Add bucket policy to allow CloudFront to access S3 bucket
        web_bucket.add_to_resource_policy(iam.PolicyStatement(
            actions=["s3:GetObject"],
            effect=iam.Effect.ALLOW,
            resources=[f"{web_bucket.bucket_arn}/*"],
            principals=[iam.ArnPrincipal(cdn_distribution.distribution_domain_name)],
        ))

        # Output the CloudFront distribution domain name
        cdk.CfnOutput(self, "CloudFrontDistributionDomainName",
            value=cdn_distribution.distribution_domain_name,
            description="CloudFront Distribution Domain Name")



___________

web_bucket.add_to_resource_policy(
    permission=iam.PolicyStatement(actions=["s3:GetObject"], effect=iam.Effect.ALLOW, principals=[]))
