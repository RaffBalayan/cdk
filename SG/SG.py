from aws_cdk import (Stack, aws_iam as iam, aws_ec2 as ec2, aws_ssm as ssm,)
from constructs import Construct


class SGStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,vpc:ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        env_name = self.node.try_get_context("env")

        self.lambda_sg = ec2.SecurityGroup(self, 'lambdasg',
                security_group_name='lambda-sg',
                vpc=vpc,
                description="SG for labmbda",
                allow_all_outbound=True
                 )


        lambda_role = iam.Role(self, 'lambdarole',
                               assumed_by=iam.ServicePrincipal(service='lambda.amazonaws.com'),
                               role_name='lambda-role',
                               managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                                   managed_policy_name='service-role/AWSLambdaVPCAccessExecutionRole'
                               )]
                               )

        lambda_role.add_to_policy(
            statement=iam.PolicyStatement(
                actions=['s3:*', 'rds:*'],
                resources=['*']
            )
        )
        # SSM Parameters
        ssm.StringParameter(self, 'lambdasg-param',
                            parameter_name='/' + env_name + '/lambda-sg',
                            string_value=self.lambda_sg.security_group_id
                            )