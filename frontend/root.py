from calendar import month
import datetime
import os.path
from pickle import FALSE
import sys
from tkinter import Button, Canvas, Frame, Label, Menu, PhotoImage, Tk
from tkinter import constants as con
from tkinter import font as font
from tkinter import messagebox as msg
from tkinter import ttk
import socketio
import forms
import style
import purchase
import sales_bill

sio = socketio.Client()
theme_state = False             #False if dark
task_place = False              #taskbar placement
noti_place = False              #notification placement
ip = None                       #server address
tax_check = False


#-------form open counts----------#
prod_form = [0 , 3 , "Already 3 Product Forms are open"]
firm_form = [0 , 1 , "Already Firm Form is open"]
category_form = [0 , 1 , "Already Category Form is open"]
account_form = [0 , 3 , "Already 3 Account Forms are open"]
employ_form = [0 , 1 , "Already Employee Form is open"]
tax_form = [0 , 1 , "Already Tax Form is open"]
purchase_form = [0 , 1 , "Already Purchase Form is open"]
sales_form = [0 , 1 , "Already Sales Form is open"]
report_form = [0 , 3 , "Already 3 Report Forms are open"]
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
        if not (each.isdigit() or each != "-" or each != "/"):
            flag = False
    return flag

def val_none(char):
    return False



#------------------------validations ends---------------------------#


def close(): 
    if int(lbl_task_cnt.cget("text"))>0:
        msg.showinfo("Info" , "CLOSE ALL TABS BEFORE EXIT!")
        return
    
    root.quit()
    sio.disconnect()

#----------------------Admin menu-----------------------#     
def admin_panel():
    if lbl_user_type.cget("text") != "ADMIN":
        #ask if mesagebox required
        return

