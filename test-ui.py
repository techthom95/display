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
f1=font.Font(weight="bold", size=14) # Font 1
f2=font.Font(weight="bold", size=8) # Font 2

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

def conn_check():
    if comm.main("check") != -1:
        connection['text'] = "Connected"
        connection.config(bg="green")
    else:
        connection['text'] = "Not connected"
        connection.config(bg="red")
    if time == "0" and connection['text'] == "Connected":
        connection['text'] = "Connected (Simulation Check = 0)"
        connection.config(bg="orange")
    if time != "0":
        root.after(time, conn_check)

def recv():
    if int(textbox1.get()) > 0 and textbox2.get() != "":
        var= { "db":db[int(textbox1.get())-1][0],
                "size":db[int(textbox1.get())-1][1],
                "layout":db[int(textbox1.get())-1][2],
                "id":textbox2.get(),
                "val":0
            }
        data = comm.main("recv", **var)
        if data != -1:
            textbox3.delete(0, END)
            textbox3.insert(0, data[0][var.get('id')])
        else:
            logger.debug("field is empty")

def send():
    if textbox4.get() != "":
        var= { "db":db[int(textbox1.get())-1][0],
                "size":db[int(textbox1.get())-1][1],
                "layout":db[int(textbox1.get())-1][2],
                "id":textbox2.get(),
                "val":int(textbox4.get())
            }
        comm.main("send", **var)
    else:
        logger.debug("field is empty")

# Define root objects
connection = Label(root, text="Not connected", bg="red")

# Define "main frame" objects
framekl1 = Frame(root, bg="white")
framekl2 = Frame(root, bg="white")

# Define "frame Kolum 1" objects
framekl1row1 = Frame(framekl1, bg="white")
framekl1row2 = Frame(framekl1, bg="white")
framekl1row3 = Frame(framekl1, bg="white")
label1 = Label(framekl1row1, text="DB Nummer", bg="white", width=12, font=f2)
label2 = Label(framekl1row2, text="Tag Name", bg="white", width=12, font=f2)
textbox1 = Entry(framekl1row1, relief="solid", justify="center", font=f2)
textbox1.insert(0, "2")
textbox2 = Entry(framekl1row2, relief="solid", justify="center", font=f2)
textbox2.insert(0, "id1")
btn1 = Button(framekl1row3, text="Receive", bg="#58F", font=f1, command= lambda: recv())

# Define "frame Kolum 2" objects
framekl2row1 = Frame(framekl2, bg="white")
framekl2row2 = Frame(framekl2, bg="white")
framekl2row3 = Frame(framekl2, bg="white")
label3 = Label(framekl2row1, text="Value Received", bg="white", width=12, font=f2)
label4 = Label(framekl2row2, text="Value To Send", bg="white", width=12, font=f2)
textbox3 = Entry(framekl2row1, relief="solid", font=f2)
textbox4 = Entry(framekl2row2, relief="solid", font=f2)
btn2 = Button(framekl2row3, text="Send", bg="#58F", font=f1, command= lambda: send())

# Place root objects in order
connection.pack(side=TOP,fill="both")

# Place "main frame" objects in order
framekl1.pack(side=LEFT, fill="both", expand="yes", pady=5, padx=10)
framekl2.pack(side=RIGHT, fill="both", expand="yes", pady=5, padx=10)

# Place "frame Kolum 1" objects in order
framekl1row1.pack(side=TOP, fill="both", expand="yes", pady=5, padx=20)
framekl1row2.pack(side=TOP, fill="both", expand="yes", pady=5, padx=20)
framekl1row3.pack(side=TOP, fill="both", expand="yes", pady=5, padx=20)
label1.pack(side=LEFT)
textbox1.pack(side=RIGHT, fill="x", expand="yes", ipady=4, padx=20)
label2.pack(side=LEFT)
textbox2.pack(side=RIGHT, fill="x", expand="yes", ipady=4, padx=20)
btn1.pack(side=BOTTOM, fill="both", expand="yes")

# Place "frame Kolum 2" objects in order
framekl2row1.pack(side=TOP, fill="both", expand="yes", pady=5, padx=20)
framekl2row2.pack(side=TOP, fill="both", expand="yes", pady=5, padx=20)
framekl2row3.pack(side=TOP, fill="both", expand="yes", pady=5, padx=20)
label3.pack(side=LEFT)
textbox3.pack(side=RIGHT, fill="x", expand="yes", ipady=4, padx=20)
label4.pack(side=LEFT)
textbox4.pack(side=RIGHT, fill="x", expand="yes", ipady=4, padx=20)
btn2.pack(side=BOTTOM, fill="both", expand="yes")

# Read configuration
logger.debug("reading general configuration")
time = config()[0]
db = config()[1]
if db == -1:
    logger.error("configuration error")
    messagebox.showerror("ERROR", "Configuration ERROR")
else:

    # Setting up variables

    conn_check()
    mainloop() # Running mainloop always last