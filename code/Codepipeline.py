from aws_cdk import (Stack, aws_ssm as ssm, aws_s3 as s3, aws_iam as iam, aws_codepipeline as cp,
                     aws_codecommit as ccm , aws_codepipeline_actions as cp_actions,aws_codebuild as cb )
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
        build_project=cb.PipelineProject(self,"calculator_app",
                                         project_name="calculator",
                                         description="weighting calculator",
                                         environment=cb.BuildEnvironment(build_image=cb.LinuxBuildImage.STANDARD_3_0,
                                                                         environment_variables={
                                                                        "distibutionid": cb.BuildEnvironmentVariable(value=cdn_id)
                                                                         }),
                                         cache=cb.Cache.bucket(bucket=artifac_bucket,prefix="codebuild-cache"),
                                        )

        pipeline = cp.Pipeline(self,"calculator_pipeline",
                               pipeline_name=env_name+"-calculator_pipeline",
                               artifac_bucket=artifac_bucket,
                               restart_execution_on_update=False)
        source_output = cp.Artifact(artifact_name="source"),
        build_output = cp.Artifact(artifact_name="build")

        pipeline.add_stage(stage_name="Source", actions=[
            cp_actions.CodeCommitSourceAction(
                action_name="CodeCommitSource",
                repository=source_repo,
                output=source_output)])

        pipeline.add_stage(stage_name="Build",actions=[
            cp_actions.CodeBuildAction(
                action_name="Build",
                input=source_output,
                project=build_project,
                outputs=[build_output]
            )
        ])

        pipeline.add_stage(stage_name="Deploy",actions=[
             cp_actions.S3DeployAction(
                 bucket=cal_bucket,
                 input=build_output,
                 action_name="Deploy",
                 extract=True
             )
         ])

        build_project.role.add_to_principal_policy(iam.PolicyStatement(
            actions=["cloudfront:CreateInvalidation"],
            resources=["*"]
        ))