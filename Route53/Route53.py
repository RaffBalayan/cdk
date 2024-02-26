import aws_cdk as cdk
from aws_cdk import aws_ssm as ssm
from aws_cdk import Stack
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets
from constructs import Construct
from aws_cdk import aws_cloudfront as cf
from CF.CF_stack import CFStack

class Route53Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        env_name = self.node.try_get_context("env")

        distribution = cf.Distribution.from_distribution_attributes(
            self, "MyImportedDistribution",
            distribution_id="E1QEX8XV0GDSNS",
            domain_name="d2ju9prb65yvht.cloudfront.net"
        )


        # Define the hosted zone
        hosted_zone = route53.HostedZone(self, "HostedZone",
                                         zone_name ='callc.am')


        route53.ARecord(self, "ARecord",
                        zone=hosted_zone,
                        record_name="web",
                        target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution)))

        ssm.StringParameter(
            self,
            "hostedzone-id",
            parameter_name=f"/{env_name}/hz-id",
            string_value=hosted_zone.hosted_zone_id,
        )

