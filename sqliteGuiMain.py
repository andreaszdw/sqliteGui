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
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel

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
      
        self.parent.title("sqlite Gui test")
        self.makeMenu()
        self.pack(fill=tk.BOTH, expand=1)

        # two paned window
        pw = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        pw.pack(fill=tk.BOTH, expand=1)

        self.dbTree = ttk.Treeview(pw)
        #tree["columns"]=("one","two")
        #tree.column("one", width=100 )
        #tree.column("two", width=100)
        #tree.heading("one", text="coulmn A")
        #tree.heading("two", text="column B")
        #self.dbTree.insert("" , 0,    text="Line 1")#, values=("1A","1b"))
        #id2 = self.dbTree.insert("", 1, "dir2", text="Dir 2")
        #self.dbTree.insert(id2, "end", "dir 2", text="sub dir 2")#, values=("2A","2B"))
        self.dbTree.insert("", 0, text="No db in use")
        #self.dbTree.pack()

        pw.add(self.dbTree)

        right = tk.Label(pw, text="right")
        pw.add(right)

        '''
        # Frame for table
        frameTable = ttk.Frame(self)
        frameTable.pack(fill=tk.BOTH, expand=1)

        self.table = TableCanvas(frameTable)
        self.table.createTableFrame()

        # statusbar
        self.statusBar = tk.Label(self, text="Datenbank: %s" % self.uiConfig["db"], bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusBar.pack(fill=tk.BOTH)'''

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

                # empty the tree
                for i in self.dbTree.get_children():
                    self.dbTree.delete(i)


                self.db = file
                select = True

                # insert the db name as toplevel in tree
                self.dbTree.insert("", 0, self.db, text=self.db)

                #self.statusBar["text"] = "Datenbank: %s" % os.path.basename(self.db)

                #save in ini
                self.uiConfig["db"] = self.db
                pickle.dump(self.uiConfig, open("ini", "wb"))

                # connect to db
                self.conn = sqlite3.connect(self.db)

                # get cursor
                c = self.conn.cursor()

                # get the table names
                c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
                result = c.fetchall()

                tmpCount = 0
                for r in result:

                    tmpCount += 1
                    # insert every table as child in tree
                    tmpChild = self.dbTree.insert(self.db, tmpCount, text=r)

                    # get the table_info
                    c.execute("PRAGMA table_info(%s)" % r)
                    childs = c.fetchall()

                    tmpCounti = 0
                    for ch in childs:
                        tmpCounti += 1
                        tmpChildi = self.dbTree.insert(tmpChild, tmpCounti, text=ch[1])



                    print r
                    print ""

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
