#!/usr/bin/env python3
# comm.py>
from configparser import *
import sys, logging, snap7, time

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

# Define configuration
def config():
    try:
        config = ConfigParser()
        config.read("config.ini")
        var1 = config.get("DEFAULT", "ip")
        var2 = config.get("DEFAULT", "port")
        return var1, var2
    except Exception as e:
        logging.error(e)
        return -1

# Define main function
def main(var1, var2):
    # Read configuration
    ip = config()[0]
    port = int(config()[1])
    if ip == -1 or port == -1:
        return -1

    db10_layout="""
    0           id              INT
    2           name            STRING[6]
    10.0        testbool1       BOOL
    10.1        testbool2       BOOL
    10.2        testbool3       BOOL
    10.3        testbool4       BOOL
    10.4        testbool5       BOOL
    10.5        testbool6       BOOL
    10.6        testbool7       BOOL
    10.7        testbool8       BOOL
    12          testreal        REAL
    16          testdword       DWORD"""

    try:
        client = snap7.client.Client()
        client.connect(ip, 0, 0, port)
        client.get_connected()
        all_data = client.db_read(var1, 0, 20)
        db10 = snap7.util.DB(0, all_data, db10_layout, 0, 1)

        print(db10[0])
        #print(db10[0]["testbool3"])
        #print(db10[0])
    except Exception as e:
        #logging.error(e)
        return -1

while 1:
    if main(1, 0) == -1:
        sys.exit()
    time.sleep(3)