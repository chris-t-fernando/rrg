import json

string = {
    "Records": [
        {
            "messageId": "7021de3e-5de9-413b-bab0-09ba937ee6ff",
            "receiptHandle": "AQEBSf6GS21orKx3Xy4WSBcFnHLjGAJdPAdfqCQYjdBNihwQFgJTNMyJa4gqA99n+zW9P/TJhXfk3Avcs+MvDbXgkJG7S1RZ309MzAL5Fqyt0YaNoziesXZxRGaEqDaozGjEiVKvHUpDKnZmzL4xvoUh3yFw867ukYCTmOjcU5bKT6FnyGRUfb9qXy+hwO+iL9OO0VxSH4G15pJCF6Pg4y7uYWDBnH4zUi4WZLprMIx+0HQB67kjvOCot6NJMRQqQKmWBR/g/ifXzvHkkAUYMvnstfXIxnR85P16hXe41nacyH9E7qCLNF2VsXWFHDfKcmNPW02x3umNMJYSoOPrZ7FBe7LrOKz39SkU9R/yEH8cYzQfHlrF7xaZG1vxJTcp5fBratNBLSgCAPfSCPSA6MnRYg==",
            "body": '{"quoteObject": [{"quote_date": "2021-04-26", "stock_code": "2be", "open": 0.04899999871850014, "high": 0.04899999871850014, "low": 0.04899999871850014, "close": 0.04899999871850014, "volume": 0}]}',
            "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1626478191721",
                "SenderId": "AIDAJBRAAZQ4REFJVXYLQ",
                "ApproximateFirstReceiveTimestamp": "1626478191723",
            },
            "messageAttributes": {
                "stock_code": {
                    "stringValue": "2be",
                    "stringListValues": [],
                    "binaryListValues": [],
                    "dataType": "String",
                }
            },
            "md5OfBody": "f343b83f553d7a87ed8f5b2e91cf11b8",
            "md5OfMessageAttributes": "d16f39891f89ea035c9b371fcbe85536",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:us-west-2:036372598227:quote-updates",
            "awsRegion": "us-west-2",
        }
    ]
}
