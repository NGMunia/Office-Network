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



'''
  GET: Getting Device info through API
    - This will also format the output in a more readable format.
'''
url = 'http://192.168.30.100:8000/Devices/info'
result = (requests.get(url).json())

for result in result:
    rp('\n\n'f'[cyan]Device:{result.get("hostname")}[/cyan]')
    print("-"*50)
    for key,value in result.items():
        print(f'{key:>15} : {value}')




'''
  POST: Configuring VLANs with API
    - We create a dictionary (data) that contains the data to be sent in the request body. 
      We use the json parameter of the requests.post() method to automatically encode the payload as JSON.

    - After sending the request, we check the response status code. 
      If it's 200, we assume the request was successful and print the response data. 
      Otherwise, we print an error message along with the actual status code returned by the API.
'''
url  = 'http://192.168.30.100:8000/Devices/Switches/VLANs/create'

data =      {
                'switch_ip': '10.1.1.1',
                'vlan_ID' : 150,
                'vlan_name': 'PyScript-VLAN'
            }
result = requests.post(url,json=data)
if result.status_code == 200:
    rp(' Response ',result.status_code,'\n','VLAN '+str(data.get('vlan_ID')),'configured successfully!')
else:
    rp(' Response ',result.status_code,'\n','VLAN '+str(data.get("vlan_ID")), 'not configured.\n Ethernet VLAN-ID should range between 2-1001')




'''
  DELETE: Deleting VLANS.
    - This DELETE  request script will remove resource data (VLAN) on the switch.
'''
url  = 'http://192.168.30.100:8000/Devices/Switches/VLANs/remove'

data =  {
          'switch_ip': '10.1.1.1',
          'vlan_ID' : 150,
        }
result = requests.delete(url,json=data)
if result.status_code == 200:
    rp(' Response ',result.status_code,'\n','VLAN '+str(data.get('vlan_ID')),'removed successfully!')
else:
    rp(' Response ',result.status_code,'\n','VLAN '+str(data.get("vlan_ID")), 'has not been removed')

