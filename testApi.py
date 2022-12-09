import requests

import json

response_API = requests.post('http://172.17.0.2:5000/campusSubjects', json={
    'campus': 'UBCO'
})

print(response_API.text)