#---------------------settings menu---------------------#
def firms(e = None): 
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    if firm_form[0] == 'True':
        msg.showinfo('Info' , "It is already open")
        return
    forms.firm(root, [frm_main , frm_task_others, frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Firms" , [num_alpha ,email ,decimal , barcode , name  , decimal , pos_integer , mobile]  , [os.path.expanduser('~') , ip , tax_check , user] , firm_form)

def products(e = None): 
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    if prod_form[0] == 'True':
        msg.showinfo('Info' , "It is already open")
        return
    forms.prods(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Products" , [num_alpha ,email ,decimal , barcode , name  , decimal , pos_integer ] , [os.path.expanduser('~') , ip , user] , prod_form)

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
    forms.categories(root, [frm_main , frm_task_others, frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Categories" , [name] , [os.path.expanduser('~')  ,ip,user] ,  category_form)

def employees(e = None): 
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    forms.emp(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Employees" , [num_alpha  , name , mobile] , [os.path.expanduser('~') , ip , user] , employ_form)

def accounts(e = None): 
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    forms.acc(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Accounts" , [num_alpha  , name , mobile , email , barcode] , [os.path.expanduser('~') , ip ,tax_check, user] , account_form )

def purch(e = None): 
    user_type = lbl_user_type.cget("text")
    if user_type == "EMPLOY" :
        msg.showerror("Error" , "You do not have the access to open this file")
        return
    purchase.purchase(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Purchase Entry" , [num_alpha ,pos_decimal ,decimal , barcode , name  , decimal , pos_integer , mobile , date] , [ip , tax_check, user , year] , purchase_form , sio)


#1{
root = Tk()
root.resizable(con.FALSE , con.FALSE)
root.protocol("WM_DELETE_WINDOW" , close)

root.bind_all("<Control-f>", firms)
root.bind_all("<Control-p>", products)
root.bind_all("<Control-t>", taxes)
root.bind_all("<Control-g>", categories)
root.bind_all("<Control-e>", employees)
root.bind_all("<Control-q>", accounts)


root_hgt = root.winfo_screenheight()-34
root_wdt = root.winfo_screenwidth()-10
root.geometry(str(int(root_wdt))+"x"+str(int(root_hgt))+"-0-0")


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


frm_menu = ttk.Frame(root , width = root_wdt , height = int(0.035*root_hgt) , style = "root_menu.TFrame")

lbl_task_cnt = ttk.Label(frm_menu , text = "0" , width = 2 , style = "root_task_cnt.TLabel")
frm_menubar = Frame(frm_menu)
menu_settings_head = ttk.Menubutton(frm_menubar , text = "Admin" , direction = 'below',style = "root_menu.TMenubutton")
menu_settings = Menu(menu_settings_head , tearoff = 0 , font = ('Tahoma' , -18 ) )
menu_settings.add_command(label = "Admin Panel" , command = admin_panel)
menu_settings_head['menu'] = menu_settings

menu_accounts_head = ttk.Menubutton(frm_menubar , text = "Settings" , direction = 'below',style = "root_menu.TMenubutton" )
menu_accounts = Menu(menu_accounts_head , tearoff = 0 , font = ('Tahoma' , 13 ) )
menu_accounts.add_command(label = "Firms" , command = firms , accelerator = "Ctrl+f" , underline = 1)
menu_accounts.add_command(label = "Products" , command = products , accelerator = "Ctrl+p" , underline = 1)
menu_accounts.add_command(label = "Categories" , command = categories , accelerator = "Ctrl+g" , underline = 1)
menu_accounts.add_command(label = "Taxes" , command = taxes , accelerator = "Ctrl+t" , underline = 1)
menu_accounts.add_command(label = "Employees" , command = employees , accelerator = "Ctrl+e" , underline = 1)
menu_accounts.add_command(label = "Accounts" , command = accounts , accelerator = "Ctrl+q" , underline = 1)
menu_accounts.add_command(label = "Purchases" , command = purch  , underline = 1)
menu_accounts_head['menu'] = menu_accounts


lbl_ntfc_cnt = ttk.Label(frm_menu , text = "0" , width = 2 , style = "root_ntfc_cnt.TLabel")

frm_menu.pack_propagate(False)
lbl_task_cnt.pack(side = con.LEFT , anchor = con.CENTER)
frm_menubar.pack(side = con.LEFT , anchor = con.W , padx = int(root_wdt*0.005)) 
menu_settings_head.grid(row = 0 , column = 0 , ipadx = int(root_wdt*0.003))
menu_accounts_head.grid(row = 0 , column = 1 , ipadx = int(root_wdt*0.003))
lbl_ntfc_cnt.pack(side = con.RIGHT , anchor = con.CENTER)

frm_task_view = ttk.Frame(root , width = int(0.01*root_wdt) , height = int(0.865*root_hgt) , style = "root_main.TFrame")
frm_task_view.bind("<Enter>" , view_task)
frm_main = ttk.Frame(root , width = int(0.98*root_wdt) , height = int(0.865*root_hgt) , style = "root_main.TFrame")
frm_main.grid_propagate(False)
frm_ntfc_view = ttk.Frame(root , width = int(0.011*root_wdt) , height = int(0.865*root_hgt) , style = "root_main.TFrame")
#frm_ntfc_view.bind("<Enter>" , view_ntfc)

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

frm_task.pack_propagate(False)
frm_task_others.pack(side = con.LEFT , padx = 1)
frm_task_sales.pack(side = con.RIGHT , padx = 1)




frm_menu.grid(row = 0, column = 0 , columnspan = 3)

frm_task_view.grid(row = 1 , column = 0)
frm_main.grid(row = 1 , column = 1)
frm_ntfc_view.grid(row = 1 , column = 2)

frm_status.grid(row = 3 , column = 0 ,columnspan = 3)

year = datetime.datetime.now().strftime("%y")
if(int(datetime.datetime.now().strftime("%m")) >3 ) : year = int(year)+1 

try:
    lbl_user_name.config(text = sys.argv[1])    
    lbl_user_type.config(text = sys.argv[2])
    if(sys.argv[2]) == "TAXI":
        print("taxTrue")
        userType = "ADMIN"
        tax_check = True
    else:
        userType = sys.argv[2]

    lbl_fin_year.config(text = sys.argv[3])
    lbl_server_name.config(text = sys.argv[4])
    ip = sys.argv[5]
    sio.connect("http://"+ip+":5000/" , headers = {"user_name" : sys.argv[1] , "user_type" : userType, "form_type" : "root"  , "fin_year":sys.argv[3]})
    
except:
    #print("Except Here")

    #ip = "192.168.1.33"
    ip = "127.0.0.1"
    lbl_user_name.config(text = "ADMIN")    
    lbl_user_type.config(text = "ADMIN")
    lbl_fin_year.config(text = "2021-2022")
    lbl_server_name.config(text = "server")
    sio.connect("http://"+ip+":5000/", headers = {"user_name" : "ADMIN" , "user_type" : "ADMIN", "form_type" : "root" , "fin_year":"2021-2022"})

    
user =lbl_user_name.cget("text")
#tax_check = False

#sales_bill.sales_bill(root, [frm_main , frm_task_sales , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Sales Entry" , [num_alpha ,pos_decimal ,decimal , barcode , name  , decimal , pos_integer , mobile , date] , [ip , tax_check, user , year] , sales_form , sio)
#purchase.purchase(root, [frm_main , frm_task_others , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Purchase Entry" , [num_alpha ,pos_decimal ,decimal , barcode , name  , decimal , pos_integer , mobile , date] , [ip , tax_check, user , year] , purchase_form , sio)

root.mainloop()