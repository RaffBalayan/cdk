#!/usr/bin/env python3
import aws_cdk as cdk
import aws_cdk.aws_ssm as ssm
#from Network.VPC import VPCStack
#from SG.SG import SGStack
#
from CF.CF_stack import CFStack
from Storage.s3Stack import S3Stack
from code import codecommit
from code.Codepipeline import Pipeline
from code.codecommit import CodecommitStack
from Route53.Route53 import Route53Stack
#from acm.acm_skack import AcmStack
from Lambda.aws_lambda import LambdaStack



app = cdk.App()
#vpc_stack = VPCStack(app, "vpc")
#sg_stack = SGStack(app, "sg-stack", vpc=vpc_stack.vpc)



route53 = Route53Stack(app, "Route-53", env=cdk.Environment(account="174851338573", region="eu-central-1"))

# s3_stack = S3Stack(app, "s3stack")
cf_stack = CFStack(app, "cf", s3bucket=cdk.Fn.import_value("Calculator-bucket"))
#acm_stack = AcmStack(app, "acm")
code = CodecommitStack(app, 'codecommit')
pipeline = Pipeline(app, 'pipeline', s3bucket=cdk.Fn.import_value("Calculator-bucket"))
aws_lam = LambdaStack(app,"cflambda", s3bucket=cdk.Fn.import_value("Calculator-bucket"))
app.synth()