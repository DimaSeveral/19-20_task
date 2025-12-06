import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import socket
import json
from messages import MENUS, TASK1, TASK2, TASK4

def send_request(task: str, params: dict):
    """Отправляет запрос на сервер и возвращает ответ"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(('localhost', 9999))
            request = {"task": task, "params": params}
            sock.send(json.dumps(request).encode('utf-8'))
            response = sock.recv(4096).decode('utf-8')
            return json.loads(response)
    except ConnectionRefusedError:
        print("❌ Не удалось подключиться к серверу. Запущен ли server.py?")
        return None
    except Exception as e:
        print(f"❌ Ошибка соединения: {e}")
        return None

def run_task1():
    print(f"\n{TASK1['title']}")
    text = input(TASK1["prompt_text"]).strip()
    if not text:
        print(TASK1["empty_input"])
        return

    response = send_request("task1", {"text": text})
    if response:
        if response["status"] == "success":
            result = response["result"]
            if result:
                print(TASK1["result"].format(result))
            else:
                print(TASK1["no_unique"])
        else:
            print("Ошибка:", response["message"])

def run_task2():
    print(f"\n{TASK2['title']}")
    text = input(TASK2["prompt_text"]).strip()
    if not text:
        print(TASK2["empty_input"])
        return

    response = send_request("task2", {"text": text})
    if response:
        if response["status"] == "success":
            words = response["result"]["words"]
            length = response["result"]["length"]
            if words:
                print(TASK2["result"].format(words, length))
            else:
                print(TASK2["no_words"])
        else:
            print("Ошибка:", response["message"])

def run_task4():
    print(f"\n{TASK4['title']}")
    print(TASK4["intro"])
    
    a_str = input(TASK4["prompt_a"]).strip()
    if not a_str:
        print(TASK4["empty_input"])
        return
    try:
        a = list(map(int, a_str.split()))
    except ValueError:
        print(TASK4["error_input"].format("Некорректные цифры"))
        return

    b_str = input(TASK4["prompt_b"]).strip()
    if not b_str:
        print(TASK4["empty_input"])
        return
    try:
        b = list(map(int, b_str.split()))
    except ValueError:
        print(TASK4["error_input"].format("Некорректные цифры"))
        return

    op = input(TASK4["prompt_op"]).strip().lower()
    if op not in ('add', 'sub'):
        print(TASK4["invalid_op"])
        return

    response = send_request("task4", {"a": a, "b": b, "op": op})
    if response:
        if response["status"] == "success":
            print(TASK4["result"].format(response["result"]))
        else:
            print("Ошибка:", response["message"])

def main():
    print("Клиент запущен. Подключение к серверу...")
    while True:
        print("\n" + "="*50)
        print(MENUS["main_title"])
        print("1. " + MENUS["task1"])
        print("2. " + MENUS["task2"])
        print("3. " + MENUS["task4"])
        print("4. " + MENUS["exit"])
        choice = input(MENUS["prompt_choice"]).strip()

        if choice == '1':
            run_task1()
        elif choice == '2':
            run_task2()
        elif choice == '3':
            run_task4()
        elif choice == '4':
            print(MENUS["exit_message"])
            break
        else:
            print(MENUS["invalid_choice"])

if __name__ == "__main__":
    main()