from aws_cdk import (Stack, aws_iam as iam, aws_ec2 as ec2, aws_ssm as ssm,)
from constructs import Construct


class SGStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,vpc:ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        env_name = self.node.try_get_context("env")

        lambda_sg = ec2.SecurityGroup(self, 'lambdasg',
                security_group_name='lambda-sg',
                vpc=vpc,
                description="SG for labmbda",
                allow_all_outbound=True
                 )