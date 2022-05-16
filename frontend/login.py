import os
import requests
import style
from datetime import datetime as date
from tkinter import Tk , PhotoImage
from tkinter import constants as con
from tkinter import messagebox as msg
from tkinter import ttk
from subprocess import check_output
ip = "192.168.0.100"



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

def combo_entry_out(e):
    e.widget.select_clear()

def submit(e):
    global ip
    user_name = ent_user_name.get().upper()
    user_pass = ent_user_pass.get()
    year = combo_year.get()

    server = "server"
    if len(rad_system.state())>0:
        server = "system"
        
        

    if user_name == "" or user_pass =="":
        msg.showerror("Error" , "ENTER ALL DETAILS!")
        ent_user_name.focus_set()
        ent_user_name.select_range(0,con.END)
        return

    if year not in fin_years:
        msg.showerror("Error" , "SELECT YEAR FROM DROP DOWN!")
        combo_year.focus_set()
        combo_year.select_range(0,con.END)
        return

    try:
        if server != 'server':
            ip = "192.168.0.103" 
        resp = requests.get("http://"+ip+":5000/login",params = {"user_name":user_name , "user_pass":user_pass , "year" : year , "server" : server })  
             
    except:
        msg.showinfo("Info","Server Not Available")
        return
    
    #for successful login
    if resp.status_code == 200:
        resp = resp.json()
        if len(resp)>0: 
            user_type = resp[0]['user_type']
        else:
            msg.showerror("ERROR" , "Username Or Password Incorrect!")
            return

    #response code = 101 for same system login twice        
    elif resp.status_code == 101:                                                                                                     
        msg.showerror("ERROR" , "Application is already running")
        return

    #response code = 102 for same user login twice
    else:                                                                                                                               
        msg.showerror("ERROR" , "This User has logged in already!")
        return
    #@ set exe file location

    #root = os.path.expanduser('~')+"\\Hosangadi2.0\\frontend\\root.py "+str(user_name)+" "+str(user_type)+" "+str(year)+" "+str(server)+" "+ip
    root = 'C:\\Program Files\\Hosangadi2.0\\root\\root.exe '+str(user_name)+" "+str(user_type)+" "+str(year)+" "+str(server)+" "+ip 
    login.destroy()
    #os.system(root)
    check_output(args = root,shell = False) 
    


login = Tk()


photo = PhotoImage(file = "C:\\Program Files\\Hosangadi2.0\\logo_hosagadi.png")
login.iconphoto(con.FALSE,photo)
login.title("Hosangadi Login")
num_alpha = login.register(val_num_alpha)
pos_int = login.register(val_pos_int)
login_hgt = login.winfo_screenheight()-34
login_wdt = login.winfo_screenwidth()-10
login.geometry(str(int(login_wdt*0.3))+"x"+str(int(login_hgt*0.3))+"+"+str(int(login_wdt*0.3))+"+"+str(int(login_hgt*0.3)))

style = style.style(login_hgt , login_wdt)
style.theme_use("dark_theme")  

login.option_add("*TCombobox*Listbox*Font", ('Lucida Console', -int(login_hgt*0.025), 'bold'))
style.configure("window.Treeview.Heading", foreground="#333333" , font = ("Ariel",-(int(login_hgt*0.03))))


rad_server_name = None
start_year = 2021                                       
cur_year = int(date.today().strftime("%Y"))
cur_mon = int(date.today().strftime("%m"))

if cur_mon<4:
    end_year = cur_year
else:
    end_year = cur_year+1

fin_years = []                                     #all financial year record available

for i in range(start_year , end_year):
    fin_years.append(str(i)+"-"+str(i+1))

fin_years.reverse()

main_frame = ttk.Frame(login , height = str(int(login_hgt*0.3)) , width =int(login_wdt*0.3) ,  style = "root_main.TFrame")
main_frame.grid_propagate(False)


lbl_user_name = ttk.Label(main_frame , text = "User Name :" , style = "window_text_large.TLabel")
lbl_user_pass = ttk.Label(main_frame , text = "Password  :" , style = "window_text_large.TLabel")
lbl_year = ttk.Label(main_frame , text = "Year      :" ,  style = "window_text_large.TLabel")

ent_user_name = ttk.Entry(main_frame , width = 12 ,   font = ('Lucida Grande' , -int(login_hgt*0.025)) ,  validate="key", validatecommand=(num_alpha, '%P'))
ent_user_name.bind("<FocusOut>" , combo_entry_out)

ent_user_pass = ttk.Entry(main_frame  , width = 12 ,   font = ('Lucida Grande' , -int(login_hgt*0.025))  , show = "*", validate="key", validatecommand=(pos_int, '%P')) 
ent_user_pass.bind("<Return>" , submit)
ent_user_pass.bind("<FocusOut>" , combo_entry_out)


combo_year = ttk.Combobox(main_frame , width = 12  ,values =fin_years , font = ('Lucida Grande' , -int(login_hgt*0.025)))
combo_year.bind("<FocusOut>" , combo_entry_out)
#combo_year.bind("<KeyPress>" , dropdown)
combo_year.bind("<Return>" , submit)
combo_year.insert(con.END , fin_years[0])
combo_year.config(state = 'readonly')

rad_server = ttk.Radiobutton(main_frame , variable = rad_server_name ,value = 0 ,  style = "window_radio.TRadiobutton" , text = "SERVER")
rad_system = ttk.Radiobutton(main_frame , variable = rad_server_name ,value = 1 ,  style = "window_radio.TRadiobutton" , text = "SYSTEM")

btn_submit = ttk.Button(main_frame , text = "Submit" , style = "window_btn_large.TButton" ,command = lambda : submit(None))
btn_submit.bind("<Return>" , submit)


main_frame.pack()
lbl_user_name.grid(row = 0 , column = 0 , pady = int(login_hgt*0.01) )
ent_user_name.grid(row = 0 , column = 1 , columnspan = 2 , sticky = con.W)
lbl_user_pass.grid(row = 1 , column = 0, pady = int(login_hgt*0.01))
ent_user_pass.grid(row = 1 , column = 1, columnspan = 2 , sticky = con.W)
lbl_year.grid(row = 2 , column = 0, pady = int(login_hgt*0.01))
combo_year.grid(row = 2 , column = 1, columnspan = 2 , sticky = con.W)
rad_system.grid(row = 3 , column = 1, pady = int(login_hgt*0.01))
rad_server.grid(row = 3 , column = 2 , padx = int(login_wdt*0.01))

btn_submit.grid(row = 4 , column = 0 )

rad_server.invoke()

ent_user_name.focus_set()


login.mainloop()
