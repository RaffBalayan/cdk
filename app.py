#!/usr/bin/env python3
import aws_cdk as cdk
import aws_cdk.aws_ssm as ssm
#from Network.VPC import VPCStack
#from SG.SG import SGStack
#
from CF.CF_stack import CFStack
from Storage.s3Stack import S3Stack
from code.Codepipeline import Pipeline
from code.codecommit import CodecommitStack
app = cdk.App()
#vpc_stack = VPCStack(app, "vpc")
#sg_stack = SGStack(app, "sg-stack", vpc=vpc_stack.vpc)

s3_stack = S3Stack(app, "s3stack")
cf_stack = CFStack(app, "cf", s3bucket=cdk.Fn.import_value("Calculator-bucket"))
code = CodecommitStack(app, 'codecommit')

pipeline = Pipeline(app, 'pipeline', s3bucket=cdk.Fn.import_value("Calculator-bucket"))

app.synth()


