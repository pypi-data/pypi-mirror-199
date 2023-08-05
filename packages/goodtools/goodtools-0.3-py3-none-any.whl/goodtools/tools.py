import tkinter as tk
import socket
import threading
from tkinter import messagebox
import time


class tools:
    def __init__(self):
        self.x = None

    def delay(self, sec):
        time.sleep(sec)

    def start_thread(self, target, args=(), delay=None):
        if delay:
            tools.delay(self, delay)
        thread = threading.Thread(target=target, args=args())
        thread.start()
        return thread

    def isPalindrome(self, data):
        self.x = data
        self.x_list = list(str(self.x))
        self.index = 0
        self.same = 0
        for digit in self.x_list:
            self.index += 1
            if digit == self.x_list[len(self.x_list) - self.index]:
                self.same += 1
        if not self.index == self.same:
            return False
        else:
            return True

    def multiply(self, num1, num2):
        return str(int(num1) * int(num2))

    def divide(self, num1, num2):
        return str(int(num1) / int(num2))

    def plus(self, num1, num2):
        return str(int(num1) + int(num2))

    def minus(self, num1, num2):
        return str(int(num1) - int(num2))

    def is_valid_parentheses(self, s: str) -> bool:
        stack = []
        mapping = {")": "(", "}": "{", "]": "["}
        for char in s:
            if char in mapping:
                top_element = stack.pop() if stack else '#'
                if mapping[char] != top_element:
                    return False
            else:
                stack.append(char)
        return not stack

    def merge_sorted_lists(self, list1, list2):
        merged_list = []
        i = j = 0
        while i < len(list1) and j < len(list2):
            if list1[i] < list2[j]:
                merged_list.append(list1[i])
                i += 1
            else:
                merged_list.append(list2[j])
                j += 1
        merged_list.extend(list1[i:])
        merged_list.extend(list2[j:])
        return merged_list

    def evaluate(self, expression):
        try:
            result = eval(expression)
            return result
        except (SyntaxError, ZeroDivisionError):
            return "Invalid expression"

    def is_valid_number(self, data):
        try:
            float(data)
            return True
        except ValueError:
            return False

    def filter_real_numbers(self, data):
        real_numbers = []
        for elem in data:
            if isinstance(elem, (int, float)):
                real_numbers.append(elem)
        return real_numbers

    def all_real_numbers(self, numbers):
        for num in numbers:
            if not isinstance(num, (int, float)):
                return False
        return True



class GUI:
    def __init__(self, title="GUI", icon=None, width=500, height=500):
        self.ver = "0.3"
        self.root = tk.Tk()
        self.root.title(title)
        print("Tools GUI")
        print("------------")
        print("Based on Tkinter")
        print("(C)2023 Luis Schuimer NetCast NLC")
        print("------------")
        print(f"Version: {self.ver}")
        print("-------------")
        if icon:
            self.root.iconbitmap(icon)
        self.root.geometry(f"{width}x{height}")
        self.elements = []

    def add_label(self, text, font_size=12):
        label = tk.Label(self.root, text=text, font=("Arial", font_size))
        label.pack()
        self.elements.append(label)
        return label

    def add_button(self, text, command=None, font_size=12, width=10, height=2):
        button = tk.Button(self.root, text=text, command=command, font=("Arial", font_size), width=width,
                           height=height)
        button.pack()
        self.elements.append(button)
        return button

    def add_entry(self, font_size=12, width=20):
        entry = tk.Entry(self.root, font=("Arial", font_size), width=width)
        entry.pack()
        self.elements.append(entry)
        return entry

    def add_textbox(self, font_size=12, width=50, height=10):
        textbox = tk.Text(self.root, font=("Arial", font_size), width=width, height=height)
        textbox.pack()
        self.elements.append(textbox)
        return textbox

    def get_elements(self):
        return self.elements

    def change_element(self, element, **kwargs):
        for key in kwargs:
            if key == "text":
                element.config(text=kwargs[key])
            elif key == "command":
                element.config(command=kwargs[key])
            elif key == "font_size":
                element.config(font=("Arial", kwargs[key]))
            elif key == "width":
                element.config(width=kwargs[key])
            elif key == "height":
                element.config(height=kwargs[key])

    def show(self):
        print("GUI started...")
        self.root.mainloop()

    def msg_box(self, title, message):
        messagebox.showinfo(title, message)

    def reset_screen(self):
        for element in self.elements:
            element.destroy()

    def set_size(self, width, height):
        self.root.geometry(f"{width}x{height}")

    def set_title(self, title):
        self.root.title(title)

    def set_icon(self, icon):
        self.root.iconbitmap(icon)

    def get_textbox_data(self, textbox):
        return textbox.get("1.0", tk.END).strip()


class Client_Chat:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        self.client_socket.sendall(f"{self.username} has joined the chat".encode())
        threading.Thread(target=self.receive_data).start()

    def send_data(self, data):
        self.client_socket.sendall(f"{self.username}: {data}".encode())

    def receive_data(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                print(data)
            except:
                print("Connection lost")
                break

    def disconnect(self):
        self.client_socket.sendall(f"{self.username} has left the chat".encode())
        self.client_socket.close()


class Server_Chat:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.clients = []

    def listen(self):
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connected by {client_address}")
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    print(f"Disconnected from {client_socket.getpeername()}")
                    self.clients.remove(client_socket)
                    client_socket.close()
                    break
                print(f"Received from {client_socket.getpeername()}: {data}")
                for client in self.clients:
                    if client != client_socket:
                        client.sendall(data.encode())
            except:
                print(f"Disconnected from {client_socket.getpeername()}")
                self.clients.remove(client_socket)
                client_socket.close()
                break