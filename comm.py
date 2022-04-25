#!/usr/bin/env python3
# comm.py>
from configparser import *
import sys, logging, snap7, time

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Define configuration
def config():
    try:
        config = ConfigParser()
        config.read("config.ini")
        var1 = config.get("DEFAULT", "ip")
        var2 = config.get("DEFAULT", "port")
        var3 = config.get("DEFAULT", "db1")
        var4 = config.get("DEFAULT", "db2")
        return var1, var2, var3, var4
    except Exception as e:
        logger.error(e)
        return -1

# Define main function
def main(var1, var2):
    # Read configuration
    ip = config()[0]
    port = int(config()[1])
    db1_layout = config()[2]
    db2_layout = config()[3]
    if ip == -1 or port == -1 or db1_layout == -1 or db2_layout == -1:
        return -1

    # Connect to client
    try:
        client = snap7.client.Client()
        client.connect(ip, 0, 0, port)
    except:
        return -1
    
    # While connected to client
    while client.get_connected() == True:
        try:
            all_data = client.db_read(var1, 0, var2)
            db1 = snap7.util.DB(0, all_data, db1_layout, 0, 1)

            all_data = client.db_read(var1 + 1, 0, var2 - 10)
            db2 = snap7.util.DB(0, all_data, db2_layout, 0, 1)

            #logger.info(db10[0])
            #print(db10[0]["testbool3"])
            #print(db10[0])
            return db1, db2
        except:
            return -1