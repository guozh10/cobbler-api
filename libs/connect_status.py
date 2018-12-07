# -*- coding:utf8 *-*
#guozhenhui
import os,sys
from  commands import getoutput, getstatusoutput
class ping(object):
    def __init__(self,ip):
        pass
        self.ip    = ip
    def conn_ip(self):
        Ping = 'ping  -c 2 %s ' %self.ip
        # os.system(Ping)
        status,out = getstatusoutput(Ping)
        if status == 0 :
            return 'True'
        else:
            return 'Flase'
if __name__ == "__main__":
    ss = ping('192.168.100.250').conn_ip()
    if ss == "True":
       print('ip tong')
    else:
       print('ip not tong')
    
