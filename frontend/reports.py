from tkinter import  constants as con  , ttk , messagebox as msg , StringVar , IntVar
from requests import get 
from other_classes import base_window , image_viewer
from datetime import timedelta,datetime as date
from math import ceil
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Spacer,Paragraph
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from webbrowser import open as edge
import os
import tkinter as tk
import traceback
import datetime



class return_reports(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations,others , return_report_form):
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , return_report_form)
        
        if base == None:
            return
        self.year = others[3]
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.ip = others[0]

        start_year = 2021                                       
        cur_year = int(date.today().strftime("%Y"))
        cur_mon = int(date.today().strftime("%m"))
        if cur_mon<4:
            end_year = cur_year
        else:
            end_year = cur_year+1
        fin_years = []                                     #all financial year record available

        for i in range(start_year , end_year):
            fin_years.append(str(i)+"-"+str(i+1)[2:])
        fin_years.reverse()

        self.lbl_firms = ttk.Label(self.main_frame , text = "Firm      :" , style = "window_text_medium.TLabel")
        self.combo_firms = ttk.Combobox(self.main_frame , validate="key", values = ['SOMANATH STORES' , 'SOMANATH ENTERPRISES'] , state = "readonly" , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30 , style = "window_combo.TCombobox") 
        self.combo_firms.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_year = ttk.Label(self.main_frame , text = "Year      :" , style = "window_text_medium.TLabel")
        self.combo_year = ttk.Combobox(self.main_frame , validate="key", values = fin_years , state = "readonly" , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30 , style = "window_combo.TCombobox") 
        self.combo_year.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_quarter = ttk.Label(self.main_frame , text = "Quarter   :"  ,style = "window_text_medium.TLabel")
        self.combo_quarter = ttk.Combobox(self.main_frame , validate="key",values = ['1st - APRIL-JUNE' , '2nd - JULY-SEPTEMBER' , '3rd - OCTOBER-DECEMBER' , '4th - JANUARY-MARCH'] , state = "readonly" , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30 , style = "window_combo.TCombobox") 
        self.combo_quarter.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_quarter.bind("<<ComboboxSelected>>" , self.filter_months)

        self.lbl_month = ttk.Label(self.main_frame , text = "Month     :"  ,style = "window_text_medium.TLabel")
        self.combo_month = ttk.Combobox(self.main_frame , validate="key",values = ['APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER' ,'JANUARY','FEBRUARY','MARCH'] , state = "readonly" , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30 , style = "window_combo.TCombobox") 
        self.combo_month.bind("<FocusOut>" , self.combo_entry_out)

        self.btn_sales = ttk.Button(self.main_frame , text = "Sales Report" , width = 18 , style = "window_btn_medium.TButton" ,command = lambda : self.sales(None))
        self.btn_sales.bind("<Return>" , self.sales)

        self.btn_purchase = ttk.Button(self.main_frame , text = "Purchase Report" , width = 18 , style = "window_btn_medium.TButton" ,command = lambda : self.purchase(None))
        self.btn_purchase.bind("<Return>" , self.purchase)

        self.lbl_cust = ttk.Label(self.main_frame , text = "Customer  :" , style = "window_text_medium.TLabel")
        self.combo_cust = ttk.Combobox(self.main_frame , validate="key", validatecommand=(validations[0], '%P') , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30 , style = "window_combo.TCombobox") 
        self.combo_cust.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_cust.bind("<Down>" , self.get_customers)
        self.combo_cust.bind("<Button-1>" , self.get_customers)

        self.btn_mntly_report = ttk.Button(self.main_frame , text = "Monthly Sales Report" , width = 24 , style = "window_btn_medium.TButton" ,command = lambda : self.monthly(None))
        self.btn_mntly_report.bind("<Return>" , self.monthly)

        self.btn_gstr04 = ttk.Button(self.main_frame , text = "GSTR04 Annual Report" , width = 24 , style = "window_btn_medium.TButton" ,command = lambda : self.gstr04(None))
        self.btn_gstr04.bind("<Return>" , self.gstr04)


        self.lbl_firms.grid(row = 0 , column = 0 , pady = int(self.main_hgt * 0.03) , padx = int(self.main_wdt * 0.03))
        self.combo_firms.grid(row = 0 , column = 1)
        self.lbl_year.grid(row = 1 , column = 0, pady = int(self.main_hgt * 0.03), padx = int(self.main_wdt * 0.03))
        self.combo_year.grid(row = 1 , column = 1)
        self.lbl_quarter.grid(row = 2 , column = 0, pady = int(self.main_hgt * 0.03), padx = int(self.main_wdt * 0.03))
        self.combo_quarter.grid(row = 2 , column = 1)
        self.lbl_month.grid(row = 3 , column = 0, pady = int(self.main_hgt * 0.03), padx = int(self.main_wdt * 0.03))
        self.combo_month.grid(row = 3 , column = 1)
        self.btn_sales.grid(row = 4 , column = 1)
        self.btn_purchase.grid(row = 5 , column = 1)
        self.lbl_cust.grid(row = 6 , column = 0, pady = int(self.main_hgt * 0.03), padx = int(self.main_wdt * 0.03))
        self.combo_cust.grid(row = 6 , column = 1)
        self.btn_mntly_report.grid(row = 7 , column = 1)
        self.btn_gstr04.grid(row = 8 , column = 1 , pady = self.main_hgt*0.05)

    def combo_entry_out(self , e):
        e.widget.select_clear()

    def filter_months(self , e):
       
        quarter = self.combo_quarter.get()

        if quarter == '1st - APRIL-JUNE': 
            values = ['APRIL','MAY','JUNE']
        elif quarter == '2nd - JULY-SEPTEMBER':
            values = ['JULY','AUGUST','SEPTEMBER']
        elif quarter == '3rd - OCTOBER-DECEMBER':
            values = ['OCTOBER','NOVEMBER','DECEMBER' ]
        else:
            values = ['JANUARY','FEBRUARY','MARCH']

        self.combo_month.config(values = values , state = con.NORMAL)
        self.combo_month.delete(0 , con.END)
        self.combo_month.insert(0 , values[0])
        self.combo_month.config(state = "readonly")

    def sales(self , e):
        firm = self.combo_firms.get()
        year = self.combo_year.get()
        quarter = self.combo_quarter.get()
        month = self.combo_month.get()

        if firm == '':
            msg.showinfo('Info' , 'Select Firm')
            self.combo_firms.focus_set()
            return
        if year == '':
            msg.showinfo('Info' , 'Select Financial Year')
            self.combo_year.focus_set()
            return

        if quarter == '' and month =='':
            msg.showinfo('Info' , 'Select Month or Quarter')
            self.combo_quarter.focus_set()
            return
        if firm == 'SOMANATH STORES':
            firm = 'SSM'
            monthList = ['APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER' ,'JANUARY','FEBRUARY','MARCH']
            nextMonth = monthList.index(month)+1
            year_Date = year[2:4]
            if nextMonth > 9:
                year_Date = year[-2:]
            if nextMonth == 12:
                nextMonth = 0
            nextMonth = monthList[nextMonth]
            lastDay = (str(date.strptime("20"+str(year_Date)+"-"+nextMonth+"-05",'%Y-%B-%d').replace(day=1) - timedelta(days=1))).split(" ")[0]
            firstDay = lastDay[:-2]+"01"
            
            req = get("http://"+self.ip+":7000/SalesReport",params= {'firm':firm,'dbYear':year[2:4],'firstDay':firstDay,'lastDay':lastDay,'month':month} )
            
            if req.status_code== 201:
                msg.showinfo("No Data","No sales for selected data")
            else:
                msg.showinfo("Sucess","Sales Excel will be ready in few minutes")
                self.btn_sales.config(state=con.DISABLED)
        else:
            if quarter == '1st - APRIL-JUNE':
                firstDay = '20'+str(year[2:4])+"-04-01"
                lastDay = '20'+str(year[2:4])+"-06-30"
            elif quarter == '2nd - JULY-SEPTEMBER':
                firstDay = '20'+str(year[2:4])+"-07-01"
                lastDay = '20'+str(year[2:4])+"-09-30"
            elif quarter == '3rd - OCTOBER-DECEMBER':
                firstDay = '20'+str(year[2:4])+"-10-01"
                lastDay = '20'+str(year[2:4])+"-12-31"
            else :
                firstDay = '20'+str(year[2:4])+"-01-01"
                lastDay = '20'+str(year[2:4])+"-03-31"
            req = get("http://"+self.ip+":7000/cmp08",params= {'dbYear':year[2:4],'firstDay':firstDay,'lastDay':lastDay,'quarter':quarter} )
            
            if req.status_code== 201:
                msg.showinfo("No Data","No sales for selected data")
            else:
                msg.showinfo("Sucess","Sales Text will be ready in few minutes")
                self.btn_sales.config(state=con.DISABLED)

    def purchase(self , e):
        firm = self.combo_firms.get()
        year = self.combo_year.get()
        quarter = self.combo_quarter.get()
        month = self.combo_month.get()

        if firm == '':
            msg.showinfo('Info' , 'Select Firm')
            self.combo_firms.focus_set()
            return
        if year == '':
            msg.showinfo('Info' , 'Select Financial Year')
            self.combo_year.focus_set()
            return

        if quarter == '' and month =='':
            msg.showinfo('Info' , 'Select Month or Quarter')
            self.combo_quarter.focus_set()
            return
        if firm == 'SOMANATH STORES':
            firm = 1
        else:
            firm = 3
        
        monthList = ['APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER' ,'JANUARY','FEBRUARY','MARCH']
        nextMonth = monthList.index(month)+1
        year_Date = year[2:4]
        if nextMonth > 9:
            year_Date = year[-2:]
        if nextMonth == 12:
            nextMonth = 0
        nextMonth = monthList[nextMonth]
        lastDay = (str(date.strptime("20"+str(year_Date)+"-"+nextMonth+"-05",'%Y-%B-%d').replace(day=1) - timedelta(days=1))).split(" ")[0]
        firstDay = lastDay[:-2]+"01"
        if month == 'APRIL':
            firstDay = str(int(year[2:4])-1)+"-03-01"
        
        req = get("http://"+self.ip+":7000/PurchaseReport" , params= {'firm':firm,'dbYear':year[2:4],'year':year,'firstDay':firstDay,'lastDay':lastDay,'month':month})
        if req.status_code== 201:
            msg.showinfo("No Data","No purchase for selected data")
        else:
            msg.showinfo("Sucess","Purchase Excel will be ready in few minutes")
            self.btn_purchase.config(state=con.DISABLED)

    def get_customers(self,e):

        text = e.widget.get()
        
        if text == "":
            sql = "select acc_name from somanath.accounts where acc_type = 'CUST' order by acc_name"
        else:
            sql = "select acc_name from somanath.accounts where acc_type = 'CUST' and acc_name regexp '"+text+"' order by acc_name"

        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            resp = req.json()
            values = []
            for each in resp:
                values.append(each['acc_name'])

            e.widget.config(values = values)

    def monthly(self , e):

        year = self.combo_year.get()
        quarter = self.combo_quarter.get()
        month = self.combo_month.get()
        acc_name = self.combo_cust.get()


        if year == '':
            msg.showinfo('Info' , 'Select Financial Year')
            self.combo_year.focus_set()
            return

        if quarter == '' and month =='':
            msg.showinfo('Info' , 'Select Month or Quarter')
            self.combo_quarter.focus_set()
            return

        if acc_name == '':
            msg.showinfo('Info' , 'Select Customer from drop down')
            self.combo_cust.select_range(0,con.END)
            self.combo_cust.focus_set()
            return

        sql = "select acc_id from somanath.accounts where acc_name = '"+acc_name+"'"

        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        acc_id = req.json()
        if acc_id == []:
            msg.showinfo('Info' , 'Select Customer from drop down')
            self.combo_cust.focus_set()
            self.combo_cust.select_range(0,con.END)
            return


        acc_id = acc_id[0]['acc_id']



        monthList = ['APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER' ,'JANUARY','FEBRUARY','MARCH']
        nextMonth = monthList.index(month)+1
        year_Date = year[2:4]
        if nextMonth > 9:
            year_Date = year[-2:]
        if nextMonth == 12:
            nextMonth = 0
        nextMonth = monthList[nextMonth]
        lastDay = (str(date.strptime("20"+str(year_Date)+"-"+nextMonth+"-05",'%Y-%B-%d').replace(day=1) - timedelta(days=1))).split(" ")[0]
        firstDay = lastDay[:-2]+"01"
        if month == 'APRIL':
            firstDay = str(int(year[2:4])-1)+"-03-01"



        acc_name = acc_name.title()
       
        
        
        req1 = get("http://"+self.ip+":6000/onlySql", params={"sql" : 'SELECT count(sales_id) as count  FROM somanath20'+str(year[2:4])+'.sales where sales_acc ='+str(acc_id)+' and sale_date >= "'+firstDay+'" and sale_date <="'+lastDay+'"' })
        count = req1.json()[0]['count'] 
        if count == 0:
            msg.showinfo('Info' , 'Select Sales Found')
            return
        req = get("http://"+self.ip+":6000/reports/getMontlyReport" , 
            params = { "acc_id" : acc_id , "limit" : count ,'sdate' :firstDay,'edate' :lastDay,
                        'invNo' : '' ,'db' : year[2:4] }) 
        
        values = [] 
        total = 0
        for each in req.json():
            x = req.json()[each]
            total += float(x[0][2])
            values.append([x[1],x[0][0],x[0][1],x[0][2]])
        values.sort(key=lambda x: x[0])
        fileName=os.path.expanduser('~')+"\\Desktop\\Invoices\\MonthlyReport.pdf"
        data = [['Product Name', 'Price', 'Qty', 'Value']]
        for each in values:
            data.append(each)
        
        pdf = SimpleDocTemplate(fileName,pagesize=A4,rightMargin=20*mm, leftMargin=20*mm, topMargin=2*mm, bottomMargin=0)

        table = Table(data)
    
        style = TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.green),
            ('TEXTCOLOR',(0,0),(-1,0),colors.white),
            ('FONTNAME',(0,0),(-1,0),'Times-Bold'),
            ('ALIGN',(0,0),(-1,0),'LEFT'),
            ('ALIGN',(0,0),(1,-1),'LEFT'),
            ('ALIGN',(1,1),(-1,-1),'RIGHT'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTNAME',(0,0),(-1,-1),'Helvetica'),
            ('FONTSIZE',(0,1),(0,-1),12),
            ('FONTSIZE',(1,1),(-1,-1),10),
            ('FONTSIZE',(0,0),(-1,0),12),
            ('BOTTOMPADDING',(0,0),(-1,0),6),
            ('BACKGROUND',(0,1),(-1,-1),colors.beige),
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ])

        table.setStyle(style)

        rowNumb = len(data)
        for i in range(1, rowNumb):
            ts = TableStyle([('BACKGROUND',(0,i),(-1,i),colors.white)])
            table.setStyle(ts)
        elems = []

        elems.append(Paragraph("<font size=13>Sales Report "+month+"</font>",getSampleStyleSheet()['Title']))
        elems.append(Spacer(0,-10))
        elems.append(table)
        elems.append(Spacer(0,5))
        elems.append(Paragraph("<font size=10>Total Amount: Rs." +str("{:.00f}".format(ceil(total)))+"</font>",getSampleStyleSheet()['Title']))
        elems.append(Spacer(0,-10))
        elems.append(Paragraph("<font size=15><i>"+acc_name+"</i></font>",getSampleStyleSheet()['Title']))
    
        pdf.build(elems)
        homedir = os.path.expanduser("~").split('\\')[-1]
        edge(r"C:\\Users\\"+homedir+"\\Desktop\\Invoices\\MonthlyReport.pdf")

    def gstr04(self , e):
        year = self.combo_year.get()
        if year == '':
            msg.showinfo('Info' , 'Select Financial Year')
            self.combo_year.focus_set()
            return
        get("http://"+self.ip+":7000/gstr04" , params = {'dbYear' : year[2:4]})
        msg.showinfo("Sucess","GSTR4 Excel will be ready in few minutes")
        
      

