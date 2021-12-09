import socket
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

class DirectChat():
    def __init__(self, ipv6="::", porta:int=3205):
        # Cria um socket UDP/IPv6
        self.s = socket.socket(socket.AF_INET6 , socket.SOCK_DGRAM )
        self.ipv6 = ipv6
        self.porta = porta
        # Escuta conexões nesse endereço IP e porta
        self.s.bind((ipv6,porta))
        print(f"{cores.VERMELHO}\nDigite 'exit' ou Ctrl + C para sair.{cores.RESET}")
        # Adiciona ação personalizada quando o usuario pressionar Ctrl + C
        signal.signal(signal.SIGINT, self.stop)
        # Chama o metodo que vai receber as mensagens em um looping
        self.rec()
    
    def rec(self):
        while True:
            # Recebe mensagem do cliente
            msg = self.s.recvfrom(1024)
            if msg[0].decode() == "":
                pass
            else:
                # Imprime a mensagem com algumas formatações
                print(f"{cores.AMARELO}\t\t\t\t[{cores.VERDE}{msg[1][0]}{cores.AMARELO}:{msg[0].decode()}{cores.RESET}")

    def stop(self, sig=None, frame=None):
        print(f"{cores.AMARELO}Você fechou a conexão")
        # Fecha o socket
        self.s.close()
        # Finaliza a aplicação
        os._exit(0)

if __name__ == "__main__":
    print(f"{cores.AMARELO}\t\t\t====> SERVIDOR - UDP DIRECT CHAT   <====={cores.RESET}")
    # Recebe os dados de ip e porta da variaveis de ambiente e caso não exista usa o valor padrão
    ipv6 = os.getenv("DIRECT_CHAT_IPV6", "::")
    p = int(os.getenv("DIRECT_CHAT_PORTA", "3205"))
    print(f"{cores.AMARELO}\nExecutando em {cores.VERDE}{ipv6}{cores.AMARELO}:{cores.CIANO}{p}{cores.RESET}")
    # Inicia o servidor
    DirectChat(ipv6, p)
