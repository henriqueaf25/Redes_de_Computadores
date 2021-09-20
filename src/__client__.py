import socket

# endereço para a conexão
SERVER = "127.0.1.1"
PORT = 8080
ADDR = (SERVER, PORT)
BITS = 64
# formato utf-8 para codificação de mensagens
COD = 'utf-8'
# definição do client
# AF_NET para ipv4 e SOCK_STREAM para protocolo TCP
CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    CLIENT.connect(('127.0.0.1', PORT))
except:
    CLIENT.connect(ADDR)


# variaveis auxiliares para inclusão de pessoas
auxlist = []
index = 0

# Na função GET, cada mensagem tem duas funções write()//.send(). Uma para o tamanho da mensagem para fins de decodificação e outra para a mensagem em si


def GET(message):
    global index, auxlist
    # condições específicas para a inclusão de pessoas na agenda
    if message.lower() == 'y' and index > 1 and auxlist[index-1] == "Pessoa não encontrada. Deseja inseri-la na lista?[Y/N]":
        print("Digite o número de telefone a ser associado a",
              auxlist[index-2])
        phone = input()
        nome = auxlist[index-2]
        send_phone = phone.encode(COD)
        send_phone_distance = str(len(send_phone)).encode(COD)
        send_phone_distance += b' ' * (BITS - len(send_phone_distance))
        send_nome = nome.encode(COD)
        send_nome_distance = str(len(send_nome)).encode(COD)
        send_nome_distance += b' ' * (BITS - len(send_nome_distance))
        add_check = "addPerson"
        send_add_check = add_check.encode(COD)
        send_add_check_distance = str(len(send_add_check)).encode(COD)
        send_add_check_distance += b' ' * (BITS - len(send_add_check_distance))
        CLIENT.send(send_add_check_distance)
        CLIENT.send(send_add_check)
        CLIENT.send(send_phone_distance)
        CLIENT.send(send_phone)
        CLIENT.send(send_nome_distance)
        CLIENT.send(send_nome)
        print(CLIENT.recv(2048).decode(COD))
    # caso não atenda as especificações de inclusão, a mensagem será checada no .csv
    else:
        auxlist.append(message)
        index += 1
        send_message = message.encode(COD)
        send_distance = str(len(send_message)).encode(COD)
        send_distance += b' ' * (BITS - len(send_distance))
        # método write()
        CLIENT.send(send_distance)
        CLIENT.send(send_message)
        # método read()
        answer = CLIENT.recv(2048).decode(COD)
        if answer == "Pessoa não encontrada. Deseja inseri-la na lista?[Y/N]":
            auxlist.append(answer)
            index += 1
        print(answer)


print("Digite o nome da pessoa a ser consultada")
print("Digite 'exit' ou 'n' a qualquer momento para sair")
# enquanto o usuário não digitar 'exit' ou 'n', o programa continuará rodando. Caso digite, a conexão será encerrada(server side) e o programa será encerrado.
while True:
    name = input()
    GET(name)
    if name.lower() == 'n' or name.lower() == 'exit':
        break
