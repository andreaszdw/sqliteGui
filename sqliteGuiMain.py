#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
sqliteGuiMain.py

Frontend for sqlite

author  : Andreas Grätz
created : 27.02.2017
main    : andreaszdw@googlemail.com
"""


import Tkinter as tk
import sqlite3
import tkFileDialog 

#-----------------------------------------------------------------------------#
class MainWindow(tk.Frame):
    
    #-----------------------------------------------------#
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        self.db = ""
        
    #-----------------------------------------------------#
    def initUI(self):
      
        self.parent.title("File dialog")
        self.pack(fill=tk.BOTH, expand=1)
        
        self.makeMenu()

        '''menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = tk.Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        menubar.add_cascade(label="File", menu=fileMenu)        '''
        
        self.txt = tk.Text(self)
        self.txt.pack(fill=tk.BOTH, expand=1)

    #-----------------------------------------------------#
    def makeMenu(self):

        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = tk.Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        menubar.add_cascade(label="File", menu=fileMenu)  
            
    #-----------------------------------------------------#
    def selectDB(self, filename):

        f = open(filename, "r")
        text = f.read()
        return text

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    
    root = tk.Tk()
    ex = MainWindow(root)
    root.geometry("800x400+300+300")
    root.mainloop()  
