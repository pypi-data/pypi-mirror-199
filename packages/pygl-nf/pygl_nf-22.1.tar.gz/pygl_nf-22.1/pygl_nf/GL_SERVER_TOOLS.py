import socket
from colorama import Fore,Style
from time import sleep, time
import os

class Client():
    def __init__(self,port=8000,host='localhost') -> None:
        self.port = port
        self.host = host
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        
        try:
            
            self.client.connect((self.host,self.port))

            data = self.client.recv(1024).decode('utf-8')
            os.system('cls')
            print(Style.BRIGHT+Fore.GREEN+
            '----------------------------------'+Style.RESET_ALL+Fore.RESET)
            print( Style.BRIGHT+Fore.YELLOW+'   % '+Style.DIM+Fore.GREEN + f'Connected to {data}.'+Style.RESET_ALL)
            print( Style.BRIGHT+Fore.YELLOW+'   % '+Style.DIM+Fore.GREEN + f'Server Host: {self.host}'+Style.RESET_ALL)
            print( Style.BRIGHT+Fore.YELLOW+'   % '+Style.DIM+Fore.GREEN + f'Server Port: {self.port}'+Style.RESET_ALL)
            print(Style.BRIGHT+Fore.GREEN+
            '----------------------------------'+Style.RESET_ALL+Fore.RESET)
        except:
            os.system('cls')
            print(Style.BRIGHT+Fore.RED+
            '----------------------------------'+Style.RESET_ALL+Fore.RESET)
            print( Style.BRIGHT+Fore.YELLOW+'   % '+Style.DIM+Fore.RED + f'Not connected.'+Style.RESET_ALL)
            print( Style.BRIGHT+Fore.YELLOW+'   % '+Style.DIM+Fore.RED + f'Server Host: {self.host}'+Style.RESET_ALL)
            print( Style.BRIGHT+Fore.YELLOW+'   % '+Style.DIM+Fore.RED + f'Server Port: {self.port}'+Style.RESET_ALL)
            print(Style.BRIGHT+Fore.RED+
            '----------------------------------'+Style.RESET_ALL+Fore.RESET)
   
    def Update(self,sec):
        sleep(sec)


class Server():
    def __init__(self,port=8000,host='localhost',server_name='My_server') -> None:
        self.port = port
        self.host = host
        self.server_name = server_name

        self._clients = []

        self._recv_data = 'none'
        self._recv_update = False
        self._serv_connect = False

        try:
            self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.server.bind((self.host,self.port))
            self.server.setblocking(0)
            self.server.listen(5)

            os.system('cls')
            print(Style.BRIGHT+Fore.GREEN+
            '----------------------------------'+Style.RESET_ALL+Fore.RESET)
            print(Style.DIM+Fore.GREEN+f'    Server: ({self.server_name}) created.')
            print(   f'    Host: {self.host}')
            print(   f'    Port: {self.port}'+Style.RESET_ALL+Fore.RESET )
            print(Style.BRIGHT+Fore.GREEN+
            '----------------------------------'+Style.RESET_ALL+Fore.RESET)

  
        except:
            os.system('cls')
            print(Style.BRIGHT+Fore.RED+
            '----------------------------------'+Style.RESET_ALL+Fore.RESET)
            print(Style.DIM+Fore.RED+f'Server: ({self.server_name}) not created.')
            print(f'Host: ! {self.host} !')
            print(f'Port: ! {self.port} !'+Style.RESET_ALL+Fore.RESET )
            print(Style.BRIGHT+Fore.RED+
            '----------------------------------'+Style.RESET_ALL+Fore.RESET)

    def Wait_Conect(self,milisec):  
        sleep(milisec)
        try:
                self._serv_connect = True
                client , addr =  self.server.accept()
                
                client.setblocking(0)
                print( Fore.YELLOW+'% '+Fore.RESET,end='')
                print(Fore.MAGENTA+f'Client: {addr} connected.'+Fore.RESET)
                self._clients.append([client,addr])
                client.send(f'{self.server_name}'.encode('utf-8'))
                return client , addr
                
        except:
                self._serv_connect = False
                return None , None
         
    @property  
    def clients_count(self):
        return len(self._clients)

    
        




