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
import dbTreeView as dtv
import tableView as tv

import os.path
import pickle

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

        if self.db != "":

            self.dbTree.makeTreeView(self.db)

        
    #-----------------------------------------------------#
    def initUI(self):
      
        self.parent.title("sqlite Gui test")
        self.makeMenu()
        self.pack(fill=tk.BOTH, expand=1)

        # two paned window
        self.pw = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        self.pw.pack(fill=tk.BOTH, expand=1)

        # left side of panel
        self.dbTree = dtv.dbTreeView(self.pw)

        self.dbTree.bind("<Button-1>", self.treeClick)

        self.pw.add(self.dbTree)

        # right side, to be set
        self.table = tv.tableView(self.pw, "", tableName="Leer")
        self.pw.add(self.table)


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

                #save in ini
                self.uiConfig["db"] = self.db
                pickle.dump(self.uiConfig, open("ini", "wb"))

            self.dbTree.makeTreeView()

    #-----------------------------------------------------#
    def treeClick(self, event):

        item, parentItem = self.dbTree.onClick(event)

        if parentItem == "":

            print "db = %s" % item

        elif parentItem == self.db:

            tmp = self.pw.panes()

            if(len(tmp) > 1):

                self.pw.remove(tmp[1])
                self.table = None
                self.table = tv.tableView(self.pw, db=self.db, tableName=item)
                self.pw.add(self.table)

            print len(tmp)

        else:

            print "column %s of table %s" % (item, parentItem)




    #-----------------------------------------------------#
    def exit(self):

        self.quit()


#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    
    root = tk.Tk()
    root.geometry("800x400+300+300")
    app = MainWindow(root)
    root.mainloop()  
