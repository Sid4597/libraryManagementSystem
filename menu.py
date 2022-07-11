# -*- coding: utf-8 -*-
"""
******************************************
Title       : Library Management System
Description : GUI Functions
Date        : 17-10-2021
Author      : Siddharth Shaligram
Version     : 0.0
******************************************
Change Log:
******************************************
"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from bookCharge import BookCharge
from database import Database
from bookSearch import BookSearch
from bookCheckout import BookCheckout
from bookReturn import Return


def Initialize():
    choice = messagebox.askquestion("askquestion", "Are you sure?")
    if choice == 'yes':
        db = Database()
        conn = db.connect()
        db.initialize(conn)
        messagebox.showinfo(title='Initialize', message='Initialize Successful!')
def Reset():
    choice = messagebox.askquestion("askquestion", "This will empty your Database and reset the application\nAre you sure?")
    if choice == 'yes':
        db = Database()
        conn = db.connect()
        status = db.reset()
        messagebox.showinfo(title='Checkout', message=status)
def checkMemberID(memberID):
    if len(memberID) < 5:
        return True
    else:
        messagebox.showerror(title="Error", message="MemberID should not be more then 4 characters")

def bkCharge(entBookId_Home, entMemberId_Home, tblCharge):
    bkChrg = BookCharge()
    str_BookId = entBookId_Home.get()
    str_MemberId = entMemberId_Home.get()
    if checkMemberID(str_MemberId):
        result = bkChrg.charges(str_BookId, str_MemberId)
        iid = 0
        # delete any preexisting entries
        for i in tblCharge.get_children():
            tblCharge.delete(i)

        if not result:
            messagebox.showerror(title="Error", message="No Result Found!")
        else:
            # adding data to the treeview
            for r in result:
                tblCharge.insert(parent='', index='end', iid=iid, text="Parent",
                                 values=(r[0], r[1], r[2], r[3], r[4], r[5]))
                iid += 1



def bkSearch(entBookId_Search, tblSearch):
    bkSrch = BookSearch()
    str_BookId = entBookId_Search.get()
    result = bkSrch.searchBook(str_BookId)
    iid = 0
    # delete any preexisting entries
    for i in tblSearch.get_children():
        tblSearch.delete(i)

    if not result:
        messagebox.showerror(title="Error", message="No Result Found!")
    else:
        # adding data to the treeview
        for r in result:
            tblSearch.insert(parent='', index='end', iid=iid, text="Parent",
                             values=(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
            iid += 1


def bkAdd(entMemberId_Checkout, entBookId_Checkout, tblCheckout):
    bkCkout = BookCheckout()
    str_MemberId = entMemberId_Checkout.get()
    str_BookId = entBookId_Checkout.get()
    if checkMemberID(str_MemberId):
        resultMember = bkCkout.checkMember(str_MemberId)
        if not resultMember:
            resultBook = bkCkout.checkBook(str_BookId)
            if resultBook[0][3] == '0':
                for r in resultBook:
                    tblCheckout.insert(parent='', index='end', text="Parent", values=(r[0], r[1], r[2], str_MemberId))
            else:
                messagebox.showerror(title="Error", message="Book not avaiable!\nalready assigned")
        else:
            messagebox.showerror(title="Error", message="Member has previously due books!")


def bkCheckout(tblCheckout):
    bkCkout = BookCheckout()
    cnt = 0
    x = []
    lstCheckoutBooks = []
    for i in tblCheckout.get_children():
        for j in tblCheckout.item(i)['values']:
            x.append(j)
        lstCheckoutBooks.append(x)
        x = list()
    status = bkCkout.checkout(lstCheckoutBooks)
    if status:
        for i in tblCheckout.get_children():
            tblCheckout.delete(i)
        messagebox.showinfo(title='Checkout', message='Checkout Successful!')
    else:
        messagebox.showerror(title="Error", message="Error during Checkout!\nPlease Retry")


def checkReturn(entBookId_Return, tblReturn):
    bkRtn = Return()
    # str_MemberId = lblMemberId_Return.get()
    str_BookId = entBookId_Return.get()
    result = bkRtn.bkCheck(str_BookId)

    if result == 0:
        messagebox.showerror(title="Error", message="Member has Overdue books")
    elif result == 1:
        messagebox.showerror(title="Error", message="Book issued to anyone")
    else:
        for r in result:
            tblReturn.insert(parent='', index='end', text="Parent", values=(r[0], r[1], r[2], r[3]))


def bkReturn(tblReturn):
    bkRtn = Return()
    x = []
    lstBookReturn = []
    for i in tblReturn.get_children():
        for j in tblReturn.item(i)['values']:
            x.append(j)
        lstBookReturn.append(x)
        x = list()
    result = bkRtn.bkReturn(lstBookReturn)
    if result:
        messagebox.showinfo(title='Return', message='Return Successful!')
    else:
        messagebox.showerror(title="Error", message=result)


class MainGUI:

    def __init__(self, window):
        self.__mainWin = window
        self.__mainWin.title("Library Management System")
        self.__mainWin.geometry('1280x720')
        self.__mainWin.iconbitmap('appIcon.ico')
        self.__Menubar()
        self.__Tabs()

    def __Menubar(self):  # Menu Bar
        menubar = Menu(self.__mainWin)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Initialize", command=lambda: Initialize())
        filemenu.add_command(label="Reset", command=lambda: Reset())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=tk.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.__mainWin.config(menu=menubar)

    def __TabHome(self, frame):  # Home Tab

        frmInput_Home = Frame(frame)
        frmTable_Home = Frame(frame)

        frmInput_Home.grid(column=0, row=0)
        frmTable_Home.grid(column=0, row=2)
        # Book ID input
        lblBookId_Home = Label(frmInput_Home, text="Book ID :")
        lblBookId_Home.grid(column=0, row=0, pady=10, padx=5)
        entBookId_Home = Entry(frmInput_Home)
        entBookId_Home.grid(column=1, row=0, pady=10, padx=5)

        # Member ID input
        lblMemberId_Home = Label(frmInput_Home, text="Member ID :")
        lblMemberId_Home.grid(column=2, row=0, pady=10, padx=5)
        entMemberId_Home = Entry(frmInput_Home)
        entMemberId_Home.grid(column=3, row=0, pady=10, padx=5)

        btnCheck_Home = Button(frmInput_Home, text="Check",
                               command=lambda: bkCharge(entBookId_Home, entMemberId_Home, tblCharge))
        btnCheck_Home.grid(column=4, row=0, pady=10, padx=5)

        # Display tabLe
        cols = ('#1', '#2', '#3', '#4', '#5', '#6')

        tblCharge = ttk.Treeview(frmTable_Home, columns=cols, show='headings')
        # define headings
        tblCharge.heading('#0')
        tblCharge.heading('#1', text='Member ID')
        tblCharge.heading('#2', text='Book ID')
        tblCharge.heading('#3', text='Book Title')
        tblCharge.heading('#4', text='Checkout Date')
        tblCharge.heading('#5', text='Return Date')
        tblCharge.heading('#6', text='Charges')

        tblCharge.grid(column=0, row=0)

    def __TabSearch(self, frame):  # Search tabLe
        frmInput_Search = Frame(frame)
        frmTable_Search = Frame(frame)

        frmInput_Search.grid(column=0, row=0)
        frmTable_Search.grid(column=0, row=2)

        # Book ID input
        lblBookId_Search = Label(frmInput_Search, text="Book ID :")
        lblBookId_Search.grid(column=0, row=0, pady=10, padx=5)
        entBookId_Search = Entry(frmInput_Search)
        entBookId_Search.grid(column=1, row=0, pady=10, padx=5)

        btnSearch_Search = Button(frmInput_Search, text="Search", command=lambda: bkSearch(entBookId_Search, tblSearch))
        btnSearch_Search.grid(column=2, row=0, pady=10, padx=5)

        # Display tabLe
        cols = ('#1', '#2', '#3', '#4', '#5', '#6', '#7')
        tblSearch = ttk.Treeview(frmTable_Search, columns=cols, show='headings')
        # define headings
        tblSearch.heading('#0')
        tblSearch.heading('#1', text='Book ID')
        tblSearch.heading('#2', text='Genre')
        tblSearch.heading('#3', text='Title')
        tblSearch.heading('#4', text='Author')
        tblSearch.heading('#5', text='Loan Period')
        tblSearch.heading('#6', text='Purchase Date')
        tblSearch.heading('#7', text='Member ID')

        tblSearch.grid(column=0, row=0)

    def __TabCheckout(self, frame):  # Checkout Form
        frmInput_Checkout = Frame(frame)
        frmTable_Checkout = Frame(frame)

        frmInput_Checkout.grid(column=0, row=0)
        frmTable_Checkout.grid(column=0, row=2)

        # Member ID input
        lblMemberId_Checkout = Label(frmInput_Checkout, text="Member ID :")
        lblMemberId_Checkout.grid(column=0, row=0, pady=10, padx=5)
        entMemberId_Checkout = Entry(frmInput_Checkout)
        entMemberId_Checkout.grid(column=1, row=0, pady=10, padx=5)

        # Book ID input
        lblBookId_Checkout = Label(frmInput_Checkout, text="Book ID :")
        lblBookId_Checkout.grid(column=2, row=0, pady=10, padx=5)
        entBookId_Checkout = Entry(frmInput_Checkout)
        entBookId_Checkout.grid(column=3, row=0, pady=10, padx=5)

        btnAdd_Checkout = Button(frmInput_Checkout, text="ADD",
                                 command=lambda: bkAdd(entMemberId_Checkout, entBookId_Checkout, tblCheckout))
        btnAdd_Checkout.grid(column=4, row=0, pady=10, padx=5)

        # Display tabLe
        cols = ('#1', '#2', '#3', '#4')
        tblCheckout = ttk.Treeview(frmTable_Checkout, columns=cols, show='headings')
        # define headings
        tblCheckout.heading('#0')
        tblCheckout.heading('#1', text='Book ID')
        tblCheckout.heading('#2', text='Title')
        tblCheckout.heading('#3', text='Loan Period')
        tblCheckout.heading('#4', text='Member ID')

        # adding data to the treeview
        tblCheckout.grid(column=0, row=0)

        btnCheckout_Checkout = Button(frmInput_Checkout, text="Checkout", command=lambda: bkCheckout(tblCheckout))
        btnCheckout_Checkout.grid(column=5, row=0, pady=10, padx=10)

    def __TabReturn(self, frame):
        frmInput_Return = Frame(frame)
        frmTable_Return = Frame(frame)

        frmInput_Return.grid(column=0, row=0)
        frmTable_Return.grid(column=0, row=2)

        # Book ID input
        lblBookId_Return = Label(frmInput_Return, text="Book ID :")
        lblBookId_Return.grid(column=0, row=0, pady=10, padx=5)
        entBookId_Return = Entry(frmInput_Return)
        entBookId_Return.grid(column=1, row=0, pady=10, padx=5)

        # # Member ID input
        # lblMemberId_Return = Label(frmInput_Return, text="Member ID :")
        # lblMemberId_Return.grid(column=2, row=0, pady=10, padx=5)
        # entMemberId_Return = Entry(frmInput_Return)
        # entMemberId_Return.grid(column=3, row=0, pady=10, padx=5)

        btnAdd_Return = Button(frmInput_Return, text="ADD",
                               command=lambda: checkReturn(entBookId_Return, tblReturn))
        btnAdd_Return.grid(column=4, row=0, pady=10, padx=10)

        btnReturn_Return = Button(frmInput_Return, text="Return", command=lambda: bkReturn(tblReturn))
        btnReturn_Return.grid(column=6, row=0, pady=10, padx=5)

        # Display tabLe
        cols = ('#1', '#2', '#3', '#4')
        tblReturn = ttk.Treeview(frmTable_Return, columns=cols, show='headings')
        # define headings
        tblReturn.heading('#0')
        tblReturn.heading('#1', text='Book ID')
        tblReturn.heading('#2', text='Title')
        tblReturn.heading('#3', text='Loan Period')
        tblReturn.heading('#4', text='Member ID')

        tblReturn.grid(column=0, row=0)

    def __Tabs(self):  # tabControl and Frames
        tabControl = ttk.Notebook(self.__mainWin)
        tabControl.grid(column=0, row=0, pady=10)
        tabHome = ttk.Frame(tabControl)
        tabSearch = ttk.Frame(tabControl)
        tabCheckout = ttk.Frame(tabControl)
        tabReturn = ttk.Frame(tabControl)
        tabControl.add(tabHome, text='Home')
        tabControl.add(tabSearch, text='Search')
        tabControl.add(tabCheckout, text='Checkout')
        tabControl.add(tabReturn, text='Return')
        frmHome = ttk.Frame(tabHome)
        frmHome.grid(column=0, row=0, rowspan=10)
        frmSearch = ttk.Frame(tabSearch)
        frmSearch.grid(column=0, row=0, rowspan=10)
        frmCheckout = ttk.Frame(tabCheckout)
        frmCheckout.grid(column=0, row=0, rowspan=10)
        frmReturn = ttk.Frame(tabReturn)
        frmReturn.grid(column=0, row=0, rowspan=10)

        self.__TabHome(frmHome)
        self.__TabSearch(frmSearch)
        self.__TabCheckout(frmCheckout)
        self.__TabReturn(frmReturn)


###############################
####------MAIN----------#######
###############################
def main():
    global tk
    tk = Tk()
    mGUI = MainGUI(tk)

    tk.mainloop()


if __name__ == '__main__':
    main()
