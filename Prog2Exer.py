from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from reportlab.pdfgen import canvas
import os
import datetime
import re
import csv 
#main window
mainw = Tk()
mainw.title("Window")
# mainw.geometry("1350x400")
# mainw.geometry("{0}x{1}+0+0".format(mainw.winfo_screenwidth(), mainw.winfo_screenheight()))
mainw.attributes('-fullscreen',True)
mainw.configure(bg="white")

global tblframe
tblframe = Frame(mainw)
tblframe.grid(row=21, column = 5)
global ordframe
ordframe = Frame(mainw)
ordframe.grid(row=22, column = 5)

#variables
id1 = 0
m = 0
d = 0
y = 0 
strbday = "str"
namel = 0
addl = 0
emaill = 0
bdayl = 0
name = False
cus = [[None for i in range(7)] for j in range(10)] 
orders3d = [[[None for i in range(7)] for j in range(5)] for k in range(10)]
prodslist3d = [[[None for i in range(7)] for j in range(5)] for k in range(10)]
prodslist2d = [[None for i in range(7)] for j in range(10)] 
deletedID = []
clicked = False
clickedprod = False
count = [0,0,0,0,0,0,0,0,0,0]
pid1 = 0
index = 0
change = False
quansum = 0
ordersum = 0
laborProd, ohProd, dpProd = 0, 0, 0
############################ product window ###############################################################################
def products():
    pwin = Toplevel()
    pwin.title("Products")
    pwin.geometry("1300x400")
    pwin.configure(bg="white")
    pwin.lift(aboveThis=mainw)
    global ptblframe1
    ptblframe1 = Frame(pwin)
    ptblframe1.grid(row=21, column=5)
    global ptblframe2
    ptblframe2 = Frame(pwin)
    ptblframe2.grid(row=22, column=5)
    global today
    today = datetime.date.today().strftime('%m/%d/%Y')
    global lcost, ohcost, profit
    #msg function
    global lcost, ohcost, profit
    def prodmsg(titlbar, msg):
        messagebox.showinfo(title=titlbar, message=msg)
    def prods2dwrite():
        with open('prods2d.csv', 'w', newline = '') as prods2dcsv:
            write = csv.writer(prods2dcsv)
            write.writerows(prodslist2d)
    def prods2dread():
        prods2dnew = []
        try:
            with open('prods2d.csv') as prods2dcsv:
                reader = csv.reader(prods2dcsv)
                prods2dnew = list(reader)
            for i in range(len(prods2dnew)):
                for j in range(len(prods2dnew[0])):
                    prodslist2d[i][j] = prods2dnew[i][j]
        except: 
            print("No product/s saved!")
    def prods3dwrite():
        list3d2d = []
        for a in prodslist3d:
            for b in a:
                list3d2d.append(b)
        with open('prods3d.csv', 'w', newline = '') as prods3dcsv:
            write = csv.writer(prods3dcsv)
            write.writerows(list3d2d)
    def prods3dread():  
        prods3dnew1 = []
        try:
            with open('prods3d.csv', 'r') as prods3dcsv:
                reader = csv.reader(prods3dcsv)
                prods3dnew1 = list(reader)
            prods3dnew2 = []
            index1 = len(prodslist3d)
            index2 = len(prodslist3d[0])
            index3 = len(prodslist3d[0][0])
            count = 0
            for x in range(index1):
                prods3dnew2.append([])
                for y in range(index2):
                    prods3dnew2[x].append([])
                    for z in range(index3):
                        # if count == len(prods3dnew1):
                        #     break
                        prods3dnew2[x][y].append(prods3dnew1[count][z])
                    count = count + 1
            for i in range(len(prods3dnew2)):
                for j in range(len(prods3dnew2[0])):
                    for k in range(len(prods3dnew2[0][0])):
                        if prods3dnew2[i][j][0] != '':
                            prodslist3d[i][j][k] = prods3dnew2[i][j][k]
        except:
            print('No product/s yet!')
    def countwrite():
        count2d = []
        for i in range(len(count)):
            count2d.append([count[i]])
        try:
            with open('count.csv', 'w',newline = '') as cntfile:
                write = csv.writer(cntfile)
                write.writerows(count2d)
        except:
            print("No product/s saved!")
    def countread():
        countnew = []
        try:
            with open('count.csv') as cntfile:
                reader = csv.reader(cntfile)
                countnew = list(reader)
        except:
            print('No customer saved!')
        for i in range(len(countnew)):
            for j in range(len(countnew[0])):
                count[i] = int(countnew[i][j])
    def writeIn():
        inCost = [int(str(lcost.get())), int(str(ohcost.get())), int(str(profit.get()))]
        inCost2d = []
        for i in range(len(inCost)):
            inCost2d.append([inCost[i]])
        with open('costs.csv', 'w', newline='') as cntfile:
            write = csv.writer(cntfile)
            write.writerows(inCost2d)
    def savecosts():
        writeIn()
    prods2dread()
    prods3dread()
    countread()
############################ product functions #########################################################################
    def psave():
        global pid1
        order = 0
        typel = len(ptype.get())
        quan1l= len(quan1.get())
        costl = len(cost.get())
        descl = len(pdesc.get())
        index = 0
        print(prodslist2d)
        if prodslist2d[0][0] == None:
            pid1 = 1
        else:
            while prodslist2d[index][0] != '' and prodslist2d[index][0] != None:
                index = index + 1
            pid1 = int(prodslist2d[index-1][0]) + 1
        if typel == 0 or quan1l == 0 or costl == 0 or descl == 0: 
            msg("Error!", "Incomplete Credentials")
        else:
            pid.set(pid1)
            prodcreds = [str(pid1), ptype.get(), pdesc.get(), quan1.get(), cost.get(), str(today), order]
            for j in range(len(prodslist2d[0])):
                if(j == 4):
                    prodslist2d[index][j] = "-------"
                prodslist2d [index][j] = prodcreds[j]
            for k in range(len(prodslist3d[0][0])):
                prodslist3d [index][count[index]][k] = prodcreds[k]
            dr.set(today)
            prods2dwrite()
            prods3dwrite()
            count[index] = count[index] + 1
            countwrite()
            for pent2 in ptblframe2.winfo_children():
                    pent2.destroy()
            prodtbl1()
            prodmsg("Success", "Product has been added!")
    #stock in
    def stockin():
        global quansum
        order = 0
        typel = len(ptype.get())
        quan2l= len(quan2.get())
        costl = len(cost.get())
        quansum = 0 
        if clickedprod == False:
            prodmsg("Error", "Please select a product to add stocks")
        elif clickedprod == True:
            if typel == 0 or quan2l == 0 or costl == 0: 
                prodmsg("Error!", "Incomplete Credentials")
            else:
                prodcreds = [pselect+1, ptype.get(), pdesc.get(), quan2.get(), cost.get(), str(today), order]
            for k in range(len(prodslist3d[0][0])):
                prodslist3d [pselect][count[pselect]][k] = prodcreds[k]
            for l in range(len(prodslist3d[0])):
                if(prodslist3d[pselect][l][0] != None):
                    quansum = quansum + int(prodslist3d[pselect][l][3])
            for j in range(len(prodslist2d[0])):   
                if(j == 3):
                    prodslist2d[pselect][j] = quansum
                if(j == 4):
                    prodslist2d[pselect][j] = "-------"
                prodslist2d[pselect][j]    
            prods2dwrite()
            prods3dwrite()
            count[pselect] = count[pselect] + 1
            countwrite()
            prodmsg("Success", "Stock has been added!")
            for pent2 in ptblframe2.winfo_children():
                pent2.destroy()
            prodtbl1()
            prodtbl2()
    #selectrow table 1
    def pselectrow(prow):
        global pselect
        global clickedprod
        pselect = prow.widget._row
        pid.set(prodslist2d[pselect][0])
        ptype.set(prodslist2d[pselect][1])
        pdesc.set("")
        quan1.set(prodslist2d[pselect][3])
        quan2.set("")
        cost.set("")
        dr.set("")
        clickedprod = True
        for pent2 in ptblframe2.winfo_children():
            pent2.destroy()
        print('P1: ')
        print(prodslist3d)
        prods2dwrite()
        prods3dwrite()
        prodtbl2()
        prodtbl1()
    #selectrow table 2
    def pselectrow2(prow2):
        global pselect2
        global clickedprod2
        pselect2 = prow2.widget._row
        print('P2: ')
        print(pselect2)
        clickedprod2 = True
############################ product entry #########################################################################
    #title
    label = Label(pwin, text="Products Stock-In")
    label.config(font=("Product Sans", 10))
    label.grid(column=2, row=1, pady=(10,10), padx=(5,5))
    #product id & input
    label = Label(pwin, text="Product ID:")
    label.config(font=("Product Sans", 10))
    label.grid(column=1, row=2, pady=(5,5), padx=(5,5))
    
    pid = IntVar()
    pidwin = Entry(pwin, textvariable=pid, state="readonly")
    pidwin.grid(column=2, row=2, pady=(5,5))
    #product type & input
    label = Label(pwin, text="Product Type:")
    label.config(font=("Product Sans", 10))
    label.grid(column=1, row=3, padx=(5,5))
    
    ptype = StringVar()
    ptypewin = Entry(pwin, textvariable=ptype)
    ptypewin.grid(column=2, row=3, pady=(5,5), padx=(5,5))
    #product desc & input
    label = Label(pwin, text="Product Desc:")
    label.config(font=("Product Sans", 10))
    label.grid(column=3, row=3,  pady=(5,5), padx=(5,5))

    pdesc = StringVar()
    pdescwin = Entry(pwin, textvariable=pdesc)
    pdescwin.grid(column=4, row=3,  pady=(5,5), padx=(5,5))
    #product quan1 and quan2 & input
    label = Label(pwin, text="Product Quantity:")
    label.config(font=("Product Sans", 10))
    label.grid(column=1, row=7)
    
    quan1 = StringVar()
    quan1ent = Entry(pwin, textvariable=quan1)
    quan1ent.grid(column=2, row=7)
    
    plus = Label(pwin, text="+")
    plus.grid(column=3, row=7)

    quan2 = StringVar()
    quan2ent = Entry(pwin, textvariable=quan2)
    quan2ent.grid(column=4, row=7, pady=(5,5), padx=(5,5))
    #product cost & input
    label = Label(pwin, text="Product Cost:")
    label.config(font=("Product Sans", 10))
    label.grid(column=1, row=8, pady=(5,5), padx=(5,5))
    
    cost = StringVar()
    costent = Entry(pwin, textvariable=cost)
    costent.grid(column=2, row=8, pady=(5,5), padx=(5,5))
    #date received & input
    label = Label(pwin, text="Date Received:")
    label.config(font=("Product Sans", 10))
    label.grid(column=1, row=9, pady=(5,5), padx=(5,5))
    
    dr = StringVar()
    drwin = Entry(pwin, textvariable=dr, state="readonly")
    drwin.grid(column=2, row=9, pady=(5,5), padx=(5,5))
    #save button
    psbtn = Button(pwin, text="Save", command=psave)
    psbtn.grid(column=1, row=10, pady=(5,5), padx=(5,5))
    #stock in button
    sibtn = Button(pwin, text="Stock-in", command=stockin)
    sibtn.grid(column=1, row=11, pady=(5,5), padx=(5,5))
    #labor cost
    label = Label(pwin, text="Labor Cost:")
    label.config(font=("Product Sans", 10))
    label.grid(column=1, row=12,  pady=(5,5), padx=(5,5))

    lcost = StringVar()
    lcostwin = Entry(pwin, textvariable=lcost)
    lcostwin.grid(column=2, row=12,  pady=(5,5), padx=(5,5))
    #overhead cost
    label = Label(pwin, text="Overhead Cost:")
    label.config(font=("Product Sans", 10))
    label.grid(column=3, row=12,  pady=(5,5), padx=(5,5))

    ohcost = StringVar()
    ohcostwin = Entry(pwin, textvariable=ohcost)
    ohcostwin.grid(column=4, row=12,  pady=(5,5), padx=(5,5))
    #desired profit
    label = Label(pwin, text="Desired Profit:")
    label.config(font=("Product Sans", 10))
    label.grid(column=1, row=13,  pady=(5,5), padx=(5,5))

    profit = StringVar()
    profitwin = Entry(pwin, textvariable=profit)
    profitwin.grid(column=2, row=13,  pady=(5,5), padx=(5,5))
    #save costs button
    savebtn = Button(pwin, text="Save", command=savecosts)
    savebtn.grid(column=4, row=13, pady=(5,5))
    def readIn():
        costsnew = []
        try:
            with open('costs.csv', 'r') as cntfile:
                reader = csv.reader(cntfile)
                costsnew = list(reader)
            lcost.set(int(costsnew[0][0]))
            ohcost.set(int(costsnew[1][0]))
            profit.set(int(costsnew[2][0]))
        except:
            pass
    readIn()
