import boto3

def handler(event, context):
    client = boto3.client('cloudfront')
    distribution_id = 'EBCA00R8AL6FK'
    invalidation = client.create_invalidation(
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
