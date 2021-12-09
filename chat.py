import socket
import threading
import os
import signal
import sys

# Classe com as cores a serem exibidas
class cores:
    BRANCO = '\033[37m'
    AZUL = '\033[34m'
    CIANO = '\033[36m'
    VERDE = '\033[32m'
    AMARELO = '\033[33m'
    VERMELHO = '\033[31m'
    RESET = '\033[0m'

class DirectChat():
    def __init__(self, ipv6="::", porta:int=3205):
        self.s = socket.socket(socket.AF_INET6 , socket.SOCK_DGRAM )
        self.ipv6 = ipv6
        self.porta = porta
        self.ipv6_dest = None
        self.porta_dest = None
        self.conectado = False
        self.s.bind((ipv6,porta))
        self.x1 = threading.Thread( target = self.rec )
        self.x2 = threading.Thread( target = self.send )
    
    def conectToIp(self, ip6, p):
        self.ipv6_dest = ip6
        self.porta_dest = p
        self.x1.start()
        self.x2.start()
        print(f"{cores.AMARELO}\nConversando com {cores.VERDE}{self.ipv6_dest}:{self.porta_dest}{cores.RESET}")
        print(f"{cores.VERMELHO}\nDigite 'exit' ou Ctrl + C para sair.{cores.RESET}")
        signal.signal(signal.SIGINT, self.stop)
    
    def rec(self):
        while True:
            msg = self.s.recvfrom(1024)
            if msg[0].decode() == "":
                self.conectado = True
            elif msg[0].decode() == "exit":
                print(f"{cores.VERMELHO}\t\t\t\t{msg[1][0]}:{msg[1][1]} desconectou{cores.RESET}")
            else:
                print(f"{cores.AMARELO}\t\t\t\t[{msg[1][0]}:{msg[1][1]}]: {cores.CIANO}{msg[0].decode()}{cores.RESET}")

    def send(self):
        while True:
            msg = input()
            if msg == "exit":
                self.stop()
            try:
                self.s.sendto(msg.encode() , (self.ipv6_dest,self.porta_dest) )
                print(f"{cores.AMARELO}[Você]: {cores.VERMELHO}{msg}{cores.RESET}")
            except:
                print(f"{cores.VERMELHO}{self.ipv6_dest}:{self.porta_dest} não está conectado{cores.RESET}")
            
    
    def stop(self, sig=None, frame=None):
        if self.conectado:
            print("Você fechou a conexão")
            self.s.sendto("exit".encode() , (self.ipv6_dest,self.porta_dest) )
            self.conectado = False
        os._exit(0)

if __name__ == "__main__":
    print(f"{cores.AMARELO}\t\t\t====>  UDP DIRECT CHAT   <====={cores.RESET}")
    d = DirectChat(os.getenv("DIRECT_CHAT_IPV6", "::"), int(os.getenv("DIRECT_CHAT_PORTA", "3205")))
    if len(sys.argv) > 2:
        d.conectToIp(sys.argv[1], int(sys.argv[2]))
    elif os.getenv("DIRECT_CHAT_IPV6_DEST") is not None and os.getenv("DIRECT_CHAT_PORTA_DEST") is not None:
        d.conectToIp(os.getenv("DIRECT_CHAT_IPV6_DEST"), int(os.getenv("DIRECT_CHAT_PORTA_DEST")))
    else:
        print(f"{cores.VERMELHO}\nPasse como argumentos o ipv6 e a porta.\nEx: python3 chat2.py <ipv6> <porta>\nOu use as variaveis de ambiente DIRECT_CHAT_IPV6_DEST e DIRECT_CHAT_PORTA_DEST para informar o ip e porta para mandar mensagens.{cores.RESET}")
        os._exit(0)
