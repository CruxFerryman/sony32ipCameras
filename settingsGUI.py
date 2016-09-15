#!/usr/bin/env python
import Tkinter as tkinter
import ttk
from GUIfiles.SWAlignTab import createSWAtab
from GUIfiles.TKZAlignTab import createTKZtab
from time import strftime



GUIglobals={'default_save_dir':'D:\Duke\Sony\cameraData'}

top = tkinter.Tk()
top.wm_title('Camera Control')
top.geometry("1000x1000")

notebook = ttk.Notebook(top)
SW = createSWAtab(notebook,GUIglobals)
PTZ = createTKZtab(notebook,GUIglobals)
notebook.add(SW, text='Imaging Controls')
notebook.add(PTZ, text='PTZ Setup')
notebook.pack()



top.mainloop()
