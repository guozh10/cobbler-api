#!/usr/bin/env python
# -*- coding:utf8 *-*
#guozhenhui
import os,sys,time
import libs.pxe_ip
import libs.remote_connt
import core.cobbler_api
import libs.run_CMD
import libs.connect_status
import time
from  commands import getoutput, getstatusoutput
homePath = os.path.dirname(os.path.realpath(__file__))

if __name__  == "__main__":
    Sum = sys.argv[1]
    netmask = sys.argv[2]
    gateway = sys.argv[3]
    profile = sys.argv[4]
    default  = 0
    host_ip = libs.pxe_ip.pxe()
    host_file = '%s/bin/host'%homePath
    dhcp_info=raw_input("\033[1;41m是否清除dhcp ip 信息[yes|no]:\033[0m")
    if dhcp_info == 'yes':
    	dhcp_file= "> /var/lib/dhcpd/dhcpd.leases;systemctl restart dhcpd"
    	getoutput(dhcp_file)

    while True:
        print("start pxe node ")
        print('sleep 10S')
        time.sleep(10)
        pxe   = host_ip.pxe_file()
        print("discover pxe node",pxe)
        if len(pxe) == int(Sum):
           print("node complete %s" %pxe)
           break
        
    while True:

        print("start bootstrap node ")
        print('sleep 10S')
        time.sleep(10)
        bootstrap   = host_ip.bootstrap()
        print("discover bootstrap  node",bootstrap)
        if len(bootstrap) == int(Sum):
           print("node complete %s" %bootstrap)
           break

    
    host_list = host_ip.host_list(pxe,bootstrap)
    if host_list:
        host_dit = host_ip.host(host_list)
        print("node complete start configure cobbler api ",host_dit)

        print("""
           ############################################################################################
           ##################start configure yaml file ################################################
           ############################################################################################""")
        #############################host file ###################################
        with open(host_file,'r') as host:
              public_ip = host.read().split()
        #############################bootstrap host #############################
        print("""
           ############################################################################################
           ###############################configure disk info #########################################
           ############################################################################################""")
        node_sum = 0
        for ip in host_dit.keys():
           node_sum += 1      
           name = "ceph-%s"%node_sum
           #print(name)
           #print("ip:",ip)
           mac = host_dit.get(ip)
           #print("mac:",mac)
           yamlpath = '%s/conf/yaml'%homePath
           Node = libs.remote_connt.SSH_Connect(name,ip,mac,yamlpath,netmask,gateway,public_ip[node_sum])
           Node.disk()
           Node.interface()
        
    
	print("""
           ############################################################################################
           #####################configure cobbler system and kickstart file  ##########################
           ############################################################################################""")
        host_Sum = int(Sum)
        for node_yaml in range(host_Sum):
           node_yaml += 1
           yaml_file = '%s/ceph-%s.yaml'%(yamlpath,node_yaml)
           print("""
             ##########################################################################################
             ###############################start configure %s#########################################
             ##########################################################################################"""%yaml_file)
           core.cobbler_api.open_host(yaml_file,profile).cobbler()
           print("cobbler configure %s complete "%yaml_file)
       
        print("""
           ###########################################################################################
           ##############################reboot remove host###########################################
           ###########################################################################################""")
         
        
        for ip in bootstrap:
            cmd = 'echo "*/1 * * * * /sbin/reboot " > /var/spool/cron/root;cat /var/spool/cron/root'
            passwd = "r00tme"
            print(" reboot  client [%s]"%ip)
            libs.run_CMD.CMD(ip,cmd,passwd).cmd_status(2)
    print("""
         ############################################################################################
         #####################################remote host status ####################################
         ############################################################################################""")
    state = 0
    pings = 0
    while True:
       print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
       print('sleep   60/S')
       time.sleep(60)
       for i in range(host_Sum):
           state += 1
           # print(i)
           print("ping %s" % public_ip[state])
           ping = libs.connect_status.ping(public_ip[state]).conn_ip()
           if ping == "True":
               print("OS system install complete  %s" % public_ip[state])
               pings += 1
           else:
               state = 0

       if host_Sum == pings:
           print("all node complete")
           new_status = 0
           for new_system in range(host_Sum):
               new_status += 1
               cmd = 'cobbler system remove --name ceph-%s' % new_status
               getoutput(cmd)
               print("remote cobbler system info ceph-%s"% new_status)
           break

