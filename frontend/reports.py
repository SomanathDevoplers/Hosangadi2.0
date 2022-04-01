from tkinter import  constants as con  , ttk , messagebox as msg , StringVar , IntVar
from requests import get 
from other_classes import base_window , image_viewer
from datetime import timedelta,datetime as date


class return_reports(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations,others , return_report_form):
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , return_report_form)
        
        if base == None:
            return
        self.year = others[3]
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()

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
            
            req = get("http://localhost:7000/SalesReport",params= {'firm':firm,'dbYear':year[2:4],'firstDay':firstDay,'lastDay':lastDay} )
            
            if req.status_code== 201:
                msg.showinfo("No Data","No sales for selected data")
            else:
                msg.showinfo("Sucess","Sales Excel will be ready in few minutes")
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
            monthList = ['APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER' ,'JANUARY','FEBRUARY','MARCH']
            nextMonth = monthList.index(month)+1
            if nextMonth == 12:
                nextMonth = 0
            nextMonth = monthList[nextMonth]
            lastDay = (str(date.strptime("20"+str(year[2:4])+"-"+nextMonth+"-05",'%Y-%B-%d').replace(day=1) - timedelta(days=1))).split(" ")[0]
            firstDay = lastDay[:-2]+"01"
            req = get("http://localhost:7000/PurchaseReport" , params= {'firm':firm,'dbYear':year[2:4],'year':year,'firstDay':firstDay,'lastDay':lastDay,'month':month})
            if req.status_code== 201:
                msg.showinfo("No Data","No purchase for selected data")
            else:
                msg.showinfo("Sucess","Purchase Excel will be ready in few minutes")
                self.btn_purchase.config(state=con.DISABLED)
        else:
            firm = 3
            
        
