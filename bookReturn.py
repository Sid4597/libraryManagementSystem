# -*- coding: utf-8 -*-
"""
******************************************
Title       : Library Management System
Description : Book Return Functions
Date        : 21-10-2021
Author      : Siddharth Shaligram
Version     : 0.0
******************************************
Change Log:
******************************************
"""
from database import Database
import datetime as dt


class Return:

    def bkCheck(self, bookId=""):
        if bookId != "":
            db = Database()
            conn = db.connect()
            Query_bk = f'SELECT ID,Member_Id,Title,Loan_Period from Book_Info where ID = {bookId}'
            result1 = db.Read(Query_bk, conn)
            memberId = result1[0][1]
            if memberId == '0':
                return 1
            else:
                cDate = dt.date.today()
                # cDate = cDate.strftime('%Y-%m-%d')
                conn1 = db.connect()
                Query_Mem = f'SELECT max(TransactionID),Book_ID,Return_Date from Loan_History where Return_Status <> "X" and Book_ID in (Select ID from Book_Info where Member_Id = "{memberId}")'
                result2 = db.Read(Query_Mem, conn1)
                rDate = result2[0][2]
                # rDate = datetime.strptime(rDate)
                rDate = dt.datetime.strptime(rDate, '%Y-%m-%d')
                rDate = rDate.date()
                if rDate >= cDate:
                    return result1
                else:
                    return 0

    def bkReturn(self, lstBookReturn):  # [[1, 'ssha', 'Harry Potter', 28]]
        lstBookId = []
        if lstBookReturn != "":
            for r in lstBookReturn:
                lstBookId.append(r[0])
            db = Database()
            conn = db.connect()
            status = db.Return(lstBookId, conn)
            return statuss
