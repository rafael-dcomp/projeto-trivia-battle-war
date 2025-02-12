import socket

host = "52.90.108.237"  # IP da instância EC2
port = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

mensagem = client_socket.recv(1024)
print(mensagem.decode())

client_socket.close()
