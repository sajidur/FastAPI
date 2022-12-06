from fastapi import APIRouter
from paramiko import SSHClient
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from view_model.ssh_execute import SSHExecute
from config.db import conn
from models.command import commands
from config.ssh_config import host_conf,password_conf,user_conf
import paramiko


sshCltr = APIRouter()

@sshCltr.get("/")
def read_root():
    return {"Hello": host_conf}

@sshCltr.post("/ssh/execute", description="Execute a SSH Script")
def execute(ssh: SSHExecute):
    result= conn.execute(commands.select().where(commands.c.id ==ssh.id)).first()
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host_conf, username=user_conf, password=password_conf)
    # Run a command (execute PHP interpreter)
    stdin, stdout, stderr = client.exec_command(result.command)
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
    json_compatible_item_data = jsonable_encoder(stdout.channel.recv_exit_status())
    return JSONResponse(content=json_compatible_item_data)

@sshCltr.post("/ssh/add", tags=["SSHExecutes"], response_model=SSHExecute, description="Create a new ssh command")
def create_user(ssh: SSHExecute):
    new_command = {"name": ssh.name, "command": ssh.command}
    result = conn.execute(commands.insert().values(new_command))
    return conn.execute(commands.select().where(commands.c.id == result.lastrowid)).first()

@sshCltr.post("/ssh")
def post():
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host_conf, username=user_conf, password=password_conf)
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
    json_compatible_item_data = jsonable_encoder(stdout.channel.recv_exit_status())
    return JSONResponse(content=json_compatible_item_data)