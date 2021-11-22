from tkinter import Tk , Frame , Button , constants as con , ttk , Menu , Label , font as font , Canvas , PhotoImage , messagebox as msg
import os.path, style , login , firm , taxes , cats , users , accounts , employs , products

theme_state = False             #False if dark
task_place = False              #taskbar placement
noti_place = False              #notification placement


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

def logout(e):
    if lbl_user_type.cget("text") =="   -   ":
        return

    if int(lbl_task_cnt.cget("text")) != 0:
        msg.showinfo("Info" , "CLOSE ALL TABS BEFORE LOGGING OUT")
        return
    
    ans = msg.askokcancel("Logout" , "DO YOU WANT TO LOG OUT?")
    if not ans: 
        return

    lbl_user_name.config(text = "   -   ")
    lbl_user_type.config(text = "   -   ")
    lbl_fin_year.config(text = "   -   ")
    login_main =  login.login([root,frm_main], [lbl_user_name , lbl_user_type , lbl_fin_year] ,[0.98*root_hgt , root_wdt] , num_alpha)
    #remaining

def val_num_alpha(char):
    flag = True
    for each in char:
        if not (each.isalpha() or each.isdigit() or each.isspace() or each == "_"):
            flag = False
    return flag
            
def val_dec(char):
    flag = True
    for each in char:
        if not ( each.isdigit() or each == "."):
            flag = False
    return flag

def val_email(char):
    flag = True
    for each in char:
        if not (each.isalpha() or each.isdigit() or each == "_" or each == "@" or each == "."):
            flag = False
    return flag

def close():
    root.destroy()
    return
    if int(lbl_task_cnt.cget("text"))>0:
        msg.showinfo("Info" , "CLOSE ALL TABS BEFORE EXIT!")
        return
    else:
        root.quit()

#----------------------Admin menu-----------------------#     
def admin_panel():
    if lbl_user_type.cget("text") != "ADMIN":
        #ask if mesagebox required
        return

