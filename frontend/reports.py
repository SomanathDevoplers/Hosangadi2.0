from tkinter import  constants as con  , ttk , messagebox as msg , StringVar , IntVar
from requests import get 
from other_classes import base_window , image_viewer


class report(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations,others , report_form):
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , report_form)
        
        if base == None:
            return
            
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.rad_rep = StringVar()



        self.frm_tree = ttk.Frame(self.main_frame , width = int(self.main_wdt*0.65), height = int(self.main_hgt*0.9))
        #if self.root.winfo_screenheight() < 1000: self.frm_tree.config( height = int(self.main_hgt*0.224)) 
        self.frm_tree.pack_propagate(False)

        self.ent_search = ttk.Entry(self.frm_tree  , width = 50 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_search.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_search.bind('<Return>' , self.search)
    
        self.tree = ttk.Treeview(self.frm_tree ,selectmode = "browse", takefocus = True , show = "headings" , style = "window.Treeview" , height = 3)
        self.tree.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.scroll_y = ttk.Scrollbar(self.frm_tree , orient = con.VERTICAL , command = self.tree.yview)
        self.scroll_x = ttk.Scrollbar(self.frm_tree , orient = con.HORIZONTAL , command = self.tree.xview)
        self.tree.config(yscrollcommand = self.scroll_y.set , xscrollcommand = self.scroll_x.set)

        self.tree['columns'] = ('date','sup','cp','qty')
        self.tree.heading('date' , text = 'DATE')
        self.tree.heading('sup' , text = 'SUPPLIER')
        self.tree.heading('cp' , text = 'COST')
        self.tree.heading('qty' , text = 'QTY')
        


        self.tree_wdt = self.frm_tree.winfo_reqwidth()-self.scroll_y.winfo_reqwidth()
        self.tree.column('date' , width = int(self.tree_wdt*0.17) ,minwidth = int(self.tree_wdt*0.17) , anchor = "e")
        self.tree.column('sup' , width = int(self.tree_wdt*0.35) , minwidth = int(self.tree_wdt*0.35) , anchor = "w")
        self.tree.column('cp' , width = int(self.tree_wdt*0.1) , minwidth = int(self.tree_wdt*0.1) , anchor = "e")
        self.tree.column('qty' , width = int(self.tree_wdt*0.1) ,minwidth = int(self.tree_wdt*0.1) , anchor = "e")
        

        self.scroll_y.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.ent_search.pack()
        self.scroll_x.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        self.tree.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)

        self.tree.insert('','end' ,tags=("a",), values = ('000' , 'SOMANATH STORES MARAVANTHE' ))
        self.tree.insert('','end' ,tags=("a",), values = ('000' , 'SOMANATH STORES MARAVANTHE' , '00' , '99999.99', '99999.99','99999.99','999999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99',))
        self.tree.insert('','end' ,tags=("a",), values = ('000' , 'SOMANATH STORES MARAVANTHE' , '00' , '99999.99', '99999.99','99999.99','999999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99',))







        self.frm_cust_wise = ttk.Frame( self.main_frame , height = int(self.main_hgt*0.2) , width = int(self.main_wdt*0.3)) #to give white border
        self.frm_cust_wise.pack_propagate(False)

        self.frm_cust_wise_2 = ttk.Frame( self.frm_cust_wise , height = int(self.main_hgt*0.2-8) , width = int(self.main_wdt*0.30-8) , style = "root_main.TFrame")
        self.frm_cust_wise_2.grid_propagate(False)

        self.rad_cust = ttk.Radiobutton(self.frm_cust_wise_2 , variable = self.rad_rep , value = 0 , style = "window_radio.TRadiobutton" , text = "Customer Wise")
        self.lbl_cust_name = ttk.Label(self.frm_cust_wise_2 , text = "Name :" , style = "window_text_medium.TLabel")

        self.combo_cust_name = ttk.Combobox(self.frm_cust_wise_2  , state = con.DISABLED , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30) 
        self.combo_cust_name.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_cust_from = ttk.Label(self.frm_cust_wise_2 , text = "From :" , style = "window_text_medium.TLabel")
        self.ent_cust_from = ttk.Entry(self.frm_cust_wise_2  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_cust_from.bind('<FocusOut>' , self.combo_entry_out)

        self.lbl_cust_to = ttk.Label(self.frm_cust_wise_2 , text = "To :" , style = "window_text_medium.TLabel")
        self.ent_cust_to = ttk.Entry(self.frm_cust_wise_2  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_cust_to.bind('<FocusOut>' , self.combo_entry_out)

        self.lbl_cust_sale = ttk.Label(self.frm_cust_wise_2 , text = "Sale :" , style = "window_text_medium.TLabel")
        self.combo_cust_sale = ttk.Combobox(self.frm_cust_wise_2  , state = con.DISABLED , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30) 
        self.combo_cust_sale.bind("<FocusOut>" , self.combo_entry_out)


        self.rad_cust.grid(row = 0 , column = 0 , columnspan = 2 )
        self.lbl_cust_name.grid(row = 1 , column = 0 , pady = self.main_hgt * 0.01)
        self.combo_cust_name.grid(row = 1 , column = 1 , columnspan=3)
        self.lbl_cust_from.grid(row = 2 , column = 0)
        self.ent_cust_from.grid(row = 2 , column = 1, sticky = con.W)
        self.lbl_cust_to.grid(row = 2 , column = 2)
        self.ent_cust_to.grid(row = 2 , column = 3 , sticky = con.E)
        self.lbl_cust_sale.grid(row = 3 , column = 0, pady = self.main_hgt * 0.01)
        self.combo_cust_sale.grid(row = 3 , column = 1 , columnspan = 3)
        self.frm_cust_wise_2.pack(padx = 4 , pady = 4)




        self.frm_supp_wise = ttk.Frame( self.main_frame , height = int(self.main_hgt*0.2) , width = self.main_wdt*0.3) #to give white border
        self.frm_supp_wise.pack_propagate(False)

        self.frm_supp_wise_2 = ttk.Frame( self.frm_supp_wise , height = int(self.main_hgt*0.2-8) , width = int(self.main_wdt*0.30-8) , style = "root_main.TFrame")
        self.frm_supp_wise_2.grid_propagate(False)

        self.rad_supp = ttk.Radiobutton(self.frm_supp_wise_2 , variable = self.rad_rep , value = 0 , style = "window_radio.TRadiobutton" , text = "Supplier Wise")
        self.lbl_supp_name = ttk.Label(self.frm_supp_wise_2 , text = "Name :" , style = "window_text_medium.TLabel")

        self.combo_supp_name = ttk.Combobox(self.frm_supp_wise_2  , state = con.DISABLED , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30) 
        self.combo_supp_name.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_supp_from = ttk.Label(self.frm_supp_wise_2 , text = "From :" , style = "window_text_medium.TLabel")
        self.ent_supp_from = ttk.Entry(self.frm_supp_wise_2  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_supp_from.bind('<FocusOut>' , self.combo_entry_out)

        self.lbl_supp_to = ttk.Label(self.frm_supp_wise_2 , text = "To :" , style = "window_text_medium.TLabel")
        self.ent_supp_to = ttk.Entry(self.frm_supp_wise_2  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_supp_to.bind('<FocusOut>' , self.combo_entry_out)

        self.lbl_supp_sale = ttk.Label(self.frm_supp_wise_2 , text = "Sale :" , style = "window_text_medium.TLabel")
        self.combo_supp_sale = ttk.Combobox(self.frm_supp_wise_2  , state = con.DISABLED , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30) 
        self.combo_supp_sale.bind("<FocusOut>" , self.combo_entry_out)


        self.rad_supp.grid(row = 0 , column = 0 , columnspan = 2 )
        self.lbl_supp_name.grid(row = 1 , column = 0 , pady = int(self.main_hgt * 0.01))
        self.combo_supp_name.grid(row = 1 , column = 1 , columnspan=3)
        self.lbl_supp_from.grid(row = 2 , column = 0)
        self.ent_supp_from.grid(row = 2 , column = 1, sticky = con.W)
        self.lbl_supp_to.grid(row = 2 , column = 2)
        self.ent_supp_to.grid(row = 2 , column = 3 , sticky = con.E)
        self.lbl_supp_sale.grid(row = 3 , column = 0, pady = int(self.main_hgt * 0.01))
        self.combo_supp_sale.grid(row = 3 , column = 1 , columnspan = 3)
        self.frm_supp_wise_2.pack(padx = 4 , pady = 4)






        self.btn_frame = ttk.Frame(self.main_frame , style = "root_main.TFrame")

        
        self.btn_get = ttk.Button(self.btn_frame , text = "Get Reports"  , style = "window_btn_medium.TButton" ,command = lambda : self.get(None))
        self.btn_get.bind("<Return>" , self.get) 
        self.btn_refresh = ttk.Button(self.btn_frame , text = "Refresh" , width = 7 , style = "window_btn_medium.TButton" ,command = lambda : self.refresh(None))
        self.btn_refresh.bind("<Return>" , self.refresh)

       
        self.btn_get.grid(row = 0 , column = 0 , padx = int(self.main_wdt*0.01))
        self.btn_refresh.grid(row = 0 , column = 1 , padx = int(self.main_wdt*0.01))


        self.frm_cust_wise.grid(row = 0 , column = 0)
        self.frm_supp_wise.grid(row = 1 , column = 0)
        self.frm_tree.grid(row = 0 , column = 1 , rowspan= 4 , pady = int(self.main_hgt * 0.01))
        self.btn_frame.grid(row = 5 , column = 1)

    







    def combo_entry_out(self , e):
        e.widget.select_clear()

    def get(self):
        pass

    def refresh(self):
        pass

    def search(self):
        pass
