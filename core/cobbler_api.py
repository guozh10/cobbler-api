#!/usr/bin/env python
# -*- coding:utf8 *-*
#guozhenhui
import os,sys
import time
from  commands import getoutput, getstatusoutput
import yaml
path_name = os.path.dirname(os.path.dirname(__file__))
sys.path.append(path_name)
print(path_name)

class cobbler_api(object):
    def __init__(self,Name,Mac,Interface,kickistart,disk,ip,netmask,gateway,profile):
        self.Name           = Name
        self.Mac            = Mac
        self.Interface      =Interface
        self.kickstart      =kickistart
        self.disk	    = disk
        self.ip		    = ip
        self.netmask	    = netmask
        self.gateway        = gateway
        self.profile        = profile
        pass
    def _file(self):
        print('start copy ks file and set disk name')
        open(self.kickstart,'w').write(open('%s/template/node-2.ks'%path_name,'r').read())
        with open(self.kickstart,'r+') as f:
            info    = f.readlines()
            f.seek(0)
            for line in info:
                line_new = line.replace('sda',self.disk)
                f.write(line_new)
    def _delete_system(self):
        cmd = '''cobbler system list | grep %s''' %self.Name
        del_name ='''cobbler system remove --name %s''' %self.Name
        status, result = getstatusoutput(cmd)
        if status == 0 :
            getoutput(del_name)
            os.remove(self.kickstart)
            print("node esxi start delete")
        else:
            print("start add node ")
    def new(self):
        cmd='''
            cobbler system add --name %s \
            --mac-address=%s  --interface=%s \
            --ip-address=%s  --subnet=%s \
            --gateway=%s \
            --static=1 --hostname=%s \
            --kickstart=%s --profile=%s\
        ''' %(self.Name,self.Mac,self.Interface,self.ip,self.netmask,self.gateway,self.Name,self.kickstart,self.profile)

        self._delete_system()
        self._file()
        status, result = getstatusoutput(cmd)
        if status == 0:
            pass
            print("ok",self.Name)
        else:
            print("not ",self.Name)
            print(result)
        getoutput('cobbler sync')

class open_host(object):
    def __init__(self,node_yaml,profile):
        self.node_yaml   = node_yaml
        self.profile     = profile
    def _configure(self):
        with open(self.node_yaml,'r') as f:
            cont = f.read()
            f1 =  yaml.load(cont)
        return f1
    def cobbler(self):   
        conf = self._configure()
        host_info = conf.get('host')
        interface = host_info['interface']
        mac = host_info['mac']
        disk = host_info['disk']
        ip = host_info['ip']
        netmask = host_info['netmask']
        gateway = host_info['gateway']
        name = host_info['hostname']
        kickistart  = "/var/lib/cobbler/kickstarts/%s.ks" %name
        intance  = cobbler_api(name,mac,interface,kickistart,disk,ip,netmask,gateway,self.profile)
        intance.new()
if __name__ =="__main__":
    name        = "ceph5"
    mac         = "7c:d3:0a:e5:38:10"
    interface   = "eth3"
    disk        = "sdf"
    kickistart  = "/var/lib/cobbler/kickstarts/%s.ks" %name
    
    intance     = cobbler_api(name,mac,interface,kickistart,disk)
    intance.new()
    homePath = os.path.dirname(os.path.dirname(__file__))
   
