# simple UDP chat,  A.B.Glazov
#coding: utf8
#== подключить библиотеки
from Tkinter import *
from socket import *
import threading
from time import *
import time
import ttk
import tkFileDialog
import subprocess

#== сокет для приема сообщений
HOST_IN = ''
PORT_IN = 3000
BUFSIZE = 1024
SOCKADDR_IN = (HOST_IN,PORT_IN)
uServSock = socket(AF_INET,SOCK_DGRAM)
uServSock.bind(SOCKADDR_IN)
#== список значений загружаемого файла для values Combobox
v = []
#== список адрессов user-ов
users = []
#== очередь для приема сообщений и флаг ее занятости
ls_in =[]
busy_in = 0
#== функция приема сообщений
def work_in():
        global ls_in
        global busy_in
        global users
        while True:
                data,addr = uServSock.recvfrom(BUFSIZE)
                if addr not in users:
                        users.append(addr)
                itsatime = time.strftime("%H.%M.%S", time.localtime())
                loc_data = data.decode('cp1251')
                st = 'received from: ' +  addr[0] + ':' + str(addr[1]) + '  [' + itsatime + ']' + ' msg: '  + loc_data
                for user in users:
                        if addr != users:
                                uServSock.sendto(data,user)
                while busy_in:
                        sleep(0.001)
                busy_in = 2
                ls_in.append(st)
                busy_in = 0

                sleep(0.001)
        uServSock.close()

#== поток приема сообщений
tr_in = threading.Thread( target = work_in )
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
tr_out = threading.Thread( target = work_out )
tr_out.daemon = True
tr_out.start()
#= выход из чата
def Quit(event):
    global root
    root.destroy()
#= Загрузка IP адрессов с txt файла
def LoadFile(event):
    global v
    fn = tkFileDialog.Open(root, filetypes = [('*.txt files', '.txt')]).show()
    if fn == '':
        return
    cb.delete(0, 'end')
    with open(fn, 'rt') as f:
         line = f.readline()
         v = f.read()
         cb.set(line)
         cb.configure(values = v)
#= Сохранение IP адрессов в txt файле
def SaveFile(event):
    fn = tkFileDialog.SaveAs(root, filetypes = [('*.txt files', '.txt')]).show()
    if fn == '':
        return
    if not fn.endswith(".txt"):
        fn+=".txt"
    open(fn, 'wt').write(cb.get())

#== основная программа: графическая часть
root = Tk()
root.geometry("660x666+400+100")
root.title("UDP Чат")
#== установка статичного окна
root.resizable(width=False, height=False)
#== стиль для верхней панели настроек
style = ttk.Style()
style.theme_settings("default", {
   "TCombobox": {
       "configure": {"padding": 5},
       "map": {
           "background": [("active", "green2"),
                          ("!disabled", "green4")],
           "fieldbackground": [("!disabled", "green3")],
           "foreground": [("focus", "OliveDrab1"),
                          ("!disabled", "OliveDrab2")]
       }
   }
})
##== панель для ввода сообщений (нижняя)
pn_out = Frame(root,bg = '#bfbfbf', bd = 2)
pn_out.pack(side = 'bottom', fill = 'both')

###== метка для Ip адреса
#Label(pn_out, text = '', bg='darkred' ).grid( row=0, column=0)
#Label(pn_out, text = 'Ip_dest:' ).grid( row=1, column=0)

###== функция и поле ввода Ip адреса получателя
def set_ipout(event):
        global SOCKADDR_SRV
        ip_out = cb.get()
        SOCKADDR_SRV = (ip_out,PORT_SRV)
#== Combobox
cb = ttk.Combobox(root, width = 50, values = v)
cb.bind('<Return>', set_ipout)
cb.bind('<<ComboboxSelected>>', set_ipout)
cb.pack()
#ed_ipout = Entry(pn_out, width = 30)
#ed_ipout.grid( row=1, column=1)
#ed_ipout.bind('<Return>',set_ipout)

###== метка для поля отправляемого сообщения
#msg = Label(pn_out, text = 'message:' ).grid( row=1, column=1)

def arp(event):
        sp = subprocess.Popen("arp -a", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.read()
        tb_mess.insert(END, sp.decode('cp866'))


###== функция и поле ввода отправляемого сообщения
def send_mess(event):
    mess_out = ed_out.get().strip()
    if len(mess_out) > 0:
            tb_mess.insert(END, "\n>>> " + mess_out)
            ed_out.delete(0,END)
            ls_out.append(mess_out)

ed_out = Entry(pn_out, width = 90)
ed_out.grid( row = 1, column = 1)
ed_out.bind('<Return>',send_mess)

#== Кнопки Load,Save,Quit
loadBtn = Button(root, text = 'Load')
saveBtn = Button(root, text = 'Save')
quitBtn = Button(root, text = 'Quit')
okBtn = Button(root, text = 'Accept settings')

loadBtn.bind("<Button-1>", LoadFile)
saveBtn.bind("<Button-1>", SaveFile)
quitBtn.bind("<Button-1>", Quit)
okBtn.bind("<Button-1>", set_ipout)

loadBtn.place(x = 1, y = 1, width = 55, height = 20)
saveBtn.place(x = 56, y = 1, width = 55, height = 20)
quitBtn.place(x = 111, y = 1, width = 55, height = 20)
okBtn.place(x = 492, y = 1, width = 84, height = 20)

#== Кнопка отправки сообщений
bn = Button(pn_out, text = "Enter")
bn.bind("<Button-1>", send_mess)
bn.place(x = 530,y = -3,width = 128, height = 25)
bt = Button(root, text = "Arp packet")
bt.bind("<Button-1>", arp)
bt.place(x = 578, y = 1, width = 82, height = 20)
##== панель для вывода получекнных сообщений (основная)
pn_mess = Frame(root, height = 570, width = 700)
pn_mess.pack(side = 'top', expand = 1, fill = 'both')

###== текстовое поле для вывода получекнных сообщений
tb_mess = Text(pn_mess, height = 30, wrap=WORD )
tb_mess.pack(side = 'left', fill = 'both', expand = 1)
###== функция с применением цветов при нажатии на кнопку
def oks():
    okBtn['text'] = 'Аpplied'
    okBtn['bg'] = '#289c0e'
    okBtn['activebackground'] = '#f20c0c'
    okBtn['fg'] = '#ffffff'
    okBtn['activeforeground'] = '#ffffff'
def aS():
    bt['text'] = 'Аrp +'
    bt['bg'] = '#f20c0c'
    bt['activebackground'] = '#289c0e'
    bt['fg'] = '#ffffff'
    bt['activeforeground'] = '#ffffff'
###== полоса прокрутки для текстового поля получекнных сообщений
sb_mess = Scrollbar(pn_mess)
sb_mess['command'] = tb_mess.yview
tb_mess['yscrollcommand'] = sb_mess.set
okBtn['command'] = oks
bt['command'] = aS
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
