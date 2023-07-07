
#This script will backup startup configuration every day at 11:00 AM

from Device_list import R1, R2, R3, R4, HQ_SW1, HQ_SW2, HQ_SW3, BR_SW1, BR_SW2
from netmiko import ConnectHandler
from rich import print as rprint
import schedule
import time


def backup_conf():
    """Backing up Configurations..."""
    rprint('\n'f'[cyan]{backup_conf.__doc__}[/cyan]'+'\n')
    
    for routers in R1, R2, R3, R4:
        print(f'Connecting to Router {routers.get("ip")}...')
        ip = routers.get('ip')
        
        conn = ConnectHandler(**routers)
        conn.enable()
        output = conn.send_command('show run')
        
        with open("RTR_"+ip,'w') as f:
            f.write(output)
        print('Finished backing up config\n') 
        
    for switches in HQ_SW1, HQ_SW2, HQ_SW3, BR_SW1, BR_SW2:
        print(f'Connecting to Switch {switches.get("ip")}...')
        conn = ConnectHandler(**switches)
        conn.enable()
        
        ip = switches.get('ip')
        output = conn.send_command('show run')
        
        with open("SW_"+ip,'w') as f:
            f.write(output)
        print('Finished backing up config\n') 
       
schedule.every().day.at("11:00").do(backup_conf)
while True:
    schedule.run_pending()
    time.sleep(1)
    