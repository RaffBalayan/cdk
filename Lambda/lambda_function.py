# lambda_function.py

import boto3
import json

def lambda_handler(event, context):
    cloudfront = boto3.client('cloudfront')
    distribution_id = 'E1QEX8XV0GDSNS'
    invalidation = cloudfront.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': [
                    '/*'  # Invalidate everything. Adjust this to target specific paths.
                ]
            },
            'CallerReference': str(event['time'])  # Use the event time as a unique reference
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Cache invalidation request submitted successfully.')
    }
