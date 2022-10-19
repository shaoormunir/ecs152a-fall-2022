# Week 5
This folder contains the relevant code for week 5 discussions. The *echo-client.py* and *echo-server.py* contains a simple example of client and servers implemented using socket APIs.

To run them on a command line tool, use the following command to first run the server:
```
python3 echo-server.py -p <portnumber> -i <hostname>
```
Then open a new terminal window and run the following command to run the client:
```
python3 echo-client.py -p <portnumber> -i <hostname>
```
Make sure that the port numbers and the hostnames are the same in both commands, otherwise you will encounter a refused connection error.

The *multiconn-client.py* and *multiconn-server.py* are examples of servers and clients using selectors to ensure non-blocking, asynchronous communication.

First run the server on the command line using:
```
python3 multiconn-server.py -p <portnumber> -i <hostname>
```

Then run the client using:
```
python3 multiconn-client.py -p <portnumber> -i <hostname> -n <connections>
```


## Happy Coding!