######table & reading csv files#####
    def prodtbl1():
        global pent1 
        label = ["Product ID", "Product Type", "Product Desc", "Total Quantity", "Total Cost", "Date Received", "Orders"]
        for a in range(len(label)):
            j = Entry(ptblframe1) 
            j.insert(END, label[a])
            j.grid(row=1, column=a+4)
        for x in range (len(prodslist2d)):
            for y in range (len(prodslist2d[0])):
                if prodslist2d[x][y] != None and prodslist2d[x][y] != '':
                    pent1 = Entry(ptblframe1)
                    pent1.insert(END, str(prodslist2d[x][y]))
                    pent1._row = x
                    pent1.grid(row=x+2, column=y+4)
                    pent1.bind('<Button-1>', pselectrow)
        slabel = Label(ptblframe2, text="Stock-IN")
        slabel.grid(row=1, column=5)
    def prodtbl2():
        global pent2
        label = ["Product ID", "Product Type", "Product Desc", "Total Quantity", "Total Cost", "Date Received", "Orders"]
        for a in range(len(label)):
            j = Entry(ptblframe2)
            j.insert(END, label[a])
            j.grid(row=2, column=a+5)
        for y in range (len(prodslist3d[0])):
            for z in range (len(prodslist3d[0][0])):
                if prodslist3d[pselect][y][z] != None and prodslist3d[pselect][y][z] != '':
                    pent2 = Entry(ptblframe2)
                    pent2.insert(END, str(prodslist3d[pselect][y][z]))
                    pent2._row = y
                    pent2.grid(row=y+3, column=z+5)
                    pent2.bind('<Button-1>', pselectrow2)
    prodtbl1()
    if(change == True):
        prodtbl1()
        prodtbl2()   
############################ menubar #########################################################################
#menubar
menubar = Menu(mainw)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Products", command=products) 
filemenu.add_command(label="Orders")
filemenu.add_separator() 
filemenu.add_command(label="Exit", command=mainw.quit) 
mainw.config(menu=menubar)
############################ main functions #########################################################################
#checkname
def checkname(gname):
    global name
    name == False
    gname = cname.get()
    regexname = '^[A-Z][a-z]+[,]\s[A-Z][a-zA-Z]+$'
    a = re.findall(regexname, gname)
    if re.search(regexname, gname):
        namelabel.config(text="Valid Name/Format")
        name = True
    else:
        namelabel.config(text="Invalid Name/Format")
        name = False
#checknum
def checknum(number):
    try:
        int(number)
        return True
    except ValueError:
        print('invalid')
#checkemail
def checkemail(e):
    email = cemail.get()
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+\.(com)$'
    if (re.search(regex, email)):
        emailcheck.config(text="Good Email")
    else:
        emailcheck.config(text="Bad Email")
#bdaycheck format
def checkbdayformat(bday):
    try:
        datetime.datetime.strptime(bday, '%m/%d/%Y')
        return True
    except ValueError:
        pass
#bdaycheck
def checkbday(e):
    global strbday
    if checkbdayformat(cbday.get()):
        strbday = cbday.get()
        if checkminor(strbday):
            bdaycheck.config(text="Valid Birthday")
    else:
        bdaycheck.config(text="Invalid Birthday/Minor")
#checkminor
def checkminor(bday):
    global m
    global d
    global y
    today = datetime.date.today()
    m, d, y = strbday.split("/")    
    cubday = datetime.date(int(y), int(m), int(d))
    diff = (today-cubday).days/(365)
    if int(diff) >= 18:
        return True
    else:
        return False
##selecting row
def selectrow(row):
    global clicked
    global cselect
    cselect = row.widget._row
    cid.set(cus[cselect][0])
    cname.set(cus[cselect][1])
    cadd.set(cus[cselect][2])
    cnum.set(cus[cselect][3])
    cemail.set(cus[cselect][4])
    cbday.set(cus[cselect][5])
    cgen.set(cus[cselect][6])
    clicked = True
    for ordEnt in ordframe.winfo_children():
        ordEnt.destroy()
    maintbl()
    ordertbl()
