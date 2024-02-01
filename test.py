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


export class HelloCdkStack extends Stack {
  constructor(scope: App, id: string, props?: StackProps) {
    super(scope, id, props);

    const myFirstBucket = new Bucket(this, 'MyFirstBucket', {
      versioned: true,
      encryption: BucketEncryption.S3_MANAGED,
      bucketName: 'cdk-example-bucket-for-test',
      websiteIndexDocument: 'index.html',
      blockPublicAccess: BlockPublicAccess.BLOCK_ALL
    });

    new BucketDeployment(this, 'DeployWebsite', {
      sources: [Source.asset('dist')],
      destinationBucket: myFirstBucket
    });

    const oia = new OriginAccessIdentity(this, 'OIA', {
      comment: "Created by CDK"
    });
    myFirstBucket.grantRead(oia);

    new CloudFrontWebDistribution(this, 'cdk-example-distribution', {
      originConfigs: [
        {
          s3OriginSource: {
            s3BucketSource: myFirstBucket,
            originAccessIdentity: oia
          },
          behaviors: [
            { isDefaultBehavior: true }
          ]
        }
      ]
    });
  }
}

~~~~~~~~~~~~


- name: online-weight-calculator
  origin_access_identity: true
  encryption: S3_MANAGED
  access_control: BUCKET_OWNER_FULL_CONTROL
  block_public_access:
    block_public_acls: false
    block_public_policy: false
    ignore_public_acls: false
    restrict_public_buckets: false
  removal_policy: RETAIN
  export_cfn_output: false
  event_notifications:
    - name: invalidate_online_weight_calculator
      lambda_name: cache-invalidator
      s3n_type: lambda
      event_actions:
        - action: OBJECT_CREATED
          filters:
            - type: suffix
              filter: index.html

