import socket
import threading
import os
import signal

# Classe com as cores a serem exibidas
class cores:
    BRANCO = '\033[37m'
    AZUL = '\033[34m'
    CIANO = '\033[36m'
    VERDE = '\033[32m'
    AMARELO = '\033[33m'
    VERMELHO = '\033[31m'
    RESET = '\033[0m'

s = socket.socket(socket.AF_INET6 , socket.SOCK_DGRAM )

ip = "::"
porta = 3205
s.bind((ip,porta))

print(f"{cores.AMARELO}\t\t\t====>  UDP DIRECT CHAT   <====={cores.RESET}")

d_ip = input(f"{cores.VERDE}IP do Destino: {cores.RESET}")
d_porta = int(input(f"{cores.VERDE}Porta: {cores.RESET}"))

print(f"{cores.VERMELHO}\nDigite 'exit' ou Ctrl + C para sair.{cores.RESET}")

def stop(sig=None, frame=None):
    print("Você fechou a conexão")
    s.sendto("exit".encode() , (d_ip,d_porta) )
    os._exit(0)
    

signal.signal(signal.SIGINT, stop)

def send():
    while True:
        msg = input()
        if msg == "exit":
            stop()
        print(f"{cores.AMARELO}[Você]: {cores.VERMELHO}{msg}{cores.RESET}")
        s.sendto(msg.encode() , (d_ip,d_porta) )

def rec():
    while True:
        msg = s.recvfrom(1024)
        if msg[0].decode() == "exit":
            print(f"Conexão fechada por {msg[1][0]}")
            os._exit(0)
        print(f"{cores.AMARELO}\t\t\t\t[{msg[1][0]}:{msg[1][1]}]: {cores.CIANO}{msg[0].decode()}{cores.RESET}")

x1 = threading.Thread( target = send )
x2 = threading.Thread( target = rec )

x1.start()
x2.start()
