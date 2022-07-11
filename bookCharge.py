# -*- coding: utf-8 -*-
"""
******************************************
Title       : Library Management System
Description : Book Charge Functions
Date        : 19-10-2021
Author      : Siddharth Shaligram
Version     : 0.0
******************************************
Change Log:
******************************************
"""
from database import Database
import datetime as dt


class BookCharge:
    def charges(self, bookId="", memberId=""):
        chrgData = []
        db = Database()
        conn = db.connect()
        cDate = dt.date.today()
        rDate = cDate.strftime('%Y-%m-%d')

        Query = f"SELECT Log_Table.Member_Id, Book_ID, Title, Checkout_Date, Return_Date, max(TransactionID) from Loan_History join Book_Info on ID = " \
                f"Book_ID WHERE Return_Date < '{rDate}' and Return_Status <> 'X'"

        Query = f"SELECT Member_Id, Book_ID, Title, Checkout_Date, Return_Date, max(TransactionID) from Log_Table " \
                f"WHERE Return_Date < '{rDate}' and Return_Status <> 'X'"
        if bookId != "":
            Query = Query + " and Book_ID = '" + str(bookId) + "'"
        if memberId != "":
            Query = Query + " and Member_Id = '" + str(memberId) + "'"
        else:
            Query = Query + " and Member_Id <> 0 group by Book_ID ORDER by TRANSACTIONID "


        result = db.Read(Query, conn)
        print(result)
        for r in result:
            rDate = dt.datetime.strptime(r[4], '%Y-%m-%d')
            rDate = rDate.date()
            day = cDate - rDate
            day = day.days
            chrg = int(day) * 0.25
            lst = list(r)
            lst.append(chrg)
            chrgData.append(lst)
        return chrgData


def main():
    bkChrg = BookCharge()
    res = bkChrg.search()


if __name__ == '__main__':
    main()
