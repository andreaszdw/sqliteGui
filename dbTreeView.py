#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
dbTreeView.py

tkinter treeview for sqlite

author  : Andreas Grätz
created : 07.03.2017
main    : andreaszdw@googlemail.com
"""

import Tkinter as tk
import ttk
import sqlite3


#---------------------------------------------------------#
class dbTreeView(ttk.Treeview):

    
    #-----------------------------------------------------#
    def __init__(self, parent):

        ttk.Treeview.__init__(self, parent)

        self.heading("#0", text="DB in use:")
        self.insert("", 0, text="None")

    
    #-----------------------------------------------------#
    def makeTreeView(self, db):

        # empty the tree
        for i in self.get_children():
            self.delete(i)

        # insert the db name as toplevel in tree
        self.insert("", 0, db, text=db)

        # connect to db
        conn = sqlite3.connect(db)

        # get cursor
        c = conn.cursor()

        # get the table names
        c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        result = c.fetchall()

        tmpCount = 0
        for r in result:

            tmpCount += 1
            # insert every table as child in tree
            tmpChild = self.insert(db, tmpCount, text=r)

            # get the table_info
            c.execute("PRAGMA table_info(%s)" % r)
            childs = c.fetchall()

            tmpCounti = 0
            for ch in childs:
                tmpCounti += 1
                self.insert(tmpChild, tmpCounti, text=ch[1])


    #-----------------------------------------------------#
    def onClick(self, event):

        item = self.identify('item', event.x, event.y)
        return self.item(item, "text"), self.item(self.parent(item), "text")
