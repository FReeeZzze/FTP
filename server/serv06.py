# -*- coding: utf-8 -*-
# === serv06.py ====
# --- example of work with ftp 

from socket import *
import time
import threading

import servfn
# === handling functions dictionary ==== 
cmd_dict = {'st:':servfn.repl_text, 'se:':servfn.repl_echo , 
			'pf:':servfn.put_file, 	'gf:':servfn.get_file,}

# === first thread for broadcast===
#loc_ip = gethostbyname(gethostname())		#-- get self IP
print 'Ваш IP: '.decode('utf-8') + servfn.loc_ip
brd_adr = "10.255.255.255"

sk_ip = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP) 
sk_ip.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, 2)

def send_locip(interval, loc_ip):
	while 1:
		sk_ip.sendto( ' ', ( brd_adr, 3010))
		print ' От '.decode('utf-8') + servfn.loc_ip + ' к '.decode('utf-8') + brd_adr
		time.sleep(interval)

tr_ip = threading.Thread( target = send_locip, args =(2.5, servfn.loc_ip))
tr_ip.daemon = True
tr_ip.start()


# === main block ====
print 'serv06.py\nОжидание:'.decode('utf-8')
while True:
	data,addr = servfn.uServSock.recvfrom(servfn.BUFSIZE)
	data = data.decode('utf-8')
	cmd = data[0:3]
	if cmd in cmd_dict.keys():
		func = cmd_dict[cmd]
		res = func(data, addr)
		if res == -1:   
			break
	else:
		answ = 'unknown command :( '
		servfn.uServSock.sendto( '%s' %(answ), addr)
# === end of work ====
print 'Сервер остановлен '.decode('utf-8')
