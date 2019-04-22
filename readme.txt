
Run the metaserver with the command python3 metaserver.py then run server.py with python3 server.py

Afterwards, type P2P on server to send flag to the metaserver, the metaserver will then refer port numbers to clientservers that are requesting to join the network.

This is a multi-threaded python server, the main thread is responsible for listening for client connections and then once a connection is established, a thread is dispatched to handle inpuRun the metaserver with the command python3 metaserver.py then run server.py with python3 server.py

Afterwards, type P2P on server to send flag to the metaserver, the metaserver will then refer port numbers to clientservers that are requesting to join the network.

This is a multi-threaded python server, the main thread is responsible for listening for client connections and then once a connection is established, a thread is dispatched to handle input.

The file-sharing has not been implemented.


There is a bug where sending the flag will result in "invalid flag" even though the flag is correct; if this happens just type the correct flag again and it will work.
