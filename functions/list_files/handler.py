import boto3
import json
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    try:
        table = dynamodb.Table(os.environ['TABLE_NAME'])

        params = event.get('queryStringParameters') or {}
        owner = params.get('owner')

        if owner:
            result = table.query(
                IndexName='owner-index',
                KeyConditionExpression=Key('owner').eq(owner)
            )
        else:
            result = table.scan()

        items = result.get('Items', [])

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(items, default=str)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }