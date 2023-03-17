from cmath import log
import os.path
import io
import sys
from datetime import datetime
from tkinter import constants as con
from tkinter import font as font
from tkinter import messagebox as msg
from tkinter import ttk , Frame,  Menu , Tk , Text , PhotoImage
import socketio
import forms
import style
import purchase
import sales
import reports
import traceback
from threading import Thread
from playsound import playsound
play_sound = False
homedir = os.path.expanduser('~')
from time import sleep
from requests import get
#sys.setdefaultencoding('UTF8')




class notification:
    def __init__(self , text):

        global play_sound
        play_sound = True
        self.new_noti_frame_2 = ttk.Frame(frm_ntfc , height = root_hgt*0.3 , width = int(0.4*root_wdt))
        self.new_noti_frame_2.pack_propagate(False)
        self.new_noti_frame = ttk.Frame(self.new_noti_frame_2 , height = root_hgt*0.3 - 8 , width = int(0.4*root_wdt) - 10 , style = "root_menu.TFrame")
        self.new_noti_frame.pack_propagate(False)
        self.new_noti_frame.pack(pady = 4)
        self.new_noti_frame_2.pack()
        lbl_ntfc_cnt.config(text = int(lbl_ntfc_cnt.cget("text")) + 1)

        self.error_text = Text(self.new_noti_frame  , font = ('Lucida Grande' , -int(root_hgt*0.018)) , width = 70,  wrap = 'word' )
        self.error_text.insert(0.0 , text)
        self.error_text.bind("<Return>" , self.stop_sound)
        self.error_text.pack()
        view_ntfc(None)
        self.start_sound()
        f = open("C:\\Program Files\\Hosangadi2.0\\Error.txt", "a")
        f.write('\n'+datetime.now().strftime("%d/%m/%Y %H:%M:%S")+'\n'+str(text)+'\n')
        f.close()
        
    def sound(self):
        global play_sound
        count = 0
        while(play_sound and count<5):
            count += 1
            playsound("C:\\Program Files\\Hosangadi2.0\\error.mp3")
        

    def stop_sound(self , e):
        global play_sound
        password = self.error_text.get(0.0 , con.END).split("\n")[-2]
        if password == 'seen':
            play_sound = False
        
    def start_sound(self):
        Thread(target = self.sound).start()
        

sio = socketio.Client()
theme_state = False             #False if dark
task_place = False              #taskbar placement
noti_place = False              #notification placement
ip = None                       #server address
tax_check = False


def show_error(*args):
    for each in str(traceback.format_tb(args[3])).split(":"):
        if each == " Packets out of order. Got":
            f = open("C:\\Program Files\\Hosangadi2.0\\Error.txt", "a")
            f.write('\n'+datetime.now().strftime("%d/%m/%Y %H:%M:%S")+'\n'+"Packets of the Order"+'\n')
            f.close()
            return
    notification(traceback.format_tb(args[3]))
    #root.bell()

Tk.report_callback_exception = show_error

def socketKeepAlive():
    
    while(True):
        try:
            sio.emit('keepAlive')
            sleep(30)
        except:
            pass
    
    

@sio.on('error')
def hello(data):
    notification(data)
    
@sio.on('reportReady')
def reportReady(data,fileName):

    if data != "Purchase Report":
        file = get("http://"+ip+":6000/images/"+str(fileName))
        f = open(os.path.join(homedir , 'desktop' , 'Invoices' , 'reports',str(fileName)) , 'wb')
        f.write(file.content)
        f.close()
    else:
        
        file = get("http://"+ip+":6000/images/"+str(fileName.split(" ")[0]))
        f = open(os.path.join(homedir , 'desktop' , 'Invoices', 'reports',str(fileName.split(" ")[0])) , 'wb')
        f.write(file.content)
        f.close()
        file = get("http://"+ip+":6000/images/"+str(fileName.split(" ")[1]))
        f = open(os.path.join(homedir , 'desktop' , 'Invoices', 'reports',str(fileName.split(" ")[1])) , 'wb')
        f.write(file.content)
        f.close()

    msg.showinfo("Info" , " Report is Ready")


