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
    def __init__(self):
        self.s = socket.socket(socket.AF_INET6 , socket.SOCK_DGRAM )
        self.porta = int(os.getenv("DIRECT_CHAT_PORTA", "3205"))
        self.ipv6_dest = None
        self.porta_dest = None
    
    def conectToIp(self, ip6, p):
        self.ipv6_dest = ip6
        self.porta_dest = p
        try:
            self.s.sendto("".encode() , (self.ipv6_dest,self.porta_dest) )
        except:
            print(f"{cores.VERMELHO}\nErro ao se conectar com {cores.VERDE}{self.ipv6_dest}{cores.AMARELO}:{cores.CIANO}{self.porta_dest}{cores.RESET}")
            self.close()
            os._exit(0)
        print(f"{cores.AMARELO}\nConversando com {cores.VERDE}{self.ipv6_dest}{cores.AMARELO}:{cores.CIANO}{self.porta_dest}{cores.RESET}")
        print(f"{cores.VERMELHO}\nDigite 'exit' ou Ctrl + C para sair.{cores.RESET}")
        signal.signal(signal.SIGINT, self.stop)
        self.send()
    
    def send(self):
        while True:
            msg = input()
            if msg == "exit":
                self.stop()
            try:
                self.s.sendto(f"{cores.CIANO}{self.porta}{cores.AMARELO}]: {cores.CIANO}{msg}".encode() , (self.ipv6_dest,self.porta_dest) )
                print(f"{cores.AMARELO}[Você]: {cores.VERMELHO}{msg}{cores.RESET}")
            except KeyboardInterrupt:
                break
            except:
                print(f"{cores.VERDE}{self.ipv6_dest}{cores.AMARELO}:{cores.CIANO}{self.porta_dest}{cores.VERMELHO} não está conectado{cores.RESET}")
            
    def close(self):
        self.s.close()
    def stop(self, sig=None, frame=None):
        print(f"{cores.AMARELO}Você fechou a conexão")
        self.close()
        os._exit(0)

if __name__ == "__main__":
    print(f"{cores.AMARELO}\t\t\t====>  CLIENT - UDP DIRECT CHAT   <====={cores.RESET}")
    d = DirectChat()
    if len(sys.argv) > 2:
        d.conectToIp(sys.argv[1], int(sys.argv[2]))
    elif os.getenv("DIRECT_CHAT_IPV6_DEST") is not None and os.getenv("DIRECT_CHAT_PORTA_DEST") is not None:
        d.conectToIp(os.getenv("DIRECT_CHAT_IPV6_DEST"), int(os.getenv("DIRECT_CHAT_PORTA_DEST")))
    else:
        print(f"{cores.VERMELHO}\nPasse como argumentos o ipv6 e a porta.\nEx: python3 chat2.py <ipv6> <porta>\nOu use as variaveis de ambiente DIRECT_CHAT_IPV6_DEST e DIRECT_CHAT_PORTA_DEST para informar o ip e porta para mandar mensagens.{cores.RESET}")
        d.close()
        os._exit(0)
