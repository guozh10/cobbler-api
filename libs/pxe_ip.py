#!/usr/bin/env python
# -*- coding:utf8 *-*
#guozhenhui
import os,sys
from  commands import getoutput, getstatusoutput
path_name = os.path.dirname(os.path.dirname(__file__))
sys.path.append(path_name)
# print(path_name)
class  pxe(object):
    def __init__(self,):
        pass

    def  pxe_file(self):
        pxe_host  = "grep -B 10 PXEClient /var/lib/dhcpd/dhcpd.leases|awk '/192.168.100/ {print $2 }'"
        stu,cmd = getstatusoutput(pxe_host)

        if stu == 0:
            Host_ip = cmd.strip().split()
        return Host_ip

    def bootstrap(self):
        pxe_host = "grep -B 10 bootstrap /var/lib/dhcpd/dhcpd.leases|awk '/192.168.100/ {print $2 }'"
        stu, cmd = getstatusoutput(pxe_host)
        if stu == 0:
            host_ip = cmd.strip().split()
        return host_ip

    def host_list(self,pxe,boot):
        #pxe = pxe
        #boot = bootstrap
        pxe.sort()
        boot.sort()
        if len(pxe) == len(boot):
            return boot
        else:
            print('-1',pxe,boot)
    def host(self,host_l):
        host = {}
        for h in host_l:
  
           cmd = """grep -A 10 %s  /var/lib/dhcpd/dhcpd.leases |awk '/hardware/ {print $3}' |awk -F ";" '{print $1}'"""%h
           stu, mac = getstatusoutput(cmd)
           host.setdefault(h,mac)
        return host
if __name__ == "__main__":
   pass
   host_ip  = pxe()
   print( host_ip.pxe_file())
   print(host_ip.bootstrap())
   lists = host_ip.host_list(host_ip.pxe_file(),host_ip.bootstrap())
   print(lists)
   print(host_ip.host(host_ip.host(lists)))
