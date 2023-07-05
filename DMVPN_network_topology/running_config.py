
#Making backup files of the running-config:

from Device_list import R1, R2, R3, R4, HQ_SW1, HQ_SW2, HQ_SW3, BR_SW1, BR_SW2
from datetime import datetime
from netmiko import ConnectHandler


time = datetime.now().replace(microsecond=0)

for routers in R1, R2, R3, R4:
    print(f'Connecting to Router {routers.get("ip")}...')
    conn = ConnectHandler(**routers)
    conn.enable()
    
    ip = routers.get('ip')
    output = conn.send_command('show run')+'\n'
    
    with open("RTR_"+"_"+ip+"_"+str(time),"w")as f:
        f.write(output)
        
for switches in  HQ_SW1, HQ_SW2, HQ_SW3, BR_SW1, BR_SW2:
    print(f'Connecting to Switch {switches.get("ip")}...')
    conn = ConnectHandler(**switches)
    conn.enable()
    
    ip = switches.get('ip')
    output = conn.send_command('show run')
    
    with open("SW_"+"_"+ip+"_"+str(time),"w")as f:
        f.write(output)