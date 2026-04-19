import json
import boto3
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
    phone = ""

    if event.get("queryStringParameters") and event["queryStringParameters"].get("phone"):
        phone = event["queryStringParameters"]["phone"]
    elif 'body' in event and event['body']:
        body = json.loads(event['body'])
        phone = body.get('phone', '')
    else:
        phone = event.get("phone", "")

    if not phone:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "กรุณาระบุเบอร์โทรศัพท์"
            })
        }

    response = table.scan()
    items = response.get('Items', [])

    active_status = ['waiting', 'near', 'confirmed', 'serving', 'called']

    matched = [
        item for item in items
        if item.get('phone') == phone and item.get('status') in active_status
    ]

    if not matched:
        return {
            "statusCode": 404,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "ไม่พบคิวที่ใช้งานอยู่สำหรับเบอร์โทรนี้"
            })
        }

    queue = sorted(matched, key=lambda x: int(x['queue_number']))[0]

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps(queue, default=decimal_converter)
    }