#---------------------settings menu---------------------#
def firms(e = None):
    user_type = lbl_user_type.cget("text")
    if not (user_type == "ADMIN" or user_type == "OWNER"):
        #ask if mesagebox required
        return
    #taxes.taxes(root, [frm_main , frm_task_others] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Taxes" , [decimal] , [os.path.expanduser('~') , style])
    firm.firm(root, [frm_main , frm_task_others] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Firms" , [num_alpha,email] , [os.path.expanduser('~') , style])

#1{
root = Tk()
root.resizable(con.FALSE , con.FALSE)
root.protocol("WM_DELETE_WINDOW" , close)
root.bind_all("<Control-h>", firms)
root_hgt = root.winfo_screenheight()-34
root_wdt = root.winfo_screenwidth()-10
root.geometry(str(int(root_wdt))+"x"+str(int(root_hgt))+"-0-0")
num_alpha = root.register(val_num_alpha)
decimal = root.register(val_dec)
email = root.register(val_email)
style = style.style(root_hgt , root_wdt)
style.theme_use("dark_theme")  

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
menu_accounts.add_command(label = "Firms" , command = firms , accelerator = "Ctrl+s" , underline = 1)
menu_accounts_head['menu'] = menu_accounts


lbl_ntfc_cnt = ttk.Label(frm_menu , text = "0" , width = 2 , style = "root_ntfc_cnt.TLabel")
lbl_logout = ttk.Label(frm_menu , text = " Logout " , style = "root_menu_btn.TLabel")
lbl_logout.bind("<Button-1>" , logout)

frm_menu.pack_propagate(False)
lbl_task_cnt.pack(side = con.LEFT , anchor = con.CENTER)
frm_menubar.pack(side = con.LEFT , anchor = con.W , padx = int(root_wdt*0.005)) 
menu_settings_head.grid(row = 0 , column = 0 , ipadx = int(root_wdt*0.003))
menu_accounts_head.grid(row = 0 , column = 1 , ipadx = int(root_wdt*0.003))
lbl_ntfc_cnt.pack(side = con.RIGHT , anchor = con.CENTER)
lbl_logout.pack(side = con.RIGHT , padx = int(root_wdt*0.003))


frm_task_view = ttk.Frame(root , width = int(0.01*root_wdt) , height = int(0.865*root_hgt) , style = "root_main.TFrame")
frm_task_view.bind("<Enter>" , view_task)
frm_main = ttk.Frame(root , width = int(0.98*root_wdt) , height = int(0.865*root_hgt) , style = "root_main.TFrame")
frm_main.grid_propagate(False)
frm_ntfc_view = ttk.Frame(root , width = int(0.011*root_wdt) , height = int(0.865*root_hgt) , style = "root_main.TFrame")
frm_ntfc_view.bind("<Enter>" , view_ntfc)

frm_status = ttk.Frame(root , width = root_wdt , height = int(0.105*root_hgt) , style = "root_status.TFrame")
frm_status.grid_propagate(False)

lbl_fin_year_txt = ttk.Label(frm_status , text = "Year :" , style = "status_text.TLabel")
lbl_fin_year = ttk.Label(frm_status , text = "   -   " , width = 10 , style = "status_text.TLabel")
lbl_user_name_txt = ttk.Label(frm_status , text = "User :" , style = "status_text.TLabel")
lbl_user_name = ttk.Label(frm_status , text = "   -   " , width = 10 , style = "status_text.TLabel")
lbl_user_type_txt = ttk.Label(frm_status , text = "Type :" , style = "status_text.TLabel")
lbl_user_type = ttk.Label(frm_status , text = "   -   " , width = 10 , style = "status_text.TLabel")

lbl_fin_year_txt.grid(row = 0 , column = 0)
lbl_fin_year.grid(row = 0 , column = 1)
lbl_user_name_txt.grid(row = 1 , column = 0)
lbl_user_name.grid(row = 1 , column = 1)
lbl_user_type_txt.grid(row = 2 , column = 0)
lbl_user_type.grid(row = 2 , column = 1)

frm_task = ttk.Frame(root , width = int(0.4*root_wdt) , height = int(0.865*root_hgt) , style = "root_task.TFrame")
frm_task.bind("<Leave>" , view_task)
frm_task_sales = ttk.Frame(frm_task , width = int(0.2*root_wdt)-2 , height = int(0.865*root_hgt)-2 , style = "root_task_sales.TFrame")
frm_task_sales.pack_propagate(False)
frm_task_others = ttk.Frame(frm_task , width = int(0.2*root_wdt)-2 , height = int(0.865*root_hgt)-2 , style = "root_task_sales.TFrame")
frm_task_others.pack_propagate(False)

frm_ntfc = ttk.Frame(root , width = int(0.4*root_wdt) , height = int(0.865*root_hgt) , style = "root_task.TFrame" )
frm_ntfc.bind("<Leave>" , view_ntfc)

frm_task.pack_propagate(False)
frm_task_sales.pack(side = con.LEFT , padx = 1)
frm_task_others.pack(side = con.RIGHT , padx = 1)





frm_menu.grid(row = 0, column = 0 , columnspan = 3)

frm_task_view.grid(row = 1 , column = 0)
frm_main.grid(row = 1 , column = 1)
frm_ntfc_view.grid(row = 1 , column = 2)

frm_status.grid(row = 3 , column = 0 ,columnspan = 3)

#firm.firm(root, [frm_main , frm_task_others, frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Firms" , [num_alpha,email] , [os.path.expanduser('~') , style])
#login_main = login.login([root,frm_main], [lbl_user_name , lbl_user_type , lbl_fin_year] ,[0.98*root_hgt , root_wdt] , num_alpha)
#taxes.taxes(root, [frm_main , frm_task_others, frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Taxes" , [decimal])
#cats.categories(root, [frm_main , frm_task_others, frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Categories" , [num_alpha,email] , [os.path.expanduser('~') , style])
#users.users(root, [frm_main , frm_task_others, frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Users" , [num_alpha,email] , [os.path.expanduser('~') , style])
#accounts.acc(root, [frm_main , frm_task_others, frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Accounts" , [num_alpha,email] , [os.path.expanduser('~') , style])
employs.emp(root, [frm_main , frm_task_others, frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Employees" , [num_alpha,email] , [os.path.expanduser('~') , style])
products.prods(root, [frm_main , frm_task_sales , frm_task] , [int(0.865*root_hgt) , int(0.98*root_wdt)] ,[lbl_task_cnt] ,"Products" , [num_alpha,email] , [os.path.expanduser('~') , style])

root.mainloop()
