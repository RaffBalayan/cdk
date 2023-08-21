from aws_cdk import (Stack, aws_cloudfront as cdn, aws_ssm as ssm, aws_s3 as s3, aws_iam as iam, aws_codepipeline as cp,
                     aws_codecommit as ccm )
from constructs import Construct

class Pipeline(Stack):

    def __init__(self, scope: Construct, construct_id: str, s3bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        env_name = self.node.try_get_context("env")

        cal_bucket = s3.Bucket.from_bucket_name(self,'cal-bucket-id',bucket_name=s3bucket)
        cdn_id = ssm.StringParameter.from_string_parameter_name(self,"cdni-d",string_parameter_name="/"+env_name+"/app-distribution-id")
        source_repo = ccm.Repository.from_repository_name(self, "RepoId",repository_name="calculator")

        artifac_bucket = s3.Bucket(self,"ArtifactBucket",
                                   encryption=s3.BucketEncryption.S3_MANAGED,
                                    access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL)

        pipeline = cp.Pipeline(self,"calculator_pipeline",
                               pipeline_name=env_name+"-calculator_pipeline",
                               artifac_bucket=artifac_bucket,
                               restart_execution_on_update=False)
        Source_output = cp.Artifact(artifact_name="source")
        