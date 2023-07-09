
import ntc_templates
from Device_list import R1, R2
from netmiko import ConnectHandler
from rich import print as rprint

for routers in R1, R2:
    conn = ConnectHandler(**routers)
    conn.enable()

    rprint(conn.send_command('show standby brief', use_textfsm=True))