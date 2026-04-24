import boto3
import json
import os

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    try:
        file_id = event['pathParameters']['file_id']

        table = dynamodb.Table(os.environ['TABLE_NAME'])
        result = table.get_item(Key={'file_id': file_id})

        if 'Item' not in result:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'File not found'})
            }

        item = result['Item']

        download_url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': os.environ['BUCKET_NAME'],
                'Key': item['s3_key']
            },
            ExpiresIn=300
        )

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'file_id': file_id,
                'filename': item['filename'],
                'download_url': download_url
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }