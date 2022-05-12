#!/usr/bin/env python3
from tkinter import *
from tkinter import font
from tkinter import messagebox
from configparser import *
import sys, logging, comm

root=Tk() # Create main window
root.title('Test UI') # Window title
root.configure(bg='white') # Window background
root.minsize(400, 200) # Window size minimum
#root.state('zoomed') # Normal fullscreen
#root.attributes("-fullscreen", True) # Canvas fullscreen
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

# Define configuration
def config():
    var1 = [[],[],[]]
    var2 = [[],[],[]]
    try:
        config = ConfigParser()
        config.read("config.ini")
        var1[0] = int(config.get("DB1", "address"))
        var1[1] = int(config.get("DB1", "size"))
        var1[2] = config.get("DB1", "layout")
        var2[0] = int(config.get("DB2", "address"))
        var2[1] = int(config.get("DB2", "size"))
        var2[2] = config.get("DB2", "layout")
        return var1, var2
    except:
        return -1

def updater():
    data= { "db":db2[0],
            "size":db2[1],
            "layout":db2[2]
        }
    data = comm.main("recv", **data)[0]
    if data != -1:
        text1['text'] = data["id1"]
    root.after(1000, updater)

def submit():
    data= { "db":db2[0],
            "size":db2[1],
            "layout":db2[2],
            "id":"id1",
            "val":int(entry1.get())
        }
    comm.main("send", **data)


# Define sub window
text1 = Label(root, text="Not connected")
entry1 = Entry(root, text="")
btn1 = Button(root, text="send", command=submit)

# Place root objects in order
text1.pack(side=TOP)
entry1.pack(side=TOP)
btn1.pack(side=BOTTOM)

# Read configuration
db1 = config()[0]
db2 = config()[1]
if db1 == -1 or db2 == -1:
    sys.exit()
else:
    updater()
    mainloop() # Running mainloop always last