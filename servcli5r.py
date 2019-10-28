# simple UDP chat,  A.B.Glazov
#coding: utf8
#== подключить библиотеки
from Tkinter import *
from socket import *
import threading
from time import *
import ftplib
import ttk
import tkFileDialog
import os
#== сокет для приема сообщений
HOST_IN = ''
PORT_IN = 3000
BUFSIZE = 1024
SOCKADDR_IN = (HOST_IN,PORT_IN)
uServSock = socket(AF_INET,SOCK_DGRAM)
uServSock.bind(SOCKADDR_IN)

#== очередь для приема сообщений и флаг ее занятости
ls_in =[]
busy_in = 0

#== функция приема сообщений
def work_in():
        global ls_in
        global busy_in
        while True:
                data,addr = uServSock.recvfrom(BUFSIZE)
                loc_data = data.decode('cp1251')
                st = 'receivedd from: ' +  addr[0] + ', data: ' +  loc_data

                while busy_in:
                        sleep(0.001)
                busy_in = 2
                ls_in.append(st)
                busy_in = 0

                sleep(0.001)

        uServSock.close()

#== поток приема сообщений
tr_in = threading.Thread( target = work_in)
tr_in.daemon = True
tr_in.start()

#== сокет для отправки сообщений
HOST_OUT = '127.0.0.1'
PORT_OUT = 3000
BUFSIZE = 1024
SOCKADDR_OUT = (HOST_OUT,PORT_OUT)
uCliSock = socket(AF_INET,SOCK_DGRAM)

#== очередь отправки сообщений и признак ее занятости
ls_out =[]
busy_out = 0

#== сокет получателя сообщений
HOST_SRV = '10.1.0.190'
PORT_SRV = 3000
SOCKADDR_SRV = (HOST_SRV,PORT_SRV)

#== функция отправки сообщений
def work_out():
        global ls_out
        global busy_out
        global SOCKADDR_SRV
        while True:
                if not busy_out:
                        busy_out = 1
                        if len(ls_out) > 0:
                                st = ls_out.pop(0)
                                st = st.encode('cp1251')
                                uCliSock.sendto(st, SOCKADDR_SRV)
                        busy_out = 0
                sleep(0.001)
        uCliSock.close()

#== поток отправки сообщений
tr_out = threading.Thread( target = work_out)
tr_out.daemon = True
tr_out.start()

#== основная программа: графическая часть
root = Tk()
root.geometry("660x666+400+100")
root.title("Чат")
root.resizable(width=False, height=False)

##== панель для ввода сообщений (нижняя)
pn_out = Frame(root, height = 50, bg = 'darkgreen')
pn_out.pack(side = 'bottom', fill = 'x')

###== метка для Ip адреса
Label(pn_out, text = '', bg='darkgreen' ).grid( row=0, column=0)
Label(pn_out, text = 'Ip_dest:' ).grid( row=1, column=0)

###== функция и поле ввода Ip адреса получателя
def set_ipout(event):
        global SOCKADDR_SRV
        ip_out = ed_ipout.get().strip()
        SOCKADDR_SRV = (ip_out,PORT_SRV)

ed_ipout = Entry(pn_out, width = 30)
ed_ipout.grid( row=1, column=1)
ed_ipout.bind('<Return>',set_ipout)

###== метка для поля отправляемого сообщения
Label(pn_out, text = 'message:' ).grid( row=1, column=3)

###== функция и поле ввода отправляемого сообщения
def send_mess(event):
    mess_out = ed_out.get().strip()
    if len(mess_out) > 0:
            tb_mess.insert(END, "\n>>> " + mess_out)
            ed_out.delete(0,END)
            ls_out.append(mess_out)

ed_out = Entry(pn_out, width = 30)
ed_out.grid( row=1, column=4)
ed_out.bind('<Return>',send_mess)

def put_file(event):
        fn = tkFileDialog.Open(root, filetypes = [('all files', '*.*')]).show()
        namef = os.path.basename(fn)
        try:
               ftp = ftplib.FTP('127.0.0.1')
               ftp.login('freeezzz', 'qwerty')
               ftp.storbinary("STOR " + namef, open(namef, 'rb') , 1024)
               tb_mess.insert(END, '\npuf_file: ' + namef)
               ftp.quit()
        except:
               tb_mess.insert(END, '\nftp error.')
               return -1
        return 1
loadBtn = Button(root, text = 'Load')
loadBtn.bind("<Button-1>", put_file)
loadBtn.pack()
##== панель для вывода получекнных сообщений (основная)
pn_mess = Frame(root, height = 570, width = 700)
pn_mess.pack(side = 'top', expand = 1, fill = 'both')

###== текстовое поле для вывода получекнных сообщений
tb_mess = Text(pn_mess, height = 30, wrap=WORD )
tb_mess.pack(side = 'left', fill = 'both', expand = 1)

###== полоса прокрутки для текстового поля получекнных сообщений
sb_mess = Scrollbar(pn_mess)
sb_mess['command'] = tb_mess.yview
tb_mess['yscrollcommand'] = sb_mess.set
sb_mess.pack(side = 'right', fill = 'y')

#== главная функция, запускаемая в цикле
def main():
    if len( ls_in ) > 0:
        mess_in  = ls_in.pop(0)
        tb_mess.insert(END, "\n<<< " + mess_in)
    root.after(30, main)

main()

#== запуск приложения в работу
root.mainloop()
