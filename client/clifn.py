# -*- coding: utf-8 -*-
# === clifn.py ====
from socket import *
import platform
import subprocess
import os
import sys
import ftplib

# === form client socket ====
LOCKHOST = '127.0.0.1'          #-- for ftp on the localhost
HOST = '127.0.0.1'
PORT = 3000
BUFSIZE = 1024
SOCKADDR = (HOST,PORT)
uCliSock = socket(AF_INET,SOCK_DGRAM)
uCliSock.settimeout(5)
servip_set = set()
LOGIN = ''
PASSWORD = ''
# === handling functions ====
def ftp_loggin(param):
        global LOGIN
        global PASSWORD
        LOGIN = raw_input('LOGIN > ')
        PASSWORD = raw_input('PASSWORD > ')
def set_addr(param):
        global HOST
        global SOCKADDR
        global PORT
        HOST = param[3:]
        SOCKADDR = (HOST,PORT)
        print "new_host: ", HOST
        return 1

def send_command(param):
        #print 'send_text: ', param 
        uCliSock.sendto(param, SOCKADDR)
        try:
                answ, addr = uCliSock.recvfrom(BUFSIZE)
        except:
                answ = 'нет ответа  :('.decode('utf-8')
        print SOCKADDR[0], " ", answ
        return 1

def multisend_command(param):
        global HOST
        global SOCKADDR
        global PORT

        ip_list = list(servip_set)
        if len(ip_list) > 0:
                for ip in ip_list:
                        HOST = ip
                        SOCKADDR = (HOST,PORT)
                        uCliSock.sendto(param, SOCKADDR)
                        try:
                                answ, addr = uCliSock.recvfrom(BUFSIZE)
                        except: 
                                answ = 'нет ответа  :('.decode('utf-8')
                        print SOCKADDR[0], " ", answ
        else:
                print "нет живых серверов :(".decode('utf-8')
        return 1

def help():
        print "====================== СПРАВКА ПО КОМАНДАМ ======================".decode('utf-8')
        print "Вы можете ввести: адресс, текст, команду имени файла".decode('utf-8')
        print "Для примера:".decode('utf-8')
        print "csa:10.1.2.13          - установить адрес для контакта ".decode('utf-8')
        print "sst:privet medved      - отправить текст для выбранного IP".decode('utf-8')
        print "sse:privet             - отправить текст с эхо ".decode('utf-8')
        print "spf:1.txt              - положить файл с сервера на ftp".decode('utf-8')
        print "sgf:2.txt              - получить файл с ftp на сервер".decode('utf-8')
        print "sew:                   - завершить работу выбранного сервера".decode('utf-8')
        print ""
        print "mst:privet medved      - отправить текст на все серверы".decode('utf-8')
        print "mse:privet             - отправить текст с echofor на все серверы".decode('utf-8')
        print "mpf:1.txt              - положить файл со всех серверов в ftp".decode('utf-8')
        print "mgf:2.txt              - получить файл с ftp на все серверы".decode('utf-8')
        print ""
        print "cpf:3.txt              - положить файл с клиента на FTP".decode('utf-8')
        print "cgf:4.txt              - получить файл с ftp клиенту".decode('utf-8')
        print "cli:                   - список серверов ip".decode('utf-8')
        print "clf:                   - список файлов сервера основной директории".decode('utf-8')
        print "clf:123                - список файлов в директории".decode('utf-8')
        print "cdf:123.txt            - удалить файл в директории".decode('utf-8')
        print "ccd:ABGlazov           - сосздать директорию".decode('utf-8')
        print "cdd:Сортировка         - проверить удалить директорию".decode('utf-8')
        print "cpi:ya.ru              - проверить пинг".decode('utf-8')
        print "cew:                   - конец работы с клиентом".decode('utf-8')
        print "================================================================="
def put_file(param):                    #-- FTP server on the client host
        print 'put_file: ', param 
        file_name = param[3:]
        ftp = ftplib.FTP(LOCKHOST)
        ftp.login(LOGIN, PASSWORD) 
        try:
                ftp.storbinary("STOR " + file_name, open(file_name, "rb"), 1024)
                ftp.quit()
        except:
                print "ftp error:  :(";
                return -1
        return 1

def get_file(param):
        print 'get_file: ', param 
        file_name = param[3:]
        ftp = ftplib.FTP(LOCKHOST)
        ftp.login(LOGIN, PASSWORD)
        try:
                ftp.retrbinary("RETR " + file_name, open(file_name, "wb").write)
                ftp.quit()
        except:
                print "ftp error:  :("
                return -1
        return 1

def list_ip(param):
        ip_list = list(servip_set)
        print "Активные IPs:".decode('utf-8')
        for ip in ip_list:
                print ip
        return 1

def end_work(param):
        uCliSock.close() 
        return -1
def create_dir(param):
        try:
                print 'create_dir: ', param[3:]
                ftp = ftplib.FTP(LOCKHOST)
                ftp.login(LOGIN, PASSWORD)
                ftp.mkd(param[3:].decode('cp1251').encode('utf-8'))
                print 'Dir: ' + param[3:] + ' created!'
        except ftplib.error_perm:
                print 'Такая директория уже существует.'.decode('utf-8')
def delete_dir(param):
        try:
                print 'delete_dir ', param[3:]
                ftp = ftplib.FTP(LOCKHOST)
                ftp.login(LOGIN, PASSWORD)
                ftp.rmd(param[3:].decode('cp1251').encode('utf-8'))
                print 'Dir: ' + param[3:] + ' deleted.'
        except ftplib.error_perm:
                print "Директория не пуста или такой директории не существует".decode('utf-8')
def delete_files(param):
        try:
                print 'delete_files: ', param[3:]
                ftp = ftplib.FTP(LOCKHOST)
                ftp.login(LOGIN, PASSWORD)
                ftp.delete(param[3:].decode('cp1251').encode('utf-8'))
                print 'File: ' + param[3:] + ' deleted.'
        except ftplib.error_perm:
                print "Нет такого файла.".decode('utf-8')        
def list_files(param):
        try:
                print 'list_files: ', param[3:]
                ftp = ftplib.FTP(LOCKHOST)
                ftp.login(LOGIN,PASSWORD)
                #ftp.login("freeezzz", "qwerty")
                if not param[3:]:
                        print 'В директории ['.decode('utf-8') + ftp.pwd() + ']:'
                        files = []
                        ftp.dir(files.append)
                        #files = ftp.nlst()
                        for f in files:
                                print f.decode('utf-8')
                        if not files:
                                print 'Директория пуста.'.decode('utf-8')
                else:
                        ftp.cwd('/' + param[3:])
                        files = []
                        ftp.dir(files.append)
                        print '======================'
                        print 'В директории ['.decode('utf-8') + ftp.pwd() + ']:'
                        for f in files:
                                print f.decode('utf-8')
                        if not files:
                                print 'Директория пуста.'.decode('utf-8')
        except ftplib.error_perm:
                print "Нет указанного файла или директории".decode('utf-8')
def ping(param):
        command = ['ping', '-n', '5', param[3:]]
        response = subprocess.call(command)
        if response == 0:
            print 'От '.decode('utf-8') + param[3:] + ' есть ответ!'.decode('utf-8')
        else:
            print 'От '.decode('utf-8') + param[3:] + ' нет ответа :('.decode('utf-8')


