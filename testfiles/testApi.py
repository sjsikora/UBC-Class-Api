import requests

import json

response_API = requests.post('http://127.0.0.1:5000/campusSubjects', json={
    'campus': 'UBCO'
})

print(response_API.text)
