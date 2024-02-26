import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_route53 as r53,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_cloudfront as cf,
aws_certificatemanager as acm
)
from constructs import Construct


class AcmStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        env_name = self.node.try_get_context("env")
        account_id = cdk.Aws.ACCOUNT_ID

        zone_id = ssm.StringParameter.from_string_parameter_name(self, 'zone_id_ssm', string_parameter_name=f"/{env_name}/hz-id")
        dns_zone= r53.HostedZone.from_hosted_zone_attributes(self,"hosted_zone",hosted_zone_id=zone_id.string_value,
                                                             zone_name='callc.am')
        self.acm_meneger = acm.Certificate(self, "acm_id",domain_name="callc.am",subject_alternative_names=["*.callc.am"],
                                           validation=acm.CertificateValidation.from_dns_multi_zone({"web.callc.am": dns_zone}))
