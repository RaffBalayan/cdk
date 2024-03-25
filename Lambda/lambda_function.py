import boto3

def  lambda_handler(event, context):
    ssm = boto3.client('ssm')
    cloudfront = boto3.client('cloudfront')

    parameter = ssm.get_parameter(Name='/dev/app-distribution-id', WithDecryption=True)
    distribution_id = parameter['Parameter']['Value']

    invalidation = cloudfront.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': ['/*']
            },
            'CallerReference': 'some-unique-string'
        }
    )
    return invalidation
