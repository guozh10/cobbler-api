# cobbler-api
Cobbler automatically deploys OS systems
cd  cobbler-api
#configure OS access ip address
#note
#Please do not clear the first line of Public_IP
cat ./bin/host
  Public_IP
  10.121.223.12
  10.121.223.13


sh ./bin/run_cobbler.sh start 2  255.255.255.0 192.168.100.254 Centos-7.5-x86_64
