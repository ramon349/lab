import sys
#account for difference between python 2 and python 7 
if sys.version_info.major < 3.0: 
    import Tkinter as tk
    from Tkinter import filedialog as fd 
else: 
    import tkinter as tk 
    from tkinter import filedialog as fd 
from extractInfo import main

def analyzeData():
    """ callback fcn: ask user for file, call parse funciton , save output  """
    filename = fd.askopenfilename()
    newFile = fd.asksaveasfilename(defaultextension='.csv')
    main(filename,newFile)
    print("DONE") 
root = tk.Tk()
root.title("Ramon's app") 
tk.Button(root,text="Select File",command=analyzeData ).pack() 
tk.mainloop()
