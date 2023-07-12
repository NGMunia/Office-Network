
from fastapi import FastAPI
from netmiko import ConnectHandler
from Device_list import RTR1, fW1, core
import ntc_templates


app = FastAPI()


#Devices Info API:   
@app.get('/Devices/info')
def DeviceHealth():
    
    output= []
    
    for devices in RTR1, fW1, core:
        
        conn = ConnectHandler(**devices)
        conn.enable()

        result= (conn.send_command('show version',use_textfsm=True))[0]
        output.append(result)

    return(output)


