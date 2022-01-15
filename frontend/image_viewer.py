from tkinter import Label , ttk ,  constants as con
import PIL

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