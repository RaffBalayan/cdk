#!/usr/bin/env python3
import aws_cdk as cdk


from Network.VPC import VPCStack
from SG.SG import SGStack

app = cdk.App()
vpc_stack = VPCStack(app, "vpc")
sg = SGStack(app, "sg-stack",vpc=vpc_stack.vpc)
app.synth()


