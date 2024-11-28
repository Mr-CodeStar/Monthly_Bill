import customtkinter as ctk
from datetime import datetime
from tkinter import ttk
from tkinter import messagebox
import os
import sqlite3
import string

current_date=datetime.now()
month_name=current_date.strftime("%B")
year=current_date.strftime("%Y")

if os.path.exists("Bill_data/"):
    if os.path.exists("Bill_data/"+month_name+str(year)+".db"):
        pass
    else:
        cons=sqlite3.connect("Bill_data/"+month_name+str(year)+".db")
        cursor=cons.cursor()
        table1="""create table buget(amount REAL)"""
        table2="""create table data(item TEXT,price REAL,date TEXT,quantity TEXT)"""
        try:
            cursor.execute(table1)
            query="insert into buget(amount) values (?)"
            values=(0,)
            cursor.execute(query,values)
            cons.commit()
            cursor.execute(table2)
        except Exception:
            messagebox.showerror(title="Error",message="table not created ")
        cons.close()
else:
    os.makedirs("Bill_data")
    cons=sqlite3.connect("Bill_data/"+month_name+str(year)+".db")
    cursor=cons.cursor()
    table1="""create table buget(amount REAL)"""
    table2="""create table data(item TEXT,price REAL,date TEXT,quantity TEXT)"""
    try:
        cursor.execute(table1)
        query="insert into buget(amount) values (?)"
        values=(0,)
        cursor.execute(query,values)
        cons.commit()
        cursor.execute(table2)
    except Exception:
        messagebox.showerror(title="Error",message="table not created ")
    cons.close()

