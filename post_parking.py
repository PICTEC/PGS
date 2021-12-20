import json
from geojson import Point
import requests

operatorAPI = 'https://pgs.pictec.eu/operator/v1/'

key = '326ad07a621f394f15a29bf09a89e49fc7a6a077'

header = {
    'Authorization': 'ApiKey ' + key,
    'Content-Type': 'application/json'
}

parkingCoords = Point((21.132109, 55.705404))

parkingExample = {
    "location": parkingCoords,
    "registration_number": "Test-001",
    "time_end": "2019-12-03T01:00:00Z",
    "time_start": "2019-12-01T10:00:00Z",
    "zone": 3,
    "domain": "KLP"
}

if __name__ == '__main__':
    jsonParkingExample = json.dumps(parkingExample)
    #print(jsonParkingExample)
    r = requests.post(operatorAPI + 'parking/', jsonParkingExample, headers=header)
    print(r.content)
