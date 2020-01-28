# CLAI server

We use socket communication with the CLAI server to listen to requests from the client (Bash terminal)
and respond with commands from the skills.

## Usage

##### Open socket server
```bash
>> python3 ./src/clai.py start 
```
###### directives
|directive|Description |
|--------|-------------| 
| start| Start the socket server if it isn't up | 
| stop     | Stop the socket server       | 

###### options
 
| param | default | description |
|--------|-------------|-------------|
| --host | localhost | host to open server and clients |
| --port | 8010 | port to open server and clients |

 
##### Open Client
```bash
>> python3 multiclient_con.py <host> <port>
```

