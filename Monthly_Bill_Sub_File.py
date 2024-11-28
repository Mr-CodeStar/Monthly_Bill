from datetime import datetime
import customtkinter as ctk
import os
import sqlite3
from tkinter import messagebox,ttk

class PreviousMonthBill(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Monthly-Bills")
        self.minsize(1300,700)
        self.maxsize(1300,700)
        #################################### Month Name#######################################
        self.month_name=ctk.CTkLabel(self,text="Month:-",font=("bold",30))
        self.month_name.place(x=10,y=28)
        self.month_value=ctk.CTkEntry(self,width=315,height=30,font=("Bod",40))
        self.month_value.place(x=150,y=20)
        self.bind("<Return>",self.Display)
    def Display(self,event):
        monthname=self.month_value.get()
        self.current_date=datetime.now()
        self.month__name=self.current_date.strftime("%B")
        self.year=self.current_date.strftime("%Y")
        if os.path.exists("Bill_data/"+monthname+".db"):
            if monthname!=(self.month__name+str(self.year)):
                self.month_value.destroy()
                self.month_name.destroy()
                self.month_name=ctk.CTkLabel(self,text=monthname,font=("bold",30))
                self.month_name.place(x=570,y=28)
                distree=ttk.Treeview(self,columns=("Item","Price","Date","Quantity"),show="headings",height=25)
                style = ttk.Style()
                style.configure("Treeview",
                        background="#2B2B2B",
                        foreground="white",
                        fieldbackground="#2B2B2B",
                        font=('Arial', 12))
                distree.heading("Price",text="Price")
                distree.heading("Item",text="Item")
                distree.heading("Date",text="Date")
                distree.heading("Quantity",text="Quantity")
                distree.column("Item",anchor="center",width=320)
                distree.column("Price",anchor="center",width=320)
                distree.column("Date",anchor="center",width=320)
                distree.column("Quantity",anchor="center",width=320)
                cons=sqlite3.connect("Bill_data/October2024.db")
                cursor=cons.cursor()
                cursor.execute("select * from data")
                data=cursor.fetchall()
                for item in data:
                    distree.insert("", "end", values=item)
                distree.place(x=10,y=100)
                cons.close()
            else:
                messagebox.showerror(title="Error",message="The Month is currently present in the main window so can't open it from here")
                self.month_value.delete(0,"end")
        else:
            messagebox.showerror(title="Error",message="No such Monthly-Buget exist")
            self.destroy()
obj=PreviousMonthBill()
obj.mainloop()