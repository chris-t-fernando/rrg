import requests
import json
import logging, sys

# from fastapi.testclient import TestClient
# from rest_api.driver_main import app
import pytest
import boto3

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# client = TestClient(app)

ssm = boto3.client("ssm")
rest_endpoint = (
    ssm.get_parameter(Name="/rrg-creator/rest-endpoint").get("Parameter").get("Value")
)


def startBanner(testNumber):
    logging.info("=========================================")
    logging.info(f"starting use case {testNumber}")


def endBanner(testNumber):
    logging.info(f"finished use case {testNumber}")
    logging.info("=========================================")


@pytest.mark.parametrize(
    "route, parameter, http_response",
    [
        # fakeroute
        ("/fakeroute", None, 404),
        # stock use case 1
        # uc1-noparm
        ("/stock", None, 200),
        # uc1-1parm
        ("/stock", {"stock_code": ["z1p"]}, 200),
        # uc1-2parm
        ("/stock", {"stock_code": ["avh", "bhp"]}, 200),
        # uc1-1longparm
        # todo: handle invalid stock_codes better - maybe have a key at the end of the return showing ignored/invalid stock_codes?
        ("/stock", {"stock_code": ["long code"]}, 404),
        # uc1-1invalidparm
        ("/stock", {"stock_code": ["zzz"]}, 404),
        # uc1-badkey
        ("/stock", {"fake_key": ["fake_code"]}, 400),
        # stock use case 2
        # uc2-goodcode
        ("/stock/bhp", None, 200),
        # uc2-longcode
        ("/stock/fake_stock", None, 404),
        # uc2-invalidcode
        ("/stock/zzz", None, 404),
        # stock use case 3
        # uc3-goodcode
        ("/stock/14d/quotes/weekly", None, 200),
        # uc3-badroute
        ("/stock/14d/quotes/fakeendpoint", None, 404),
        # uc3-longcode
        ("/stock/fake_stock/quotes/weekly", None, 404),
        # uc3-invalidcode
        ("/stock/zzz/quotes/weekly", None, 404),
        # uc3-startdate
        ("/stock/14d/quotes/weekly", {"start_date": "2021-01-01"}, 200),
        # uc3-enddate
        ("/stock/14d/quotes/weekly", {"end_date": "2021-01-01"}, 200),
        # uc3-startandenddates
        (
            "/stock/14d/quotes/weekly",
            {"start_date": "2021-01-01", "end_date": "2021-02-01"},
            200,
        ),
        # uc3-endbeforestart
        (
            "/stock/14d/quotes/weekly",
            {"start_date": "2022-12-31", "end_date": "2021-01-01"},
            200,
        ),
        # uc3-periodd
        ("/stock/14d/quotes/weekly", {"period": "10d"}, 200),
        # uc3-periodw
        ("/stock/14d/quotes/weekly", {"period": "3w"}, 200),
        # uc3-periodm
        ("/stock/14d/quotes/weekly", {"period": "1m"}, 200),
        # uc3-periody
        ("/stock/14d/quotes/weekly", {"period": "1y"}, 200),
        # uc3-periodblank
        ("/stock/14d/quotes/weekly", {"period": ""}, 400),  # invalid period
        # uc3-periodnone
        ("/stock/14d/quotes/weekly", {"period": None}, 400),  # invalid period
        # uc3-invalidparm
        ("/stock/14d/quotes/weekly", {"fake_parameter": None}, 400),  # invalid request
        # stock use case 4???
        # stock use case 5
        # uc5-noparm
        ("/quote/weekly/stock", None, 200),
        # uc5-1parm
        ("/quote/weekly/stock", {"stock_code": ["14d"]}, 200),  # one valid code
        # uc5-2parm
        (
            "/quote/weekly/stock",
            {"stock_code": ["14d", "bhp"]},
            200,
        ),
        # uc5-1invalidparm
        (
            "/quote/weekly/stock",
            {"stock_code": ["zzz", "bhp"]},
            200,
        ),
        # uc5-1longparm
        (
            "/quote/weekly/stock",
            {"stock_code": ["code too long", "bhp"]},
            200,
        ),
        # uc5-badparmtype
        (
            "/quote/weekly/stock",
            {"stock_code": "bad_type"},
            400,
        ),
        # uc5-stocknone
        (
            "/quote/weekly/stock",
            {"stock_code": None},
            400,
        ),
        # uc5-badparm
        ("/quote/weekly/stock", {"fake_parameter": None}, 400),  # invalid request
        # stock use case 6
        # uc6-goodquote
        ("/quote/stock/weekly/2021-03-15", None, 200),
        # uc6-goodquote1parm
        (
            "/quote/stock/weekly/2021-03-15",
            {"stock_code": ["bhp"]},
            200,
        ),
        # uc6-goodquote2parm
        (
            "/quote/stock/weekly/2021-03-15",
            {"stock_code": ["bhp", "avh"]},
            200,
        ),
        # uc6-1longparm
        (
            "/quote/stock/weekly/2021-03-15",
            {"stock_code": ["one bad parameter", "avh"]},
            200,
        ),
        # uc6-invalidquote
        ("/quote/stock/weekly/2021-03-14", None, 404),  # no weekly data for this date
        # uc6-badparmtype
        ("/quote/stock/weekly/2021-03-15", {"stock_code": "bad type"}, 400),  # bad type
        # uc6-invalidcode
        ("/quote/stock/weekly/2021-03-15", {"stock_code": ["zzz"]}, 404),  # fake code
        # uc6-stocknone
        (
            "/quote/stock/weekly/2021-03-15",
            {"stock_code": None},
            400,
        ),
        # uc6-longcode
        (
            "/quote/stock/weekly/2021-03-15",
            {"stock_code": ["code too long"]},
            400,
        ),
        # uc6-badparm
        (
            "/quote/stock/weekly/2021-03-15",
            {"fake_parameter": ["avh"]},
            400,
        ),
    ],
    ids=[
        "fakeroute",
        "uc1-noparm",
        "uc1-1parm",
        "uc1-2parm",
        "uc1-1longparm",
        "uc1-1invalidparm",
        "uc1-badkey",
        "uc2-goodcode",
        "uc2-longcode",
        "uc2-invalidcode",
        "uc3-goodcode",
        "uc3-badroute",
        "uc3-longcode",
        "uc3-invalidcode",
        "uc3-startdate",
        "uc3-enddate",
        "uc3-startandenddates",
        "uc3-endbeforestart",
        "uc3-periodd",
        "uc3-periodw",
        "uc3-periodm",
        "uc3-periody",
        "uc3-periodblank",
        "uc3-periodnone",
        "uc3-invalidparm",
        "uc5-noparm",
        "uc5-1parm",
        "uc5-2parm",
        "uc5-1invalidparm",
        "uc5-1longparm",
        "uc5-badparmtype",
        "uc5-stocknone",
        "uc5-badparm",
        "uc6-goodquote",
        "uc6-goodquote1parm",
        "uc6-goodquote2parm",
        "uc6-1longparm",
        "uc6-invalidquote",
        "uc6-badparmtype",
        "uc6-invalidcode",
        "uc6-stocknone",
        "uc6-longcode",
        "uc6-badparm",
    ],
)
def test_rest_api(route, parameter, http_response):
    # response = client.get(route, json=parameter)
    response = requests.get(rest_endpoint + route, json=parameter)
    if not response.status_code == http_response:
        pass
    assert response.status_code == http_response


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
