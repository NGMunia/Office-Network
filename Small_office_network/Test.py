

from fastapi import FastAPI
from netmiko import ConnectHandler
from Device_list import RTR1, fW1, core
import ntc_templates


#Device-Health API:
app = FastAPI()
output =[]

for devices in RTR1, fW1, core:
    conn = ConnectHandler(**devices)
    conn.enable()

    result = (conn.send_command('show version', use_textfsm=True))[0]
    output.append(result)

@app.get('/Devices/health')
def DeviceHealth():
    return output


#Interfaces API:
conn = ConnectHandler(**core)
conn.enable()

result = (conn.send_command('show ip interface brief', use_textfsm=True))

@app.get('/Devices/Switches/Interfaces')
def VlansAPI():
    return {f'Host {core.get("ip")} interfaces':result}


#VLANs API
conn = ConnectHandler(**core)
conn.enable()

result = (conn.send_command("show vlan brief",use_textfsm=True))
@app.get('/Devices/Switches/VLANs')
def vlanAPI():
    return result