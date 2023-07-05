
from Device_list import R1, R2, R3, R4, HQ_SW1, HQ_SW2, HQ_SW3, BR_SW1, BR_SW2
from netmiko import ConnectHandler
from rich import print as rprint




# Configuring R1:
#  - HSRPv2
#  - IPSLA
#  - Object tracking

conn = ConnectHandler(**R1)
conn.enable()

rprint(f'[yellow]Common Configurations'+'\n'+'  - HSRPv2\n'+'  - IPSLA\n'+'  - Object tracking\n'+'[/yellow]')

ip_sla_config   = ['int e0/1','ip address 44.67.28.2 255.255.255.252','no shut','ip route 0.0.0.0 0.0.0.0 44.67.28.1',
                   'ip sla 10','icmp-echo 44.67.28.1','frequency 10','exit','ip sla schedule 10 start-time now life forever']

object_track    = ['track 10 ip sla 10','delay up 5 down 5']

hsrpv2_commands = ['int e0/0.10',
                   'encapsulation dot1q 10',
                   'ip addres 10.1.10.1 255.255.255.0',
                   'standby version 2',
                   'standby 10 ip 10.1.10.3',
                   'standby 10 priority 110',
                   'standby 10 preempt',
                   'standby 10 track 10 decrement 30',

                   'int e0/0.20',
                   'standby version 2',
                   'standby 20 ip 10.1.20.3',
                   'standby 20 preempt']

tunnel_config   = ['int tunnel 10',
                   'tunnel mode gre multipoint',
                   'tunnel source e0/1',
                   'tunnel key 10',
                   'ip address 172.31.10.1 255.255.255.0',
                   'ip nhrp map multicast dynamic',
                   'ip nhrp network-id 10',
                   'ip mtu 1400',
                   'ip nhrp authentication dmvpn']

eigrp_config    = ['router eigrp DMVPN-EIGRP',
                   'address-family ipv4 autonomous-system 100',
                   'network 172.31.10.0',
                   'network 10.1.10.0',
                   'network 10.1.20.0',
                   'af-interface tunnel 10',
                   'no split-horizon',
                   'no next-hop-self',
                   'af-interface e0/0.20',
                   'passive-interface',
                   'af-interface e0/0.10',
                   'passive-interface']
for commands in ip_sla_config, object_track, hsrpv2_commands,tunnel_config, eigrp_config:
    rprint(conn.send_config_set(commands)+'\n')
    conn.save_config()




# Configuring R2:
#  - HSRPv2
#  - IPSLA
#  - Object tracking

conn = ConnectHandler(**R2)
conn.enable()

rprint(f'[yellow]Common Configurations'+'\n'+'  - HSRPv2\n'+'  - IPSLA\n'+'  - Object tracking\n'+'[/yellow]')

ip_sla_config   = ['int e0/1','ip address 32.19.86.2 255.255.255.252','no shut','ip route 0.0.0.0 0.0.0.0 32.19.86.1',
                   'ip sla 20','icmp-echo 32.19.86.1','frequency 10','exit','ip sla schedule 20 start-time now life forever']

object_track    = ['track 20 ip sla 20','delay up 5 down 5']

hsrpv2_commands = ['int e0/0.10',
                   'encapsulation dot1q 10',
                   'ip addres 10.1.10.2 255.255.255.0',
                   'standby version 2',
                   'standby 10 ip 10.1.10.3',
                   'standby 10 preempt',
                   
                   'int e0/0.20',             
                   'standby version 2',
                   'standby 20 ip 10.1.20.3',
                   'standby 20 priority 110',
                   'standby 20 preempt',
                   'standby 20 track 1 decrement 30']

tunnel_config   = ['int tunnel 20',
                   'tunnel mode gre multipoint',
                   'tunnel source e0/1',
                   'tunnel key 20',
                   'ip address 172.31.20.1 255.255.255.0',
                   'ip nhrp map multicast dynamic',
                   'ip nhrp network-id 20',
                   'ip mtu 1400',
                   'ip nhrp authentication dmvpn']

eigrp_config    = ['router eigrp DMVPN-EIGRP',
                   'address-family ipv4 autonomous-system 100',
                   'network 172.31.20.0',
                   'network 10.1.10.0',
                   'network 10.1.20.0',
                   'af-interface tunnel 20',
                   'no split-horizon',
                   'no next-hop-self',
                   'af-interface e0/0.20',
                   'passive-interface',
                   'af-interface e0/0.10',
                   'passive-interface']
for commands in ip_sla_config, object_track, hsrpv2_commands, tunnel_config, eigrp_config:
    rprint(conn.send_config_set(commands)+'\n')
    conn.save_config()




#Configuring Spokes:
#  - LAN and DHCP
#  - NetFlow

rprint(f'[yellow]Common Configurations'+'\n'+'  - LAN and DHCP\n'+'  - NetFlow\n'+'[/yellow]')
for devices in R3, R4:
    conn = ConnectHandler(**devices)
    conn.enable()

    lan_subif = input(f'Host {devices.get("ip")} VLAN subinterface: ')
    udp_port  = input(f'Host {devices.get("ip")} NetFlow UDP port: ')

    lan_conf  = ['int e0/0.'+str(lan_subif),
                 'encapsulation dot1q '+str(lan_subif),
                 'ip address 10.1.'+str(lan_subif)+'.1 255.255.255.0',
                 'ip helper-address 10.1.20.254',
                 'int e0/0',
                 'no shut']
    netflow   = ['ip flow-export version 9',
                 'ip flow-export destination 10.1.20.254 '+udp_port,
                 'int e0/0.'+str(lan_subif),
                 'ip flow ingress',
                 'ip flow egress',
                 'ip flow-top-talkers',
                 'top 5',
                 'sort-by bytes']   
    for commands in lan_conf, netflow:
        rprint(conn.send_config_set(commands)+'\n')
        conn.save_config()
    



#Common Configs
#  - SNMP
#  - syslog
#  - Banner motd

rprint(f'[yellow]Common Configurations'+'\n'+'  - SNMP\n'+'  - Syslog\n'+'  - Banner MOTD\n'+'[/yellow]')
for devices in R1, R2, R3, R4, HQ_SW1, HQ_SW2, HQ_SW3, BR_SW1, BR_SW2:
    conn = ConnectHandler(**devices)
    conn.enable()

    snmp   =  ['ip access-list standard SNMP_ACL',
               'permit host 10.1.20.254',
               'snmp-server community devices_snmp ro SNMP_ACL',
               'snmp-server system-shutdown',
               'snmp-server host 10.1.20.254 traps version 2c devices_snmp']
    syslog =  ['logging monitor informational',
               'logging host 10.1.20.254',
               'logging trap']
    banner =  ['banner motd ^',
               ("*"*33),
               '    Python Network Automation   ',
               ("*"*33),'^',
               'line console 0',
               'motd-banner',
               'line vty 0 4',
               'motd-banner']
    for commands in snmp, syslog, banner:
        rprint(conn.send_config_set(commands)+'\n')
        conn.save_config()

