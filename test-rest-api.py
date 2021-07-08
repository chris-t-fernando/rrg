import requests
import json
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.INFO)


def startBanner(testNumber):
    logging.info("=========================================")
    logging.info(f"starting use case {testNumber}")


def endBanner(testNumber):
    logging.info(f"finished use case {testNumber}")
    logging.info("=========================================")


# use case 1
def useCaseOne():
    useCase = "one"
    startBanner(useCase)

    params = {"stock_code": ["avh", "bhp"]}

    r = requests.get("http://127.0.0.1:8001/stock", json=params)
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))

    endBanner(useCase)


# use case 2
def useCaseTwo():
    useCase = "two"
    startBanner(useCase)

    r = requests.get("http://127.0.0.1:8001/stock/bhp")
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))

    endBanner(useCase)


# use case 3
def useCaseThree():
    useCase = "three"
    startBanner(useCase)

    r = requests.get("http://127.0.0.1:8001/stock/14d/quotes/weekly")
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))

    endBanner(useCase)


# use case 4
def useCaseFour(dot, params=None):
    useCase = "Four" + dot
    startBanner(useCase)

    if params == None:
        r = requests.get("http://127.0.0.1:8001/stock/14d/quotes/weekly")
    else:
        r = requests.get("http://127.0.0.1:8001/stock/14d/quotes/weekly", json=params)

    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))

    endBanner(useCase)


# use case 5
def useCaseFive(dot, params=None):
    useCase = "Five" + dot
    startBanner(useCase)

    if params == None:
        r = requests.get("http://127.0.0.1:8001/quote/weekly/stock")
    else:
        r = requests.get("http://127.0.0.1:8001/quote/weekly/stock", json=params)

    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))

    endBanner(useCase)


# use case 6
def useCaseSix(dot, params=None):
    useCase = "Six" + dot
    startBanner(useCase)

    if params == None:
        r = requests.get("http://127.0.0.1:8001/quote/stock/weekly/2021-03-15")
    else:
        r = requests.get(
            "http://127.0.0.1:8001/quote/stock/weekly/2021-03-15", json=params
        )

    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))

    endBanner(useCase)


# useCaseOne()
# useCaseTwo()
# useCaseThree()
# useCaseFour('1', params = {
#        'start_date': '2021-01-01'
#    }
# )

# useCaseFour('2', params = {
#        'end_date': '2021-01-01'
#    }
# )

# useCaseFour('3', params = {
#        'start_date': '2021-01-01',
#        'end_date': '2021-02-01'
#    }
# )

# useCaseFour('4', params = {
#        'period': '10d'
#    }
# )

# useCaseFour('5', params = {
#        'period': '3w'
#    }
# )

# useCaseFour('6', params = {
#        'period': '1m'
#    }
# )

# useCaseFour('7', params = {
#        'period': '1y'
#    }
# )

# useCaseFour('8', params = None)

# useCaseFive("1", params=None)
# useCaseFive("2", params={"stock_code": ["14d", "bhp"]})

# useCaseSix("1")
# useCaseSix("2", params={"stock_code": ["bhp"]})


# SECTOR TESTS
# use case 1
def sectorUseCaseOne():
    useCase = "one"
    startBanner(useCase)

    params = {"sector_code": ["xmj", "xij"]}

    r = requests.get("http://127.0.0.1:8001/sector", json=params)
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))

    endBanner(useCase)


# use case 2
def sectorUseCaseTwo():
    useCase = "two"
    startBanner(useCase)

    r = requests.get("http://127.0.0.1:8001/sector/xmj")
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))

    endBanner(useCase)


# use case 3
def sectorUseCaseThree():
    useCase = "three"
    startBanner(useCase)

    r = requests.get("http://127.0.0.1:8001/sector/xmj/quotes/weekly")
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))

    endBanner(useCase)


# use case 4
def sectorUseCaseFour(dot, params=None):
    useCase = "Four" + dot
    startBanner(useCase)

    if params == None:
        r = requests.get("http://127.0.0.1:8001/sector/xmj/quotes/weekly")
    else:
        r = requests.get("http://127.0.0.1:8001/sector/xmj/quotes/weekly", json=params)

    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))

    endBanner(useCase)


# use case 5
def sectorUseCaseFive(dot, params=None):
    useCase = "Five" + dot
    startBanner(useCase)

    if params == None:
        r = requests.get("http://127.0.0.1:8001/quote/sector/weekly")
    else:
        r = requests.get("http://127.0.0.1:8001/quote/sector/weekly", json=params)

    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))

    endBanner(useCase)


# use case 6
def sectorUseCaseSix(dot, params=None):
    useCase = "Six" + dot
    startBanner(useCase)

    if params == None:
        r = requests.get("http://127.0.0.1:8001/quote/sector/weekly/2021-03-14")
    else:
        r = requests.get(
            "http://127.0.0.1:8001/quote/sector/weekly/2021-03-14", json=params
        )

    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))

    endBanner(useCase)


sectorUseCaseOne()
sectorUseCaseTwo()
sectorUseCaseThree()
sectorUseCaseFour("4", params={"period": "100d"})

sectorUseCaseFour("5", params={"period": "10w"})

sectorUseCaseFour("6", params={"period": "2m"})

sectorUseCaseFour("7", params={"period": "1y"})

sectorUseCaseFour("8", params=None)

sectorUseCaseFive("1", params=None)
sectorUseCaseFive("2", params={"sector_code": ["xmj", "xij"]})

sectorUseCaseSix("1")
sectorUseCaseSix("2", params={"sector_code": ["xmj"]})
