
from csv import writer
from Device_list import core, RTR1, fW1
from netmiko import ConnectHandler
from rich import print as rprint

with open('/home/munia/Scripts/Small_office_network/Devices.csv','w',newline='') as f:
    write_data = writer(f)
    write_data.writerow(['Hostname','IP address','Version','Image','Serial-No','Uptime'])

    for devices in core, RTR1, fW1:
        conn = ConnectHandler(**devices)
        conn.enable()
        output = (conn.send_command('show version',use_textfsm=True))[0]

        hostname = output.get('hostname')
        ip_addr  = devices.get('ip')
        version  = output.get('version')
        image    = output.get('running_image')
        serial   = output.get('serial')
        uptime   = output.get('uptime')

        write_data.writerow([hostname,ip_addr,version,image,serial,uptime])




