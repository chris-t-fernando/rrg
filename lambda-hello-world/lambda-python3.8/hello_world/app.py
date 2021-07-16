from __future__ import print_function
import json
import boto3
import pymysql.cursors

# import traceback
# import logging, sys

# handler for pulling config from SSM
def getSSMParameter(ssm, parameterPath, encryptionOption=False):
    return (
        ssm.get_parameter(Name=parameterPath, WithDecryption=encryptionOption)
        .get("Parameter")
        .get("Value")
    )


# can only reference tuples by position index, not by column name - annoying!
# shamelessly stolen from https://kadler.io/2018/01/08/fetching-python-database-cursors-by-column-name.html#
class CursorByName:
    def __init__(self, cursor):
        self._cursor = cursor

    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()
        return {
            description[0]: row[col]
            for col, description in enumerate(self._cursor.description)
        }


def lambda_handler(event, context):

    # print(json.dumps(event))

    # set up boto SSM
    ssmClient = boto3.client("ssm")

    connection = pymysql.connect(
        host=getSSMParameter(ssmClient, "/rrg-creator/rds-endpoint"),
        user=getSSMParameter(ssmClient, "/rrg-creator/rds-user"),
        password=getSSMParameter(ssmClient, "/rrg-creator/rds-password", True),
        database=getSSMParameter(ssmClient, "/rrg-creator/rds-database"),
        cursorclass=pymysql.cursors.DictCursor,
    )

    sqlSelect = "select count(*) from weekly_stock_quotes where stock_code = %s and quote_date = %s"

    insertQuotes = []

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

    with connection:
        with connection.cursor() as cursor:
            listOfQuotes = json.loads(event["Records"][0]["body"])
            if not "quoteObject" in listOfQuotes.keys():
                print("Unable to find quoteObject in payload")
                return False

            for x in listOfQuotes["quoteObject"]:
                sqlParameters = (
                    x["stock_code"],
                    x["quote_date"],
                )
                cursor.execute(sqlSelect, sqlParameters)
                result = cursor.fetchone()
                # print(result["count(*)"])
                if result["count(*)"] == 0:
                    print(
                        f"Queuing for insert: stock_code: {x['stock_code']} quote for date: {x['quote_date']}"
                    )
                    insertQuotes.append(
                        (
                            x["quote_date"],
                            x["stock_code"],
                            x["open"],
                            x["high"],
                            x["low"],
                            x["close"],
                            x["volume"],
                        )
                    )

                else:
                    print(
                        f"Skipping stock_code: {x['stock_code']} quote for date: {x['quote_date']}"
                    )

            sqlInsert = "insert into weekly_stock_quotes (quote_date, stock_code, open_price, high_price, low_price, close_price, volume) values (%s, %s, %s, %s, %s, %s, %s)"

            try:
                for y in insertQuotes:
                    # print(sqlInsert, y)
                    # now do the inserts
                    cursor.execute(sqlInsert, y)

                connection.commit()
                print("Successfully inserted quotes")
            except Exception as e:
                print(f"Failed to insert: {str(e)}")

    return ""
