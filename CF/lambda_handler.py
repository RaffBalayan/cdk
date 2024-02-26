import boto3

def handler(event, context):
    client = boto3.client('cloudfront')
    distribution_id = 'E1QEX8XV0GDSNS'
    invalidation = client.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': ['/*']  # Invalidate all files; modify as needed
            },
            'CallerReference': str(event['time'])  # Use a unique reference
        }
    )
    return invalidation['Invalidation']['Id']
