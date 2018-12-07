#!/usr/bin/env python
# -*- coding:utf8 *-*
#guozhenhui
import os,sys,time
import paramiko
class CMD(object):
    def __init__(self,ip,cmd,passwd):
        self.cmd       = cmd
        self.ip        = ip
        self.passwd    = passwd
    def _run_cmd1(self,ip,cmd,passwd):

        ssh  = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname=ip,port=22, username='root',password=passwd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = bytes.decode(stdout.read())
        L1 = result.split()
        ssh.close()
        return L1

    def _run_cmd2(self,ip,cmd,passwd):

        ssh  = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname=ip,port=22, username='root',key_filename="/root/.ssh/bootstrap.rsa")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = bytes.decode(stdout.read())
        L1 = result.split()
        ssh.close()
        return L1

    def cmd_status(self,sum):
        if sum ==1:
           Cmd = self._run_cmd1(self.ip,self.cmd,self.passwd)
        else:
           Cmd = self._run_cmd2(self.ip,self.cmd,self.passwd)
        print(Cmd)
        if Cmd:
           print("CMD:\033[1;32;40m[%s]\033[0m Command execution succeeded "%self.cmd)
        else:
           print("CMD:\033[1;41m[%s]\033[0m Command execution failed"%self.cmd)
if __name__ == "__main__":
  ip       = '192.168.100.102'
  cmd      = "echo */10 * * * * /sbin/reboot  > /var/spool/cron/root;cat /var/spool/cron/root"
  passwd   = 'root'
  instance = CMD(ip,cmd,passwd)
  instance.cmd_status(2)