class purchase_cashflow(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations,others , return_report_form):
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , return_report_form)
        
        if base == None:
            return
        self.year = others[3]
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.ip = others[0]
        self.year = others[3]

        self.screen_height = root.winfo_screenheight()


        self.lbl_supplier = ttk.Label(self.main_frame , text = " Name :" , style = "window_text_medium.TLabel")
        self.combo_supplier = ttk.Combobox(self.main_frame , validate="key", validatecommand=(validations[0], '%P') , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 38 , style = "window_combo.TCombobox") 
        self.combo_supplier.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_supplier.bind("<Down>" , self.get_suppliers)
        self.combo_supplier.bind("<Button-1>" , self.get_suppliers)


        self.lbl_from_cashflow = ttk.Label(self.main_frame , text = " From :" , style = "window_text_medium.TLabel")
        self.ent_from_cashflow = ttk.Entry(self.main_frame  , width = 10 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_from_cashflow.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_to_cashflow = ttk.Label(self.main_frame , text = " To   :" , style = "window_text_medium.TLabel")
        self.ent_to_cashflow = ttk.Entry(self.main_frame  , width = 10,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_to_cashflow.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_limit_cashflow = ttk.Label(self.main_frame , text = " Last :" , style = "window_text_medium.TLabel")
        self.ent_limit_cashflow = ttk.Entry(self.main_frame  , width = 10 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[2], '%P'))
        self.ent_limit_cashflow.bind("<FocusOut>" , self.combo_entry_out)

        self.btn_get_cashflow = ttk.Button(self.main_frame , text = "Get Reports" , width = 12 , style = "window_btn_medium.TButton" ,command = lambda : self.get_cashflow(None) )
        self.btn_get_cashflow.bind("<Return>" , self.get_cashflow)



        #if self.screen_height > 1000 : 
        self.frm_tree_cashflow = ttk.Frame(self.main_frame , width = self.main_wdt*0.537 , height = int(self.main_hgt*0.65))
        #else:self.frm_tree_cashflow = ttk.Frame(self.main_frame , width = self.main_wdt*0.4-16 , height = int(self.main_hgt*0.65))
        self.frm_tree_cashflow.pack_propagate(False)
        self.tree_cashflow = ttk.Treeview(self.frm_tree_cashflow ,selectmode = "browse", takefocus = True , show = "headings" , style = "window.Treeview" , height = 6)
        self.tree_cashflow.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree_cashflow.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.scroll_y_cashflow = ttk.Scrollbar(self.frm_tree_cashflow , orient = con.VERTICAL , command = self.tree_cashflow.yview)
        self.scroll_x_cashflow = ttk.Scrollbar(self.frm_tree_cashflow , orient = con.HORIZONTAL , command = self.tree_cashflow.xview)
        self.tree_cashflow.config(yscrollcommand = self.scroll_y_cashflow.set , xscrollcommand = self.scroll_x_cashflow.set)

        self.tree_cashflow['columns'] = ( 'date','billno','billamt','amtpaid','mode')

        self.tree_cashflow.heading('date' , text = 'DATE')
        self.tree_cashflow.heading('billno' , text = 'BNO')
        self.tree_cashflow.heading('billamt' , text = 'AMT')
        self.tree_cashflow.heading('amtpaid' , text = 'PAID')
        self.tree_cashflow.heading('mode' , text = 'MODE')
    
        self.tree_cashflow_wdt = self.tree_cashflow.winfo_reqwidth()-self.scroll_y_cashflow.winfo_reqwidth()

        
        """if self.screen_height > 1000:
            self.tree_cashflow.column('date' , width = int(self.tree_cashflow_wdt*0.145)  , anchor = "w")
            self.tree_cashflow.column('billno' , width = int(self.tree_cashflow_wdt*0.1)  , anchor = "center")
            self.tree_cashflow.column('billamt' , width = int(self.tree_cashflow_wdt*0.16)  , anchor = "e")
            self.tree_cashflow.column('amtpaid' , width = int(self.tree_cashflow_wdt*0.16) , anchor = "e")
            self.tree_cashflow.column('mode' , width = int(self.tree_cashflow_wdt*0.16)   , anchor = "e")
        
        else:"""
        self.tree_cashflow.column('date' , width = int(self.tree_cashflow_wdt*0.2)  , anchor = "w")
        self.tree_cashflow.column('billno' , width = int(self.tree_cashflow_wdt*0.2)  , anchor = "center")
        self.tree_cashflow.column('billamt' , width = int(self.tree_cashflow_wdt*0.2)  , anchor = "e")
        self.tree_cashflow.column('amtpaid' , width = int(self.tree_cashflow_wdt*0.2) , anchor = "e")
        self.tree_cashflow.column('mode' , width = int(self.tree_cashflow_wdt*0.2)   , anchor = "e")



        self.scroll_y_cashflow.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x_cashflow.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        self.tree_cashflow.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)



        self.lbl_supplier.grid(row = 0 , column = 0 , pady = int(self.main_hgt*0.01))
        self.combo_supplier.grid(row = 0 , column = 1 , columnspan = 5 , sticky= con.W )

        self.lbl_from_cashflow.grid(row = 1 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_from_cashflow.grid(row = 1 , column = 1 , sticky= con.W )

        self.lbl_to_cashflow.grid(row = 2 , column = 0)
        self.ent_to_cashflow.grid(row = 2 , column = 1 , sticky= con.W)

        self.lbl_limit_cashflow.grid(row = 3 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_limit_cashflow.grid(row = 3 , column = 1 , sticky= con.W)

        self.btn_get_cashflow.grid(row = 4 , column = 1 , sticky = con.W , columnspan = 2)

        self.frm_tree_cashflow.grid(row = 5 , column = 0 , columnspan = 5 , padx = int(self.main_wdt *0.1))

    def get_suppliers(self,e):
        
        text = e.widget.get()
        if text == "":
            sql = "select acc_name from somanath.accounts where acc_type = 'SUPP' order by acc_name"
        else:
            sql = "select acc_name from somanath.accounts where acc_type = 'SUPP' and acc_name regexp '"+text+"' order by acc_name"

        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            resp = req.json()
            values = []
            for each in resp:
                values.append(each['acc_name'])

            e.widget.config(values = values)

    def combo_entry_out(self , e):
        e.widget.select_clear()

    def get_cashflow(self , e):
        child = self.tree_cashflow.get_children()
        for each in child:
            self.tree_cashflow.delete(each)

        sup_name = self.combo_supplier.get()
        limit = self.ent_limit_cashflow.get()
        
        if sup_name == "":
            msg.showerror("Error" , "Select Supplier")
            self.combo_supplier.select_range(0,con.END)
            self.combo_supplier.focus_set()
            return

        if sup_name!= "":
            if sup_name not in self.combo_supplier['values']:
                msg.showerror("Error" , "Select Name from the list")
                self.combo_supplier.select_range(0,con.END)
                self.combo_supplier.focus_set()
                return

        from_date = self.ent_from_cashflow.get()
        to_date = self.ent_to_cashflow.get()


        if limit == "":
            date1 = from_date.split("/")
            if len(date1)!=3:
                date1 = from_date.split("-")
                if len(date1) != 3:
                    msg.showinfo("Info" , "Enter date in following format \n 'dd-mm-yy' or 'dd/mm/yy ")
                    self.ent_from_cashflow.delete(0,con.END)
                    self.ent_from_cashflow.focus_set()
                    return

            try:
                date(int(date1[2]), int(date1[1]), int(date1[0]))
            except ValueError:
                msg.showinfo("Info" , "Enter correct date")
                self.ent_from_cashflow.delete(0,con.END)
                self.ent_from_cashflow.focus_set()
                return

            
            if len(date1[2])%2 !=0 :
                msg.showinfo("Info" , "Enter correct date")
                self.ent_from_cashflow.delete(0,con.END)
                self.ent_from_cashflow.focus_set()
                return

            if len(date1[0]) == 1:
                date1[0] = '0' + date1[0]

            if len(date1[1]) == 1:
                date1[1] = '0' + date1[1]    

            if len(date1[2]) == 2:
                date1[2] = '20' + date1[2]    

            
            self.ent_from_cashflow.delete(0,con.END)
            self.ent_from_cashflow.insert(0,date1[0] + "-" + date1[1] + "-" + date1[2])        
            self.ent_from_cashflow.select_clear()
            from_date = date1[2] + "-" + date1[1] + "-" + date1[0]





        sql = "select acc_id from somanath.accounts where acc_name = '"+sup_name+"'"

        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        acc_id = req.json()
        if acc_id == []:
            msg.showinfo('Info' , 'Select Supplier from drop down')
            self.combo_supplier.focus_set()
            self.combo_supplier.select_range(0,con.END)
            return


        if to_date != "":
            date1 = to_date.split("/")
            if len(date1)!=3:
                date1 = to_date.split("-")
                if len(date1) != 3:
                    msg.showinfo("Info" , "Enter date in following format \n 'dd-mm-yy' or 'dd/mm/yy ")
                    self.ent_to_cashflow.delete(0,con.END)
                    self.ent_to_cashflow.focus_set()
                    return

            try:
                date(int(date1[2]), int(date1[1]), int(date1[0]))
            except ValueError:
                msg.showinfo("Info" , "Enter correct date")
                self.ent_to_cashflow.delete(0,con.END)
                self.ent_to_cashflow.focus_set()
                return

            
            if len(date1[2])%2 !=0 :
                msg.showinfo("Info" , "Enter correct date")
                self.ent_to_cashflow.delete(0,con.END)
                self.ent_to_cashflow.focus_set()
                return

            if len(date1[0]) == 1:
                date1[0] = '0' + date1[0]

            if len(date1[1]) == 1:
                date1[1] = '0' + date1[1]    

            if len(date1[2]) == 2:
                date1[2] = '20' + date1[2]    

            
            self.ent_to_cashflow.delete(0,con.END)
            self.ent_to_cashflow.insert(0,date1[0] + "-" + date1[1] + "-" + date1[2])        
            self.ent_to_cashflow.select_clear()

            to_date = date1[2] + "-" + date1[1] + "-" + date1[0]




        if limit != "":
            from_date = ''
            to_date = '' 
        else:
            limit = 10000000
             
        

        req = get("http://"+self.ip+":6000/reports/getCashflowPurchase" , params = { "acc_id" : acc_id[0]['acc_id'] , "limit" : limit ,'sdate' :from_date,'edate' :to_date,'invNo' : '' ,'db' : self.year })
        data = req.json()

        i = 0
        for each in data:
            tags = 'b'
            if i%2 == 0:
                tags = 'a'
            pur_id =  each['trans_pur']
            if pur_id == None:
                pur_id = "-"
            else:
                pur_id = pur_id.split("_")[1]

            trans_amt = each['trans_amt']
            if trans_amt == None:
                trans_amt = '-'
            else:
                trans_amt = "{:.2f}".format(round(float(each['trans_amt']),2))

            

            self.tree_cashflow.insert('','end',tags=(tags ), values = [each['transdate'], pur_id, trans_amt ,  "{:.2f}".format(round(float(each['amt_paid']),2))  , each['trans_mode']])
            i +=1




class customer_balance(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,others , customer_balance_report_form):
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , customer_balance_report_form)
        
        if base == None:
            return
        self.year = others[3]
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.ip = others[0]
        self.year = others[3]
        self.screen_height = root.winfo_screenheight()

        self.lbl_total_bal_text = ttk.Label(self.main_frame , text = "Total Balance : " , style = "window_text_medium.TLabel")
        self.lbl_total_bal = ttk.Label(self.main_frame   , width = 18 , style = "window_lbl_ent.TLabel" ,   justify = con.RIGHT)



        self.frm_tree_custbal = ttk.Frame(self.main_frame , width = self.main_wdt*0.7 , height = int(self.main_hgt*0.774))
        self.frm_tree_custbal.pack_propagate(False)
        self.tree_custbal = ttk.Treeview(self.frm_tree_custbal ,selectmode = "browse", takefocus = True , show = "headings" , style = "window.Treeview" , height = 6)
        self.tree_custbal.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree_custbal.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.scroll_y_custbal = ttk.Scrollbar(self.frm_tree_custbal , orient = con.VERTICAL , command = self.tree_custbal.yview)
        self.scroll_x_custbal = ttk.Scrollbar(self.frm_tree_custbal , orient = con.HORIZONTAL , command = self.tree_custbal.xview)
        self.tree_custbal.config(yscrollcommand = self.scroll_y_custbal.set , xscrollcommand = self.scroll_x_custbal.set)

        self.tree_custbal['columns'] = ( 'name','bal' , 'last_trans')

        self.tree_custbal.heading('name' , text = 'Name')
        self.tree_custbal.heading('bal' , text = 'Balance')
        self.tree_custbal.heading('last_trans' , text = 'Last Transaction')


        self.tree_custbal_wdt = self.tree_custbal.winfo_reqwidth()-self.scroll_y_custbal.winfo_reqwidth()
        if self.screen_height>1000:
            self.tree_custbal.column('name' , width = int(self.tree_custbal_wdt)  , anchor = "w")
            self.tree_custbal.column('bal' , width = int(self.tree_custbal_wdt*0.5)  , anchor = "e")
            self.tree_custbal.column('last_trans' , width = int(self.tree_custbal_wdt*0.7)  , anchor = "center")
        else:
            self.tree_custbal.column('name' , width = int(self.tree_custbal_wdt*0.75)  , anchor = "w")
            self.tree_custbal.column('bal' , width = int(self.tree_custbal_wdt*0.3)  , anchor = "e")
            self.tree_custbal.column('last_trans' , width = int(self.tree_custbal_wdt*0.5)  , anchor = "center")


    

        self.scroll_y_custbal.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x_custbal.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        self.tree_custbal.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)

        self.frm_tree_custbal.grid( row = 0 , column= 0 , columnspan = 2 , padx = int(self.main_wdt *0.1) , pady = int(self.main_wdt * 0.01))
        self.lbl_total_bal_text.grid(row = 1 , column = 0 , sticky= con.E)
        self.lbl_total_bal.grid(row = 1 , column = 1 , sticky=con.W)




        sql = "SELECT acc_cls_bal_firm1+acc_cls_bal_firm2+acc_cls_bal_firm3 as balance , acc_name , somanath.accounts.acc_id as acc_id  FROM somanath20"+self.year+".acc_bal , somanath.accounts where somanath20"+self.year+".acc_bal.acc_id = somanath.accounts.acc_id and somanath.accounts.acc_type = 'CUST'  order by  acc_cls_bal_firm1+acc_cls_bal_firm2+acc_cls_bal_firm3 desc"
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        data = req.json()

        sum = 0
        i = 0
        for each in data:
            tags = 'b'
            if i%2 == 0:
                tags = 'a'

            sql = "SELECT date_format(max(trans_date),'%d-%b-%y') as last_date from somanath20"+str(self.year)+".cashflow_sales where trans_acc = " + str(each["acc_id"])
            res = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql}).json()[0]['last_date']

            if res == None:
                last_date = "-"
            else:
                last_date = res

            sum += each["balance"]

            self.tree_custbal.insert('','end',tags=(tags ), values = [each['acc_name'] , "{:.2f}".format(each["balance"]) , last_date])
            i +=1

        self.lbl_total_bal.config(text = "{:.2f}".format(sum))



