
from netmiko import ConnectHandler
from Device_list import RTR1, fW1, core
import ntc_templates
from rich import print as rprint

conn = ConnectHandler(**core)
conn.enable()
result = (conn.send_command('show ip interface brief', use_textfsm=True))

rprint(result)