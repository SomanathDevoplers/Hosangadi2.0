from tkinter import  Event, Tk, ttk , constants as con , messagebox as msg
from datetime import datetime as date



class login:
    def __init__(self ,frames , lbl_btn , dmsn , val_num_alpha):
        self.main = frames[0]
        self.lbl_btn = lbl_btn
        start_year = 2020
        cur_year = int(date.today().strftime("%Y"))
        cur_mon = int(date.today().strftime("%m"))

        if cur_mon<4:
            end_year = cur_year
        else:
            end_year = cur_year+1

        self.fin_years = []

        for i in range(start_year , end_year):
            self.fin_years.append(str(i)+"-"+str(i+1))
            

        self.base_frame = ttk.Frame(frames[1] , height = int(dmsn[0]*0.3) , width = int(dmsn[1]*0.3) , style = "window_base.TFrame")
        self.base_frame.pack_propagate(False)

        self.title_frame = ttk.Frame(self.base_frame , height = int(dmsn[0]*0.3*0.12)-2 , width = int(dmsn[1]*0.3)-4 ,  style = "root_menu.TFrame")
        self.title_frame.pack_propagate(False)
        self.btn_close = ttk.Label(self.title_frame , text = "X" , style = "window_close.TLabel")
        self.btn_close.bind("<Button-1>" , self.close )

        self.main_frame = ttk.Frame(self.base_frame , height = int(dmsn[0]*0.3*0.88)-3 , width = int(dmsn[1]*0.3)-4 ,  style = "root_main.TFrame")
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()

        
        self.lbl_user_name = ttk.Label(self.main_frame , text = "User Name :" , style = "window_text.TLabel")
        self.lbl_user_pass = ttk.Label(self.main_frame , text = "Password  :" , style = "window_text.TLabel")
        self.lbl_year = ttk.Label(self.main_frame , text = "Year      :" ,  style = "window_text.TLabel")
        
        self.ent_user_name = ttk.Entry(self.main_frame , width = 12 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.13)) ,  validate="key", validatecommand=(val_num_alpha, '%P'))
        self.ent_user_pass = ttk.Entry(self.main_frame  , width = 12 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.13)) , show = "*" , validate="key", validatecommand=(val_num_alpha, '%P')) 
        self.combo_year = ttk.Combobox(self.main_frame , width = 12  ,values =self.fin_years , font = ('Lucida Grande' , -int(self.main_hgt*0.13))) 
        self.combo_year.insert(con.END , self.fin_years[-1])

        self.btn_submit = ttk.Button(self.main_frame , text = "Submit" , style = "window_btn.TButton" ,command = lambda : self.submit(None))
        self.btn_submit.bind("<Return>" , self.submit)

        self.base_frame.pack(anchor = con.CENTER , pady = int(dmsn[0]/4))
        self.title_frame.pack(anchor = con.N , pady = 2)
        self.btn_close.pack(side = con.RIGHT)
        self.main_frame.pack(anchor = con.S)
        #self.widget_frame.pack(anchor = con.CENTER)


        self.lbl_user_name.place(x = int(self.main_wdt*0.08) , y = int(self.main_hgt*0.03))
        self.ent_user_name.place(x = int(self.main_wdt*0.5) , y = int(self.main_hgt*0.02))
        self.lbl_user_pass.place(x = int(self.main_wdt*0.08) , y = int(self.main_hgt*0.22))
        self.ent_user_pass.place(x = int(self.main_wdt*0.5) , y = int(self.main_hgt*0.22))
        self.lbl_year.place(x = int(self.main_wdt*0.08) , y = int(self.main_hgt*0.42))
        self.combo_year.place(x = int(self.main_wdt*0.5) , y = int(self.main_hgt*0.42))
        
        self.btn_submit.place(x = int(self.main_wdt*0.1) , y = int(self.main_hgt*0.7))

        


    def submit(self , e):
        user_name = self.ent_user_name.get().upper()
        user_pass = self.ent_user_pass.get()
        fin_year = self.combo_year.get()

        if user_name == "" or user_pass =="":
            msg.showerror("Error" , "ENTER ALL DETAILS!")
            return

        if fin_year not in self.fin_years:
            msg.showerror("Error" , "SELECT YEAR FROM DROP DOWN!")
            return
        
        user_type = "ADMIN"  #get from backend
        
        self.lbl_btn[0].config(text = user_name)
        self.lbl_btn[1].config(text = user_type)
        self.lbl_btn[2].config(text = fin_year)
 
           
    def close(self ,e):
        self.main.quit()
        





