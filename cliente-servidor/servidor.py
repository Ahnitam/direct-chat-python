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
        self.s.bind((ipv6,porta))
        print(f"{cores.VERMELHO}\nDigite 'exit' ou Ctrl + C para sair.{cores.RESET}")
        signal.signal(signal.SIGINT, self.stop)
        self.rec()
    
    def rec(self):
        while True:
            msg = self.s.recvfrom(1024)
            if msg[0].decode() == "":
                pass
            else:
                print(f"{cores.AMARELO}\t\t\t\t[{cores.VERDE}{msg[1][0]}{cores.AMARELO}:{msg[0].decode()}{cores.RESET}")

    def stop(self, sig=None, frame=None):
        print(f"{cores.AMARELO}Você fechou a conexão")
        self.s.close()
        os._exit(0)

if __name__ == "__main__":
    print(f"{cores.AMARELO}\t\t\t====> SERVIDOR - UDP DIRECT CHAT   <====={cores.RESET}")
    ipv6 = os.getenv("DIRECT_CHAT_IPV6", "::")
    p = int(os.getenv("DIRECT_CHAT_PORTA", "3205"))
    print(f"{cores.AMARELO}\nExecutando em {cores.VERDE}{ipv6}{cores.AMARELO}:{cores.CIANO}{p}{cores.RESET}")
    d = DirectChat(ipv6, p)