################################buttons###################################
#save button
def save():
    global tblframe
    global id1
    global clicked 
    namel = len(cname.get())
    addl = len(cadd.get())
    emaill = len(cemail.get())
    bdayl = len(cbday.get())
    cnuml = len(cnum.get())
    indexnxt = 0
    id1 = 0
    gen = cgen.get()
    deletedID.sort()
    if namel == 0 or addl == 0 or cnuml == 0 or emaill == 0 or bdayl == 0 or gen == "----------": 
        msg("Error!", "Incomplete Credentials")
    else:
        if checknum(cnum.get()) == True and cnuml == 11 and emailcheck['text'] == "Good Email" and bdaycheck['text'] == "Valid Birthday" and name == True:
            cuswrite()
            cusread()
            if cus[0][0] == '':
                indexnxt = 0
                id1 = 1
            else:
                while cus[indexnxt][0] != '':
                    if indexnxt == len(cus):
                        msg("Error", "Limit reached!")
                    else:
                        indexnxt += 1
                id1 = int(cus[indexnxt-1][0])+1
            if len(deletedID) == 0:
                cid.set(id1)
                creds = [str(id1), cname.get(), cadd.get(), cnum.get(), cemail.get(), cbday.get(), cgen.get()]
                for i in range(7):
                    cus[indexnxt][i] = creds[i]
            else:
                it = iter(deletedID)
                id2 = next(it)
                print("before: ")
                print(deletedID)
                deletedID.remove(id2)
                print("after: ")
                print(deletedID)
                creds = [str(id2), cname.get(), cadd.get(), cnum.get(), cemail.get(), cbday.get(), cgen.get()]
                for i in range(7):
                    cus[indexnxt][i] = creds [i]
                delwrite()
            cuswrite()
            maintbl()
            msg("Success", "Customer has been added!")
        else:
            msg("Error!", "Please make sure that: \n Name must not contain numbers. \n Name must follow 'Last, First' format. \n Contact number must be 11 integers. \n Email/birthday must be valid \n Follow given birthday format. \n Minors are not allowed.")
        for ordEnt in ordframe.winfo_children():
            ordEnt.destroy()
#update button 
def update():
    global clicked
    print('update is working')
    namel = len(cname.get())
    addl = len(cadd.get())
    emaill = len(cemail.get())
    bdayl = len(cbday.get())
    cnuml = len(cnum.get())
    gen = cgen.get() 
    if namel == 0 or addl == 0 or cnuml == 0 or emaill == 0 or bdayl == 0 or gen == "----------": 
        msg("Error!", "Incomplete Credentials")
    else:
        if checknum(cnum.get()) == True and cnuml == 11 and emailcheck['text'] == "Good Email" and bdaycheck['text'] == "Valid Birthday" and name == True:
            if clicked is True:
                creds = [cid.get(), cname.get(), cadd.get(), cnum.get(), cemail.get(), cbday.get(), cgen.get()]
                for i in range(len(cus[0])):
                    cus[cselect][i] = creds[i]
                print(cus)
                cuswrite()
                maintbl()
                msg("Success!", "Customer has been updated.")
            else:
                msg("Error!", "Please select a row to update.")
#delete button
def delete():
    global clicked
    namel = len(cname.get())
    addl = len(cadd.get())
    emaill = len(cemail.get())
    bdayl = len(cbday.get())
    cnuml = len(cnum.get())
    gen = cgen.get()
    if namel == 0 or addl == 0 or cnuml == 0 or emaill == 0 or bdayl == 0 or gen == "----------": 
            msg("Error!", "Incomplete Credentials")
    else:
        if clicked is True:
            print(cus[cselect][0])
            dID = str(cus[cselect][0])
            deletedID.append(dID)
            cus.pop(cselect)
            cuswrite()
            delwrite()
            msg("Success!", "Customer deleted!")
            for ent in tblframe.winfo_children():
                ent.destroy()
            maintbl()
        else: 
            msg("Error!", "Please select a row to be deleted")
#add order button
def add():
    global change
    selectedBool = False
    try:
        cselect
        pselect
        pselect2
        selectedBool = True
    except NameError:
        selectedBool = False
    if(selectedBool):
        prodID = prodslist3d[pselect][pselect2][0]
        prodType = prodslist3d[pselect][pselect2][1]
        prodDesc = prodslist3d[pselect][pselect2][2]
        prodQuan = prodslist3d[pselect][pselect2][3]
        prodCost = prodslist3d[pselect][pselect2][4]
        prodOrder =  prodslist3d[pselect][pselect2][6]
        prodDividend = int(prodQuan) + int(prodOrder)
        quanProd = 1
        unitCost = 0
        check = False
        inNum = 1
        maxRow = 0
        for i in range(len(orders3d[0])):
            if(orders3d[cselect][i][0] != None):
                maxRow = i
        inNum = cselect + 1
        labor = lcost.get()
        overhead = ohcost.get()
        dp = profit.get()
        if(len(labor) != 0 or len(overhead) != 0 or len(dp) != 0):
            if(orders3d[cselect][0][0] == None):
                unitCost = (int(prodCost) / int(prodDividend))+ int(labor)+int(overhead)+int(dp)
                prodcreds = [inNum, prodID, prodType, prodDesc, quanProd, unitCost, str(today)]
                for i in range(len(orders3d[0][0])):
                    orders3d[cselect][0][i] = prodcreds[i]
            else:
                for i in range(len(orders3d[0])):
                    if(orders3d[cselect][i][0] != None):
                        if(orders3d[cselect][i][1] == prodID):
                            if(orders3d[cselect][i][2] == prodType):
                                if(orders3d[cselect][i][3] == prodDesc):
                                    index = i
                                    check = True
                if(check == True):
                    inNum = int(orders3d[cselect][index][0])
                    quanProd = int(orders3d[cselect][index][4]) + 1
                    unitCost = (int(prodCost) / int(prodDividend))+ int(labor)+int(overhead)+int(dp)
                    prodcreds = [inNum, prodID, prodType, prodDesc, quanProd, unitCost, str(today)]
                    for i in range(len(orders3d[0][0])):
                        orders3d[cselect][index][i] = prodcreds[i]
                else:
                    quanProd = 1
                    unitCost = (int(prodCost) / int(prodDividend))+ int(labor)+int(overhead)+int(dp)
                    prodcreds = [inNum, prodID, prodType, prodDesc, quanProd, unitCost, str(today)]
                    for i in range(len(orders3d[0][0])):
                        orders3d[cselect][maxRow+1][i] = prodcreds[i]
            change = True
            afterAdd()
            ordwrite()
            maintbl()
            ordertbl()
        else:
            msg("Error!", "Input labor cost, overhead cost, and desired profit.")
    else:
        msg("Error", "No customer/product")
#after add
def afterAdd():
    global ordersum
    ordersum = 0
    prodslist2d[pselect][3] = int(prodslist2d[pselect][3]) - 1
    prodslist3d[pselect][pselect2][3] = int(prodslist3d[pselect][pselect2][3]) - 1
    prodslist3d[pselect][pselect2][6] = int(prodslist3d[pselect][pselect2][6]) + 1
    for i in range(len(prodslist3d[0])):
        if(prodslist3d[pselect][i][0] != None):
            ordersum = ordersum + int(prodslist3d[pselect][i][6])
    print("ordersum: ")
    print(ordersum)
    prodslist2d[pselect][6] = ordersum
#pdf 
def createpdf():
    if clicked and orders3d[cselect][0][0] != None:
        subtotal = 0.0
        c = canvas.Canvas("invoice.pdf")
        c.setFont("Helvetica-Bold", 15)
        c.drawString(400, 750, "CUSTOMER INVOICE")
        c.drawString(55, 750, "Iya Enterprise")
        c.setFont("Helvetica", 10)
        c.drawString(55, 735, "Abc Street, Def Building")
        c.drawString(55, 720, "Davao City, Davao del Sur")
        c.drawString(55, 705, "Philippines")                        ####
        c.drawString(400, 735, str(datetime.date.today().strftime('%m/%d/%Y')))
        c.drawString(400, 720, "Invoice No. " + orders3d[cselect][0][0])
        c.drawString(400, 705, "Customer No. " + cus[cselect][0])
        c.line(5, 695, 590, 695)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(55, 650, "Bill To")
        c.setFont("Helvetica", 10)
        c.drawString(55, 635, cus[cselect][1])
        c.drawString(55, 620, cus[cselect][2])
        c.drawString(55, 605, cus[cselect][3])
        c.setFont("Helvetica-Bold", 13)
        c.drawString(150, 560, "PRODUCT")
        c.drawString(330, 560, "QUANTITY")
        c.drawString(430, 560, "UNIT PRICE")
        c.setFont("Helvetica", 11)
        y = 525
        for i in range(len(orders3d[0])):
            if orders3d[cselect][i][0] != None:
                c.drawString(150, y, str(orders3d[cselect][i][2]) + " " + str(orders3d[cselect][i][3]))
                c.drawString(350, y, str(orders3d[cselect][i][4]))
                c.drawString(450, y, str(orders3d[cselect][i][5]))
                y -= 20
                subtotal += (float(orders3d[cselect][i][5]) * float(orders3d[cselect][i][4]))
        c.setFont("Helvetica-Bold", 11)
        c.drawString(340, y-20, "SUBTOTAL")
        c.drawString(340, y-40, "TAX 12%")
        c.drawString(340, y-60, "TOTAL")
        c.drawString(450, y-60, str(subtotal + (subtotal * 0.12)))
        c.setFont("Helvetica", 11)
        c.drawString(450, y-20, str(subtotal))
        c.drawString(450, y-40, str(subtotal * 0.12))
        c.save()
        os.startfile("invoice.pdf")
    else:
        msg("Error", "No customer selected/Customer has no orders!")
#msg function
def msg(titlbar, msg):
    messagebox.showinfo(title=titlbar, message=msg)
############################ main window #########################################################################
#title
tlabel = Label(mainw, text="Customer Registration System", width=30, height=1, anchor="center")
tlabel.configure(font=("Courier", 20))
tlabel.grid(column=2, row=1, pady=(10, 10))

#customer id & input
label = Label(mainw, text="Customer ID:", height=1, anchor="w")
tlabel.config(font=("Product Sans", 10))
label.grid(column=1, row=2, pady=(5,5))

cid = IntVar()
idwin = Entry(mainw, textvariable=cid, state="readonly")
idwin.grid(column=2, row=2, pady=(5,5))

#customer name & input
label = Label(mainw, text="Customer Name:", height=1, anchor="w")
label.grid(column=1, row=3, pady=(5,5))

cname = StringVar()
nwin = Entry(mainw, textvariable=cname)
nwin.grid(column=2, row=3, pady=(5,5))
nwin.bind("<KeyRelease>", checkname)

namelabel = Label(mainw, text="Last, First", height=1, anchor="center")
namelabel.grid(column=3, row=3, pady=(5,5))

#customer address & input
label = Label(mainw, text="Customer Address:", height=1, anchor="w")
label.grid(column=1, row=4, pady=(5,5))

cadd = StringVar()
cwin = Entry(mainw, textvariable=cadd)
cwin.grid(column=2, row=4, pady=(5,5))

#customer num & input
label = Label(mainw, text="Contact Number:", height=1, anchor="w")
label.grid(column=1, row=5, pady=(5,5))

cnum = StringVar()
nwin = Entry(mainw, textvariable=cnum)
nwin.grid(column=2, row=5, pady=(5,5))

#customer email & input
label = Label(mainw, text="Customer Email:", height=1, anchor="w")
label.grid(column=1, row=6, pady=(5,5))

cemail = StringVar()    
ewin = Entry(mainw, textvariable=cemail)
ewin.grid(column=2, row=6, pady=(5,5))
ewin.bind("<KeyRelease>", checkemail)

emailcheck = Label(mainw, text="e.g youremail@domain.com", height=1, anchor="center")
emailcheck.grid(column=3, row=6, pady=(5,5))

#bday & input
label = Label(mainw, text="Customer Bday:", height=1, anchor="w")
label.grid(column=1, row=7, pady=(5,5))

cbday = StringVar()
bwin = Entry(mainw, textvariable=cbday)
bwin.grid(column=2, row=7, pady=(5,5))
bwin.bind("<KeyRelease>", checkbday)

bdaycheck = Label(mainw, text="MM/dd/yyyy", height=1, anchor="center")
bdaycheck.grid(column=3, row=7, pady=(5,5))

