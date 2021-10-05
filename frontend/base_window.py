from tkinter import ttk , constants as con

class base_window:
    def __init__(self , root ,frames , dmsn , title):
        self.base_frame = ttk.Frame(frames[0] , height = int(dmsn[0]) , width = dmsn[1] , style = "window_base.TFrame")
        self.base_frame.pack_propagate(False)

        

        self.title_frame = ttk.Frame(self.base_frame , height = int(dmsn[0]*0.05)-2 , width = int(dmsn[1])-2 ,  style = "root_menu.TFrame")
        self.title_frame.pack_propagate(False)
        self.lbl_title = ttk.Label(self.title_frame , text = title[0] , style = "window_title.TLabel")
        self.btn_min = ttk.Label(self.title_frame , text = "-" , style = "window_close.TLabel")
        self.btn_min.bind("<Button-1>" , self.minimize )
        self.btn_close = ttk.Label(self.title_frame , text = "X" , style = "window_close.TLabel")
        self.btn_close.bind("<Button-1>" , self.close )
        self.main_frame = ttk.Frame(self.base_frame , height = int(dmsn[0]*0.95) , width = int(dmsn[1])-2 ,  style = "root_main.TFrame")
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()

        self.base_frame.pack()
        self.title_frame.pack(anchor = con.N , pady = 1)
        self.lbl_title.pack(side = con.LEFT)
        self.btn_close.pack(side = con.RIGHT)
        self.btn_min.pack(side = con.RIGHT)
        self.main_frame.pack()

    def close(self,e):
        self.base_frame.destroy()
    
    def minimize(self , e):
        self.base_frame.pack_forget()
        pass

