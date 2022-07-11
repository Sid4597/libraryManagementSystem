# -*- coding: utf-8 -*-
"""
******************************************
Title       : Library Management System
Description : Database Functions
Date        : 18-10-2021
Author      : Siddharth Shaligram
Version     : 0.0
******************************************
Change Log:
******************************************
"""

import sqlite3
from sqlite3 import Error
import datetime as dt


class Database:

    def connect(self):
        conn = None
        try:
            conn = sqlite3.connect('Library.db')
        except Error as e:
            return e
        return conn

    def __createBook_Info(self, conn):
        qry_bookInfo = """ CREATE TABLE if not exists "Book_Info" (
                    	"ID"	INTEGER NOT NULL UNIQUE,
                    	"Genre"	TEXT NOT NULL,
                    	"Title"	TEXT NOT NULL,
                    	"Author"	TEXT NOT NULL,
                    	"Loan_Period"	INTEGER NOT NULL,
                    	"Purchase_Date"	TEXT NOT NULL,
                    	"Member_Id"	TEXT,
                    	PRIMARY KEY("ID"))
                        """
        qry_BookInsert = """INSERT INTO Book_Info(ID,Genre,Title,Author,Loan_Period,Purchase_Date,Member_Id)
                            VALUES(?,?,?,?,?,?,?)"""

        try:
            cur = conn.cursor()
            cur.execute(qry_bookInfo)
        except Error as e:
            return e

        try:
            txtBook_info = open('book_info.txt')
        except Exception as e:
            print('Could not read Book_Info.txt')

        if txtBook_info != "":
            rows = txtBook_info.readlines()
            cur = conn.cursor()
            for r in rows:
                r = r.split(",")
                r[6] = r[6].rstrip()
                cur.execute(qry_BookInsert, r)
            conn.commit()
            txtBook_info.close()
            return cur.lastrowid

    def __createLoan_History(self, conn):
        qry_loanHistory = """CREATE TABLE if not exists "Loan_History" (
                        	"TransactionID"	INTEGER NOT NULL UNIQUE,
                        	"Book_ID"	INTEGER NOT NULL,
                        	"Checkout_Date"	TEXT NOT NULL,
                        	"Return_Date"	TEXT NOT NULL,
                        	PRIMARY KEY("TransactionID"))
                            """
        qry_LoanInsert = """INSERT INTO Loan_History(TransactionID,Book_ID,Checkout_Date,Return_Date)
                            VALUES(?,?,?,?)"""

        try:
            cur = conn.cursor()
            cur.execute(qry_loanHistory)
        except Error as e:
            return e

        try:
            txtLoan_history = open('loan_history.txt')
        except Error as e:
            print('Could not read loan_history.txt')

        # inconsistency between loan, log and book_info where books are issued
        if txtLoan_history != "":
            rows = txtLoan_history.readlines()
            # cur = conn.cursor()
            for r in rows:
                r = r.split(",")
                r[3] = r[3].rstrip()
                cur.execute(qry_LoanInsert, r)
            conn.commit()
            txtLoan_history.close()
            return cur.lastrowid

    def __createLog_Table(self, conn):
        global e
        qry_LogTable = """CREATE TABLE if not exists "Log_Table" (
                                "TransactionID"	INTEGER NOT NULL UNIQUE,
                                "Book_ID"	TEXT NOT NULL,
                                "Checkout_Date"	TEXT,
                                "Return_Date"	TEXT,
                                "Member_Id"	TEXT,
                                "Return_Status"	TEXT,
                                "Genre"	TEXT,
                                PRIMARY KEY("TransactionID")
                            );"""

        qry_LogInsert = "INSERT INTO 'Log_Table' (TransactionID,Book_ID,Checkout_Date,Return_Date,Member_ID,Genre," \
                        "Return_Status) VALUES(?,?,?,?,?,?,?)"

        MemberNames = ["ssha", "shru", "hupy", "mlan", "dkud"]
        qry_Genre = "SELECT ID, Genre,Member_Id from Book_Info "
        memName = 0
        try:
            cur = conn.cursor()
            cur.execute(qry_LogTable)
        except Error as e:
            return e

        try:
            txtLoan_history = open('loan_history.txt')
        except Error as e:
            print('Could not read loan_history.txt')

            # inconsistency between loan, log and book_info where books are issued
        if txtLoan_history != "":
            rows = txtLoan_history.readlines()
            x = len(rows) - 3
            for i,r in enumerate(rows):
                r = r.split(",")
                r[3] = r[3].rstrip()
                if i < x:
                    r.append(MemberNames[memName])
                    memName += 1
                    if memName == len(MemberNames):
                        memName = 0
                else:
                    r.append('ssha')
                try:
                    cur.execute(qry_Genre)
                    lstGenre = cur.fetchall()
                    for g in lstGenre:
                        if str(g[0]) == r[1]:
                            r.append(g[1])
                    if i < x:
                        r.append('X')
                    else:
                        r.append(' ')
                    cur.execute(qry_LogInsert,r)
                except Error as e:
                    return e

            conn.commit()
            txtLoan_history.close()
            return cur.lastrowid
    def initialize(self, conn):
        rowsBook = self.__createBook_Info(conn)
        print(f"{rowsBook} entries created in book_info")
        rowsLoan = self.__createLoan_History(conn)
        print(f"{rowsLoan} entries created in loan_history")
        rowsLog = self.__createLog_Table(conn)
        print(f"{rowsLog} entries created in Log_Table")
        conn.close()

    def reset(self, conn):
        dropBook_Info = "drop TABLE Book_Info"
        dropLoan_History = "drop TABLE Loan_History"
        dropLog_Table = "drop TABLE Log_Table"
        try:
            cur = conn.cursor()
            cur.execute(dropBook_Info)
            cur.execute(dropLoan_History)
            cur.execute(dropLog_Table)
            conn.commit()
            cur.close()
            return 'DataBase Cleared'
        except Error as e:
            return e

    def Read(self, query, conn):
        if query != "":
            try:
                cur = conn.cursor()
                cur.execute(query)
                result = cur.fetchall()
            except Error as e:
                return e
            cur.close()
            conn.close()
            return result
        else:
            return 'Query is empty'

    def Checkout(self, lstCheckoutBooks, conn):
        if lstCheckoutBooks != "":
            try:
                cur = conn.cursor()
                for r in lstCheckoutBooks:
                    qry_updateBook_Checkout = f"UPDATE Book_Info SET Member_Id = '{r[3]}' where ID = {r[0]}"
                    cur.execute(qry_updateBook_Checkout)
                    try:
                        # rDate = dt.datetime.strptime(r,'%Y-%m-%d')
                        cDate = dt.date.today()
                        # cDate = cDate.date()
                        rDate = cDate + dt.timedelta(r[2])
                        cDate = cDate.strftime('%Y-%m-%d')
                        rDate = rDate.strftime('%Y-%m-%d')
                        qry_InsertLoan_Checkout = f"Insert into Loan_History (Book_ID, Checkout_Date, Return_Date) values ('{r[0]}','{cDate}','{rDate}')"

                        cur.execute(qry_InsertLoan_Checkout)
                        qry_LogInsert_Checkout = f"INSERT INTO 'Log_Table' (BookID,Checkout_Date,Return_Date,MemberID,Genre)" \
                                                 f"VALUES('{r[0]}','{cDate}','{rDate}','{r[3]}',)"
                        conn.commit()
                    except Error as e:
                        return e
            except Error as e:
                return e
            conn.commit()
            cur.close()
            conn.close()
            return True

    def Return(self, lstReturnBooks, conn):
        if lstReturnBooks != "":
            try:
                cur = conn.cursor()
                for r in lstReturnBooks:
                    qry_returnBook = f"UPDATE Book_Info Set Member_Id = '0' where ID = {r}"
                    cur.execute(qry_returnBook)

            except Error as e:
                return e

            try:

                rDate = dt.date.today()
                rDate = rDate.strftime('%Y-%m-%d')
                for r in lstReturnBooks:
                    qry_returnBook = f"UPDATE Loan_History Set Return_Date = '{rDate}',Return_Status = 'X' where Book_ID = {r} and Return_Status <> 'X'"
                    # print(qry_returnBook,'\n')
                    cur.execute(qry_returnBook)
            except Error as e:
                return e
            conn.commit()
            cur.close()
            conn.close()
            return True


###############################
####------MAIN----------#######
###############################
def main():
    db = Database()
    options = "Choose a option :\n1) Test Initialization\n2)Test Read Function\n3)Test Book Checkout\n4)Test Book " \
              "Return "
    print(options)
    testcase = input("Enter the number of your choice : ")
    conn = db.connect()
    if testcase == '1':
        reset = db.reset(conn)
        print(reset)
        init = db.initialize(conn)
        print(init)
    elif testcase == '2':
        qry = "Select * from Book_Info"
        result = db.Read(qry, conn)
        for r in result:
            print(r)
    # elif testcase == 3:


if __name__ == '__main__':
    main()
