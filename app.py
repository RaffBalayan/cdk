#!/usr/bin/env python3
import aws_cdk as cdk
from CF.CF_stack import CFStack
from code.Codepipeline import Pipeline
from code.codecommit import CodecommitStack
from Route53.Route53 import Route53Stack
from Lambda.aws_lambda import LambdaFunctionStack
from storage.bucketstack import S3BucketStack
from la_s3.add_per import Addaccess
from acm.acm_skack import AcmStack



app = cdk.App()
code = CodecommitStack(app, 'codecommit')
s3_stack = S3BucketStack(app, "s3stack")
cf_stack = CFStack(app, "cf", s3bucket=cdk.Fn.import_value("Calculator-bucket"))
pipeline = Pipeline(app, 'pipeline', s3bucket=cdk.Fn.import_value("Calculator-bucket"))
route53 = Route53Stack(app, "Route-53", env=cdk.Environment(account="174851338573", region="eu-central-1"))
add_access = Addaccess(app, 'addaccess')
acmstack = AcmStack(app, "acmstack"   )

cf_stack.add_dependency(s3_stack)
pipeline.add_dependency(cf_stack)
add_access.add_dependency(pipeline)
route53.add_dependency(add_access)
acmstack.add_dependency(route53)

app.synth()