#! /usr/bin/env python

from socket import *
import sys
import statistic
import deal
import time




SERVERHOST=sys.argv[1]
SERVERPORT=int(sys.argv[2])
MYHOST=sys.argv[3]
MYPORT=int(sys.argv[4])
myid=sys.argv[5]
statistic.myid=myid
myname='cherryliu'
SERADDR=(SERVERHOST,SERVERPORT)
MYADDR=(MYHOST,MYPORT)
BUFSIZE=1024
client=socket(AF_INET,SOCK_STREAM)
client.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
client.setsockopt(SOL_SOCKET,SO_KEEPALIVE,1)
client.setsockopt(IPPROTO_TCP,TCP_KEEPIDLE,1)
client.setsockopt(IPPROTO_TCP,TCP_KEEPINTVL,1)
client.setsockopt(IPPROTO_TCP,TCP_KEEPCNT,10)
client.bind(MYADDR)

while client.connect_ex(SERADDR):
	#sleep=
	time.sleep(0.07)

#time.sleep(0.4)
data='reg: %s %s \n' % (myid,myname)

try:
	client.send(data)
except socket.error,arg:
	(errno,err_msg)=arg
	print "Connect server failed: %s, errno=%d" % (err_msg,errno)

print 'hello'

while True:
	while True:
		data=client.recv(BUFSIZE)
		print data
		if len(data):
			#msg=data
			#print(msg,'\n')
			break
	data=data.split('\n')	
	deal.deal_msg(data,client)








