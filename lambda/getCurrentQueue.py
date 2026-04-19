import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('queue_db')

def lambda_handler(event, context):
    response = table.scan()
    items = response.get('Items', [])

    waiting_items = [item for item in items if item.get('status') == 'waiting']

    if not waiting_items:
        current_queue = 0
    else:
        current_queue = min(int(item['queue_number']) for item in waiting_items)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "current_queue": current_queue
        })
    }
