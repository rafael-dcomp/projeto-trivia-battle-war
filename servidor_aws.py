import socket

HOST = '0.0.0.0'  # Aceita conexões de qualquer IP
PORT = 5000  # Porta para comunicação

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Aguarda conexões

print(f"Servidor rodando em {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Conexão recebida de {client_address}")
    client_socket.sendall(b"Bem-vindo ao servidor!\n")
    client_socket.close()
