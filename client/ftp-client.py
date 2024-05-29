import socket

HOST = 'localhost'
PORT = 8881
work = True

# Функция для сохранения файла на клиенте


def save_file(file_name, content):
    with open(file_name, 'wb') as file:
        file.write(content)

# Функция для загрузки файла с сервера


def download_file(file_name):
    sock.send(f"download {file_name}".encode('utf-8'))
    content = sock.recv(1024)
    save_file(file_name, content)


# Функция для чтения файла с клиента
def read_file(file_name):
    with open(file_name, 'rb') as file:
        content = file.read()
        return content

# Функция для загрузки файла на сервер


def upload_file(file_name):
    sock.send(f"upload {file_name}".encode('utf-8'))
    content = read_file(file_name)
    sock.send(content)
    response = sock.recv(1024).decode('utf-8')
    print(response)


while work:
    request = input('>')

    sock = socket.socket()
    sock.connect((HOST, PORT))
    # загрузка файла с сервера
    if request.startswith('download'):
        download_file(request.split()[1])
        continue
    # загрузка файла на сервера
    if request.startswith('upload'):
        upload_file(request.split()[1])
        continue
    sock.send(request.encode())

    response = sock.recv(1024).decode()
    print(response)

    if request == 'exit':
        work = False
    sock.close()
