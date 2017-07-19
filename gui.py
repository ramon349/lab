import sys
from tkinter import filedialog as fd  
from extractInfo import main

def analyzeData():
	filename = fd.askopenfilename()
	newFile = fd.asksaveasfilename()
	print( main(filename,newFile) )
if sys.version_info.major < 3.0: 
    import Tkinter as tk
else: 
    import tkinter as tk 

root = tk.Tk()
root.title("Ramon's app") 
tk.Button(root,text="Select File",command=analyzeData ).pack() 
tk.mainloop()
