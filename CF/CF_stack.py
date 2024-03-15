from aws_cdk import Stack, aws_cloudfront as cdn, aws_ssm as ssm, aws_iam as iam, aws_s3 as s3,aws_route53 as r53,aws_route53_targets as targets
from constructs import Construct
import aws_cdk as cdk



class CFStack(Stack):
    def __init__(self, scope: Construct, construct_id: str,s3bucket , **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        env_name = self.node.try_get_context("env")
        bucket_name = s3.Bucket.from_bucket_name(self, "s3bucket", s3bucket)


        self.cdn_id = cdn.CloudFrontWebDistribution(
            self,
            "webSiteCloudFront",
            origin_configs=[
                cdn.SourceConfiguration(
                    behaviors=[cdn.Behavior(is_default_behavior=True)],
                    s3_origin_source=cdn.S3OriginConfig(
                        s3_bucket_source=bucket_name,
                        origin_access_identity=cdn.OriginAccessIdentity(self, "weighting-calculator-OAI"),
                    ),
                )
            ],
            error_configurations=[
                cdn.CfnDistribution.CustomErrorResponseProperty(
                    error_code=400, response_code=200, response_page_path="/"
                )
            ],
        )

        ssm.StringParameter(
            self,
            "cdn-dist-id",
            parameter_name=f"/{env_name}/app-distribution-id",
            string_value=self.cdn_id.distribution_id,
        )

        ssm.StringParameter(
            self,
            "cdn-url",
            parameter_name=f"/{env_name}/app-cdn-url",
            string_value=f"https://{self.cdn_id.distribution_domain_name}",
        )

        # ssm.StringParameter(
        #     self,
        #     "cdn-arn",
        #     parameter_name=f"/{env_name}/cdn-arn",
        #     string_value=f"arn:aws:cloudfront::{cdk.Aws.ACCOUNT_ID}:distribution/{self.cdn_id.distribution_id}",
        # )
