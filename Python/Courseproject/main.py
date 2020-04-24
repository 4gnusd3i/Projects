#!/usr/bin/env python3

"""
This script makes use of the classes and methods defined in StockItAll.py. It presents the user with a CLI used to
interact with StockItAll.py and creates a server for remotely adding new items to the StockTracker.
At startup of the script, it will check for saved items and append them to StockTracker item_list.
At shutdown of the script, it will save the items contained in StockTracker item_list.

Author: 4gnusd3i
License: MIT
"""

import Courseproject.StockItAll as SIA
import csv
import threading
import socket
import time

# Variable for easier referencing to class in class-file
ST = SIA.StockTracker()


# Function for CLI operations
def cli():
    """
    This is the function that produces the CLI that is used to interact with StockItAll.py.
    The function is being ran on a separate thread 'thread_one'.
    At 'Startup', the function will run check_file() and sleep for 0.1 sec before starting 'Main Loop'.
    The 'Main Loop' included in this function, makes sure that the CLI remains active until the user wants to exit.
    At 'Shutdown', the function will run write_file() before the thread exits.

    Returns:
        None
    """
    cli_input = ""

    # Startup
    check_file()
    time.sleep(0.1)

    # Main Loop
    while cli_input != "5":
        print("----------------------------------------------------------------------------")
        cli_input = input("Please choose an option:\n"
                          "0. Display constructor usage\n"
                          "1. Add an item\n"
                          "2. Update an items amount\n"
                          "3. Show an items information\n"
                          "4. Show all items information\n"
                          "5. Exit\n"
                          "Input: ")

        if cli_input == "0":
            print("\nDisplaying __repr__ of item_list:")
            print(repr(ST.item_list))
        elif cli_input == "1":
            SIA.StockTracker.add_item_cli(ST)
        elif cli_input == "2":
            SIA.StockTracker.update_item_amount(ST)
        elif cli_input == "3":
            SIA.StockTracker.show_item(ST)
        elif cli_input == "4":
            SIA.StockTracker.show_all_items(ST)

    # Shutdown
    print("\nWriting changes to stock.csv")
    write_file()
    print("Exiting console\n")


# Function for server operations
def server():
    """
    This function uses the socket and the time module.
    The function is used to run a server that can be connected to by client.py and interacts with SockItAll.py.
    The function is being ran on a separate thread 'thread_two'.
    All messages produced by the server will be distinctly marked by '!SERVER! date+time !SERVER!'.
    At 'Configuration', all local variables used to initiate the server are defined.
    At 'Startup', the server will notify that it is waiting for an incoming connection and notify when it receives one.
    At 'Main Loop', the server will use the received data to interact with the StockTracker method add_item_server()
    defined in StockItAll.py, until the exit condition is met.
    At 'Shutdown', the server socket will close, so the thread can exit.

    Returns:
        None
    """
    # Configuration
    version = socket.AF_INET
    protocol = socket.SOCK_STREAM
    sock = socket.socket(version, protocol)

    ip = "127.0.0.1"
    port = 9182

    sock.bind((ip, port))
    sock.listen()

    # Startup
    print("\n!SERVER! {} !SERVER!\nWaiting for connection on {}:{}\n".format
          (time.strftime("%d.%m.%y %H:%M", time.localtime()), ip, port))
    con, address = sock.accept()
    print("\n!SERVER! {} !SERVER!\nIncoming connection from: {}\n".format
          (time.strftime("%d.%m.%y %H:%M", time.localtime()), address[0]))

    data = ""
    # Main Loop
    while data != "exit":
        data = con.recv(1024).decode()
        if data != "exit":
            try:
                ST.add_item_server(data)
                print("\n!SERVER! {} !SERVER!\n'{}' added to item_list\n".format
                      (time.strftime("%d.%m.%y %H:%M", time.localtime()), data))
            except Exception as e:
                print(e)

    # Shutdown
    print("\n!SERVER! {} !SERVER!\nClient disconnected! Shutting down server!\n".format
          (time.strftime("%d.%m.%y %H:%M", time.localtime())))
    sock.close()


# Function for checking/reading stock.csv
def check_file():
    """
    This function uses the csv module.
    The function attempts to read the stock.csv file and append the information found as objects in the StockTracker
    item_list created in StockItAll.py.
    If the file cannot be opened, it will assume the file does not exist and raise an IOError, which notifies the user
    that a new file will be created upon end of session.

    Returns:
        None
    """
    try:
        with open("stock.csv", "r") as file:
            print("Items loaded from stock.csv\n")
            reader = csv.reader(file)
            for row in reader:
                ST.item_list.append(SIA.StockItem(row[0], row[1], row[2]))
    except IOError:
        print("Stock file not found! A new file will be created at end of session...\n")


def write_file():
    """
    This function uses the csv module.
    The function creates a new file if there is none present, or overwrites the old file with the content of
    StockTracker item_list located in StockItAll.py.

    Returns:
        None
    """
    with open("stock.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for item in ST.item_list:
            writer.writerow([item.code, item.description, item.amount])


if __name__ == "__main__":
    thread_one = threading.Thread(target=cli)
    thread_two = threading.Thread(target=server)
    thread_one.start()
    thread_two.start()
