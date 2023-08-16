#!/usr/bin/env python3
import aws_cdk as cdk


from Network.VPC import VPCStack
from SG.SG import SGStack
from Storage.s3Stack import S3Stack
from CF.CF_stack import CFStack
app = cdk.App()
vpc_stack = VPCStack(app, "vpc")
sg_stack = SGStack(app, "sg-stack", vpc=vpc_stack.vpc)
s3_stack = S3Stack(app, "s3_stack", props=app.account)
cdn_stack = CFStack(app,"cdn" ,s3bucket=cdk.Fn.import_value("front-bucket"))
app.synth()


