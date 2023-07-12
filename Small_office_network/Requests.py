'''
HTTP requests methods:
  - GET    Read method that retrieves information
  - POST   create method that submits new data.
  - PUT    updates the entire resource data
  - PATCH  updates a part of the resource data.
  - DELETE deletes the resource data
'''


import requests
from rich import print as rp


#Device-Health API GET request
url = 'http://192.168.30.100:8000/Devices/info'
result = requests.get(url).json()
rp(result)



