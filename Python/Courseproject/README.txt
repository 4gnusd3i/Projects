# Courseproject
This was made as part of a courseproject in Python at the school I attended.
Our task was to make a classfile that were to handle individual stockitems, store them and offer
methods for adding, displaying and modifying items. Further we were asked to make a main script
that were to present the user with a CLI to perform such actions. The main script should check a file
for saved items from earlier sessions on launch and them load them. On shutdown the main script 
should save the current items to file. The script should also run a server to which a client could
connect to in order to add new items remotely. Therefore it was to run 2 threads in order to
accommodate for both the CLI and the server. Lastly the client script should present the user with a
simple GUI made with Tkinter and should communicate with the main script, to allow the user to add items. 

The files should be run in the following order: main.py -> client.py
This is to start the server in main.py before the client in client.py triest to connect.
Upon shutdown the main.py script will not exit before the connection from client.py is terminated.
