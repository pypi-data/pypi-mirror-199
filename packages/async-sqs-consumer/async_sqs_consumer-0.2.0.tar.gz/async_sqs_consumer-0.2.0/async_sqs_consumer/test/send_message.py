import boto3
import json
import uuid

client = boto3.client("sqs", region_name="us-east-1")

for _ in range(30):
    client.send_message(
        QueueUrl=(
            "https://sqs.us-east-1.amazonaws.com/205810638802/integrates_rebase"
        ),
        MessageBody=json.dumps(
            {
                "task": "report",
                "id": uuid.uuid4().hex,
                "args": ["hello world"],
            }
        ),
    )
