import json
import boto3
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('queue_db')

def decimal_converter(obj):
    if isinstance(obj, Decimal):
        if obj % 1 == 0:
            return int(obj)
        return float(obj)
    raise TypeError

def lambda_handler(event, context):

    response = table.scan()
    items = response.get('Items', [])

    waiting_items = [item for item in items if item.get('status') == 'waiting']

    if not waiting_items:
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "ไม่มีคิวที่รออยู่",
                "called_queue": None
            }, default=decimal_converter)
        }

    current_item = min(waiting_items, key=lambda x: int(x['queue_number']))

    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    table.update_item(
        Key={
            'queue_id': current_item['queue_id']
        },
        UpdateExpression="SET #s = :s, updated_at = :u",
        ExpressionAttributeNames={
            '#s': 'status'
        },
        ExpressionAttributeValues={
            ':s': 'done',
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
            "message": f"เรียกคิว {current_item['queue_number']} แล้ว",
            "called_queue": current_item['queue_number']
        }, default=decimal_converter)
    }