@sio.on('hasOwnbackup')
def backupOwnLostData(sales , purchases):
    user_type = lbl_user_type.cget("text")
    purchase.purchase(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Purchase Entry" , [num_alpha ,pos_decimal ,decimal , barcode , name  , decimal , pos_integer , mobile , date , email] , [ip , tax_check, user , year , homedir , form_id] , purchase_form , sio , prod_form , update_sp_form,purchases)


#-------form open counts----------#
prod_form = [0 , 3 , "Already 3 Product Forms are open"]
firm_form = [0 , 1 , "Already Firm Form is open"]
category_form = [0 , 1 , "Already Category Form is open"]
account_form = [0 , 3 , "Already 3 Account Forms are open"]
employ_form = [0 , 1 , "Already Employee Form is open"]
tax_form = [0 , 1 , "Already Tax Form is open"]
purchase_form = [0 , 1 , "Already Purchase Form is open"]
sales_form = [0 , 6 , "Already 6 Sales Form are open"]
return_report_form = [0 , 1 , "Already GST RETURN Form is open"]
update_sp_form = [0 , 3 , "Already 3 Update SP Forms are open"]
order_list_form = [0 , 1 , "Already Order List Form is open"]
purchase_cashflow_form = [0 , 1 , "Already Purchase Cashflow Form is open"]
customer_balance_report_form = [0 , 1 , "Already Customer Balance Form is open"]
profit_report_form = [0 , 1 , "Already Profit Report Form is open"]
barcode_form = [0 , 1 , "Already Barcode Form is open"]
db_form = [0 , 1 , "Already Backup Form is open"]


#---------------------------------#

def view_task(e):
    global task_place,root_hgt ,root_wdt
    if not task_place:
        frm_task.place(x = 0 , y = (0.034*root_hgt))
        frm_task.lift()
        
    else: 
        frm_task.place(x = int(-0.5*root_wdt) , y = (0.034*root_hgt))
        
    task_place = not task_place

def view_ntfc(e):
    global noti_place,root_hgt , root_wdt
    if not noti_place:
        if lbl_ntfc_cnt.cget("text") != '0':
            frm_ntfc.place(x = (root_wdt-0.4*root_wdt) , y = (0.034*root_hgt))
            frm_ntfc.lift()
    else:
        frm_ntfc.place(x = root_wdt+10, y = (0.034*root_hgt))
    noti_place = not noti_place

#------------------------validations-------------------------------#
def val_num_alpha(char):
    flag = True
    for each in char:
        if not (each.isalpha() or each.isdigit() or each.isspace() or each == "_"):
            flag = False
    return flag

def val_pos_int(char):
    flag = True
    for each in char:
        if not (each.isdigit()):
            flag = False
    return flag

def val_int(char):
    flag = True

    if len(char)>0:
        if "-" in char[1:]:
            return False

    for each in char:
        if not (each.isdigit()):
            flag = False
    return flag

def val_barcode(char):
    flag = True
    for each in char:
        if not (each.isalpha() or each.isdigit()):
            flag = False
    return flag

def val_name(char):
    flag = True
    for each in char:
        if not (each.isalpha() or each.isdigit() or each.isspace() or each == "."):
            flag = False
    return flag

def val_pos_dec(char):
    flag = True
    points = 0
    for each in char:
        if each == ".":
            points += 1
    

    for each in char:
        if not (each.isdigit() or each == "."):
            flag = False

    if points>1:
        return False

    return flag

def val_dec(char):
    flag = True
    points = 0
    for each in char:
        if each == ".":
            points += 1

    if len(char)>0:
        if "-" in char[1:]:
            return False

    for each in char:
        if not (each.isdigit() or each == "." or each == "-"):
            flag = False

    if points>1:
        return False
        
    return flag

def val_email(char):
    flag = True
    for each in char:
        if not (each.isalpha() or each.isdigit() or each == "_" or each == "@" or each == "."):
            flag = False
    return flag

def val_mobile(char):
    flag = True
    
    if len(char)>0:
        if "+" in char[1:]:
            return False

    for each in char:
        if not (each.isdigit() or each == "+"):
            flag = False
    return flag

def val_date(char):
    flag = True
    for each in char:
        if not (each.isdigit() or each == "-"):
            flag = False
    return flag

def val_none(char):
    return False



#------------------------validations ends---------------------------#


def close(): 
    if play_sound:
        msg.showinfo("Info" , "Call Shivanand / Krishnanand")
        
        return

    if int(lbl_task_cnt.cget("text"))>0:
        msg.showinfo("Info" , "CLOSE ALL TABS BEFORE EXIT!")
        return
    root.quit()
    sio.disconnect()
    
    

def firms(e = None): 
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    if firm_form[0] == 'True':
        msg.showinfo('Info' , "It is already open")
        return
    forms.firm(root, [frm_main , frm_task_others, frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Firms" , [num_alpha ,email ,decimal , barcode , name  , decimal , pos_integer , mobile]  , [homedir , ip , tax_check , user] , firm_form)

def products(e = None): 
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    if prod_form[0] == 'True':
        msg.showinfo('Info' , "It is already open")
        return
    forms.prods(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Products" , [num_alpha ,email ,decimal , barcode , name  , decimal , pos_integer ] , [homedir , ip , user , year , sio] , prod_form)
  
def taxes(e = None): 
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    forms.taxes(root, [frm_main , frm_task_others, frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Taxes" , [pos_integer],ip,user , tax_form)

def categories(e = None): 
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    forms.categories(root, [frm_main , frm_task_others, frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Categories" , [name] , [homedir  ,ip,user] ,  category_form)

def employees(e = None): 
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    forms.emp(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Employees" , [num_alpha  , name , mobile] , [homedir , ip , user] , employ_form)

def accounts(e = None): 
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    forms.acc(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Accounts" , [num_alpha  , name , mobile , email , barcode] , [homedir , ip ,tax_check, user , year] , account_form )

def purch(e = None): 
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    purchase.purchase(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Purchase Entry" , [num_alpha ,pos_decimal ,decimal , barcode , name  , decimal , pos_integer , mobile , date , email] , [ip , tax_check, user , year , homedir , form_id] , purchase_form , sio , prod_form , update_sp_form)

def sales_bill(e = None):
    sales.sales(root, [frm_main , frm_task_sales , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Sales Entry" , [num_alpha ,pos_decimal ,decimal , barcode , name  , decimal , pos_integer , mobile , date , email] , [ip , tax_check, user , year , homedir , form_id] , sales_form , sio , account_form)

def updatesp(e = None):
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    forms.update_sp(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Update SP" , [ num_alpha , pos_decimal] , [ip ,tax_check, user , year] , update_sp_form )
    
def orderList(e = None):
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    forms.order_list(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Order List" , [ num_alpha , pos_decimal] , [ip ,tax_check, user , year] , order_list_form )

def return_report(e = None):
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    reports.return_reports(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"GST Returns" , [ name  , date, pos_decimal] , [ip ,tax_check, user , year] , return_report_form )

def purchase_cashflow(e = None):
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    reports.purchase_cashflow(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Purchase Cashflow" , [ name  , date, pos_integer] , [ip ,tax_check, user , year] , purchase_cashflow_form )


def customer_balance(e = None):
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    reports.customer_balance(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Customer Balance"  , [ip ,tax_check, user , year] , customer_balance_report_form )

def profit_report(e = None):
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    reports.profit_report(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Profit Report"  , [date] ,  [ip ,tax_check, user , year] , profit_report_form )

def print_barcode(e = None):
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    forms.barcodes(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Barcodes" , [ num_alpha , pos_decimal , pos_integer] , [ip ,tax_check, user , year] , barcode_form )

def data_backup(e = None):
    forms.db(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Data Backup" , [name] , [ip , homedir, year] , db_form )

#1{
root = Tk()
root.resizable(con.FALSE , con.FALSE)
root.protocol("WM_DELETE_WINDOW" , close)


root.bind_all("<Alt-s>", sales_bill)
root.bind_all("<Alt-S>", sales_bill)
root.bind_all("<Alt-p>", purch)
root.bind_all("<Alt-P>", purch)
root.bind_all("<Alt-u>", updatesp)
root.bind_all("<Alt-U>", updatesp)
root.bind_all("<Alt-r>", products)
root.bind_all("<Alt-R>", products)
root.bind_all("<Alt-a>", accounts)
root.bind_all("<Alt-A>", accounts)


photo = PhotoImage(file = "C:\\Program Files\\Hosangadi2.0\\logo_hosagadi.png")
root.iconphoto(con.FALSE,photo)
root.title("Hosangadi                                                                                                                                                                                                                      Developed by :- Shiva & Krishna ")

root_hgt = root.winfo_screenheight()-34
root_wdt = root.winfo_screenwidth()-10
root.geometry(str(int(root_wdt))+"x"+str(int(root_hgt))+"-0-0")
#root.geometry(str(int(root_wdt))+"x"+str(int(root_hgt))+"+900-0")


num_alpha = root.register(val_num_alpha)
pos_integer = root.register(val_pos_int)
integer = root.register(val_int)
pos_decimal = root.register(val_pos_dec)
decimal = root.register(val_dec)
email = root.register(val_email)
none = root.register(val_none)
barcode = root.register(val_barcode)
name = root.register(val_name)
mobile = root.register(val_mobile)
date = root.register(val_date)


style = style.style(root_hgt , root_wdt)
style.theme_use("dark_theme")  

root.option_add("*TCombobox*Listbox*Font", ('Lucida Console', -int(root_hgt*0.025), 'bold'))
style.configure("window.Treeview.Heading", foreground="#333333" , font = ("Ariel",-(int(root_hgt*0.03))))


frm_menu = ttk.Frame(root , width = root_wdt , height = int(0.035*root_hgt) , style = "root_menu.TFrame" )

lbl_task_cnt = ttk.Label(frm_menu , text = "0" , width = 2 , style = "root_task_cnt.TLabel")
frm_menubar = Frame(frm_menu)
menu_entry_head = ttk.Menubutton(frm_menubar , text = "ENTRIES" , direction = 'below',style = "root_menu.TMenubutton" , takefocus = False)
menu_entry = Menu(menu_entry_head , tearoff = 0 , font = ('Lucida Console' , -int(root_hgt*0.022))) 
menu_entry.add_command(label = "SALES ENTRY" , command = sales_bill , accelerator = "Alt+S" , underline = 1)
menu_entry.add_command(label = "PURCHASE ENTRY" , command = purch , accelerator = "Alt+P" , underline = 1)
menu_entry.add_command(label = "UPDATE SP" , command = updatesp , accelerator = "Alt+U" , underline = 1)
menu_entry.add_command(label = "BARCODES" , command = print_barcode )
menu_entry_head.config(menu = menu_entry)

menu_registry_head = ttk.Menubutton(frm_menubar , text = "REGISTRIES" , direction = 'below',style = "root_menu.TMenubutton" , takefocus = False)
menu_registry = Menu(menu_registry_head , tearoff = 0 , font = ('Lucida Console' , -int(root_hgt*0.022)))
menu_registry.add_command(label = "PRODUCTS" , command = products , accelerator = "Alt+R" , underline = 1)
menu_registry.add_command(label = "ACCOUNTS" , command = accounts , accelerator = "Alt+A" , underline = 1)
menu_registry_head.config(menu = menu_registry)


menu_settings_head = ttk.Menubutton(frm_menubar , text = "SETTINGS" , direction = 'below',style = "root_menu.TMenubutton" , takefocus = False)
menu_settings = Menu(menu_settings_head , tearoff = 0 , font = ('Lucida Console' , -int(root_hgt*0.022)))
menu_settings.add_command(label = "CATEGORIES" , command = categories)
menu_settings.add_command(label = "TAXES" , command = taxes)
menu_settings.add_command(label = "EMPLOYEES" , command = employees)
menu_settings.add_command(label = "DATA BACKUP" , command = data_backup)
#menu_settings.add_command(label = "FIRMS" , command = firms)
menu_settings_head.config(menu = menu_settings)


menu_reports_head = ttk.Menubutton(frm_menubar , text = "REPORTS" , direction = 'below',style = "root_menu.TMenubutton" , takefocus = False)
menu_reports = Menu(menu_reports_head , tearoff = 0 , font = ('Lucida Console' , -int(root_hgt*0.022)))
menu_reports.add_command(label = "GST REPORTS" , command = return_report)
menu_reports.add_command(label = "STOCK REPORTS" )
menu_reports.add_command(label = "ORDER LIST" ,  command = orderList)
menu_reports.add_command(label = "PURCHASE CASHFLOW" ,  command = purchase_cashflow)
menu_reports.add_command(label = "CUSTOMER BALANCE" ,  command = customer_balance)
menu_reports.add_command(label = "PROFIT REPORT" ,  command = profit_report)

menu_reports_head.config(menu = menu_reports)










lbl_ntfc_cnt = ttk.Label(frm_menu , text = "0" , width = 2 , style = "root_ntfc_cnt.TLabel")

frm_menu.pack_propagate(False)
lbl_task_cnt.pack(side = con.LEFT , anchor = con.CENTER)
frm_menubar.pack(side = con.LEFT , anchor = con.W , padx = int(root_wdt*0.005)) 
menu_settings_head.grid(row = 0 , column = 0 , ipadx = int(root_wdt*0.006))
menu_reports_head.grid(row = 0 , column = 1 , ipadx = int(root_wdt*0.006))
menu_registry_head.grid(row = 0 , column = 2 , ipadx = int(root_wdt*0.006))
menu_entry_head.grid(row = 0 , column = 3 , ipadx = int(root_wdt*0.006))
lbl_ntfc_cnt.pack(side = con.RIGHT , anchor = con.CENTER)

frm_task_view = ttk.Frame(root , width = int(0.01*root_wdt) , height = int(0.865*root_hgt) , style = "root_main.TFrame")
frm_task_view.bind("<Enter>" , view_task)


frm_main = ttk.Frame(root , width = int(0.98*root_wdt) , height = int(0.865*root_hgt) , style = "root_main.TFrame")
frm_main.grid_propagate(False)


frm_ntfc_view = ttk.Frame(root , width = int(0.012*root_wdt) , height = int(0.865*root_hgt) , style = "root_main.TFrame")
frm_ntfc_view.bind("<Enter>" , view_ntfc)

frm_status = ttk.Frame(root , width = root_wdt , height = int(0.105*root_hgt) , style = "root_status.TFrame")
frm_status.grid_propagate(False)

lbl_fin_year_txt = ttk.Label(frm_status , text = "Year :" , style = "status_text.TLabel")
lbl_fin_year = ttk.Label(frm_status , text = "   -   " , width = 10 , style = "status_text.TLabel")
lbl_user_name_txt = ttk.Label(frm_status , text = "User :" , style = "status_text.TLabel")
lbl_user_name = ttk.Label(frm_status , text = "   -   " , width = 10 , style = "status_text.TLabel")
lbl_user_type_txt = ttk.Label(frm_status , text = "Type :" , style = "status_text.TLabel")
lbl_user_type = ttk.Label(frm_status , text = "   -   " , width = 10 , style = "status_text.TLabel")
lbl_server_name_txt = ttk.Label(frm_status , text = "Server :" , style = "status_text.TLabel")
lbl_server_name = ttk.Label(frm_status , text = "   -   " , width = 10 , style = "status_text.TLabel")

lbl_fin_year_txt.grid(row = 0 , column = 0)
lbl_fin_year.grid(row = 0 , column = 1)
lbl_user_name_txt.grid(row = 1 , column = 0)
lbl_user_name.grid(row = 1 , column = 1)
lbl_user_type_txt.grid(row = 2 , column = 0)
lbl_user_type.grid(row = 2 , column = 1)
lbl_server_name_txt.grid(row = 0 , column = 3)
lbl_server_name.grid(row = 0 , column = 4)

frm_task = ttk.Frame(root , width = int(0.4*root_wdt) , height = int(0.865*root_hgt) , style = "root_task.TFrame")
frm_task.bind("<Leave>" , view_task)
frm_task_sales = ttk.Frame(frm_task , width = int(0.2*root_wdt)-2 , height = int(0.865*root_hgt)-2 , style = "root_task_sales.TFrame")
frm_task_sales.pack_propagate(False)
frm_task_others = ttk.Frame(frm_task , width = int(0.2*root_wdt)-2 , height = int(0.865*root_hgt)-2 , style = "root_task_sales.TFrame")
frm_task_others.pack_propagate(False)

frm_ntfc = ttk.Frame(root , width = int(0.4*root_wdt) , height = int(0.865*root_hgt) , style = "root_task.TFrame" )
frm_ntfc.bind("<Leave>" , view_ntfc)
frm_ntfc.pack_propagate(False)


frm_task.pack_propagate(False)
frm_task_sales.pack(side = con.LEFT , padx = 1)
frm_task_others.pack(side = con.RIGHT , padx = 1)




frm_menu.grid(row = 0, column = 0 , columnspan = 3)

frm_task_view.grid(row = 1 , column = 0)
frm_main.grid(row = 1 , column = 1)
frm_ntfc_view.grid(row = 1 , column = 2)

frm_status.grid(row = 3 , column = 0 ,columnspan = 3)

#year = datetime.datetime.now().strftime("%y")
#if(int(datetime.datetime.now().strftime("%m")) >3 ) : year = int(year)+1 





try:
    lbl_user_name.config(text = sys.argv[1])    
    lbl_user_type.config(text = sys.argv[2])
    year = sys.argv[3][2:4]

    if(sys.argv[2]) == "TAXI":
        userType = "ADMIN"
        tax_check = True
    else:
        userType = sys.argv[2]

    lbl_user_type.config(text = userType)
    lbl_fin_year.config(text = sys.argv[3])
    lbl_server_name.config(text = sys.argv[4])
    ip = sys.argv[5]  
    form_id = sys.argv[6]
    sio.connect("http://"+ip+":5000/", headers = {"user_name" :  sys.argv[1] , "user_type" : userType, "form_type" : "root" , "fin_year": sys.argv[3] , "form_id" : form_id})



  #@ remove try excpet block
except:
    # ip = "192.168.0.103"
    ip = "127.0.0.1"
    lbl_user_name.config(text = "VIJAY")    
    lbl_user_type.config(text = "OWNER")
    lbl_fin_year.config(text = "2022-2023")
    lbl_server_name.config(text = ip)
    form_id = 'SomanathStores01'
    sio.connect("http://"+ip+":5000/", headers = {"user_name" : "HEMA" , "user_type" : "OWNER", "form_type" : "root" , "fin_year":"2022-2023" , "form_id" : form_id })
    year = "22"

user =lbl_user_name.cget("text")
Thread(target=socketKeepAlive , daemon = True).start()

products()

root.mainloop()
#edhe



