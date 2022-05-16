#!/usr/bin/env python3
# comm.py>
from configparser import *
import logging, logging.config, snap7

logging.config.dictConfig({'version': 1,'disable_existing_loggers': True,})
logger = logging.getLogger(__name__)

# Define configuration
def config():
    try:
        config = ConfigParser()
        config.read("config.ini")
        var1 = config.get("DEFAULT", "ip")
        var2 = int(config.get("DEFAULT", "port"))
        return var1, var2
    except Exception as e:
        logger.error(e)
        return -1

# Define main function
def main(var, **data):
    # Read configuration
    logger.debug("reading configuration")
    ip = config()[0]
    port = config()[1]
    if ip == -1 or port == -1:
        return -1

    # Connect to client
    try:
        logger.debug("connecting with " + ip + ":" + str(port))
        client = snap7.client.Client()
        client.connect(ip, 0, 0, port)
    except Exception as e:
        logger.error(e)
        return -1
    
    # While connected to client
    while client.get_connected() == True:
        logger.info("connected with " + ip + ":" + str(port))
        try:
            if var != "check":
                logger.debug("receiving data")
                all_data = client.db_read(data.get('db'), 0, data.get('size'))
                db_data = snap7.util.DB(0, all_data, data.get('layout'), 0, 1)
                if var == "send":
                    logger.debug("sending data")
                    db_data[0][data.get('id')] = data.get('val')
                    client.db_write(data.get('db'), 0, db_data._bytearray)
                    return
                if var == "recv":
                    return db_data
            else:
                logger.debug("connection checked")
                return
        except Exception as e:
            logger.error(e)
            return -1

# DEBUG TEST
if __name__ == "__main__":
    test = "send"
    list= { "db":2,
            "size":10,
            "id":"id1",
            "val":99,
            "layout":"""
0           id1             INT
2           id2             INT
4           id3             INT
6           id4             INT
8           id5             INT
"""
        }
    data = main(test, **list)
    if data != -1 and test == "recv":
        print(data[0])
    else:
        print(data)