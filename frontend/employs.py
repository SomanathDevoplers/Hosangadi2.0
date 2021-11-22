#emp_name, emp_address, emp_phone, emp_accno, emp_ifsc, emp_image
from tkinter import ttk , constants as con , Text , filedialog

from base_window import base_window
from PIL import Image , ImageTk
from image_viewer import image_viewer

class emp(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations,others):
        base_window.__init__(self , root ,frames , dmsn , lbls ,title)
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.emp_img = None
        self.others = others

        self.lbl_emp_name = ttk.Label(self.main_frame , text = "Employ Name      :" , style = "window_text_medium.TLabel")
        self.lbl_emp_add = ttk.Label(self.main_frame , text = "Employ Address   :" , style = "window_text_medium.TLabel")
        self.lbl_emp_mob = ttk.Label(self.main_frame , text = "Employ Mob       :" , style = "window_text_medium.TLabel")
        self.lbl_emp_acc = ttk.Label(self.main_frame , text = "Employ AC/NO     :" , style = "window_text_medium.TLabel")
        self.lbl_emp_ifsc = ttk.Label(self.main_frame , text = "Employ IFSC      :" , style = "window_text_medium.TLabel")
        self.lbl_emp_img_txt = ttk.Label(self.main_frame , text = "Employ Photo     :" , style = "window_text_medium.TLabel")

        self.ent_emp_name = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_emp_name.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_emp_add = Text(self.main_frame  , width = 30 , height = 4 ,  font = ('Lucida Grande' , -int(self.main_hgt*0.03)))
        self.ent_emp_mob = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_emp_mob.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_emp_acc = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_emp_acc.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_emp_ifsc = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_emp_ifsc.bind("<FocusOut>" , self.combo_entry_out)
        self.lbl_emp_img =  ttk.Label(self.main_frame  , width = 30 , style = "window_lbl_ent.TLabel")

        self.btn_emp_photo_brw = ttk.Button(self.main_frame , text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_photo(None))
        self.btn_emp_photo_brw.bind("<Return>" , self.file_dialog_photo)
        self.btn_emp_photo_vw = ttk.Button(self.main_frame , text = " View " , style = "window_btn_medium.TButton" ,command = lambda : self.view_photo(None))
        self.btn_emp_photo_vw.bind("<Return>" , self.view_photo)


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
                self.tree.insert('','end' ,tags=('a',), values = ("SMS"+str(i) , "Vijay" , "Somanath Stores" ))
            else:
                self.tree.insert('','end' ,tags=('b',), values = ("SMS"+str(i) , "Vijay", "Somanath Stores" ))

        self.btn_frame = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.btn_new = ttk.Button(self.btn_frame , text = "New" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.new(None))
        self.btn_new.bind("<Return>" , self.new) 
        self.btn_edit = ttk.Button(self.btn_frame , text = "Edit" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.edit(None))
        self.btn_edit.bind("<Return>" , self.edit)
        self.btn_save = ttk.Button(self.btn_frame , text = "Save" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.save(None))
        self.btn_save.bind("<Return>" , self.save)

        self.tree_wdt = self.tree_frame.winfo_reqwidth()-self.scroll_y.winfo_reqwidth()
        
        self.tree.column('id' , width = int(self.tree_wdt*0.2) ,minwidth = int(self.tree_wdt*0.15) , anchor = "w")
        self.tree.column('name' , width = int(self.tree_wdt*0.8) , minwidth = int(self.tree_wdt*0.70) , anchor = "w")


        self.lbl_emp_name.grid(row = 0 , column = 0 , pady = int(self.main_hgt*0.03) , padx = int(self.main_wdt*0.01))
        self.lbl_emp_add.grid(row = 1 , column = 0 , pady = int(self.main_hgt*0.03))
        self.lbl_emp_mob.grid(row = 2 , column = 0 , pady = int(self.main_hgt*0.03))
        self.lbl_emp_acc.grid(row = 3 , column = 0 , pady = int(self.main_hgt*0.03))
        self.lbl_emp_ifsc.grid(row = 4 , column = 0 , pady = int(self.main_hgt*0.03))
        self.lbl_emp_img_txt.grid(row = 5 , column = 0 , pady = int(self.main_hgt*0.03))

        self.ent_emp_name.grid(row = 0 , column = 1 , padx = int(self.main_hgt*0.01) , columnspan = 2)
        self.ent_emp_add.grid(row = 1 , column = 1 , columnspan = 2)
        self.ent_emp_mob.grid(row = 2 , column = 1  , columnspan = 2)
        self.ent_emp_acc.grid(row = 3 , column = 1 , columnspan = 2)
        self.ent_emp_ifsc.grid(row = 4 , column = 1 , columnspan = 2)
        self.lbl_emp_img.grid(row = 5 , column = 1 , columnspan = 2)

        self.btn_emp_photo_brw.grid(row = 6 , column = 1)
        self.btn_emp_photo_vw.grid(row = 6 , column = 2)

        self.tree_frame.grid(row = 0 , column = 4 , rowspan = 15 , padx = int(self.main_wdt*0.03) ,pady = int(self.main_hgt*0.01))
        self.scroll_y.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        self.tree.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)

        self.btn_frame.grid(row = 16 , column = 4 , sticky = con.E)
        self.btn_new.grid(row = 0 , column = 0 , padx = int(self.main_wdt*0.01))
        self.btn_edit.grid(row = 0 , column = 1 , padx = int(self.main_wdt*0.01))
        self.btn_save.grid(row = 0 , column = 2 , padx = int(self.main_wdt*0.01))








    def combo_entry_out(self , e):
        e.widget.select_clear()

    def file_dialog_photo(self , e):
        file = filedialog.askopenfilename(initialdir = self.others[0]+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        if file!= "":
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]
            self.lbl_emp_img.config(text = text)
            self.emp_img = ImageTk.PhotoImage(Image.open(file))
        else:
            self.lbl_emp_img.config(text = "")

    def view_photo(self , e):
        if self.emp_img != None or self.lbl_emp_img.cget("text") != "":
            image_viewer(self.emp_img,"Photo Image")

    def new(self , e):
        pass

    def edit(self , e):
        pass

    def save(self , e):
        pass
