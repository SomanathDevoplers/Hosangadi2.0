from tkinter import ttk , constants as con , filedialog
from PIL import Image , ImageTk
from image_viewer import image_viewer

from base_window import base_window

#tax_id, tax_type, tax_per

class categories(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations,others):
        base_window.__init__(self , root ,frames , dmsn , lbls ,title)
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.others = others
        self.image_cat = None
        

        self.lbl_cat_name = ttk.Label(self.main_frame , text = "Category Name    :" , style = "window_text_medium.TLabel")
        self.ent_cat_name = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_cat_name.bind("<FocusOut>" , self.combo_entry_out)
        self.lbl_cat_txt = ttk.Label(self.main_frame , text = "Category Image   :" , style = "window_text_medium.TLabel")
        self.lbl_cat_img = ttk.Label(self.main_frame  , width = 30 , style = "window_lbl_ent.TLabel")

        self.btn_cat_img_brw = ttk.Button(self.main_frame , text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_cat(None))
        self.btn_cat_img_brw.bind("<Return>" , self.file_dialog_cat)
        self.btn_cat_img_view = ttk.Button(self.main_frame , text = "View" , style = "window_btn_medium.TButton" ,command = lambda : self.view_cat(None))
        self.btn_cat_img_view.bind("<Return>" , self.view_cat)
        

        if root.winfo_screenheight()>1000:
            self.tree_frame = ttk.Frame(self.main_frame , height = int(self.main_hgt*0.865) , width = int(self.main_wdt*0.45) , style = "root_menu.TFrame")
        else:
            self.tree_frame = ttk.Frame(self.main_frame , height = int(self.main_hgt*0.871) , width = int(self.main_wdt*0.45) , style = "root_menu.TFrame")
        self.tree_frame.pack_propagate(False)
        self.tree_frame.grid_propagate(False)

        #self.tree_header_frame = ttk.Frame(self.tree_frame)

        self.tree = ttk.Treeview(self.tree_frame ,selectmode = "browse", takefocus = True , show = "headings" , style = "window.Treeview")
        self.tree.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.scroll_y = ttk.Scrollbar(self.tree_frame , orient = con.VERTICAL , command = self.tree.yview)
        self.scroll_x = ttk.Scrollbar(self.tree_frame , orient = con.HORIZONTAL , command = self.tree.xview)
        self.tree.config(yscrollcommand = self.scroll_y.set , xscrollcommand = self.scroll_x.set)

        

        self.tree['columns'] = ('id','name')
        self.tree.heading('id' , text = 'ID')
        self.tree.heading('name' , text = 'Name')
        #self.tree['show'] = 'headings'


        for i in range(100):
            if i%2 == 0:
                self.tree.insert('','end' ,tags=('a',), values = ("SMS"+str(i) , "Vijay"  ))
            else:
                self.tree.insert('','end' ,tags=('b',), values = ("SMS"+str(i) , "Vijay" ))

        self.btn_frame = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.btn_new = ttk.Button(self.btn_frame , text = "New" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.new(None))
        self.btn_new.bind("<Return>" , self.new) 
        self.btn_edit = ttk.Button(self.btn_frame , text = "Edit" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.edit(None))
        self.btn_edit.bind("<Return>" , self.edit)
        self.btn_save = ttk.Button(self.btn_frame , text = "Save" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.save(None))
        self.btn_save.bind("<Return>" , self.save)

        
        self.scroll_y.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        #self.tree_header_frame.pack(anchor = con.N , side = con.LEFT , fill = con.Y)
        self.tree.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)


        self.lbl_cat_name.grid(row = 0 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_cat_name.grid(row = 0 , column = 1 , columnspan = 2 )
        self.lbl_cat_txt.grid(row = 1 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_cat_img.grid(row = 1 , column = 1 ,  columnspan = 2)
        self.btn_cat_img_brw.grid(row = 2 , column = 1 , sticky = con.W)
        self.btn_cat_img_view.grid(row = 2 , column = 2 , padx = int(self.main_wdt*0.01))
        self.tree_frame.grid(row = 0 , column = 4 , rowspan = 15 , padx = int(self.main_wdt*0.01) , pady = int(self.main_hgt*0.035))


        self.btn_frame.grid(row = 20 , column = 4 , sticky = con.E)
        self.btn_new.grid(row = 0 , column = 0 , padx = int(self.main_wdt*0.01))
        self.btn_edit.grid(row = 0 , column = 1 , padx = int(self.main_wdt*0.01))
        self.btn_save.grid(row = 0 , column = 2 , padx = int(self.main_wdt*0.01))

        self.tree_wdt = self.tree_frame.winfo_reqwidth()-self.scroll_y.winfo_reqwidth()
        
        self.tree.column('id' , width = int(self.tree_wdt*0.2) ,minwidth = int(self.tree_wdt*0.2) , anchor = "w")
        self.tree.column('name' , width = int(self.tree_wdt*0.8) , minwidth = int(self.tree_wdt*0.6) , anchor = "w")


    def new(self , e):
        pass

    def edit(self , e):
        pass

    def save(self , e):
        pass
       
    def combo_entry_out(self , e):
        e.widget.select_clear()

    def file_dialog_cat(self , e):
        file = filedialog.askopenfilename(initialdir = self.others[0]+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        if file!= "":
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]
            self.lbl_cat_img.config(text = text)
            self.image_cat = ImageTk.PhotoImage(Image.open(file))
        else:
            self.lbl_cat_img.config(text = "")    

    def view_cat(self , e):
        if self.image_cat != None or self.lbl_cat_img.cget("text") != "":
            image_viewer(self.image_cat,"QR Code Image")