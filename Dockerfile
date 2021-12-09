FROM python:3.9-alpine
RUN mkdir /direct-chat
COPY "both-side" /direct-chat/both-side
COPY "cliente-servidor" /direct-chat/cliente-servidor
ENV DIRECT_CHAT_IPV6="::"
ENV DIRECT_CHAT_PORTA="3205"