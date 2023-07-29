from aws_cdk import core
from aws_cdk import aws_codecommit, aws_codebuild, aws_codepipeline, aws_codepipeline_actions
from aws_cdk import aws_s3, aws_cloudfront, aws_route53, aws_route53_targets

class MyCdkAppStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a CodeCommit repository
        code_commit_repo = aws_codecommit.Repository(self, "MyCodeCommitRepo", repository_name="MyAppRepo")

        # Create an S3 bucket
        s3_bucket = aws_s3.Bucket(self, "MyS3Bucket")

        # Create a CodeBuild project
        code_build_project = aws_codebuild.PipelineProject(self, "MyCodeBuildProject",
            build_spec=aws_codebuild.BuildSpec.from_object(dict(
                version="0.2",
                phases=dict(
                    install=dict(
                        commands=[
                            "echo 'Installing dependencies...'",
                            "pip install -r requirements.txt",
                        ]
                    ),
                    build=dict(
                        commands=[
                            "echo 'Building the code...'",
                            "python build.py",  # Replace with your build script commands
                        ]
                    )
                ),
                artifacts=dict(
                    files=["**/*"]
                )
            ))
        )

        # Create a CodePipeline
        pipeline = aws_codepipeline.Pipeline(self, "MyCodePipeline")

        # Add CodeCommit as the source stage
        source_stage = pipeline.add_stage(stage_name="Source")
        source_action = aws_codepipeline_actions.CodeCommitSourceAction(
            action_name="CodeCommit_Source",
            repository=code_commit_repo,
            output=aws_codepipeline.Artifact(artifact_name="SourceOutput")
        )
        source_stage.add_action(source_action)

        # Add CodeBuild as the build stage
        build_stage = pipeline.add_stage(stage_name="Build")
        build_action = aws_codepipeline_actions.CodeBuildAction(
            action_name="CodeBuild_Build",
            project=code_build_project,
            input=source_action.output_output
        )
        build_stage.add_action(build_action)

        # Add S3 deployment stage
        deploy_stage = pipeline.add_stage(stage_name="Deploy")
        deploy_action = aws_codepipeline_actions.S3DeployAction(
            action_name="S3_Deploy",
            input=build_action.output_artifact,
            bucket=s3_bucket,
        )
        deploy_stage.add_action(deploy_action)

        # Create CloudFront distribution
        cloudfront_distribution = aws_cloudfront.CloudFrontWebDistribution(self, "MyCloudFrontDistribution",
            origin_configs=[
                aws_cloudfront.SourceConfiguration(
                    s3_origin_source=aws_cloudfront.S3OriginConfig(s3_bucket_source=s3_bucket),
                    behaviors=[aws_cloudfront.Behavior(is_default_behavior=True)]
                )
            ]
        )

        # Create Route 53 Alias record for CloudFront
        hosted_zone = aws_route53.HostedZone.from_lookup(self, "MyHostedZone", domain_name="example.com")
        alias_record = aws_route53.ARecord(self, "CloudFrontAliasRecord",
            zone=hosted_zone,
            target=aws_route53.RecordTarget.from_alias(aws_route53_targets.CloudFrontTarget(cloudfront_distribution))
        )

app = core.App()
MyCdkAppStack(app, "MyCdkAppStack")
app.synth()
