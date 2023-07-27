#!/usr/bin/env python3
import os

import aws_cdk as cdk
from code.codecommit import CodecommitStack
from network.vpc import VPCStack

app = cdk.App()
CodecommitStack(app, "Codecommit")

app = cdk.App()
VPCStack(app, "VPC"
         )


app.synth()
