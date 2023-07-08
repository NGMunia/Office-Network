
import ntc_templates
import csv
from Device_list import R1, R2, R3, R4, HQ_SW1, HQ_SW2, HQ_SW3, BR_SW1, BR_SW2
from netmiko import ConnectHandler
from rich import print as rprint



with open('/home/munia/Scripts/DMVPN_network_topology/Inventory.csv','w',newline="") as f:
    write_data = csv.writer(f)
    write_data.writerow(['Hostname','IP-Address','IOS version','Serial-No','System-Image'])

    for devices in R1, R2, R3, R4, HQ_SW1, HQ_SW2, HQ_SW3, BR_SW1, BR_SW2:
        conn = ConnectHandler(**devices)
        conn.enable()

        output   = (conn.send_command('show version',use_textfsm=True))[0]

        hostname = output.get("hostname")
        ip_addr  = devices.get("ip")
        version  = output.get("version")
        serial   = output.get("serial")
        image    = output.get("running_image")

        write_data.writerow([hostname,ip_addr,version,serial,image])
    
    rprint("[green]Inventory Data written successfully![/green]")

    

with open('/home/munia/Scripts/DMVPN_network_topology/VLANS.csv','w') as f:
    write_data = csv.writer(f)
    write_data.writerow(['Hostname','VLAN-ID','Name','status','Interfaces'])

    for switches in HQ_SW1, HQ_SW2, HQ_SW3, BR_SW1, BR_SW2:
        conn = ConnectHandler(**switches)
        conn.enable()

        host    = switches.get('ip')
        list = (conn.send_command('show vlan brief', use_textfsm=True))
        write_data.writerow([host])

        for output in list:
            vlan_id = output.get('vlan_id')
            vname   = output.get('name')
            status  = output.get('status')
            intf    = output.get('interfaces')

            write_data.writerow(['',vlan_id,vname,status,intf])

    rprint("[green]VLAN Data written successfully![/green]")


