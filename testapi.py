import requests
import json


params= {
    'sectorTicker': [ 'xmj', 'xej' ]
}

r = requests.post ('http://127.0.0.1:8001/sectors', json=params)
rjson = r.json()
print (json.dumps(rjson, sort_keys=False, indent=4))


r = requests.post ('http://127.0.0.1:8001/sectors/xej')
rjson = r.json()
print (json.dumps(rjson, sort_keys=False, indent=4))