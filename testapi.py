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
    'sectorTicker': 100
}

r= requests.post ('http://127.0.0.1:8000/sectors', json=params)
print (r.json ())