#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
dbTreeView.py

tkinter tableView for sqlite

author  : Andreas Grätz
created : 07.03.2017
main    : andreaszdw@googlemail.com
"""

import Tkinter as tk
import ttk
import sqlite3
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel


#---------------------------------------------------------#
class tableView(ttk.Frame):


	#-----------------------------------------------------#
	def __init__(self, parent, db, tableName="Leer"):

		ttk.Frame.__init__(self, parent)

		self.model = TableModel()
		self.table = TableCanvas(self, model=self.model)
		self.pack(fill=tk.BOTH, expand=1)
		self.table.createTableFrame()

		
		if tableName == "Leer": 

			return

		conn = sqlite3.connect(db)		

		c = conn.cursor()

		c.execute("PRAGMA table_info(%s)" % tableName)
		
		# now create the model
		data = {}
			
		result = c.fetchall()

		colnames = []

		for r in result:

			colnames.append(r[1])

		c.execute("SELECT * from %s" % tableName)

		rows = c.fetchall()

		n = 0

		for n in range(len(rows)):
			data[n] = {}
			data[n]["label"] = n
			count = 0
			for r in rows[n]:

				data[n][colnames[count]] = r
				count +=1
		
		self.model.importDict(data)
		self.table.redrawTable()


				