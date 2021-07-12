import requests
import json
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

def useCaseZero():
    logging.info('=========================================')
    logging.info('starting use case zero')
    r = requests.get('http://127.0.0.1:8001/')
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))
    logging.info('finished use case zero')
    logging.info('=========================================')


# use case 1
def useCaseOne():
    logging.info('=========================================')
    logging.info('starting use case one')

    params = {
        'sectorTicker': [ 'xmj', 'xej' ]
    }

    r = requests.get('http://127.0.0.1:8001/sectors', json=params)
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))
    logging.info('finished use case one')
    logging.info('=========================================')


# use case 2
def useCaseTwo():
    logging.info('=========================================')
    logging.info('starting use case two')
    r = requests.get('http://127.0.0.1:8001/sectors/xej')
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))
    logging.info('finished use case two')
    logging.info('=========================================')


# use case 3
def useCaseThree():
    logging.info('=========================================')
    logging.info('starting use case three')
    params = {
        'tickers': [ '*' ]
    }

    r = requests.get('http://127.0.0.1:8001/tickers', json=params)
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))
    logging.info('finished use case three')
    logging.info('=========================================')


# use case 4
def useCaseFour():
    logging.info('=========================================')
    logging.info('starting use case four')
    r = requests.get('http://127.0.0.1:8001/tickers/bhp')
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))
    logging.info('finished use case four')
    logging.info('=========================================')


# use case 5
def useCaseFive():
    logging.info('=========================================')
    logging.info('starting use case five')
    r = requests.get('http://127.0.0.1:8001/quotes')
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))
    logging.info('finished use case five')
    logging.info('=========================================')

# use case 6
def useCaseSix():
    logging.info('=========================================')
    logging.info('starting use case six')
    r = requests.get('http://127.0.0.1:8001/quotes/weekly')
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))
    logging.info('finished use case six')
    logging.info('=========================================')

# use case 7
def useCaseSeven():
    logging.info('=========================================')
    logging.info('starting use case seven')
    params = {
        'tickers': [ 'avh', 'apt' ]
    }

    r = requests.get('http://127.0.0.1:8001/quotes/weekly/tickers', json=params)
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))
    logging.info('finished use case seven')
    logging.info('=========================================')

# use case 8
def useCaseEight():
    logging.info('=========================================')
    logging.info('starting use case eight')

    r = requests.get('http://127.0.0.1:8001/quotes/weekly/tickers/bhp')
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))
    logging.info('finished use case eight')
    logging.info('=========================================')


useCaseZero()
useCaseOne()
useCaseTwo()
useCaseThree()
useCaseFour()
useCaseFive()
useCaseSix()
useCaseSeven()
useCaseEight()
