import json

event = {
    "Records": [
        {
            "messageId": "9448d492-be1e-4465-8d1a-8edab7473256",
            "receiptHandle": "AQEBofb9Xl1WI5U3lJaWH7QvtuIuWKGjOkdzTCubjvOp+2GnDMM80TCfBPOQFcgGzSiPk4nb7Ek224mabZFB3NrkQY6JdyrBD1d1BjtOxd1sPrrGGpZERb7NBRRrkh1GDF7cex2Y3yDYRN+CdKadYP6eUAJzPh5nRg9/wLr+qtiuFNaNZQQRJLq6/xJz9tZtYpytj6gJrNnsOkdFlJuIRZnN1xKz8sLreCxitE8nGtwMKIFwUKWoOze8caWUcG9MFzzeAobfkL/HV3lXsqbNyHEmWFwJW3LVNy2lijImTYv55J1EODLBHNhzS573F4lZSSszY3rUQCja2h70qqO8vMURDauYTSWc0RUgUvynsKfFLk9sGLDi6006syEuIrwkKc9ju00yfIrSTA2P+Aa7bd2ilA==",
            "body": '{"quoteObject": [{"quote_date": "2020-10-19", "stock_code": "aby", "open": 7.400000095367432, "high": 7.420000076293945, "low": 6.800000190734863, "close": 6.920000076293945, "volume": 4271698}, {"quote_date": "2020-10-26", "stock_code": "aby", "open": 7.0, "high": 7.039999961853027, "low": 5.489999771118164, "close": 5.699999809265137, "volume": 5124079}, {"quote_date": "2020-11-02", "stock_code": "aby", "open": 6.0, "high": 6.380000114440918, "low": 5.739999771118164, "close": 6.150000095367432, "volume": 1569525}, {"quote_date": "2020-11-09", "stock_code": "aby", "open": 6.309999942779541, "high": 6.519999980926514, "low": 5.800000190734863, "close": 6.0, "volume": 2952414}, {"quote_date": "2020-11-16", "stock_code": "aby", "open": 6.190000057220459, "high": 6.760000228881836, "low": 6.119999885559082, "close": 6.690000057220459, "volume": 1327205}, {"quote_date": "2020-11-23", "stock_code": "aby", "open": 6.699999809265137, "high": 6.980000019073486, "low": 6.389999866485596, "close": 6.46999979019165, "volume": 1232343}, {"quote_date": "2020-11-30", "stock_code": "aby", "open": 6.599999904632568, "high": 6.739999771118164, "low": 5.820000171661377, "close": 5.900000095367432, "volume": 1677530}, {"quote_date": "2020-12-07", "stock_code": "aby", "open": 6.0, "high": 6.019999980926514, "low": 5.079999923706055, "close": 5.360000133514404, "volume": 1826833}, {"quote_date": "2020-12-14", "stock_code": "aby", "open": 5.46999979019165, "high": 5.480000019073486, "low": 5.150000095367432, "close": 5.289999961853027, "volume": 576227}, {"quote_date": "2020-12-21", "stock_code": "aby", "open": 5.289999961853027, "high": 5.699999809265137, "low": 5.099999904632568, "close": 5.53000020980835, "volume": 324762}, {"quote_date": "2020-12-28", "stock_code": "aby", "open": 5.53000020980835, "high": 5.769999980926514, "low": 5.369999885559082, "close": 5.380000114440918, "volume": 198346}, {"quote_date": "2021-01-04", "stock_code": "aby", "open": 5.380000114440918, "high": 5.690000057220459, "low": 5.369999885559082, "close": 5.400000095367432, "volume": 167762}, {"quote_date": "2021-01-11", "stock_code": "aby", "open": 5.400000095367432, "high": 5.579999923706055, "low": 5.300000190734863, "close": 5.460000038146973, "volume": 161361}, {"quote_date": "2021-01-18", "stock_code": "aby", "open": 5.53000020980835, "high": 6.380000114440918, "low": 5.460000038146973, "close": 6.130000114440918, "volume": 2290841}, {"quote_date": "2021-01-25", "stock_code": "aby", "open": 6.199999809265137, "high": 6.349999904632568, "low": 5.610000133514404, "close": 5.75, "volume": 542048}, {"quote_date": "2021-02-01", "stock_code": "aby", "open": 5.679999828338623, "high": 5.869999885559082, "low": 5.349999904632568, "close": 5.5, "volume": 982934}, {"quote_date": "2021-02-08", "stock_code": "aby", "open": 5.510000228881836, "high": 5.880000114440918, "low": 5.510000228881836, "close": 5.599999904632568, "volume": 197233}, {"quote_date": "2021-02-15", "stock_code": "aby", "open": 5.550000190734863, "high": 5.849999904632568, "low": 5.420000076293945, "close": 5.449999809265137, "volume": 281667}, {"quote_date": "2021-02-22", "stock_code": "aby", "open": 5.519999980926514, "high": 6.329999923706055, "low": 5.199999809265137, "close": 5.400000095367432, "volume": 1739351}, {"quote_date": "2021-03-01", "stock_code": "aby", "open": 5.480000019073486, "high": 5.590000152587891, "low": 4.860000133514404, "close": 4.860000133514404, "volume": 987552}, {"quote_date": "2021-03-08", "stock_code": "aby", "open": 4.96999979019165, "high": 5.360000133514404, "low": 4.590000152587891, "close": 5.300000190734863, "volume": 1105687}, {"quote_date": "2021-03-15", "stock_code": "aby", "open": 5.320000171661377, "high": 5.449999809265137, "low": 5.150000095367432, "close": 5.170000076293945, "volume": 522575}, {"quote_date": "2021-03-22", "stock_code": "aby", "open": 5.360000133514404, "high": 5.360000133514404, "low": 4.940000057220459, "close": 5.199999809265137, "volume": 419875}, {"quote_date": "2021-03-29", "stock_code": "aby", "open": 5.239999771118164, "high": 5.239999771118164, "low": 5.0, "close": 5.03000020980835, "volume": 142416}, {"quote_date": "2021-04-05", "stock_code": "aby", "open": 5.03000020980835, "high": 5.099999904632568, "low": 4.989999771118164, "close": 5.0, "volume": 130638}, {"quote_date": "2021-04-12", "stock_code": "aby", "open": 5.0, "high": 5.019999980926514, "low": 4.920000076293945, "close": 5.0, "volume": 319932}, {"quote_date": "2021-04-19", "stock_code": "aby", "open": 5.010000228881836, "high": 5.010000228881836, "low": 4.599999904632568, "close": 4.679999828338623, "volume": 316977}, {"quote_date": "2021-04-26", "stock_code": "aby", "open": 4.679999828338623, "high": 5.0, "low": 4.519999980926514, "close": 4.840000152587891, "volume": 823830}, {"quote_date": "2021-05-03", "stock_code": "aby", "open": 4.849999904632568, "high": 4.849999904632568, "low": 3.6500000953674316, "close": 3.680000066757202, "volume": 1937081}, {"quote_date": "2021-05-10", "stock_code": "aby", "open": 3.700000047683716, "high": 3.869999885559082, "low": 3.309999942779541, "close": 3.319999933242798, "volume": 1454438}, {"quote_date": "2021-05-17", "stock_code": "aby", "open": 3.430000066757202, "high": 3.8399999141693115, "low": 3.325000047683716, "close": 3.799999952316284, "volume": 446986}, {"quote_date": "2021-05-24", "stock_code": "aby", "open": 3.799999952316284, "high": 4.21999979019165, "low": 3.799999952316284, "close": 4.119999885559082, "volume": 578201}, {"quote_date": "2021-05-31", "stock_code": "aby", "open": 4.190000057220459, "high": 4.5, "low": 4.0, "close": 4.440000057220459, "volume": 551744}, {"quote_date": "2021-06-07", "stock_code": "aby", "open": 4.440000057220459, "high": 4.769999980926514, "low": 4.440000057220459, "close": 4.550000190734863, "volume": 471601}, {"quote_date": "2021-06-14", "stock_code": "aby", "open": 4.53000020980835, "high": 4.550000190734863, "low": 4.340000152587891, "close": 4.340000152587891, "volume": 299072}, {"quote_date": "2021-06-21", "stock_code": "aby", "open": 4.480000019073486, "high": 4.599999904632568, "low": 4.385000228881836, "close": 4.449999809265137, "volume": 386745}, {"quote_date": "2021-06-28", "stock_code": "aby", "open": 4.449999809265137, "high": 4.639999866485596, "low": 4.210000038146973, "close": 4.550000190734863, "volume": 413625}, {"quote_date": "2021-07-05", "stock_code": "aby", "open": 4.610000133514404, "high": 5.0, "low": 4.53000020980835, "close": 4.909999847412109, "volume": 359939}, {"quote_date": "2021-07-12", "stock_code": "aby", "open": 4.920000076293945, "high": 5.300000190734863, "low": 4.920000076293945, "close": 5.260000228881836, "volume": 397117}, {"quote_date": "2021-07-16", "stock_code": "aby", "open": 5.159999847412109, "high": 5.300000190734863, "low": 5.150000095367432, "close": 5.260000228881836, "volume": 86018}]}',
            "attributes": {
                "ApproximateReceiveCount": "9",
                "SentTimestamp": "1626437868963",
                "SenderId": "AIDAJBRAAZQ4REFJVXYLQ",
                "ApproximateFirstReceiveTimestamp": "1626437868963",
            },
            "messageAttributes": {
                "stock_code": {
                    "stringValue": "aby",
                    "stringListValues": [],
                    "binaryListValues": [],
                    "dataType": "String",
                }
            },
            "md5OfMessageAttributes": "509db5a294598afaf734a535e46bc374",
            "md5OfBody": "11b0add27982b0782b66e2ec3ea36d8f",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:us-west-2:036372598227:quote-updates",
            "awsRegion": "us-west-2",
        }
    ]
}

if "Records" in event.keys():
    if len(event["Records"]) == 1:
        if not "body" in event["Records"][0].keys():
            #        if not "quoteObject" in event["Records"][0]["body"].keys():
            #            print("Unable to find quoteObject in body")
            #            # return False
            #    else:
            print("Unable to find body in Records")
            # return False
    else:
        print("Expected only a single element in SQS Records List")
else:
    print("Unable to find Records in payload")
    # return False

listOfQuotes = json.loads(event["Records"][0]["body"])
# print(json.dumps(listOfQuotes))

# if "quoteObject" in listOfQuotes.key():
# print(str(type(listOfQuotes)))
if "quoteObject" in listOfQuotes.keys():
    for x in listOfQuotes["quoteObject"]:
        print(x["stock_code"])