class profit_report(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title , validations ,others , profit_report_form):
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , profit_report_form)
        
        if base == None:
            return
        self.year = others[3]
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.ip = others[0]
        self.year = others[3]
        self.screen_height = root.winfo_screenheight()

        self.frm_date = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.lbl_from_profit = ttk.Label(self.frm_date , text = " From :" , style = "window_text_medium.TLabel")
        self.ent_from_profit = ttk.Entry(self.frm_date  , width = 10 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_from_profit.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_to_profit = ttk.Label(self.frm_date , text = " To   :" , style = "window_text_medium.TLabel")
        self.ent_to_profit = ttk.Entry(self.frm_date  , width = 10,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_to_profit.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_spacer = ttk.Label(self.frm_date   , width = 1 , style = "window_text_medium.TLabel" ,   justify = con.RIGHT)


        self.btn_get_profit = ttk.Button(self.frm_date , text = "Get Profits" , width = 12 , style = "window_btn_medium.TButton" ,command = lambda : self.get_profit(None) )
        self.btn_get_profit.bind("<Return>" , self.get_profit)


        self.frm_tree_cashflow = ttk.Frame(self.main_frame , width = self.main_wdt*0.7 , height = int(self.main_hgt*0.774))
        self.frm_tree_cashflow.pack_propagate(False)
        self.tree_cashflow = ttk.Treeview(self.frm_tree_cashflow ,selectmode = "browse", takefocus = True , show = "headings" , style = "window.Treeview" , height = 6)
        self.tree_cashflow.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree_cashflow.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.scroll_y_cashflow = ttk.Scrollbar(self.frm_tree_cashflow , orient = con.VERTICAL , command = self.tree_cashflow.yview)
        self.scroll_x_cashflow = ttk.Scrollbar(self.frm_tree_cashflow , orient = con.HORIZONTAL , command = self.tree_cashflow.xview)
        self.tree_cashflow.config(yscrollcommand = self.scroll_y_cashflow.set , xscrollcommand = self.scroll_x_cashflow.set)

        self.tree_cashflow['columns'] = ( 'inv_no','total' , 'ssm' , 'scm' , 'sem')

        self.tree_cashflow.heading('inv_no' , text = 'Invoice No')
        self.tree_cashflow.heading('total' , text = 'Total Profit')
        self.tree_cashflow.heading('ssm' , text = 'SSM Profit')
        self.tree_cashflow.heading('scm' , text = 'SCM Profit')
        self.tree_cashflow.heading('sem' , text = 'SEM Profit')


        self.tree_cashflow_wdt = self.tree_cashflow.winfo_reqwidth()-self.scroll_y_cashflow.winfo_reqwidth()
        if self.screen_height>1000:
            self.tree_cashflow.column('inv_no' , width = int(self.tree_cashflow_wdt*0.23)  , anchor = "w")
            self.tree_cashflow.column('total' , width = int(self.tree_cashflow_wdt*0.27)  , anchor = "e")
            self.tree_cashflow.column('ssm' , width = int(self.tree_cashflow_wdt*0.27)  , anchor = "e")
            self.tree_cashflow.column('scm' , width = int(self.tree_cashflow_wdt*0.27)  , anchor = "e")
            self.tree_cashflow.column('sem' , width = int(self.tree_cashflow_wdt*0.27)  , anchor = "e")

        else:
            self.tree_cashflow.column('inv_no' , width = int(self.tree_cashflow_wdt*0.17)  , anchor = "w")
            self.tree_cashflow.column('total' , width = int(self.tree_cashflow_wdt*0.19)  , anchor = "e")
            self.tree_cashflow.column('ssm' , width = int(self.tree_cashflow_wdt*0.19)  , anchor = "e")
            self.tree_cashflow.column('scm' , width = int(self.tree_cashflow_wdt*0.19)  , anchor = "e")
            self.tree_cashflow.column('sem' , width = int(self.tree_cashflow_wdt*0.19)  , anchor = "e")


        self.frm_total = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.lbl_total_profit = ttk.Label(self.frm_total   , width = 18 , style = "window_lbl_ent.TLabel" ,   justify = con.RIGHT)
        self.lbl_spacer1 = ttk.Label(self.frm_total   , width = 1 , style = "window_text_medium.TLabel" ,   justify = con.RIGHT)
        self.lbl_ssm_profit = ttk.Label(self.frm_total   , width = 18 , style = "window_lbl_ent.TLabel" ,   justify = con.RIGHT)
        self.lbl_spacer2 = ttk.Label(self.frm_total   , width = 1 , style = "window_text_medium.TLabel" ,   justify = con.RIGHT)
        self.lbl_scm_profit = ttk.Label(self.frm_total   , width = 18 , style = "window_lbl_ent.TLabel" ,   justify = con.RIGHT)
        self.lbl_spacer3 = ttk.Label(self.frm_total   , width = 1 , style = "window_text_medium.TLabel" ,   justify = con.RIGHT)
        self.lbl_sem_profit = ttk.Label(self.frm_total   , width = 18 , style = "window_lbl_ent.TLabel" ,   justify = con.RIGHT)
        self.lbl_spacer4 = ttk.Label(self.frm_total   , width = 1 , style = "window_text_medium.TLabel" ,   justify = con.RIGHT)
    




        self.scroll_y_cashflow.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x_cashflow.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        self.tree_cashflow.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)


        self.lbl_from_profit.grid(row = 0 , column = 0)
        self.ent_from_profit.grid(row = 0 , column = 1)
        self.lbl_to_profit.grid(row = 0 , column = 2)
        self.ent_to_profit.grid(row = 0 , column = 3)
        self.lbl_spacer.grid(row = 0 , column = 4)
        self.btn_get_profit.grid(row = 0 , column = 5)


        self.lbl_total_profit.grid(row = 0 , column = 0)
        self.lbl_spacer1.grid(row = 0 , column = 1)
        self.lbl_ssm_profit.grid(row = 0 , column = 2)
        self.lbl_spacer2.grid(row = 0 , column = 3)
        self.lbl_scm_profit.grid(row = 0 , column = 4)
        self.lbl_spacer3.grid(row = 0 , column = 5)
        self.lbl_sem_profit.grid(row = 0 , column = 6)
        self.lbl_spacer4.grid(row = 0 , column = 7)


        


        self.frm_date.grid(row = 0 , column = 0)
        self.frm_tree_cashflow.grid( row = 1 , column= 0  , padx = int(self.main_wdt *0.1) , pady = int(self.main_wdt * 0.01))
        self.frm_total.grid(row = 2 , column= 0 ,  padx = int(self.main_wdt *0.1) , sticky=con.E)

    def get_profit(self , e):
        date = self.ent_from_profit.get().upper()

        date1 = date.split("/")
        if len(date1)!=3:
            date1 = date.split("-")
            if len(date1) != 3:
                msg.showinfo("Info" , "Enter date in following format \n 'dd-mm-yy' or 'dd/mm/yy ")
                self.ent_from_profit.focus_set()
                self.ent_from_profit.select_range(0,con.END)
                return 

        try:
            datetime.datetime(int(date1[2]), int(date1[1]), int(date1[0]))
        except ValueError:
            msg.showinfo("Info" , "Enter correct date")
            self.ent_from_profit.focus_set()
            self.ent_from_profit.select_range(0,con.END)
            return 

        
        if len(date1[2])%2 !=0 :
            msg.showinfo("Info" , "Enter correct date")
            self.ent_from_profit.focus_set()
            self.ent_from_profit.select_range(0,con.END)
            return 

        if len(date1[0]) == 1:
            date1[0] = '0' + date1[0]

        if len(date1[1]) == 1:
            date1[1] = '0' + date1[1]    

        if len(date1[2]) == 2:
            date1[2] = '20' + date1[2]    

        
        self.ent_from_profit.delete(0,con.END)
        self.ent_from_profit.insert(0,date1[0] + "-" + date1[1] + "-" + date1[2])        
        self.ent_from_profit.select_clear()

        from_date = date1[2] + "-" + date1[1] + "-" + date1[0]
        
        date = self.ent_to_profit.get().upper()

        date1 = date.split("/")
        if len(date1)!=3:
            date1 = date.split("-")
            if len(date1) != 3:
                msg.showinfo("Info" , "Enter date in following format \n 'dd-mm-yy' or 'dd/mm/yy ")
                self.ent_to_profit.focus_set()
                self.ent_to_profit.select_range(0,con.END)
                return 

        try:
            datetime.datetime(int(date1[2]), int(date1[1]), int(date1[0]))
        except ValueError:
            msg.showinfo("Info" , "Enter correct date")
            self.ent_to_profit.focus_set()
            self.ent_to_profit.select_range(0,con.END)
            return 

        
        if len(date1[2])%2 !=0 :
            msg.showinfo("Info" , "Enter correct date")
            self.ent_to_profit.focus_set()
            self.ent_to_profit.select_range(0,con.END)
            return 

        if len(date1[0]) == 1:
            date1[0] = '0' + date1[0]

        if len(date1[1]) == 1:
            date1[1] = '0' + date1[1]    

        if len(date1[2]) == 2:
            date1[2] = '20' + date1[2]

        self.ent_to_profit.delete(0,con.END)
        self.ent_to_profit.insert(0,date1[0] + "-" + date1[1] + "-" + date1[2])        
        self.ent_to_profit.select_clear()


        to_date =  date1[2] + "-" + date1[1] + "-" + date1[0]

        sql = "SELECT  sales_id , sales_ref , sales_profit   FROM somanath20"+self.year+".sales_sp where sales_id in (SELECT distinct(sales_id) FROM somanath20"+self.year+".sales where sale_date>='"+from_date+"' and sale_date<='"+to_date+"') order by sales_id , sales_ref"
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        data = req.json()

        child = self.tree_cashflow.get_children()
        for each in child:
            self.tree_cashflow.delete(each)

        if len(data) == 0:
            self.lbl_total_profit.config(text = "")
            self.lbl_ssm_profit.config(text = "")
            self.lbl_scm_profit.config(text = "")
            self.lbl_sem_profit.config(text = "")
            return

        

        sum = [0 , 0 , 0 , 0]
        prev_sale_id = data[0]["sales_id"]
        i = 0

        total_sum = [0 , 0 , 0 , 0]
    
        for each in data:
            sale_id = each["sales_id"]
            ref_id = each["sales_ref"]

            if(sale_id != prev_sale_id):
                tags = 'b'
                if i%2 == 0:
                    tags = 'a'
                total_sum[0]+= sum[0]
                self.tree_cashflow.insert('','end',tags=(tags ), values = [prev_sale_id[3:] , "{:.2f}".format(sum[0]) , "{:.2f}".format(sum[1])  , "{:.2f}".format(sum[2])  , "{:.2f}".format(sum[3]) ])
                i +=1

                prev_sale_id = sale_id
                sum = [0 , 0, 0 , 0]



            sum[0]+= each["sales_profit"]

            if(ref_id[0:3] == "SSM"):
                sum[1]+=each["sales_profit"]
                total_sum[1]+= sum[1]

            elif(ref_id[0:3] == "SCM"):
                sum[2]+=each["sales_profit"]
                total_sum[2]+= sum[2]

            else:
                sum[3]+=each["sales_profit"]
                total_sum[3]+= sum[3]



            
            
            


        tags = 'b'
        if i%2 == 0:
            tags = 'a'

        self.tree_cashflow.insert('','end',tags=(tags ), values = [prev_sale_id[3:] , "{:.2f}".format(sum[0]) , "{:.2f}".format(sum[1])  , "{:.2f}".format(sum[2])  , "{:.2f}".format(sum[3]) ])
            

        self.lbl_total_profit.config(text = "{:.2f}".format(total_sum[0] + sum[0]))
        self.lbl_ssm_profit.config(text = "{:.2f}".format(total_sum[1]))
        self.lbl_scm_profit.config(text = "{:.2f}".format(total_sum[2]))
        self.lbl_sem_profit.config(text = "{:.2f}".format(total_sum[3]))





    def combo_entry_out(self , e):
        e.widget.select_clear()

