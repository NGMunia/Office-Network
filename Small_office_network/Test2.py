
from Device_list import RTR1, fW1, core
from netmiko import ConnectHandler
from rich import print as rprint


def core_config():
    """CONFIGURING THE CORE SWITCH
    - VLANs
    - Access control lists
    - DHCP"""
    rprint(f'[yellow]{core_config.__doc__}[/yellow]')

    conn = ConnectHandler(**core)
    conn.enable()

    for v in range(10,30,10):
        vname = input(f'VLAN {v} name: ')
        vlans = ['vlan '+str(v), 'name '+vname]
        intf  = ['int vlan '+str(v),'ip address 192.168.'+str(v)+'.1 255.255.255.0','no shut']
        dhcp  = ['ip dhcp excluded-address 192.168.'+str(v)+'.1  192.168.'+str(v)+'.10' ,
                 'ip dhcp pool VLAN_'+vname,
                 'network 192.168.'+str(v)+'.0 255.255.255.0',
                 'default-router 192.168.'+str(v)+'.1',
                 'dns-server 8.8.8.8']
        for commands in vlans,intf,dhcp:
            rprint(conn.send_config_set(commands)+'\n')    

    for i in range(0,4):
        access = input('interface E0/'+str(i)+' access VLAN: ')
        ports  = ['int e0/'+str(i),'switchport mode access','switchport access vlan '+access]
        rprint(conn.send_config_set(ports)+'\n')
    conn.save_config()
core_config()    