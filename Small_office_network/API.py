
from fastapi import FastAPI
from netmiko import ConnectHandler
from Device_list import RTR1, fW1, core
import ntc_templates
from pydantic import BaseModel


app = FastAPI()


'''
  GET getting the Devices' information including: 
  software version, uptime, etc.
'''
@app.get('/Devices/info')
def Device_Info():
    
    output= []  
    for devices in RTR1, fW1, core:   
        conn = ConnectHandler(**devices)
        conn.enable()
        result= (conn.send_command('show version',use_textfsm=True))[0]
        output.append(result)
    return(output)


'''
  GET getting VLANs on a Switch:
'''
@app.get('/Devices/Switches/VLANs/get')
def get_vlans():

    conn = ConnectHandler(**core)
    conn.enable()
    result = conn.send_command('show vlan brief', use_textfsm=True)
    return result


'''
  POST: Adding VLANs on a Switch:
'''
class create_vlan_class(BaseModel):
    switch_ip : str
    vlan_ID: int
    vlan_name: str
@app.post('/Devices/Switches/VLANs/create')
def create_vlan(post : create_vlan_class):
    if post.vlan_ID == 1 or (1002 <= post.vlan_ID <= 1005):
        return {"message": "Invalid VLAN ID"}
    else:
        device  = { 
                    'device_type':'cisco_ios',
                    'ip': post.switch_ip,
                    'username':'Automation',
                    'password':'cisco123',
                    'secret':'cisco123'
                  }
        conn = ConnectHandler(**device)
        conn.enable()
        configs = ['vlan '+str(post.vlan_ID),'name '+post.vlan_name]
        output  = conn.send_config_set(configs)
        return{"message: VLAN configured successfully", output}
    

''''
  DELETE: Deleting VLANs on a switch:
'''    
class del_vlan_class(BaseModel):
    switch_ip : str
    vlan_ID: int
@app.delete('/Devices/Switches/VLANs/remove')
def delete_vlan(delete : del_vlan_class):
    device  =   { 
                    'device_type':'cisco_ios',
                    'ip': delete.switch_ip,
                    'username':'Automation',
                    'password':'cisco123',
                    'secret':'cisco123'
                }
    conn = ConnectHandler(**device)
    conn.enable()
    configs = ['no vlan '+str(delete.vlan_ID)]
    conn.save_config()
    output  = conn.send_config_set(configs)

    return{"message: VLAN deleted successfully", output}


    

    