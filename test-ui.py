#!/usr/bin/env python3
from tkinter import *
from tkinter import font
from tkinter import messagebox
from configparser import *
import logging, comm

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level="DEBUG")
logger = logging.getLogger(__name__)

root=Tk() # Create main window
root.title('Test UI') # Window title
root.configure(bg='white') # Window background
root.minsize(400, 200) # Window size minimum
#root.state('zoomed') # Normal fullscreen
#root.attributes("-fullscreen", True) # Canvas fullscreen

# Define configuration
def config():
    var2 = []
    y = 0
    try:
        config = ConfigParser()
        config.read("config.ini")
        var1 = config.get("DEFAULT", "updatetime_ms")
        for x in range(1,10000):
            if config.has_option("DB" + str(x), "size"):
                var2.append([[],[],[]])
                var2[y][0] = x
                var2[y][1] = int(config.get("DB" + str(x), "size"))
                var2[y][2] = config.get("DB" + str(x), "layout")
                y = y+1
            else:
                next
        return var1, var2
    except:
        return -1

def updater():
    data= { "db":db[1][0],
            "size":db[1][1],
            "layout":db[1][2]
        }
    data = comm.main("recv", **data)
    if data != -1:
        connection['text'] = "Connected"
        text1['text'] = data[0]["id1"]
    root.after(time, updater)

def submit():
    if entry1.get() != "":
        data= { "db":db[1][0],
                "size":db[1][1],
                "layout":db[1][2],
                "id":"id1",
                "val":int(entry1.get())
            }
        comm.main("send", **data)
    else:
        logger.debug("field is empty")


# Define sub window
connection = Label(root, text="Not connected")
text1 = Label(root, text="")
entry1 = Entry(root, text="")
btn1 = Button(root, text="send", command=submit)

# Place root objects in order
connection.pack(side=TOP)
text1.pack(side=TOP)
entry1.pack(side=TOP)
btn1.pack(side=BOTTOM)

# Read configuration
logger.debug("reading general configuration")
time = config()[0]
db = config()[1]
if db == -1:
    logger.error("configuration error")
    messagebox.showerror("ERROR", "Configuration ERROR")
else:
    updater()
    mainloop() # Running mainloop always last