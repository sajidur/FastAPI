from ast import Bytes
from base64 import decodebytes
from typing import Union
from paramiko import SSHClient
from fastapi import FastAPI
import paramiko
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/ssh")
def post():
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('host', username='sajidur', password='mypass')
    # Run a command (execute PHP interpreter)
    stdin, stdout, stderr = client.exec_command('sudo -S <<< mypass docker ps')
    # print(type(stdin))  # <class 'paramiko.channel.ChannelStdinFile'>
    # print(type(stdout))  # <class 'paramiko.channel.ChannelFile'>
    #print(type(stderr))  # <class 'paramiko.channel.ChannelStderrFile'>

    # Optionally, send data via STDIN, and shutdown when done
    stdin.write('<?php echo "Hello!"; sleep(2); ?>')
    stdin.channel.shutdown_write()

    # Print output of command. Will wait for command to finish.
    print(f'STDOUT: {stdout.read().decode("utf8")}')
    print(f'STDERR: {stderr.read().decode("utf8")}')

    # Get return code from command (0 is default for success)
    print(f'Return code: {stdout.channel.recv_exit_status()}')

    # Because they are file objects, they need to be closed
    stdin.close()
    stdout.close()
    stderr.close()
    client.close()
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}