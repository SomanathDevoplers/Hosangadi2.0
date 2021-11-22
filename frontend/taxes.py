from tkinter import ttk , constants as con , Text


from base_window import base_window

#tax_id, tax_type, tax_per

class taxes(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations):
        base_window.__init__(self , root ,frames , dmsn , lbls ,title)
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.rad_tax = -1

        self.lbl_tax_type = ttk.Label(self.main_frame , text = "Tax Type         :" , style = "window_text_medium.TLabel")
        self.lbl_tax_per = ttk.Label(self.main_frame , text = "Tax Percentage   :" , style = "window_text_medium.TLabel")
        
        self.ent_tax_per = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_tax_per.bind("<FocusOut>" , self.combo_entry_out)
        self.rad_tax_gst = ttk.Radiobutton(self.main_frame , value = 0 , variable = self.rad_tax , style = "window_radio.TRadiobutton" , text = "GST")
        self.rad_tax_cess = ttk.Radiobutton(self.main_frame , value = 1 , variable = self.rad_tax , style = "window_radio.TRadiobutton" , text = "CESS")



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

        

        self.tree['columns'] = ('id','type','per')
        self.tree.heading('id' , text = 'ID')
        self.tree.heading('type' , text = 'Type')
        self.tree.heading('per' , text = 'Percentage')
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


        self.lbl_tax_per.grid(row = 0 , column = 0 , pady = int(self.main_hgt*0.01), padx = int(self.main_wdt*0.01))
        self.ent_tax_per.grid(row = 0 , column = 1 , sticky = con.W , columnspan = 2)
        self.lbl_tax_type.grid(row = 1 , column = 0 , pady = int(self.main_hgt*0.01))
        self.rad_tax_gst.grid(row = 1 , column = 1 , padx = int(self.main_wdt*0.003) , sticky = con.W)
        self.rad_tax_cess.grid(row = 1 , column = 2)
  

        self.tree_frame.grid(row = 0 , column = 3 , rowspan = 15 , padx = int(self.main_wdt*0.01) , pady = int(self.main_hgt*0.035))
        self.scroll_y.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        #self.tree_header_frame.pack(anchor = con.N , side = con.LEFT , fill = con.Y)
        self.tree.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)

        self.btn_frame.grid(row = 20 , column = 3 , sticky = con.E)
        self.btn_new.grid(row = 0 , column = 0 , padx = int(self.main_wdt*0.01))
        self.btn_edit.grid(row = 0 , column = 1 , padx = int(self.main_wdt*0.01))
        self.btn_save.grid(row = 0 , column = 2 , padx = int(self.main_wdt*0.01))

        self.tree_wdt = self.tree_frame.winfo_reqwidth()-self.scroll_y.winfo_reqwidth()
        
        self.tree.column('id' , width = int(self.tree_wdt*0.15) ,minwidth = int(self.tree_wdt*0.15) , anchor = "w")
        self.tree.column('type' , width = int(self.tree_wdt*0.15) , minwidth = int(self.tree_wdt*0.15) , anchor = "w")
        self.tree.column('per' , width = int(self.tree_wdt*0.70) , minwidth = int(self.tree_wdt*0.70) , anchor = "w")

    def new(self , e):
        pass

    def edit(self , e):
        pass

    def save(self , e):
        pass

    def combo_entry_out(self , e):
        e.widget.select_clear()
       







