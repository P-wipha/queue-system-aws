import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('queue_db')

def lambda_handler(event, context):
    response = table.scan()
    items = response.get('Items', [])

    with table.batch_writer() as batch:
        for item in items:
            batch.delete_item(
                Key={
                    'queue_id': item['queue_id']
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
            "message": "ล้างคิวทั้งหมดเรียบร้อยแล้ว"
        })
    }
