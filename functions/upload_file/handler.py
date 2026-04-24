import boto3
import uuid
import time
import json
import os

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    try:
        body = json.loads(event['body'])
        filename = body['filename']
        size = body.get('size', 0)
        owner = body.get('owner', 'anonymous')

        file_id = str(uuid.uuid4())
        s3_key = f"uploads/{file_id}/{filename}"

        # Generate presigned URL for upload
        upload_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': os.environ['BUCKET_NAME'],
                'Key': s3_key
            },
            ExpiresIn=300
        )

        # Save metadata to DynamoDB
        table = dynamodb.Table(os.environ['TABLE_NAME'])
        table.put_item(Item={
            'file_id': file_id,
            'filename': filename,
            'size': size,
            'owner': owner,
            'timestamp': int(time.time()),
            's3_key': s3_key
        })

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'file_id': file_id,
                'upload_url': upload_url
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }