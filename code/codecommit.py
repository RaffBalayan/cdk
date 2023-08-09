from aws_cdk import (
    Stack,
   aws_codecommit as codecommit
)
from constructs import Construct
class CodecommitStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        repo = codecommit.Repository(self, "Repository",
            repository_name="calculator",
            description="test reopo"
        )