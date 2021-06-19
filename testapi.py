import requests
import json


# use case 1
params= {
    'sectorTicker': [ 'xmj', 'xej' ]
}

r = requests.post ('http://127.0.0.1:8001/sectors', json=params)
rjson = r.json()
print (json.dumps(rjson, sort_keys=False, indent=4))


# use case 2
r = requests.post ('http://127.0.0.1:8001/sectors/xej')
rjson = r.json()
print (json.dumps(rjson, sort_keys=False, indent=4))


# use case 3
params= {
    'tickers': [ 'bhp', 'avh' ]
}

r = requests.post ('http://127.0.0.1:8001/tickers', json=params)
rjson = r.json()
print (json.dumps(rjson, sort_keys=False, indent=4))


# use case 4
r = requests.post ('http://127.0.0.1:8001/tickers/bhp')
rjson = r.json()
print (json.dumps(rjson, sort_keys=False, indent=4))


# use case 5
r = requests.post ('http://127.0.0.1:8001/quotes')
rjson = r.json()
print (json.dumps(rjson, sort_keys=False, indent=4))
