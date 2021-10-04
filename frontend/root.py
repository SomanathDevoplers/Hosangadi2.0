from tkinter import Tk , Frame , Button , constants as con , ttk , Menu , Label , font as font , Canvas , PhotoImage , messagebox as msg
import style , login

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

def change_theme():
    global theme_state
    if theme_state:
        ans = msg.askyesno("Info","Do You Want to use Dark Theme?")
        if not ans:
            return
    else:
        ans = msg.askyesno("Info","Do You Want to use Light Theme?")
        if not ans:
            return


    theme_state = not theme_state
    if not theme_state:
        style.theme_use('dark_theme')
    else:
        style.theme_use('light_theme')

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
     
 

#1{
root = Tk()
root.resizable(con.FALSE , con.FALSE)

root_hgt = root.winfo_screenheight()-34
root_wdt = root.winfo_screenwidth()-10
root.geometry(str(int(root_wdt))+"x"+str(int(root_hgt))+"-0-0")
num_alpha = root.register(val_num_alpha)
decimal = root.register(val_dec) 
style = style.style(root_hgt , root_wdt)
style.theme_use("dark_theme")  





frm_menu = ttk.Frame(root , width = root_wdt , height = int(0.035*root_hgt) , style = "root_menu.TFrame")

lbl_task_cnt = ttk.Label(frm_menu , text = "99" , width = 2 , style = "root_task_cnt.TLabel")
frm_menubar = Frame(frm_menu)
menu_settings_head = ttk.Menubutton(frm_menubar , text = "Settings" , direction = 'below',style = "root_menu.TMenubutton")
menu_settings = Menu(menu_settings_head , tearoff = 0 , font = ('Tahoma' , -20 ) )
menu_settings.add_command(label = "Sales Bill"  , accelerator="Ctrl+Q")
menu_settings_head['menu'] = menu_settings

menu_accounts_head = ttk.Menubutton(frm_menubar , text = "Accounts" , direction = 'below',style = "root_menu.TMenubutton" )
menu_accounts = Menu(menu_accounts_head , tearoff = 0 , font = ('Tahoma' , 13 ) )
menu_accounts.add_command(label = "Sales Billsss" , accelerator="Ctrl+Q")
menu_accounts_head['menu'] = menu_accounts


lbl_ntfc_cnt = ttk.Label(frm_menu , text = "99" , width = 2 , style = "root_task_cnt.TLabel")
rad_dark = ttk.Checkbutton(frm_menu , command =   change_theme , style = "root_theme.TCheckbutton" )
lbl_dark = ttk.Label(frm_menu , text = "Light Theme : " , style = "root_theme.TLabel")

frm_menu.pack_propagate(False)
lbl_task_cnt.pack(side = con.LEFT , anchor = con.CENTER)
frm_menubar.pack(side = con.LEFT , anchor = con.W , padx = int(root_wdt*0.005)) 
menu_settings_head.grid(row = 0 , column = 0 , ipadx = int(root_wdt*0.003))
menu_accounts_head.grid(row = 0 , column = 1 , ipadx = int(root_wdt*0.003))
lbl_ntfc_cnt.pack(side = con.RIGHT , anchor = con.CENTER)
rad_dark.pack(side = con.RIGHT , anchor = con.CENTER )
lbl_dark.pack(side = con.RIGHT)


frm_task_view = ttk.Frame(root , width = int(0.01*root_wdt) , height = int(0.865*root_hgt) , style = "root_main.TFrame")
frm_task_view.bind("<Enter>" , view_task)
frm_main = ttk.Frame(root , width = int(0.98*root_wdt) , height = int(0.865*root_hgt) , style = "root_main.TFrame")
frm_main.pack_propagate(False)
frm_ntfc_view = ttk.Frame(root , width = int(0.011*root_wdt) , height = int(0.865*root_hgt) , style = "root_main.TFrame")
frm_ntfc_view.bind("<Enter>" , view_ntfc)

frm_status = ttk.Frame(root , width = root_wdt , height = int(0.105*root_hgt) , style = "root_status.TFrame")
frm_status.grid_propagate(False)

lbl_fin_year_txt = ttk.Label(frm_status , text = "Year     :" , style = "status_text.TLabel")
lbl_fin_year = ttk.Label(frm_status , text = "   -   " , width = 10 , style = "status_text.TLabel")
lbl_user_name_txt = ttk.Label(frm_status , text = "User     :" , style = "status_text.TLabel")
lbl_user_name = ttk.Label(frm_status , text = "   -   " , width = 10 , style = "status_text.TLabel")
lbl_user_type_txt = ttk.Label(frm_status , text = "Type     :" , style = "status_text.TLabel")
lbl_user_type = ttk.Label(frm_status , text = "   -   " , width = 10 , style = "status_text.TLabel")

lbl_fin_year_txt.grid(row = 0 , column = 0)
lbl_fin_year.grid(row = 0 , column = 1)
lbl_user_name_txt.grid(row = 1 , column = 0)
lbl_user_name.grid(row = 1 , column = 1)
lbl_user_type_txt.grid(row = 2 , column = 0)
lbl_user_type.grid(row = 2 , column = 1)

frm_task = ttk.Frame(root , width = int(0.4*root_wdt) , height = int(0.865*root_hgt) , style = "root_task.TFrame")
frm_task.bind("<Leave>" , view_task)
frm_ntfc = ttk.Frame(root , width = int(0.4*root_wdt) , height = int(0.865*root_hgt) , style = "root_task.TFrame" )
frm_ntfc.bind("<Leave>" , view_ntfc)






frm_menu.grid(row = 0, column = 0 , columnspan = 3)

frm_task_view.grid(row = 1 , column = 0)
frm_main.grid(row = 1 , column = 1)
frm_ntfc_view.grid(row = 1 , column = 2)

frm_status.grid(row = 3 , column = 0 ,columnspan = 3)


login_main = login.login([root,frm_main], [lbl_user_name , lbl_user_type , lbl_fin_year] ,[0.98*root_hgt , root_wdt] , num_alpha)

root.mainloop()
