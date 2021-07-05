import requests
import json
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

def startBanner(testNumber):
    logging.info('=========================================')
    logging.info(f'starting use case {testNumber}')

def endBanner(testNumber):
    logging.info(f'finished use case {testNumber}')
    logging.info('=========================================')


# use case 1
def useCaseOne():
    useCase = 'one'
    startBanner(useCase)

    params = {
        'stock_code': [ 'avh', 'bhp' ]
    }

    r = requests.get('http://127.0.0.1:8001/stocks', json=params)
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))
    
    endBanner(useCase)


# use case 2
def useCaseTwo():
    useCase = 'two'
    startBanner(useCase)

    r = requests.get('http://127.0.0.1:8001/stocks/bhp')
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))
    
    endBanner(useCase)


# use case 3
def useCaseThree():
    useCase = 'three'
    startBanner(useCase)

    r = requests.get('http://127.0.0.1:8001/stocks/14d/quotes/weekly')
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))
    
    endBanner(useCase)


# use case 4
def useCaseFour(dot, params = None):
    useCase = 'Four' + dot
    startBanner(useCase)

    if params == None:
        r = requests.get('http://127.0.0.1:8001/stocks/14d/quotes/weekly/')
    else:
        r = requests.get('http://127.0.0.1:8001/stocks/14d/quotes/weekly/', json=params)
    
    rjson = r.json()
    print(json.dumps(rjson, sort_keys=False, indent=4))
        
    endBanner(useCase)

useCaseOne()
useCaseTwo()
useCaseThree()
useCaseFour('1', params = {
        'start_date': '2021-01-01'
    }
)

useCaseFour('2', params = {
        'end_date': '2021-01-01'
    }
)

useCaseFour('3', params = {
        'start_date': '2021-01-01',
        'end_date': '2021-02-01'
    }
)

useCaseFour('4', params = {
        'period': '10d'
    }
)

useCaseFour('5', params = {
        'period': '3w'
    }
)

useCaseFour('6', params = {
        'period': '1m'
    }
)

useCaseFour('7', params = {
        'period': '1y'
    }
)

useCaseFour('8', params = None)