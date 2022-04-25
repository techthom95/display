#!/usr/bin/env python3
from tkinter import *
from tkinter import font
from tkinter import messagebox
from configparser import *
import sys, comm

root=Tk() # Create main window
root.title('Test UI') # Window title
root.configure(bg='white') # Window background
root.minsize(400, 200) # Window size minimum
#root.state('zoomed') # Normal fullscreen
#root.attributes("-fullscreen", True) # Canvas fullscreen

def updater():  
    text1['text'] = comm.main(1, 20)[1][0]["id1"]
    root.after(1000, updater)

# Define sub window
text1 = Label(root, text="Not connected")

# Place root objects in order
text1.pack(side=TOP)

updater()
mainloop() # Running mainloop always last