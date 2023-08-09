from aws_cdk import (Stack, aws_ec2 as ec2, aws_ssm as ssm,)
from constructs import Construct


class VPCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        env_name = self.node.try_get_context("env")

        self.vpc = ec2.Vpc(self, "calculator",
           cidr="172.32.0.0/16",
           max_azs=4,
           enable_dns_support=True,
           subnet_configuration=[
               ec2.SubnetConfiguration(
                   name="Privateee",
                   subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                   cidr_mask=22,
               )
           ]
        )

        priv_subnets = [subnet.subnet_id for subnet in self.vpc.private_subnets]

        count = 1
        for ps in priv_subnets:
            ssm.StringParameter(self, 'private-subnet-'+str(count),
                string_value=ps,
                parameter_name='/' + env_name + '/private-subnet-'+str(count))
            count += 1
