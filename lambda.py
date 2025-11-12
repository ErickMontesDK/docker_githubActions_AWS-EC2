import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    sns = boto3.client('sns', region_name='us-east-1')  
    TOPIC_ARN = 'arn:aws:sns:TU-ARN-REAL-AQUÍ'  # Topic ARN
    
    try:
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
    except json.JSONDecodeError:
        body = {}  # Fallback
    
    status = body.get('status', 'unknown')
    message = body.get('message', 'Deploy completado sin detalles.')
    
    if status == 'success':
        subject = '✅ Deploy succesful in EC2'
        body_text = f'The deploy to EC2 was successful!\n\nDetails: {message}\n\nRepo: {body.get("repo", "N/A")}\nCommit: {body.get("commit", "N/A")}'
    elif status == 'failure':
        subject = '❌ Deploy failed in EC2'
        body_text = f'The deploy to EC2 failed!\n\nError: {message}\n\nRepo: {body.get("repo", "N/A")}\nCommit: {body.get("commit", "N/A")}'
    else:
        subject = 'ℹ️ Deploy status in EC2'
        body_text = f'Status: {status}\n\nDetails: {message}'
    try:
        response = sns.publish(TopicArn=TOPIC_ARN, Message=body_text, Subject=subject)
        return {'statusCode': 200, 'body': json.dumps({'message': 'Notification sent via SNS'})}
    except ClientError as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}       