class MonthBill(ctk.CTk):
    def __init__(self,month):
        monthname=month
        #### Initilising the GUI######
        super().__init__()
        #### Basic Information ########
        self.title("Monthly-Bills")
        self.minsize(1500,900)
        self.maxsize(1500,900)
        #################################### Month Name#######################################
        self.month_name=ctk.CTkLabel(self,text=monthname,font=("bold",30))
        self.month_name.place(x=1340,y=50)
        #################################### Bugget frame#####################################
        self.bugget_frame=ctk.CTkFrame(self,width=1250,height=50)
        self.bugget_frame.place(x=50,y=50)
        cons=sqlite3.connect("Bill_data/"+month_name+str(year)+".db")
        cursor=cons.cursor()
        query="""select * from buget"""
        cursor.execute(query)
        lst=cursor.fetchall()
        cons.close()
        self.bugget_label=ctk.CTkLabel(self.bugget_frame,text=lst[0][0],font=("bold",30))
        self.bugget_label.place(x=0,y=0)
        #################################### Labels ##########################################
        self.item=ctk.CTkLabel(self,text="Item",font=("Bold",40))
        self.item.place(x=100,y=150)
        self.price=ctk.CTkLabel(self,text="Price",font=("Bold",40))
        self.price.place(x=500,y=150)
        self.date=ctk.CTkLabel(self,text="Date",font=("Bold",40))
        self.date.place(x=900,y=150)
        self.quantity=ctk.CTkLabel(self,text="Quantity",font=("Bold",40))
        self.quantity.place(x=1250,y=150)
        ################################### Entry Boxs ########################################
        self.item_value=ctk.CTkEntry(self,width=200,height=50,font=("Bold",40))
        self.item_value.place(x=50,y=250)
        self.price_value=ctk.CTkEntry(self,width=200,height=50,font=("Bold",40))
        self.price_value.place(x=450,y=250)
        self.date_value=ctk.CTkEntry(self,width=200,height=50,font=("Bold",40))
        self.date_value.place(x=850,y=250)
        self.quantity_value=ctk.CTkEntry(self,width=200,height=50,font=("Bold",40))
        self.quantity_value.place(x=1230,y=250)
        ############################### TreeView ##############################################
        self.treefunction()
        ################################## Functionality ######################################
        self.bugget_label.bind("<Double-Button-1>",self.buggetedit)
        self.bind("<Return>",self.savedata)
        self.bind("<Control-x>",self.destroy_event)
        self.tree.bind("<Triple-Button-1>",self.clicker)
        self.bind("<Delete>",self.delete)
        self.bind("<Control-u>",self.update)
        self.bind("<Control-c>",self.clearentry)
        self.bind("<Control-v>",self.viewBuget)
    def show_error(self,error):
        messagebox.showerror(title="Error",message=error)
    def viewBuget(self,event):
        messagebox.showwarning(title="Warning",message="While closing the application please close the other Windows before closing the main Window")
        import Monthly_Bill_Sub_File
    def treefunction(self):
        self.tree_frame=ctk.CTkFrame(self,width=1400,height=400)
        self.tree_frame.place(x=40,y=450)
        self.tree=ttk.Treeview(self.tree_frame,columns=("Item","Price","Date","Quantity"),show="headings",height=15)
        style = ttk.Style()
        style.configure("Treeview",
                        background="#2B2B2B",
                        foreground="white",
                        fieldbackground="#2B2B2B",
                        font=('Arial', 12))
        self.tree.heading("Item",text="Item")
        self.tree.heading("Price",text="Price")
        self.tree.heading("Date",text="Date")
        self.tree.heading("Quantity",text="Quantity")
        self.tree.column("Item",anchor="center",width=350)
        self.tree.column("Price",anchor="center",width=350)
        self.tree.column("Date",anchor="center",width=350)
        self.tree.column("Quantity",anchor="center",width=350)
        cons=sqlite3.connect("Bill_data/"+month_name+str(year)+".db")
        cursor=cons.cursor()
        cursor.execute("select * from data")
        data=cursor.fetchall()
        for item in data:
            self.tree.insert("", "end", values=item)
        self.tree.pack(fill="both",expand=True)
        cons.close()
        self.tree.bind("<Triple-Button-1>",self.clicker)
    def clicker(self,event):
        cursor_row=self.tree.focus()
        try:
            content=self.tree.item(cursor_row)
            self.row=content["values"]
            self.item_value.delete(0,"end")
            self.price_value.delete(0,"end")
            self.date_value.delete(0,"end")
            self.quantity_value.delete(0,"end")
            self.item_value.insert(0,self.row[0])
            self.price_value.insert(0,self.row[1])
            self.date_value.insert(0,self.row[2])
            self.quantity_value.insert(0,self.row[3])
        except Exception as e:
            self.show_error(e)
    def update(self,event):
        item=self.item_value.get()
        price=self.price_value.get()
        date=self.date_value.get()
        quantity=self.quantity_value.get()
        if item=="" or price=="" or date=="" or quantity=="":
            self.show_error("No field can be empty")
        else:
            for i in price:
                if i in string.ascii_letters:
                    self.show_error("string in price is not allowed")
                    break
            else:
                price=float(price)
                cons=sqlite3.connect("Bill_data/"+month_name+str(year)+".db")
                cursor=cons.cursor()
                query="select * from buget"
                cursor.execute(query)
                lst=cursor.fetchall()
                lst2=lst[0][0]
                if float(self.row[1]) >= price:
                    lst2=lst2+(float(self.row[1])-price)
                elif float(self.row[1]) <= price:
                    lst2=lst2-(price-float(self.row[1]))
                if lst2 <0:
                    self.show_error("your buget has gone negative, Can't do transaction")
                    self.bugget_label.destroy()
                    self.bugget_label=ctk.CTkLabel(self.bugget_frame,text=self.row[1],font=("bold",30))
                    self.bugget_label.place(x=0,y=0)
                    self.bugget_label.bind("<Double-Button-1>",self.buggetedit)
                else:
                    query="update buget set Amount=?"
                    cursor.execute(query,(lst2,))
                    cons.commit()
                    self.bugget_label.destroy()
                    self.bugget_label=ctk.CTkLabel(self.bugget_frame,text=lst2,font=("bold",30))
                    self.bugget_label.place(x=0,y=0)
                    self.bugget_label.bind("<Double-Button-1>",self.buggetedit)
                    query="update data set item=?,price=?,date=?,quantity=? where item=? and price=? and date=? and quantity=?"
                    value=(item,price,date,quantity,self.row[0],self.row[1],self.row[2],self.row[3])
                    try:
                        cursor.execute(query,value)
                        cons.commit()
                        cons.close()
                    except Exception as e:
                        self.show_error(e)
                        cons.close()
                    else:
                        self.item_value.delete(0,"end")
                        self.price_value.delete(0,"end")
                        self.date_value.delete(0,"end")
                        self.quantity_value.delete(0,"end")
                        self.tree_frame.destroy()
                        self.treefunction()
    def delete(self,event):
        item=self.item_value.get()
        price=self.price_value.get()
        date=self.date_value.get()
        quantity=self.quantity_value.get()
        if item=="" or price=="" or date=="" or quantity=="":
            self.show_error("No field can be empty")
        else:
            for i in price:
                if i in string.ascii_letters:
                    self.show_error("string in price is not allowed")
                    break
            else:
                price=float(price)
                cons=sqlite3.connect("Bill_data/"+month_name+str(year)+".db")
                cursor=cons.cursor()
                query="select * from buget"
                cursor.execute(query)
                lst=cursor.fetchall()
                lst2=lst[0][0]
                lst2=lst2+price
                if lst2 <0:
                        self.show_error("your buget has gone negative, Can't do transaction")
                        self.bugget_label.destroy()
                        self.bugget_label=ctk.CTkLabel(self.bugget_frame,text=self.row[1],font=("bold",30))
                        self.bugget_label.place(x=0,y=0)
                        self.bugget_label.bind("<Double-Button-1>",self.buggetedit)
                else:
                    query="update buget set Amount=?"
                    cursor.execute(query,(lst2,))
                    cons.commit()
                    self.bugget_label.destroy()
                    self.bugget_label=ctk.CTkLabel(self.bugget_frame,text=lst2,font=("bold",30))
                    self.bugget_label.place(x=0,y=0)
                    self.bugget_label.bind("<Double-Button-1>",self.buggetedit)
                    query="""delete from data where item=? and price=? and date=? and quantity=?"""
                    value=(item,price,date,quantity)
                    try:
                        cursor.execute(query,value)
                        cons.commit()
                        cons.close()
                    except Exception as e:
                        self.show_error(e)
                        cons.close()
                    else:
                        self.item_value.delete(0,"end")
                        self.price_value.delete(0,"end")
                        self.date_value.delete(0,"end")
                        self.quantity_value.delete(0,"end")
                        self.tree_frame.destroy()
                        self.treefunction()
    def destroy(self):
        super().destroy()
    def destroy_event(self,event):
        super().destroy()
    def savedata(self,event):
        item=self.item_value.get()
        price=self.price_value.get()
        date=self.date_value.get()
        quantity=self.quantity_value.get()
        if item=="" or price=="" or date=="" or quantity=="":
            self.show_error("No field can be empty")
        else:
            for i in price:
                if i in string.ascii_letters:
                    self.show_error("string in price is not allowed")
                    break
            else:
                price=float(price)
                cons=sqlite3.connect("Bill_data/"+month_name+str(year)+".db")
                cursor=cons.cursor()
                query="select * from buget"
                cursor.execute(query)
                lst=cursor.fetchall()
                lst2=lst[0][0]
                if lst2==0:
                    self.show_error("first enter a buget")
                    self.item_value.delete(0,"end")
                    self.price_value.delete(0,"end")
                    self.date_value.delete(0,"end")
                    self.quantity_value.delete(0,"end")
                    return
                else:
                    lst2=lst2-price
                if lst2 <0:
                        self.show_error("your buget has gone negative, Can't do transaction")
                        self.bugget_label.destroy()
                        self.bugget_label=ctk.CTkLabel(self.bugget_frame,text=lst[0][0],font=("bold",30))
                        self.bugget_label.place(x=0,y=0)
                        self.item_value.delete(0,"end")
                        self.price_value.delete(0,"end")
                        self.date_value.delete(0,"end")
                        self.quantity_value.delete(0,"end")
                        self.bugget_label.bind("<Double-Button-1>",self.buggetedit)
                else:
                    query="update buget set Amount=?"
                    cursor.execute(query,(lst2,))
                    self.bugget_label.destroy()
                    self.bugget_label=ctk.CTkLabel(self.bugget_frame,text=lst2,font=("bold",30))
                    self.bugget_label.place(x=0,y=0)
                    self.bugget_label.bind("<Double-Button-1>",self.buggetedit)
                    query="insert into data(item,price,date,quantity) values (?,?,?,?)"
                    values=(item,price,date,quantity)
                    try:
                        cursor.execute(query,values)
                        cons.commit()
                        cons.close()
                    except Exception as e:
                        self.show_error(e)
                        cons.close()
                    else:
                        self.item_value.delete(0,"end")
                        self.price_value.delete(0,"end")
                        self.date_value.delete(0,"end")
                        self.quantity_value.delete(0,"end")
                        self.tree_frame.destroy()
                        self.treefunction()
    def clearentry(self,event):
        self.item_value.delete(0,"end")
        self.price_value.delete(0,"end")
        self.date_value.delete(0,"end")
        self.quantity_value.delete(0,"end")
    def buggetedit(self,event):
        label_text=self.bugget_label.cget("text")
        self.bugget_label.destroy()
        self.bugget_entry=ctk.CTkEntry(self.bugget_frame,font=("Bold",30),width=200,height=50)
        self.bugget_entry.insert(0,label_text)
        self.bugget_entry.place(x=0,y=0)
        self.bugget_entry.bind("<Control-s>",self.buggetsave)
    def buggetsave(self,event):
        label_text=self.bugget_entry.get()
        self.bugget_entry.destroy()
        self.bugget_label=ctk.CTkLabel(self.bugget_frame,text=label_text,font=("bold",30))
        self.bugget_label.place(x=0,y=0)
        cons=sqlite3.connect("Bill_data/"+month_name+str(year)+".db")
        cursor=cons.cursor()
        try:
            query="update buget set Amount=?"
            values=(float(label_text),)
            cursor.execute(query,values)
            cons.commit()
            cons.close()
        except Exception as e:
            self.show_error(e)
            cons.close()
        self.bugget_label.bind("<Double-Button-1>",self.buggetedit)
monthbill=MonthBill(month_name)
monthbill.mainloop()