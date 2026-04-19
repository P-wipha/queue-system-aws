import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('queue_db')

def lambda_handler(event, context):

    if 'body' in event and event['body']:
        body = json.loads(event['body'])
    else:
        body = event

    queue_id = body.get('queue_id')
    status = body.get('status')

    if not queue_id or not status:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "กรุณาระบุ queue_id และ status"
            })
        }

    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    table.update_item(
        Key={
            'queue_id': queue_id
        },
        UpdateExpression="SET #s = :s, updated_at = :u",
        ExpressionAttributeNames={
            '#s': 'status'
        },
        ExpressionAttributeValues={
            ':s': status,
            ':u': now
        }
    )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": f"อัปเดตสถานะเป็น {status} สำเร็จ"
        })
    }
