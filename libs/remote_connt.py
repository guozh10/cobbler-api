#!/usr/bin/env python
# -*- coding:utf8 *-*
#guozhenhui
import os,sys,time
import paramiko
import yaml
homePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
#print(homePath)
sys.path.append(homePath)
yamlpath = '%s/conf/yaml'%homePath
class SSH_Connect(object):

    def __init__(self,name,ip,mac,yaml_dir,netmask,gateway,public_ip):
        self.ip         =   ip
        self.mac        = mac
        self.name       = name
        self.yaml_dir  = yaml_dir
        self.netmask   = netmask
        self.gateway	= gateway
        self.public_ip  = public_ip
        open('%s/%s.yaml'%(self.yaml_dir,self.name), 'w').write(open('%s/file.yaml'%self.yaml_dir, 'r').read())
    def disk(self):
        ssh  = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh.connect(hostname=self.ip,port=22, username='root',password='r00tme')
        ssh.connect(hostname=self.ip,port=22,username='root',key_filename="/root/.ssh/bootstrap.rsa")
        cmd = """lsblk |grep disk |awk '/disk/ {print $1,$4}'"""
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = bytes.decode(stdout.read())
        ssh.close()
        all_disk = result.split()
        print("\033[1;32;40mclient:\033[0m[%s]"%self.ip)
        print('[%s]'%all_disk)
        disk_name=raw_input('\033[1;32;40mPlease enter disk size:\033[0m')
        disk_sum = """lsblk |grep %s |awk '/disk/ {print $1}'"""%disk_name
        self._connect('sde',disk_sum)
    def interface(self):
        #mac = """ip a | awk '/%s/ {print $2}'""" % self.mac
        interface = """ip a | grep -A 1 '%s' | awk '/global/ {print $8}'""" % self.mac
        self._connect('eth0', interface)
        self._rw_file('f8', self.mac)
        self._rw_file('192.168.100.1', self.public_ip)
        self._rw_file('ceph1',self.name)
        self._rw_file('255.255.254.0',self.netmask)
        self._rw_file('192.168.100.254',self.gateway)
        # print(self.mac)
    def _connect(self,name,cmd):
        ssh  = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh.connect(hostname=self.ip,port=22, username='root',password='r00tme')
        ssh.connect(hostname=self.ip,port=22,username='root',key_filename="/root/.ssh/bootstrap.rsa")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = bytes.decode(stdout.read())
        L1 = result.split()
        #print(type(L1))
        #print(L1)
        with open('%s/%s.yaml'%(self.yaml_dir,self.name),'r+') as f:
            info   = f.readlines()
            f.seek(0)
            for line in info:
                line_new = line.replace(name, L1[0])
                f.write(line_new)
        ssh.close()
    def _rw_file(self,name,file_name):
       # print(file_name)
        with open('%s/%s.yaml'%(self.yaml_dir,self.name),'r+') as f:
            info   = f.readlines()
            f.seek(0)
        #    print(file_name)
            for line in info:
                line_new = line.replace(name, str(file_name))
                f.write(line_new)

if __name__ == '__main__':
    name = 'ceph5'
    #name = '%s.yaml' %sum
    ip = '192.168.100.103'
    mac = '00:0c:29:a9:81:3f'
    yamlpath = '%s/conf/yaml'%homePath
    ss = SSH_Connect(name,ip,mac,yamlpath)
    #ss.disk()
    ss.interface()
