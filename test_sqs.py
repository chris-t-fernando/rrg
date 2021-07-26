import boto3

sqsClient = boto3.client("sqs")

response = sqsClient.receive_message(
    QueueUrl="https://sqs.us-west-2.amazonaws.com/036372598227/quote-updates"
)

print(response)
