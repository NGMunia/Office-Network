
for v in range(10,30,10):
        vname = input(f'VLAN {v} name: ')
        vlans = ['vlan '+str(v), 'name '+vname]
        intf  = ['int vlan '+str(v),'ip address 192.168.'+str(v)+'.1 255.255.255.0','no shut']
        for commands in vlans,intf:
            print(commands,'\n')

for i in range(0,4):
        access = input('interface E0/'+str(i)+' access VLAN: ')
        ports  = ['int e0/'+str(i),'switchport mode access','switchport access vlan '+access]
        print(ports,'\n')
    