from tkinter import ttk , constants as con

class base_window:
    def __init__(self , root ,frames , dmsn , lbls ,title ):
        self.lbls = lbls
        self.lbls[0].config(text = int(self.lbls[0].cget("text"))+1)
        self.access_frame = ttk.Frame(frames[1], width = frames[1].winfo_reqwidth() , height = int(frames[1].winfo_reqheight()*0.05) , style = "window_access.TFrame")
        self.access_frame.pack_propagate(False)
        self.acc_title = ttk.Label(self.access_frame , text = title +str(int(self.lbls[0].cget("text"))) , width = 19 , style = "window_access.TLabel")
        self.acc_title.bind("<Button-1>" , self.pack_top)
        self.acc_title.bind("<Enter>" , self.acc_lbl_config_enter)
        self.acc_title.bind("<Leave>" , self.acc_lbl_config_leave)
        self.acc_close_btn = ttk.Label(self.access_frame , text = "X" , style = "access_close.TLabel")
        self.acc_close_btn.bind("<Button-1>" , self.close)
        self.acc_close_btn.bind("<Enter>" , self.acc_lbl_config_enter)
        self.acc_close_btn.bind("<Leave>" , self.acc_lbl_config_leave)

        self.base_frame = ttk.Frame(frames[0] , height = int(dmsn[0]) , width = dmsn[1] , style = "window_base.TFrame")
        self.base_frame.pack_propagate(False)

        self.title_frame = ttk.Frame(self.base_frame , height = int(dmsn[0]*0.05)-2 , width = int(dmsn[1])-2 ,  style = "root_menu.TFrame")
        self.title_frame.pack_propagate(False)
        self.lbl_title = ttk.Label(self.title_frame , text = title+"\t\t\t\t\t\t\t\t"+str(int(self.lbls[0].cget("text"))) , style = "window_title.TLabel")
        self.btn_min = ttk.Label(self.title_frame , text = "-" , style = "window_close.TLabel")
        self.btn_min.bind("<Button-1>" , self.minimize )
        self.btn_close = ttk.Label(self.title_frame , text = "X" , style = "window_close.TLabel")
        self.btn_close.bind("<Button-1>" , self.close )
        self.main_frame = ttk.Frame(self.base_frame , height = int(dmsn[0]*0.95) , width = int(dmsn[1])-2 ,  style = "root_main.TFrame")
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()


        self.acc_title.pack(side = con.LEFT)
        self.acc_close_btn.pack(side = con.RIGHT)
        self.access_frame.pack()
        self.title_frame.pack(anchor = con.N , pady = 1)
        self.lbl_title.pack(side = con.LEFT)
        self.btn_close.pack(side = con.RIGHT)
        self.btn_min.pack(side = con.RIGHT)
        self.main_frame.pack()
        self.base_frame.grid(column = 0 , row = 0)
        self.base_frame.lift()

    def close(self,e):
        self.base_frame.destroy()
        self.access_frame.destroy()
        self.lbls[0].config(text = int(self.lbls[0].cget("text"))-1)
    
    def minimize(self , e):
        self.base_frame.grid_forget()
        

    def acc_lbl_config_enter(self , e):
        self.acc_title.config(background = "#AEC1B5" , foreground = "#000")
    
    def acc_lbl_config_leave(self , e):
        self.acc_title.config(background = "#000" , foreground = "#d9cc99")

    def pack_top(self,e):
        self.base_frame.grid(row = 0 , column = 0)
        self.base_frame.lift()
