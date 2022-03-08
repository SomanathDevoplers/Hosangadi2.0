from tkinter import ttk , constants as con , messagebox as msg , Label
import PIL


class base_window:
    def __init__(self , root ,frames , dmsn , lbls ,title , form_count):
        if form_count[0] == form_count[1]:
            msg.showinfo("Info" , form_count[2])
            return

        self.form_count = form_count

        self.form_count[0] += 1
        self.lbls = lbls
        self.root_hgt = root.winfo_screenheight()-34
        self.root_wdt = root.winfo_screenwidth()-10 

        self.frm_task = frames[2]

        self.lbls[0].config(text = int(self.lbls[0].cget("text"))+1)

        self.access_frame = ttk.Frame(frames[1], width = frames[1].winfo_reqwidth() , height = int(frames[1].winfo_reqheight()*0.05) , style = "window_access.TFrame")
        self.access_frame.pack_propagate(False)
        self.acc_title = ttk.Label(self.access_frame , text = title , width = 19 , style = "window_access.TLabel")
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
        self.lbl_title = ttk.Label(self.title_frame , text = title , style = "window_title.TLabel")
        self.btn_min = ttk.Label(self.title_frame , text = "-" , style = "window_close.TLabel")
        self.btn_min.bind("<Button-1>" , self.minimize )
        self.btn_close = ttk.Label(self.title_frame , text = "X" , style = "window_close.TLabel")
        self.btn_close.bind("<Button-1>" , self.close )
        self.main_frame = ttk.Frame(self.base_frame , height = int(dmsn[0]*0.95) , width = int(dmsn[1])-2 ,  style = "root_main.TFrame")


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
        return(self)

    def close(self,e):
        self.base_frame.destroy()
        self.access_frame.destroy()
        self.lbls[0].config(text = int(self.lbls[0].cget("text"))-1)
        self.form_count[0] -= 1
        self.__del__()
    
    def minimize(self , e):
        self.base_frame.grid_forget()

    def acc_lbl_config_enter(self , e):
        self.acc_title.config(background = "#AEC1B5" , foreground = "#000")
    
    def acc_lbl_config_leave(self , e):
        self.acc_title.config(background = "#000" , foreground = "#d9cc99")

    def pack_top(self,e):
        self.base_frame.grid(row = 0 , column = 0)
        self.base_frame.lift()
        self.frm_task.place(x = int(-0.5*self.root_wdt) , y = (0.034*self.root_hgt))

    def __del__(self):
        pass

class image_viewer:
    def __init__(self , image , image_name , main_frame ):
        """self.root = Toplevel()
        self.root.geometry("+10+30")
        self.root.title(image_name)
        self.root.focus_set()
        self.root.bind("<FocusOut>" , self.close)
        self.root.bind("<Escape>" , self.close)"""
        #self.root.overrideredirect(True)
        self.image = PIL.Image.open(image)
        

        self.width , self.height = self.image.size
        self.root_height = main_frame.winfo_reqheight()
        self.root_width = main_frame.winfo_reqwidth()

        

        if self.width >= self.root_width or self.height >= self.root_height:
            self.width = self.width*0.6
            self.height = self.height*0.6
            self.image = self.image.resize((int(self.width) , int(self.height)))
            
        if self.width >= self.root_width or self.height >= self.root_height:
            self.width = self.width*0.6
            self.height = self.height*0.6
            self.image = self.image.resize((int(self.width) , int(self.height)))
       

        self.image = PIL.ImageTk.PhotoImage(self.image)
        self.frm_category = ttk.Frame( main_frame  )

        self.frm_category.bind("<Leave>" , self.close)

        self.title_frame = ttk.Frame(self.frm_category ,  style = "root_menu.TFrame")
        self.lbl_title = ttk.Label(self.title_frame , text = image_name , style = "window_title.TLabel")
        self.btn_close = ttk.Label(self.title_frame , text = "X" , style = "window_close.TLabel")
        self.btn_close.bind("<Button-1>" , self.close )

        self.label = Label(self.frm_category , image = self.image)

        self.title_frame.pack(anchor = con.N , pady = 2 , padx = 2 , fill = con.X)
        self.lbl_title.pack(side = con.LEFT , anchor = con.W)
        self.btn_close.pack(side = con.RIGHT , anchor = con.E)
        self.label.pack(fill = con.BOTH)
        self.frm_category.place( x = 20 , y = 20)
        self.frm_category.lift()



    def close(self , e):
        self.frm_category.destroy()



