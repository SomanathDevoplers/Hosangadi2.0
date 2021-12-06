from tkinter import  Event, Tk, ttk , constants as con , messagebox as msg
from datetime import datetime as date
import requests


class login:
    def __init__(self ,frames , lbl_btn , dmsn , val_num_alpha):
        self.main = frames[0]                                   #root
        self.lbl_btn = lbl_btn                                  #lbl_btn = user_name , user_type , year , server
        self.rad_server = None
        start_year = 2020                                       
        cur_year = int(date.today().strftime("%Y"))
        cur_mon = int(date.today().strftime("%m"))

        if cur_mon<4:
            end_year = cur_year
        else:
            end_year = cur_year+1

        self.fin_years = []                                     #all financial year record available

        for i in range(start_year , end_year):
            self.fin_years.append(str(i)+"-"+str(i+1))
            

        self.base_frame = ttk.Frame(frames[1] , height = int(dmsn[0]*0.3) , width = int(dmsn[1]*0.3) , style = "window_base.TFrame")
        self.base_frame.pack_propagate(False)

        self.title_frame = ttk.Frame(self.base_frame , height = int(dmsn[0]*0.3*0.12)-2 , width = int(dmsn[1]*0.3)-4 ,  style = "root_menu.TFrame")
        self.title_frame.pack_propagate(False)
        self.lbl_title = ttk.Label(self.title_frame , text = "Login" , style = "window_title.TLabel")
        self.btn_close = ttk.Label(self.title_frame , text = "X" , style = "window_close.TLabel")
        self.btn_close.bind("<Button-1>" , self.close )

        self.main_frame = ttk.Frame(self.base_frame , height = int(dmsn[0]*0.3*0.88)-3 , width = int(dmsn[1]*0.3)-4 ,  style = "root_main.TFrame")
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.main_frame.grid_propagate(False)

        
        self.lbl_user_name = ttk.Label(self.main_frame , text = "User Name :" , style = "window_text_large.TLabel")
        self.lbl_user_pass = ttk.Label(self.main_frame , text = "Password  :" , style = "window_text_large.TLabel")
        self.lbl_year = ttk.Label(self.main_frame , text = "Year      :" ,  style = "window_text_large.TLabel")
        
        self.ent_user_name = ttk.Entry(self.main_frame , width = 12 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.13)) ,  validate="key", validatecommand=(val_num_alpha, '%P'))
        self.ent_user_name.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_user_pass = ttk.Entry(self.main_frame  , width = 12 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.13)) , show = "*" , validate="key", validatecommand=(val_num_alpha, '%P')) 
        self.ent_user_pass.bind("<Return>" , self.submit)
        self.ent_user_pass.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_year = ttk.Combobox(self.main_frame , width = 12  ,values =self.fin_years , font = ('Lucida Grande' , -int(self.main_hgt*0.13)))
        self.combo_year.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_year.bind("<Return>" , self.submit)
        self.combo_year.insert(con.END , self.fin_years[-1])

        self.rad_system = ttk.Radiobutton(self.main_frame , variable = self.rad_server ,value = 2 ,  style = "window_radio.TRadiobutton" , text = "SYSTEM")
        self.rad_server = ttk.Radiobutton(self.main_frame , variable = self.rad_server ,value = 1 ,  style = "window_radio.TRadiobutton" , text = "SERVER")

        self.btn_submit = ttk.Button(self.main_frame , text = "Submit" , style = "window_btn_large.TButton" ,command = lambda : self.submit(None))
        self.btn_submit.bind("<Return>" , self.submit)

        self.base_frame.grid(padx = int(dmsn[1]/3) , pady = int(dmsn[0]/4))
        self.title_frame.pack(anchor = con.N , pady = 2)
        self.lbl_title.pack(side = con.LEFT)
        self.btn_close.pack(side = con.RIGHT)
        self.main_frame.pack(anchor = con.S)


        """self.lbl_user_name.place(x = int(self.main_wdt*0.08) , y = int(self.main_hgt*0.03))
        self.ent_user_name.place(x = int(self.main_wdt*0.5) , y = int(self.main_hgt*0.02))
        self.lbl_user_pass.place(x = int(self.main_wdt*0.08) , y = int(self.main_hgt*0.22))
        self.ent_user_pass.place(x = int(self.main_wdt*0.5) , y = int(self.main_hgt*0.22))
        self.lbl_year.place(x = int(self.main_wdt*0.08) , y = int(self.main_hgt*0.42))
        self.combo_year.place(x = int(self.main_wdt*0.5) , y = int(self.main_hgt*0.42))"""

        self.lbl_user_name.grid(row = 0 , column = 0 , pady = int(self.main_hgt*0.033) , padx = int(self.main_wdt*0.03))
        self.ent_user_name.grid(row = 0 , column = 1 , columnspan = 2 , sticky = con.W)
        self.lbl_user_pass.grid(row = 1 , column = 0, pady = int(self.main_hgt*0.033))
        self.ent_user_pass.grid(row = 1 , column = 1, columnspan = 2 , sticky = con.W)
        self.lbl_year.grid(row = 2 , column = 0, pady = int(self.main_hgt*0.033))
        self.combo_year.grid(row = 2 , column = 1, columnspan = 2 , sticky = con.W)
        self.rad_system.grid(row = 3 , column = 1, pady = int(self.main_hgt*0.033))
        self.rad_server.grid(row = 3 , column = 2 , padx = int(self.main_wdt*0.035))
        
        self.btn_submit.grid(row = 4 , column = 0 )

        self.rad_server.invoke()
        self.ent_user_name.focus_set()


    def submit(self , e):
        user_name = self.ent_user_name.get().upper()
        user_pass = self.ent_user_pass.get()
        fin_year = self.combo_year.get()
        server = "server"
        if len(self.rad_system.state())>0:
            server = "system"
            

        if user_name == "" or user_pass =="":
            msg.showerror("Error" , "ENTER ALL DETAILS!")
            self.ent_user_name.focus_set()
            self.ent_user_name.select_range(0,con.END)
            return

        if fin_year not in self.fin_years:
            msg.showerror("Error" , "SELECT YEAR FROM DROP DOWN!")
            self.combo_year.focus_set()
            self.combo_year.select_range(0,con.END)
            return
        
        if server == 'server':
            resp = requests.get("http://127.0.0.1:6000/login",params = {"user_name":user_name , "user_pass":user_pass , "year" : fin_year})            #ipchange
        else:
            resp = requests.get("http://127.0.0.1:6000/login",params = {"user_name":user_name , "user_pass":user_pass , "year" : fin_year})            #ipchange

        resp = resp.json()

        if len(resp)>0: 
            user_type = resp[0]['user_type']
        else:
            msg.showerror("ERROR" , "Username Or Password Incorrect!")
            return

        self.lbl_btn[0].config(text = user_name)
        self.lbl_btn[1].config(text = user_type)
        self.lbl_btn[2].config(text = fin_year)
        self.lbl_btn[3].config(text = server)
        self.base_frame.destroy()

    def combo_entry_out(self , e):
        e.widget.select_clear()

    def close(self ,e):
        self.main.quit() 
    