import os
import zipfile
import xml.etree.ElementTree as ET
import csv
import datetime
import shutil

class ShellEmulator:
    def __init__(self, config_path):
        self.load_config(config_path)
        self.setup_filesystem()
        self.current_directory = "/"
        self.start_logging()

    def load_config(self, config_path):
        tree = ET.parse(config_path)
        root = tree.getroot()
        self.username = root.find('username').text
        self.hostname = root.find('hostname').text
        self.fs_zip_path = root.find('fs_zip').text
        self.log_path = root.find('log_file').text

    def setup_filesystem(self):
        with zipfile.ZipFile(self.fs_zip_path, 'r') as zip_ref:
            self.fs_root = "/tmp/virtual_fs"
            zip_ref.extractall(self.fs_root)

    def start_logging(self):
        self.log_file = open(self.log_path, 'w', newline='')
        self.logger = csv.writer(self.log_file)
        self.logger.writerow(['timestamp', 'user', 'command'])

    def log(self, command):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.logger.writerow([timestamp, self.username, command])

    def run(self):
        try:
            while True:
                command = input(f"{self.username}@{self.hostname}:{self.current_directory}$ ")
                self.execute_command(command.strip())
        except KeyboardInterrupt:
            self.exit()

    def execute_command(self, command):
        if command == "exit":
            self.exit()
        elif command.startswith("ls"):
            self.ls()
        elif command.startswith("cd"):
            self.cd(command.split(" ")[1:])
        elif command.startswith("whoami"):
            self.whoami()
        else:
            print(f"Команда '{command}' не найдена")
        self.log(command)

    def ls(self):
        path = os.path.join(self.fs_root, self.current_directory[1:])
        for item in os.listdir(path):
            print(item)

    def cd(self, args):
        if not args:
            return
        path = args[0]
        if path == "..":
            self.current_directory = os.path.dirname(self.current_directory)
        else:
            new_path = os.path.join(self.fs_root, path)
            if os.path.isdir(new_path):
                self.current_directory = os.path.join(self.current_directory, path)
            else:
                print(f"Ошибка: '{path}' — не существует")

    def whoami(self):
        print(self.username)

    def exit(self):
        print("Выход из эмулятора.")
        self.log_file.close()
        exit()

if __name__ == "__main__":
    emulator = ShellEmulator("config.xml")
    emulator.run()
