#!/usr/bin/env python3
import aws_cdk as cdk
from CF.CF_stack import CFStack
from code.Codepipeline import Pipeline
from code.codecommit import CodecommitStack
from Route53.Route53 import Route53Stack
from Lambda.aws_lambda import LambdaStack



app = cdk.App()

route53 = Route53Stack(app, "Route-53", env=cdk.Environment(account="174851338573", region="eu-central-1"))
code = CodecommitStack(app, 'codecommit')
aws_lam = LambdaStack(app,"cflambda", s3bucket=cdk.Fn.import_value("Calculator-bucket"))
cf_stack = CFStack(app, "cf", s3bucket=cdk.Fn.import_value("Calculator-bucket"))
pipeline = Pipeline(app, 'pipeline', s3bucket=cdk.Fn.import_value("Calculator-bucket"))
app.synth()