#gender combobox
cgen = StringVar()
ttk.Label(mainw, text="Gender").grid(column=1, row=8)
genderchosen = ttk.Combobox(mainw, width=10, textvariable=cgen)
genderchosen['values'] = ('----------', 'Female', 'Male')
genderchosen.grid(column=2, row=8, pady=(5,5)) 
genderchosen.current(0) 
#save button
savebtn = Button(mainw, text="Save", command=save)
savebtn.grid(column=1, row=10, pady=(10,10))
#update button
ubtn = Button(mainw, text="Update", command=update)
ubtn.grid(column=2, row=10, pady=(10,10))
#delete button
dbtn = Button(mainw, text="Delete", command=delete)
dbtn.grid(column=3, row=10, pady=(10,10))
#add button
abtn = Button(mainw, text="Add Order", command=add)
abtn.grid(column=3, row=11, pady=(10,10))
#print button
pbtn = Button(mainw, text="Print Invoice", command=createpdf)
pbtn.grid(column=3, row=12, pady=(10,10))

#####table frame####

######table#####
def maintbl():
    global ent
    label = ["ID", "Name", "Address", "Contact Number", "Email", "Birthday", "Gender"]
    for a in range(len(label)):
        j = Entry(tblframe)
        j.insert(END, label[a])
        j.grid(row=20, column=a+4)
    for x in range (len(cus)):
        for y in range (len(cus[0])):
            if cus[x][y] != None and cus[x][y] != '':
                ent = Entry(tblframe)
                ent.insert(END, str(cus[x][y]))
                ent._row = x
                ent.grid(row=x+21, column=y+4)
                ent.bind('<Button-1>', selectrow)
    olabel = Label(ordframe, text="ORDERS")
    olabel.grid(row=22, column=6)
def ordertbl():
    label = ["Invoice No.", "ID", "Description", "Type", "Quantity", "Unit Price", "Date Received"]
    for a in range(len(label)):
        j = Entry(ordframe)
        j.insert(END, label[a])
        j.grid(row=23, column=a+5)
    for x in range (len(orders3d[0])):
        for y in range (len(orders3d[0][0])):
            if orders3d[cselect][x][y] != None and orders3d[cselect][x][y] != '':
                ordEnt = Entry(ordframe)
                ordEnt.insert(END, str(orders3d[cselect][x][y]))
                ordEnt._row = x
                ordEnt.grid(row=x+24, column=y+5)
    
######csv functions####
def cuswrite(): 
    try:
        with open('customers.csv', 'w',newline = '') as cuscsv:
            write = csv.writer(cuscsv)
            write.writerows(cus)
    except:
        print("No customer/s saved!")
def cusread():
    cusnew = []
    try:
        with open('customers.csv') as cuscsv:
            reader = csv.reader(cuscsv)
            cusnew = list(reader)
    except:
        print('No customer saved!')
    for i in range(len(cusnew)):
        for j in range(len(cusnew[0])):
            cus[i][j] = cusnew[i][j]
def delwrite():
    try:
        with open('delcus.csv', 'w',newline = '') as delcsv:
            write = csv.writer(delcsv)
            write.writerows(deletedID)
    except:
        print("No customer/s deleted!")
def delread():
    delnew = []
    try:
        with open('delcus.csv') as delcsv:
            reader = csv.reader(delcsv)
            delnew = list(reader)
    except:
        print('No customer deleted!')

    print (deletedID)
    for i in range(len(delnew)):
        for j in range(len(delnew[0])):
            deletedID.append(str(delnew[i][j]))
def ordwrite():
    order3d2d = []
    for a in orders3d:
        for b in a:
            order3d2d.append(b)
    with open('orders3d.csv', 'w', newline='') as ordfile:
        write = csv.writer(ordfile)
        write.writerows(order3d2d)
def ordread():
    order3dnew1 = []
    try:
        with open('orders3d.csv', 'r') as ordfile:
            reader = csv.reader(ordfile)
            order3dnew1 = list(reader)
        order3dnew2 = []
        index1 = len(orders3d)
        index2 = len(orders3d[0])
        index3 = len(orders3d[0][0])
        count = 0
        for x in range(index1):
                order3dnew2.append([])
                for y in range(index2):
                    order3dnew2[x].append([])
                    for z in range(index3):
                        # if count == len(prods3dnew1):
                        #     break
                        order3dnew2[x][y].append(order3dnew1[count][z])
                    count = count + 1
        for i in range(len(order3dnew2)):
            for j in range(len(order3dnew2[0])):
                for k in range(len(order3dnew2[0][0])):
                    if order3dnew2[i][j][0] != '':
                        orders3d[i][j][k] = order3dnew2[i][j][k]
    except:
        pass

cusread()
ordread()
delread()
maintbl()
mainw.mainloop()