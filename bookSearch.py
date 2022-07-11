# -*- coding: utf-8 -*-
"""
******************************************
Title       : Library Management System
Description : Book Search Functions
Date        : 20-10-2021
Author      : Siddharth Shaligram
Version     : 0.0
******************************************
Change Log:
******************************************
"""
from database import Database
import datetime as dt

class BookSearch:
    def searchBook(self,bookId=""):
        db = Database()
        conn = db.connect()
        Query = "SELECT * from Book_Info where Member_Id = '0'"
        if bookId != "":
            Query = Query + " and ID = " + bookId
        result = db.Read(Query,conn)
        lstbkSearch = list(result)
        return list(lstbkSearch)
