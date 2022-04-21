#!/usr/bin/env python3
# comm.py>
from configparser import *
import sys, snap7

# Define configuration
def config():
    try:
        config = ConfigParser()
        config.read("config.ini")
        var1 = config.get("DEFAULT", "ip")
        var2 = config.get("DEFAULT", "port")
        return var1, var2
    except Exception as e:
        print("[+] ERROR,", e)
        return -1

# Define main function
def main(var1, var2):
    # Read configuration
    ip = config()[0]
    port = config()[1]
    if ip == -1 or port == -1:
        return -1

    try:
        print("[+] INFO, connecting")
        client = snap7.client.Client()
        client.connect(ip, 0, 0, port)
        client.get_connected()
        data = client.db_read(var1, var2, 4)
        print(data)
    except Exception as e:
        print("[+] ERROR,", e)
        return -1

if main("1", "0") == -1:
    sys.exit()