# -*- coding: utf-8 -*-
"""
******************************************
Title       : Library Management System
Description : Book Checkout Functions
Date        : 20-10-2021
Author      : Siddharth Shaligram
Version     : 0.0
******************************************
Change Log:
******************************************
"""
from database import Database
import datetime as dt

class BookCheckout:

    def checkBook(self,bookId = ""):
        db = Database()
        conn = db.connect()
        Query = f"SELECT ID, Title, Loan_Period,Member_Id,Genre from Book_Info where ID = {bookId}"
        result = db.Read(Query,conn)
        return result


    def checkMember(self,memberId = ""):
        db = Database()
        conn = db.connect()
        cDate = dt.date.today()
        rDate = cDate.strftime('%Y-%m-%d')
        Query = f"SELECT TransactionID,Book_ID,Checkout_Date,Return_Date from Loan_History join Book_Info on Book_ID = ID  where Member_Id ='{memberId}' and Return_Date > '{rDate}'"
        result = db.Read(Query,conn)
        if not result:
            return False
        else:
            return result

    def checkout(self, lstCheckoutBooks):
        db = Database()
        conn = db.connect()
        print(lstCheckoutBooks)
        status = db.Checkout(lstCheckoutBooks, conn)
        return status
