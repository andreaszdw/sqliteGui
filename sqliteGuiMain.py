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
import ttk
import tkFileDialog

import os.path
import pickle
import sqlite3

#-----------------------------------------------------------------------------#
class MainWindow(ttk.Frame):
    
    #-----------------------------------------------------#
    def __init__(self, parent):

        ttk.Frame.__init__(self, parent)

        # look for ini-file, and use its values, else make new ini-file
        if os.path.exists("ini"):

            # ini informations laden
            self.uiConfig = pickle.load(open("ini", "rb"))

        else:
            
            # dict for ini informations
            self.uiConfig = {"width": 800,
                        "height": 400,
                        "x": 300,
                        "y": 300,
                        "db": ""}

        self.uiConfig["db"] = os.path.basename(self.uiConfig["db"])
        self.parent = parent

        self.parent.geometry("%sx%s" % (self.uiConfig["width"], self.uiConfig["height"]))
        self.initUI()
        self.db = self.uiConfig["db"]

        # binding for changing size, save info in ini
        self.bind("<Configure>", self.configure)

        #for the connection
        self.conn = ""
        
    #-----------------------------------------------------#
    def initUI(self):
      
        self.parent.title("sqlite Gui")
        self.makeMenu()
        self.pack(fill=tk.BOTH, expand=1)
        
        
        self.txt = tk.Text(self)
        self.txt.pack(fill=tk.BOTH, expand=1)

        # statusbar
        self.statusBar = tk.Label(self, text="Datenbank: %s" % self.uiConfig["db"], bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusBar.pack(fill=tk.BOTH, expand=1)

    #-----------------------------------------------------#
    def makeMenu(self):

        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = tk.Menu(menubar)
        fileMenu.add_command(label="Select DB", command=self.selectDB)
        fileMenu.add_command(label="Exit", command=self.exit)

        menubar.add_cascade(label="File", menu=fileMenu)

    #-----------------------------------------------------#
    def configure(self, event):

        self.uiConfig["width"] = event.width
        self.uiConfig["height"] = event.height

        # save info in ini-file
        pickle.dump(self.uiConfig, open("ini", "wb"))
            
    #-----------------------------------------------------#
    def selectDB(self):

        select = False

        while not select:

            file = os.path.basename(tkFileDialog.askopenfilename(title="Datenbank auswählen"))

            if file != "":

                self.db = file
                select = True

                self.statusBar["text"] = "Datenbank: %s" % os.path.basename(self.db)

                self.uiConfig["db"] = self.db

                pickle.dump(self.uiConfig, open("ini", "wb"))

        self.conn = sqlite3.connect(self.db)

        c = self.conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")

        result = c.fetchall()

        for r in result:

            c.execute("PRAGMA table_info(%s)" % r)

            print c.fetchall()

    #-----------------------------------------------------#
    def exit(self):

        self.quit()

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    
    root = tk.Tk()
    root.geometry("800x400+300+300")
    app = MainWindow(root)
    root.mainloop()  
