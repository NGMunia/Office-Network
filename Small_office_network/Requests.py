import requests
from rich import print as rp

url = 'http://192.168.30.100:8000/Devices/health'

result = requests.get(url).json()

rp(result)
