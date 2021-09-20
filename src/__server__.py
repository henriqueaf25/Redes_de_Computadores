import socket
import threading
import pandas as pd

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 8080
ADDR = (SERVER, PORT)
COD = 'utf-8'
DC = 'exit'
NOPE = 'n'
BIT = 64

# iniciando o socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# definindo como um socket server
server.bind(ADDR)

# lendo o .csv da lista telefonica
pessoas = pd.read_csv("./Telefones.csv", sep=",",
                      names=["Nome", "Telefone"], index_col=False)
pessoas = pessoas.applymap(
    lambda y: " ".join(y.split()).upper() if isinstance(y, str) else y,
    na_action='ignore')


# função que checa se existe a pessoa dada com entrada no .csv
def check(name, CONNECT):
    if name == "addPerson":
        return add_client(CONNECT)
    x = pessoas.loc[pessoas['Nome'] == name.upper()]
    if x.empty:
        return "Pessoa não encontrada. Deseja inseri-la na lista?[Y/N]"
    return x['Telefone'].to_string(header=False, index=False)


# função para adicionar pessoas no .csv
def add_client(CONNECT):
    global pessoas
    phone_len = CONNECT.recv(BIT).decode(COD)
    phone_len = int(phone_len)
    phone = CONNECT.recv(phone_len).decode(COD)
    nome_len = CONNECT.recv(BIT).decode(COD)
    nome_len = int(nome_len)
    nome = CONNECT.recv(nome_len).decode(COD)

    if not phone.isnumeric():
        return "Telefone inválido. Digite novamente o nome a ser pesquisado."
    df = {'Nome': nome.upper(), 'Telefone': phone}
    pessoas = pessoas.append(df, ignore_index=True)
    pessoas.to_csv("./Telefones.csv", index=False, header=False)
    return "Pessoa adicionada com sucesso. Caso deseje continuar, digite um nome. Caso contrário digite 'exit' ou 'n'."


# função para receber as entradas do client
def client_conn(CONNECT, address):
    print("Endereço ", address, " conectado")
    linked = True
    while linked:
        message = CONNECT.recv(BIT).decode(COD)
        if message:
            message = int(message)
            msg = CONNECT.recv(message).decode(COD)
            lw = msg.lower()
            if lw == DC or lw == NOPE:
                CONNECT.send(("Desconectado com sucesso").encode(COD))
                linked = False
            answer = check(msg, CONNECT)
            CONNECT.send((answer).encode(COD))
    CONNECT.close()
    print("Endereço ", address, " desconectou")


# função para iniciar o server
def init():
    server.listen()
    print("Server ", SERVER, " está ouvindo")
    while True:
        connect, address = server.accept()
        # aplicação multithread
        td = threading.Thread(target=client_conn, args=(connect, address))
        # para cada client conectado, uma thread é iniciada
        td.start()
        print("Conexoẽs: ", threading.activeCount() - 1)


# inicio do programa
init()
