# -*- coding:utf8 *-*
#guozhenhui
import os,sys,time
import os,sys,re
Path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(Path)

file='test.txt'
#
# class check_remote(object):
#     from commands import getoutput, getstatusoutput
#     c = 2
#     a = 0
#     ips =[]
#     cachk_ip = {}
#     while a < 20 :
#         Sum = 'cat %s | grep  PXEClient| wc -l'%file
#         S,SUN = getstatusoutput(Sum)
#         time.sleep(3)
#         print('++++++',SUN)
#         print(type(SUN))
#         print(type(c))
#         a +=1
#         if SUN == str(c):
#             print('*****************',SUN)
#             ip_state,ip = getstatusoutput("cat test.txt | grep -B 8 PXEClient|egrep lease|awk '{print $2}'")
#             ips = ip.split()
#             print(ips)
#             for i in ips:
#                cachk_ip.update({i:'flase'})
#             print(cachk_ip)
#             a = 0
#             break
#         print("dengdai 3S",a)
#
#     while a < 10:
#        time.sleep(3)
#        print("Wait 30 seconds")
#        for i in ips:
#           ping_status,ping =  getstatusoutput('ping %s'%i)
#           if ping_status == 0:
#              cachk_ip[i] = 'up'

a = {'192.168.1.1':'up','192.168.1.2':'down'}

print(len(a))
try:
    for i in a.keys():
        if a.get(i) == 'up':
            print(type(a.get(i)))
            print(a[i],'======')
            del a[i]
            print(a)

except  RuntimeError  as  e:
    print('node up')
    print('node up')
    print('node up')
    print('node up')
    print('node up',a)
    # print(a.items())


for i in a.keys():
    print(i,'sssssssssssssssssssssssssssddddddddddddddddddddd')
    if a.get(i) == 'up':
        print(type(a.get(i)))
        print(i,'ssssssssssssssssssss')
        # del a[i]
# for ii in a.values():
#     print(ii)
