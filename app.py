"""
Login to a server from an IPv4 addres
but get logged into an IPv6 server

- can I use SSHForcedCommand to force command to a proxy to the IPv6 server?
    - At this point, we know the user and therefore the server(s) they 'own'
"""
import sys
import paramiko
from flask import Flask, render_template
from jinja2 import Template
import subprocess
import random
import os

BASE_DIR = os.getenv("BASE_DIR")
TCP_PROXY_IP = os.getenv("TCP_PROXY_IP")
IPV6_SERVER_EXAMPLE = os.getenv("IPV6_SERVER_EXAMPLE")

app = Flask(__name__)


@app.route("/")
def index():
    port = random.randrange(49152, 65535)
    # Template out the ssh config file
    with open(
        f"{BASE_DIR}/files_to_mount/ssh_config/config.j2",  # noqa: E501
    ) as fp:
        template = Template(fp.read())
        rendered_template = template.render(
            ipv6=IPV6_SERVER_EXAMPLE, tcp_proxy=TCP_PROXY_IP
        )
        with open(
            f"{BASE_DIR}/files_to_mount/ssh_config/config",  # noqa: E501
            "w",
        ) as dst:
            dst.write(rendered_template)

    command = f"docker run -it -d -v {BASE_DIR}/files_to_mount/ssh_config/:/root/.ssh/ --rm -p {port}:7681 myttyd"  # noqa: E501
    subprocess.run(command, shell=True)
    return render_template("index.html", port=port)


def do_ssh():
    HOST_IP = changeme
    HOST_USERNAME = "ipv4user"
    COMMAND = "ls"
    SSH_PASSWORD = sys.argv[1]

    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if SSH_PASSWORD is not None:
        client.connect(
            HOST_IP,
            username=HOST_USERNAME,
            password=SSH_PASSWORD,
            allow_agent=False,
            look_for_keys=False,  # noqa: E501
        )
    else:
        client.connect(HOST_IP, username=HOST_USERNAME)

    stdin, stdout, stderr = client.exec_command(COMMAND)
    result = stdout.read().decode("utf-8")
    print(result)

    # close the ssh connection
    client.close()
