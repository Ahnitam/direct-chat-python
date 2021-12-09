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
        # Cria um socket UDP/IPv6
        self.s = socket.socket(socket.AF_INET6 , socket.SOCK_DGRAM )
        self.ipv6 = ipv6
        self.porta = porta
        self.ipv6_dest = None
        self.porta_dest = None
        # Escuta conexões nesse endereço IP e porta
        self.s.bind((ipv6,porta))
        # Cria uma Thread para receber as mensagens
        self.x1 = threading.Thread( target = self.rec )
    
    def conectToIp(self, ip6, p):
        self.ipv6_dest = ip6
        self.porta_dest = p
        # Inicia a Thread para receber as mensagens
        self.x1.start()

        print(f"{cores.AMARELO}\nConversando com {cores.VERDE}{self.ipv6_dest}{cores.AMARELO}:{cores.CIANO}{self.porta_dest}{cores.RESET}")
        print(f"{cores.VERMELHO}\nDigite 'exit' ou Ctrl + C para sair.{cores.RESET}")
        # Adiciona ação personalizada quando o usuario pressionar Ctrl + C
        signal.signal(signal.SIGINT, self.stop)
        # Chama o metodo para enviar mensagens
        self.send()
    
    def rec(self):
        while True:
            # Recebe mensagem do cliente
            msg = self.s.recvfrom(1024)
            if msg[0].decode() == "":
                pass
            elif msg[0].decode() == "exit":
                # Imprime a mensagem que o usuario se desconectou
                print(f"{cores.VERMELHO}\t\t\t\t {cores.VERDE}{msg[1][0]}{cores.AMARELO}:{cores.CIANO}{msg[1][1]} desconectou{cores.RESET}")
            else:
                # Imprime a mensagem com algumas formatações
                print(f"{cores.AMARELO}\t\t\t\t[{cores.VERDE}{msg[1][0]}{cores.AMARELO}:{cores.CIANO}{msg[1][1]}{cores.AMARELO}]: {cores.CIANO}{msg[0].decode()}{cores.RESET}")

    def send(self):
        while True:
            # pede para o usuario digitar a msg
            msg = input()
            if msg == "exit":
                # se ele digitar exit a aplicação vai encerrar
                self.stop()
            try:
                # envia a msg codificada
                self.s.sendto(msg.encode() , (self.ipv6_dest,self.porta_dest) )
                print(f"{cores.AMARELO}[Você]: {cores.VERMELHO}{msg}{cores.RESET}")
            except KeyboardInterrupt:
                # Se o usuario apertar Ctrl + C ele sai do looping
                break
            except:
                # Se der erro, Imprime informando q o servidor não tá ativo
                print(f"{cores.VERDE}{self.ipv6_dest}{cores.AMARELO}:{cores.CIANO}{self.porta_dest}{cores.VERMELHO} não está conectado{cores.RESET}")
            
    
    def stop(self, sig=None, frame=None):
        # fecha o socket e encerra a aplicação
        print(f"{cores.AMARELO}Você fechou a conexão")
        # Envia a mensagem para o destinatario que estou encerrando a aplicação
        self.s.sendto("exit".encode() , (self.ipv6_dest,self.porta_dest) )
        self.s.close()
        os._exit(0)

if __name__ == "__main__":
    print(f"{cores.AMARELO}\t\t\t====>  UDP DIRECT CHAT   <====={cores.RESET}")
    # Recebe os dados de ip e porta da variaveis de ambiente e caso não exista usa o valor padrão
    ipv6 = os.getenv("DIRECT_CHAT_IPV6", "::")
    p = int(os.getenv("DIRECT_CHAT_PORTA", "3205"))
    # Cria um objeto da classe DirectChat
    d = DirectChat(ipv6, p)
    print(f"{cores.AMARELO}\nExecutando em {cores.VERDE}{ipv6}{cores.AMARELO}:{cores.CIANO}{p}{cores.RESET}")
    if len(sys.argv) > 2:
        # Caso o usuario tenha passado os parametros de ip e porta pela linha de comando ele usa esses parametros
        d.conectToIp(sys.argv[1], int(sys.argv[2]))
    elif os.getenv("DIRECT_CHAT_IPV6_DEST") is not None and os.getenv("DIRECT_CHAT_PORTA_DEST") is not None:
        # Se os parametros não forem passados ele tenta usar das variaveis de ambiente
        d.conectToIp(os.getenv("DIRECT_CHAT_IPV6_DEST"), int(os.getenv("DIRECT_CHAT_PORTA_DEST")))
    else:
        # Se nenhum dos casos anteriores forem atendidos ele informa para passar os argumetos e encerra a aplicação
        print(f"{cores.VERMELHO}\nPasse como argumentos o ipv6 e a porta.\nEx: python3 chat2.py <ipv6> <porta>\nOu use as variaveis de ambiente DIRECT_CHAT_IPV6_DEST e DIRECT_CHAT_PORTA_DEST para informar o ip e porta para mandar mensagens.{cores.RESET}")
        os._exit(0)
