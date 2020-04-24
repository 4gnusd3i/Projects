#!/usr/bin/env python3

"""
This script uses tkinter to create a GUI for the user to input values.
These values are concatenated and sent to the server running in main.py, by the use of sockets.
The received data is used by main.py to create new items to be stored in StockTracker item_list.

Author: 4gnusd3i
License: MIT
"""

import socket
import tkinter
import tkinter.messagebox as mbox

# Configuration: socket
version = socket.AF_INET
protocol = socket.SOCK_STREAM
sock = socket.socket(version, protocol)

sock.connect(("127.0.0.1", 9182))


# Function for concatenating the input from the GUI
def concatenate():
    """
    This function uses the socket and the tkinter module.
    This function retrieves the values entered into the entry boxes in the GUI.
    It attempts to concatenate these values, before sending the correctly formatted string to the
    server running in main.py
    If the entered values does not match the expected type, it will raise a ValueError and inform the user of the
    correct value types.
    When this is done, the entry boxes will be cleared, and be ready for new input.

    Returns:
        None
    """
    try:
        code = int(ent_code.get())
        desc = str(ent_desc.get())
        amnt = int(ent_amnt.get())
        concat = "{}, {}, {}".format(code, desc, amnt)
        sock.send(concat.encode())
        mbox.showinfo("Item added", "{} Successfully added".format(concat))
    except ValueError:
        mbox.showinfo("ERROR!", "Make sure that 'Code' and 'Amount' is an integer,"
                                " while 'Description' is a string!")
    ent_code.delete(0, "end")
    ent_desc.delete(0, "end")
    ent_amnt.delete(0, "end")


# Function for terminating the connection to server
def terminate_connection():
    """
    This function uses the socket module.
    This function will be called from on_exit().
    The function sends the exit_command to the server to terminate the connection on
    both sides, before closing the socket.

    Returns:
        None
    """
    exit_command = "exit"
    sock.send(exit_command.encode())
    sock.close()


# Function for exiting program upon exiting the GUI
def on_exit():
    """
    This function uses the tkinter module.
    The function will be called by the window manager event.
    On confirmation by user, the function wil call terminate_connection() and end the GUI session.

    Returns:
        None
    """
    if mbox.askokcancel("Quit", "Do you want to terminate server connection?"):
        terminate_connection()
        gui.destroy()


# Configuration: tkinter

# Create GUI window
gui = tkinter.Tk()
gui.title("StockItem GUI")
gui.geometry("300x130")

# Add label and entry box for item.code
lbl_code = tkinter.Label(gui, text="Item Code:")
lbl_code.place(x=5, y=10)
ent_code = tkinter.Entry(gui)
ent_code.place(x=150, y=10)

# Add label and entry box for item.description
lbl_desc = tkinter.Label(gui, text="Item Description:")
lbl_desc.place(x=5, y=40)
ent_desc = tkinter.Entry(gui)
ent_desc.place(x=150, y=40)

# Add label and entry box for item.amount
lbl_amnt = tkinter.Label(gui, text="Item Amount:")
lbl_amnt.place(x=5, y=70)
ent_amnt = tkinter.Entry(gui)
ent_amnt.place(x=150, y=70)

# Add button for executing concatenate()
btn_send = tkinter.Button(gui, text="Add Item", command=concatenate)
btn_send.place(x=175, y=100)

# Use window manager event to execute on_exit()
gui.protocol("WM_DELETE_WINDOW", on_exit)

# Main Loop
gui.mainloop()
