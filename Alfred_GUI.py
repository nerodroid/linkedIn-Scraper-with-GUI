
from tkinter import *
from tkinter import scrolledtext
import pandas as pd
import json
import re
import time

from Alfred_linkedin import *
import Alfred_linkedin as alf
import linkedin_people_search as lps
import Alfred_linkedin_people as alp

import tkinter as tk
from tkinter import ttk
from tkinter import *

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.var = IntVar()
        self.title("LinkedIn Scraper")
        
        self.btn1=Radiobutton(self, text='Personal', variable=self.var, value=1).grid(sticky=W) 
        self.btn2=Radiobutton(self, text='Company', variable=self.var, value=2).grid(row=0,column=0)
        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")
        self.label_username.grid(row=3, sticky=W)
        self.label_password.grid(row=4, sticky=W)
        self.entry_username.grid(row=3, column=0)
        self.entry_password.grid(row=4, column=0)
        
        self.scrollbar = Scrollbar(self) 
        #self.scrollbar.pack( side = RIGHT, fill = Y ) 
        self.scrollbar.grid(row=8, column=1,rowspan=2, sticky=N+S+W)
        self.mylist = Text(self, yscrollcommand = self.scrollbar.set ) 

        #textBox=Text(root, height=2, width=10)
        self.mylist.grid(row=8,column=0)
        #niranga.fb@gmail.com
        #0714076576 
        Label(self, text="Account Type").grid(row=1,sticky=W)#pack(padx=1,pady=0,fill=Y)
        Label(self, text="Search Type").grid(row=2,sticky=W)
        self.acctype = StringVar(self)
        self.setype=StringVar(self)
        self.setype.set('Search')
        self.acctype.set('Sales Navigator')
        self.account=['Sales Navigator','Normal']
        self.searchtype=['Input','Search']
        self.acc=OptionMenu(self,self.acctype,*self.account)
        self.stype=OptionMenu(self,self.setype,*self.searchtype)
        self.acc.grid(row=1,column=0)
        self.stype.grid(row=2,column=0)
        Label(self, text="Location").grid(row=5,sticky=W)#pack(padx=1,pady=0,filmylistl=Y)
        
        self.away_var = StringVar(self)
        self.home_var = StringVar(self)
        self.ind_var = StringVar(self)
        self.away_var.set('Romania')
        self.home_var.set('Manager')
        self.ind_var.set('Accounting')
        self.countries=pd.read_json("Countries.json")
        self.Location = self.countries['Country Name'].values
        self.e = OptionMenu(self, self.away_var, *self.Location)
        self.e.grid(row=5, column=0)
        #self.e.pack(padx=1,pady=1)
        
        Label(self, text="Industry").grid(row=6,sticky=W)#pack(padx=5,pady=5,fill=Y)
        self.industries=pd.read_json("Industries.json")
        self.industry=self.industries['Industry Name'].values
        self.ind = OptionMenu(self, self.ind_var, *self.industry)
        #self.e1.grid(row=1, column=1)
        self.ind.grid(row=2,column=0)
        
        Label(self, text="Designation").grid(row=7,sticky=W)#pack(padx=5,pady=5,fill=Y)
        self.Designation=["officer","VP","manager","director","chief","head"]
        self.des = OptionMenu(self, self.home_var, *self.Designation)
        #self.e1.grid(row=1, column=1)
        self.des.grid(row=7,column=0)
        
        self.buttonCommit=ttk.Button(self, width=10, text="Submit", command=lambda: self.retrieve_input())
        self.buttonCommit.grid()
        
        self.button = ttk.Button(text="start", command=self.start)
        self.button.grid()
        
        self.progress = ttk.Progressbar(self, orient="horizontal",length=200, mode="determinate")
        self.progress.grid()

        self.bytes = 0
        self.maxbytes = 0
        self.bytes = 0
        self.maxbytes = 0

    def start(self):
        self.progress["value"] = 0
        self.maxbytes = len(self.inputValue.split('\n'))#50000 #len(inputs)
        self.progress["maximum"] = len(self.inputValue.split('\n'))
        self.account_type=self.away_var.get()
        #print(self.desig)
        
        self.read_bytes()
        
    def retrieve_input(self):
        self.inputValue=self.mylist.get("1.0","end").strip()

        self.rad_type=self.var.get()
        print(self.rad_type)

        self.username=self.entry_username.get()
        self.passwd=self.entry_password.get()
        self.loc_=self.away_var.get()
        self.loc=self.countries.loc[self.countries['Country Name'] == self.loc_]['Country Value'].values[0]
        #print( " loc is "+self.loc)
        self.industry_type=self.ind_var.get()
        self.desig=self.home_var.get()
        self.account_type=self.acctype.get()
        self.industry_val=self.industries.loc[self.industries['Industry Name'] == self.industry_type]['Industry Value'].values[0]
        #niranga.fb@gmail.com
        #0714076576

        self.search_type=self.setype.get()
        if self.account_type == "Normal":
            self.limit=100
        else:
            self.limit=1000
        
        if self.rad_type ==2 and self.search_type == 'Input':
            if self.account_type == "Normal":
                for self.current in range(len(self.inputValue.split('\n'))):
                    alf.main_func(self.username,self.passwd,self.loc,self.desig,self.inputValue[                                    self.current:self.current+100])
                    print("sleeping.........")
                    self.current+=100
                    time.sleep(36000)
            else:
                alf.main_func(self.username,self.passwd,self.loc,self.desig,self.inputValue)

        elif self.rad_type == 1 and self.search_type == 'Search':
            print("Searching profiles")
            
            lps.main_func(self.username,self.passwd,self.loc,self.inputValue.strip(),self.industry_val)
        elif self.rad_type == 1 and self.search_type == 'Input':
            alp.main_func(self.inputValue,self.username,self.passwd)
    def read_bytes(self):        
        self.bytes += 1
        self.progress["value"] = self.bytes
        if self.bytes < self.maxbytes:
            # read more bytes after 100 ms
            self.after(100, self.read_bytes)
    
app = SampleApp()
app.mainloop()
