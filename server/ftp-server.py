import socket
import os
import shutil

# Функция для получения списка файлов и папок в текущей директории


def list_files():
    files = os.listdir('.')
    return files

# Функция для создания новой папки


def create_folder(folder_name):
    os.makedirs(folder_name)

# Функция для удаления папки


def delete_folder(folder_name):
    shutil.rmtree(folder_name)

# Функция для создания нового файла с заданным содержимым


def create_file(file_name, content):
    with open(file_name, 'w') as file:
        file.write(content)

# Функция для чтения содержимого файла


def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()

# Переименовать файл


def rename_file(file_name, new_file_name):
    os.rename(file_name, new_file_name)

# Функция для сохранения файла на сервере


def save_file(file_name, content):
    with open(file_name, 'wb') as file:
        file.write(content)


    # Создание сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8881))
server_socket.listen(1)


print("Сервер файлового менеджера запущен.")

work = True
while work:
    client_socket, addr = server_socket.accept()
    print(f"Установлено соединение с {addr}")

    while work:
        request = client_socket.recv(1024).decode('utf-8')

        if not request:
            break

        if request == "list":
            files = list_files()
            client_socket.send(str(files).encode('utf-8'))

        elif request.startswith("create_folder"):
            folder_name = request.split()[1]
            create_folder(folder_name)
            client_socket.send("Папка создана".encode('utf-8'))

        elif request.startswith("delete_folder"):
            folder_name = request.split()[1]
            delete_folder(folder_name)
            client_socket.send("Папка удалена".encode('utf-8'))

        elif request.startswith("create_file"):
            file_name, content = request.split(maxsplit=2)[1:]
            create_file(file_name, content)
            client_socket.send("Файл создан".encode('utf-8'))

        elif request.startswith("read_file"):
            file_name = request.split()[1]
            content = read_file(file_name)
            client_socket.send(content.encode('utf-8'))

        elif request.startswith('rename_file'):
            file_name = request.split()[1]
            new_file_name = request.split()[2]
            rename_file(file_name, new_file_name)
            client_socket.send("Файл переименован".encode('utf-8'))

        elif request.startswith("download"):
            file_name = request.split(maxsplit=1)[1]
            content = read_file(file_name)
            client_socket.send(content)

        elif request.startswith("upload"):
            file_name = request.split(maxsplit=1)[1]
            content = client_socket.recv(1024)
            save_file(file_name, content)
            client_socket.send(
                "Файл успешно сохранен на сервере".encode('utf-8'))

        elif request.startswith('exit'):
            work = False
        else:
            client_socket.send("Неверный запрос".encode('utf-8'))

    client_socket.close()
