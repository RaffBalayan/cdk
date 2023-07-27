from aws_cdk import  (
    Stack,
    aws_ec2 as ec2
)
from constructs import Construct


class VPCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "CalculatorVPC",
            cidr="10.0.0.0/21",
            max_azs=3,
            reserved_azs=1

        )