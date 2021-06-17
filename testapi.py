import requests
import json


#class Example(BaseModel):
#    name: int 
#    other: int

params= {
    "Example": {
        'name': 1,
        'other': 2
    }
}

params= {
    'sectorTicker': [ 'xmj', 'xej' ]
}

r= requests.post ('http://127.0.0.1:8001/sectors', json=params)
print (r.json ())