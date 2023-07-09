
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

        

def R1_config():
    """CONFIGURING THE EDGE ROUTER
    - NAT
    - Access control lists"""
    rprint(f'[yellow]{R1_config.__doc__}[/yellow]')

    conn = ConnectHandler(**RTR1)
    conn.enable()
    
    nat = [
           'ip access list standard nat_acl',
           'permit 192.168.0.0 0.0.31.255',
           'int e0/0',
           'ip nat inside',
           'int e0/1',
           'ip address dhcp',
           'ip nat outside',
           'no shut',
           'ip nat inside source list nat_acl interface e0/1 overload',
           'ip route 0.0.0.0 0.0.0.0 192.168.122.1 overload']
    print(conn.send_config_set(nat)+'\n')
R1_config()

    


def firewall():
    """CONFIGURING ZONE-BASED-FIREWALL"""
    rprint(f'[yellow]{firewall.__doc__}[/yellow]')

    conn = ConnectHandler(**fW1)
    conn.enable()

    zbf  = [
            'ip access-list In_Out_acl',
            'permit tcp any any',
            'permit udp any any',
            'permit icmp any any',
            'ip access-list Out_In_acl',
            'permit host 10.1.1.6 any',
            'class-map type inspect In_Out_class',
            'match access-group name In_Out_acl',
            'class-map type inspect Out_In_class',
            'match access-group name Out_In_acl',
            'policy-map type inspect In_Out_Policy',
            'class In_Out_class',
            'inspect',
            'policy-map type inspect Out_In_policy',
            'class Out_In_class',
            'inspect',
            'zone security Inside',
            'zone security Outside',
            'zone-pair security In_Out_Zone source Inside destination Outside',
            'service-policy type inspect In_Out_policy',
            'zone-pair security Out_In_zone source Outside destination Inside',
            'service-policy type inspect Out_in_policy',
            'int e0/0',
            'zone-security Inside',
            'int e0/1',
            'zone-security Outside']
    print(conn.send_config_set(zbf)+'\n')
firewall()


#Common configs:
def common_configs():
    """Common Configs:
    - NTP
    - SNMP
    - Syslog"""
    rprint(f'[yellow]{common_configs.__doc__}[/yellow]')

    for devices in RTR1, fW1, core:
        conn = ConnectHandler(**devices)
        conn.enable()

        ntp_svr = input(f'Host {devices.get("ip")} NTP server IP: ')
        ntp_con = [
                   'ip domain lookup',
                   'ip name server 8.8.8.8',
                   'ntp server '+ntp_svr,
                   'ntp update-calendar',
                   'clock timezone GMT +3',
                   'service timestamps log datetime localtime year',
                   'service timestamps debug datetime locatime year']
        snmp    = [
                   'ip access-list standard SNMP',
                   'permit host 192.168.30.254',
                   'snmp-server community devices_snmp ro SNMP',
                   'snmp-server system-shutdown',
                   'snmp-server host 192.168.30.254 version 2c devices_snmp']
        syslog  = [
                   'logging monitor informational',
                   'logginh host 192.168.30.254',
                   'logging trap']
        
        for commands in ntp_con, snmp, syslog:
            rprint(conn.send_config_set(commands)+'\n')
            conn.save_config()
common_configs()  
        
      





