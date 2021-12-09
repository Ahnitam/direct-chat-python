# Direct CHAT em Python

Atividade desenvolvida para a disciplina de Redes de Computadores.


=========== Both Side ===========

docker run --network host -ti direct-chat python /direct-chat/both-side/chat.py \<ip> \<porta>
  
ou
  
docker run --network host -ti -e DIRECT_CHAT_IPV6_DEST=\<ip> -e DIRECT_CHAT_PORTA_DEST=\<porta> direct-chat python /direct-chat/both-side/chat.py

=========== Cliente ===========
  
docker run --network host -ti direct-chat python /direct-chat/cliente-servidor/cliente.py \<ip> \<porta>
  
ou
  
docker run --network host -ti -e DIRECT_CHAT_IPV6_DEST=\<ip> -e DIRECT_CHAT_PORTA_DEST=\<porta> direct-chat python /direct-chat/cliente-servidor/cliente.py

============ Servidor ===========
  
docker run --network host -ti direct-chat python /direct-chat/cliente-servidor/servidor.py


Referências:

https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
