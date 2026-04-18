import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('queue_db')   # เปลี่ยนถ้าชื่อตารางของแกไม่ใช่อันนี้

def lambda_handler(event, context):

    # รับข้อมูลจาก request
    if 'body' in event and event['body']:
        body = json.loads(event['body'])
    else:
        body = event

    name = body['name']
    phone = body['phone']
    device_id = body.get('device_id', 'unknown')

    now = datetime.now()
    queue_date = now.strftime('%Y-%m-%d')
    timestamp = now.strftime('%Y-%m-%dT%H:%M:%S')

    # ดึงข้อมูลทั้งหมดจาก DynamoDB
    response = table.scan()
    items = response.get('Items', [])

    # สถานะคิวที่ถือว่ายัง active
    active_status = ['waiting', 'near', 'confirmed', 'serving']

    # เช็กคิวซ้ำจาก phone หรือ device
    duplicate_queue = [
        item for item in items
        if (
            item.get('status') in active_status and
            (
                item.get('phone') == phone or
                item.get('device_id') == device_id
            )
        )
    ]

    # ถ้ามีคิวอยู่แล้ว
    if duplicate_queue:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "คุณมีคิวที่ยังไม่เสร็จอยู่แล้ว ไม่สามารถจองซ้ำได้"
            })
        }

    # หาเลขคิวของวันนี้
    today_items = [item for item in items if item.get('queue_date') == queue_date]

    if not today_items:
        next_queue = 1
    else:
        max_queue = max(int(item['queue_number']) for item in today_items)
        next_queue = max_queue + 1

    queue_id = f"Q{queue_date.replace('-', '')}-{str(next_queue).zfill(4)}"

    # บันทึกคิวใหม่
    table.put_item(
        Item={
            'queue_id': queue_id,
            'queue_date': queue_date,
            'queue_number': next_queue,
            'name': name,
            'phone': phone,
            'device_id': device_id,
            'status': 'waiting',
            'confirmed': False,
            'cancelled_by': 'none',
            'created_at': timestamp,
            'updated_at': timestamp
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
            "queue_id": queue_id,
            "queue_number": next_queue
        })
    }
