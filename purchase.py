from tkinter import  Listbox, StringVar, Text , constants as con , filedialog , messagebox as msg , ttk , Listbox , Canvas
from turtle import Turtle, width
from requests import get , post
from base_window import base_window


class purchase(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations, others , pur_form):
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , pur_form)
        if base == None:
            return
        self.main_frame.grid_propagate(False)
        self.root_frame = frames[0] 
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.ip = others[0]  
        self.tax_check = others[1] 

        

        #----------------------------------------purchase_detail_toplevel------------------------------------------------#
        self.frm_pur_details = ttk.Frame( self.root_frame , height = self.main_hgt*0.5 , width = self.main_wdt*0.4  , style = "root_menu.TFrame")
        self.frm_pur_details.grid_propagate(False)
        #self.frm_pur_details.bind("<Leave>" , self.destroy_pur_details)

        self.lbl_sup = ttk.Label(self.frm_pur_details , text = "Supplier      :" , style = "window_title.TLabel")
        self.lbl_sup_gst_txt = ttk.Label(self.frm_pur_details , text = "Supplier GST  :" , style = "window_title.TLabel")
        self.lbl_tax_meth = ttk.Label(self.frm_pur_details , text = "Tax Method    :" , style = "window_title.TLabel")
        self.lbl_firm_name = ttk.Label(self.frm_pur_details , text = "Firm          :" , style = "window_title.TLabel")
        self.lbl_firm_gst_txt = ttk.Label(self.frm_pur_details , text = "Firm GST      :" , style = "window_title.TLabel")
        self.lbl_pur_date = ttk.Label(self.frm_pur_details , text = "Date          :" , style = "window_title.TLabel")
        self.lbl_inv_no = ttk.Label(self.frm_pur_details , text = "Invoice No    :" , style = "window_title.TLabel")
        
        self.combo_supplier = ttk.Combobox(self.frm_pur_details , validate="key", validatecommand=(validations[4], '%P') , state = con.DISABLED , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30 , style = "window_combo.TCombobox") 
        self.combo_supplier.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_supplier.bind("<FocusOut>" , self.get_sup_gst)
        self.combo_supplier.bind("<Escape>" , self.destroy_pur_details)
        self.combo_supplier.bind("<Down>" , self.get_suppliers)
        self.combo_supplier.bind("<Button-1>" , self.get_suppliers)

        self.lbl_sup_gst = ttk.Label(self.frm_pur_details  , width = 30 , style = "window_lbl_ent.TLabel")

        self.combo_tax_meth = ttk.Combobox(self.frm_pur_details , values = ['In-State' , 'Out-Of-State'] ,validate="key", validatecommand=(validations[4], '%P') , state = "readonly" ,font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30 , style = "window_combo.TCombobox") 
        self.combo_tax_meth.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_tax_meth.bind("<Escape>" , self.destroy_pur_details)


        self.combo_firms = ttk.Combobox(self.frm_pur_details , validate="key", validatecommand=(validations[4], '%P') , state = con.DISABLED , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30 , style = "window_combo.TCombobox") 
        self.combo_firms.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_firms.bind("<FocusOut>" , self.get_firm_gst)
        self.combo_firms.bind("<Escape>" , self.destroy_pur_details)
        self.combo_firms.bind("<Down>" , self.get_firms)
        self.combo_firms.bind("<Button-1>" , self.get_firms)

        self.lbl_firm_gst = ttk.Label(self.frm_pur_details  , width = 30 , style = "window_lbl_ent.TLabel")

        self.ent_pur_date = ttk.Entry(self.frm_pur_details  , width = 30 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_pur_date.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_pur_date.bind("<Escape>" , self.destroy_pur_details)

        self.ent_inv_no = ttk.Entry(self.frm_pur_details  , width = 30 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[7], '%P'))
        self.ent_inv_no.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_inv_no.bind("<Escape>" , self.destroy_pur_details)

        self.lbl_sup.grid(row = 0 , column = 0 , padx = int(self.main_wdt*0.005) , pady = int(self.main_hgt*0.015))
        self.lbl_sup_gst_txt.grid(row = 1 , column = 0 , padx = int(self.main_wdt*0.005) , pady = int(self.main_hgt*0.015))
        self.lbl_tax_meth.grid(row = 2 , column = 0, padx = int(self.main_wdt*0.005) , pady = int(self.main_hgt*0.015))
        self.lbl_firm_name.grid(row = 3 , column = 0, padx = int(self.main_wdt*0.005) , pady = int(self.main_hgt*0.015))
        self.lbl_firm_gst_txt.grid(row = 4 , column = 0 , padx = int(self.main_wdt*0.005) , pady = int(self.main_hgt*0.015))
        self.lbl_pur_date.grid(row = 5 , column = 0, padx = int(self.main_wdt*0.005) , pady = int(self.main_hgt*0.015))
        self.lbl_inv_no.grid(row = 6 , column = 0, padx = int(self.main_wdt*0.005) , pady = int(self.main_hgt*0.015))
        
        self.combo_supplier.grid(row = 0 , column = 1 , sticky = con.W)
        self.lbl_sup_gst.grid(row = 1 , column = 1 , sticky = con.W)
        self.combo_tax_meth.grid(row = 2 , column = 1, sticky = con.W)
        self.combo_firms.grid(row = 3 , column = 1, sticky = con.W)
        self.lbl_firm_gst.grid(row = 4 , column = 1 , sticky = con.W)
        self.ent_pur_date.grid(row = 5 , column = 1, sticky = con.W)
        self.ent_inv_no.grid(row = 6 , column = 1, sticky = con.W)
        #self.btn_add_sup.grid(row = 0 , column = 1)
        #----------------------------------------purchase_detail_toplevel Ends here------------------------------------------------#


        #----------------------------------------ROW 1 Items-----------------------------------------------------------------------#
        self.frm_row1 = ttk.Frame( self.main_frame  , style = "root_main.TFrame")
        self.frm_row1.grid_propagate(True)

        self.lbl_bar = ttk.Label(self.frm_row1 , text = "Barcode"  , style = "window_text_medium.TLabel")
        self.ent_bar = ttk.Entry(self.frm_row1  , width = 13 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))

        self.lbl_name = ttk.Label(self.frm_row1 , text = "Product Name" , style = "window_text_medium.TLabel")
        self.ent_name = ttk.Entry(self.frm_row1  , width = 30 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))

        self.lbl_taxes = ttk.Label(self.frm_row1 , text = "Tax" , style = "window_text_medium.TLabel")
        self.ent_gst = ttk.Entry(self.frm_row1  , width = 3 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_cess = ttk.Entry(self.frm_row1  , width = 3 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))

        self.lbl_qty = ttk.Label(self.frm_row1 , text = "QTY"  , style = "window_text_medium.TLabel")
        self.ent_qty = ttk.Entry(self.frm_row1  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))


        self.lbl_cost = ttk.Label(self.frm_row1 , text = "Cost"  , style = "window_text_medium.TLabel")
        self.ent_cost = ttk.Entry(self.frm_row1  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))

        self.lbl_txb = ttk.Label(self.frm_row1 , text = "Taxble"  , style = "window_text_medium.TLabel")
        self.ent_txb = ttk.Entry(self.frm_row1  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))

        self.lbl_cost_ttl = ttk.Label(self.frm_row1 , text = "TTL Cost"  , style = "window_text_medium.TLabel")
        self.ent_cost_ttl = ttk.Entry(self.frm_row1  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))

        self.lbl_txb_ttl = ttk.Label(self.frm_row1 , text = "TTL Txbl"  , style = "window_text_medium.TLabel")
        self.ent_txb_ttl = ttk.Entry(self.frm_row1  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))

        self.lbl_pro_per = ttk.Label(self.frm_row1 , text = "Profit%"  , style = "window_text_medium.TLabel")
        self.ent_pro_per = ttk.Entry(self.frm_row1  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))

        self.lbl_tax_ttl_txt = ttk.Label(self.frm_row1 , text = "TTL Tax"  , style = "window_text_medium.TLabel")
        self.ent_gst_ttl = ttk.Entry(self.frm_row1  , width = 8 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_cess_ttl = ttk.Entry(self.frm_row1  , width = 8 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))

        
        self.lbl_bar.grid(row = 0 , column = 0 , sticky =con.W )
        self.lbl_name.grid(row = 0 , column = 1, sticky =con.W)
        self.lbl_taxes.grid(row = 0 , column = 2, sticky =con.W , columnspan = 2)
        self.lbl_qty.grid(row = 0 , column = 4, sticky =con.W)
        self.lbl_cost.grid(row = 0 , column = 5, sticky =con.W)
        self.lbl_txb.grid(row = 0 , column =6, sticky =con.W)
        self.lbl_cost_ttl.grid(row = 0 , column = 7, sticky =con.W)
        self.lbl_txb_ttl.grid(row = 0 , column = 8, sticky =con.W)
        self.lbl_pro_per.grid(row = 0 , column = 9, sticky =con.W)
        self.lbl_tax_ttl_txt.grid(row = 0 , column = 10, sticky =con.W , columnspan = 2)

        self.ent_bar.grid(row = 1 , column = 0, sticky = con.W)
        self.ent_name.grid(row = 1 , column = 1, sticky = con.W)
        self.ent_gst .grid(row = 1 , column = 2, sticky = con.W)
        self.ent_cess.grid(row = 1 , column = 3, sticky = con.W)
        self.ent_qty.grid(row = 1 , column = 4, sticky = con.W)
        self.ent_cost.grid(row = 1 , column = 5, sticky = con.W)
        self.ent_txb.grid(row = 1 , column = 6, sticky =con.W)
        self.ent_cost_ttl.grid(row = 1 , column = 7, sticky = con.W)
        self.ent_txb_ttl.grid(row = 1 , column = 8, sticky = con.W)
        self.ent_pro_per.grid(row = 1 , column = 9, sticky = con.W)
        self.ent_gst_ttl.grid(row = 1 , column = 10, sticky = con.W)
        self.ent_cess_ttl.grid(row = 1 , column = 11, sticky = con.W)


        #----------------------------------------ROW 1 Items Ends here-----------------------------------------------------------------------#

        #----------------------------------------ROW 2 items --------------------------------------------------------------------------------#
        self.frm_row2 = ttk.Frame( self.main_frame  , style = "root_main.TFrame")
        self.frm_row2.grid_propagate(True)


        self.lbl_nml_txt = ttk.Label(self.frm_row2 , text = "NML"  , style = "window_text_medium.TLabel")
        self.lbl_nml1 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_nml2 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_nml3 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_nml4 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")

        self.ent_nml1 = ttk.Entry(self.frm_row2 , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_nml2 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_nml3 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_nml4 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))

        self.lbl_htl_txt = ttk.Label(self.frm_row2 , text = " HTL"  , style = "window_text_medium.TLabel")
        self.lbl_htl1 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_htl2 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_htl3 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_htl4 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")

        self.ent_htl1 = ttk.Entry(self.frm_row2 , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_htl2 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_htl3 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_htl4 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))

        self.lbl_spl_txt = ttk.Label(self.frm_row2 , text = " SPL"  , style = "window_text_medium.TLabel")
        self.lbl_spl1 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_spl2 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_spl3 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_spl4 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")

        self.ent_spl1 = ttk.Entry(self.frm_row2 , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_spl2 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_spl3 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_spl4 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))

        self.lbl_ang_txt = ttk.Label(self.frm_row2 , text = " ANG"  , style = "window_text_medium.TLabel")
        self.lbl_ang1 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_ang2 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_ang3 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_ang4 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")

        self.ent_ang1 = ttk.Entry(self.frm_row2 , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_ang2 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_ang3 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_ang4 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))

        self.lbl_exp = ttk.Label(self.frm_row2 , text = "EXP"  , style = "window_text_medium.TLabel")
        self.ent_exp = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))

        self.lbl_nml_txt.grid(row = 0 , column = 0 , rowspan = 2)
        self.lbl_nml1.grid(row = 0 , column = 1)
        self.lbl_nml2.grid(row = 0 , column = 2)
        self.lbl_nml3.grid(row = 0 , column = 3)
        self.lbl_nml4.grid(row = 0 , column = 4)

        self.ent_nml1.grid(row = 1 , column = 1)
        self.ent_nml2.grid(row = 1 , column = 2)
        self.ent_nml3.grid(row = 1 , column = 3)
        self.ent_nml4.grid(row = 1 , column = 4)

        self.lbl_htl_txt.grid(row = 0 , column = 5, rowspan = 2)
        self.lbl_htl1.grid(row = 0 , column = 6)
        self.lbl_htl2.grid(row = 0 , column = 7)
        self.lbl_htl3.grid(row = 0 , column = 8)
        self.lbl_htl4.grid(row = 0 , column = 9)

        self.ent_htl1.grid(row = 1 , column = 6)
        self.ent_htl2.grid(row = 1 , column = 7)
        self.ent_htl3.grid(row = 1 , column = 8)
        self.ent_htl4.grid(row = 1 , column = 9)

        self.lbl_spl_txt.grid(row = 0 , column = 10, rowspan = 2)
        self.lbl_spl1.grid(row = 0 , column = 11)
        self.lbl_spl2.grid(row = 0 , column = 12)
        self.lbl_spl3.grid(row = 0 , column = 13)
        self.lbl_spl4.grid(row = 0 , column = 14)

        self.ent_spl1.grid(row = 1 , column = 11)
        self.ent_spl2.grid(row = 1 , column = 12)
        self.ent_spl3.grid(row = 1 , column = 13)
        self.ent_spl4.grid(row = 1 , column = 14)

        self.lbl_ang_txt.grid(row = 0 , column = 15, rowspan = 2)
        self.lbl_ang1.grid(row = 0 , column = 16)
        self.lbl_ang2.grid(row = 0 , column = 17)
        self.lbl_ang3.grid(row = 0 , column = 18)
        self.lbl_ang4.grid(row = 0 , column = 19)

        self.ent_ang1.grid(row = 1 , column = 16)
        self.ent_ang2.grid(row = 1 , column = 17)
        self.ent_ang3.grid(row = 1 , column = 18)
        self.ent_ang4.grid(row = 1 , column = 19)

        self.lbl_exp.grid(row = 0 , column = 20 , padx = int(self.main_wdt*0.008))
        self.ent_exp.grid(row = 1 , column = 20, padx = int(self.main_wdt*0.008))


        #----------------------------------------ROW 2 items ends here-----------------------------------------------------------------------#

        #----------------------------------------ROW 3 items --------------------------------------------------------------------------------#
        self.frm_row3 = ttk.Frame( self.main_frame  , style = "root_menu.TFrame" , height = int(self.main_hgt * 0.3) , width = int(self.main_wdt * 0.995))
        self.frm_row3.pack_propagate(False)
        
        self.tree_pur = ttk.Treeview(self.frm_row3 ,selectmode = "browse", takefocus = True , show = "headings" , style = "window.Treeview")
        self.tree_pur.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree_pur.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.scroll_y_pur = ttk.Scrollbar(self.frm_row3 , orient = con.VERTICAL , command = self.tree_pur.yview)
        self.scroll_x_pur = ttk.Scrollbar(self.frm_row3 , orient = con.HORIZONTAL , command = self.tree_pur.xview)
        self.tree_pur.config(yscrollcommand = self.scroll_y_pur.set , xscrollcommand = self.scroll_x_pur.set)

        

        self.tree_pur['columns'] = ('slno','name','gstPer','cp','qty','ttp','tcp','nml1','nml2','nml3','nml4','htl1','htl2','htl3','htl4','spl1','spl2','spl3','spl4','ang1','ang2','ang3','ang4')
        self.tree_pur.heading('slno' , text = 'No')
        self.tree_pur.heading('name' , text = 'Product Name')
        self.tree_pur.heading('gstPer' , text = '%')
        self.tree_pur.heading('cp' , text = 'Cost')
        self.tree_pur.heading('qty' , text = 'QTY')
        self.tree_pur.heading('ttp' , text = 'TTL Taxbl')
        self.tree_pur.heading('tcp' , text = 'TTL Cost')
        self.tree_pur.heading('nml1' , text = 'NRM 1')
        self.tree_pur.heading('nml2' , text = 'NRM 2')
        self.tree_pur.heading('nml3' , text = 'NRM 3')
        self.tree_pur.heading('nml4' , text = 'NRM 4')
        self.tree_pur.heading('htl1' , text = 'HTL 1')
        self.tree_pur.heading('htl2' , text = 'HTL 2')
        self.tree_pur.heading('htl3' , text = 'HTL 3')
        self.tree_pur.heading('htl4' , text = 'HTL 4')
        self.tree_pur.heading('spl1' , text = 'SPL 1')
        self.tree_pur.heading('spl2' , text = 'SPL 2')
        self.tree_pur.heading('spl3' , text = 'SPL 3')
        self.tree_pur.heading('spl4' , text = 'SPL 4')
        self.tree_pur.heading('ang1' , text = 'ANG 1')
        self.tree_pur.heading('ang2' , text = 'ANG 2')
        self.tree_pur.heading('ang3' , text = 'ANG 3')
        self.tree_pur.heading('ang4' , text = 'ANG 4')


        self.tree_pur_wdt = self.frm_row3.winfo_reqwidth()-self.scroll_y_pur.winfo_reqwidth()
        self.tree_pur.column('slno' , width = int(self.tree_pur_wdt*0.035) ,minwidth = int(self.tree_pur_wdt*0.035) , anchor = "e")
        self.tree_pur.column('name' , width = int(self.tree_pur_wdt*0.35) , minwidth = int(self.tree_pur_wdt*0.35) , anchor = "w")
        self.tree_pur.column('gstPer' , width = int(self.tree_pur_wdt*0.03) ,minwidth = int(self.tree_pur_wdt*0.03) , anchor = "e")
        self.tree_pur.column('cp' , width = int(self.tree_pur_wdt*0.1) , minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('qty' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('ttp' , width = int(self.tree_pur_wdt*0.1) , minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('tcp' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('nml1' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('nml2' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('nml3' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('nml4' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('htl1' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('htl2' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('htl3' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('htl4' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('ang1' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('ang2' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('ang3' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('ang4' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('spl1' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('spl2' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('spl3' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")
        self.tree_pur.column('spl4' , width = int(self.tree_pur_wdt*0.1) ,minwidth = int(self.tree_pur_wdt*0.1) , anchor = "e")


        self.tree_pur.insert('','end' ,tags=("a",), values = ('000' , 'SOMANATH STORES MARAVANTHE' , '00' , '99999.99', '99999.99','99999.99','999999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99','99999.99',))

        #self.tree_pur.bind('<Double-Button-1>',self.select_tree)
        #self.tree_pur.bind('<Return>',self.select_tree)

        self.scroll_y_pur.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x_pur.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        self.tree_pur.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)


        #----------------------------------------ROW 3 items ends here-----------------------------------------------------------------------#

        #----------------------------------------ROW 4 items --------------------------------------------------------------------------------#
        self.frm_row4 = ttk.Frame( self.main_frame  , style = "root_main.TFrame" , height = int(self.main_hgt * 0.33) , width = int(self.main_wdt * 0.985) )
        self.frm_row4.pack_propagate(False)

        self.tree_frame = ttk.Frame(self.frm_row4 , height = int(self.main_hgt * 0.3) , width = int(self.main_wdt * 0.3) , style = "root_menu.TFrame")
        self.tree_frame.pack_propagate(False)
        self.tree_tax = ttk.Treeview(self.tree_frame ,selectmode = "browse", takefocus = True , show = "headings" , style = "window.Treeview")
        self.tree_tax.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree_tax.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.scroll_y_tax = ttk.Scrollbar(self.tree_frame , orient = con.VERTICAL , command = self.tree_tax.yview)
        self.scroll_x_tax = ttk.Scrollbar(self.tree_frame , orient = con.HORIZONTAL , command = self.tree_tax.xview)
        self.tree_tax.config(yscrollcommand = self.scroll_y_tax.set , xscrollcommand = self.scroll_x_tax.set)

        self.tree_tax['columns'] = ('gstPer','sgst','cgst','igst','mt','cessper','cessamt')
        self.tree_tax.heading('gstPer' , text = 'GST %')
        self.tree_tax.heading('sgst' , text = 'SGST')
        self.tree_tax.heading('cgst' , text = 'CGST')
        self.tree_tax.heading('igst' , text = 'IGST')
        self.tree_tax.heading('mt' , text = '')
        self.tree_tax.heading('cessper' , text = 'CESS %')
        self.tree_tax.heading('cessamt' , text = 'AMT')

        self.tree_tax_wdt = self.tree_frame.winfo_reqwidth()-self.scroll_y_pur.winfo_reqwidth()
        self.tree_tax.column('gstPer' , width = int(self.tree_tax_wdt*0.2) ,minwidth = int(self.tree_tax_wdt*0.2) , anchor = "e")
        self.tree_tax.column('sgst' , width = int(self.tree_tax_wdt*0.3) ,minwidth = int(self.tree_tax_wdt*0.3) , anchor = "e")
        self.tree_tax.column('cgst' , width = int(self.tree_tax_wdt*0.3) ,minwidth = int(self.tree_tax_wdt*0.3) , anchor = "e")
        self.tree_tax.column('igst' , width = int(self.tree_tax_wdt*0.3) ,minwidth = int(self.tree_tax_wdt*0.3) , anchor = "e")
        self.tree_tax.column('mt' , width = int(self.tree_tax_wdt*0.08) ,minwidth = int(self.tree_tax_wdt*0.08) , anchor = "e")
        self.tree_tax.column('cessper' , width = int(self.tree_tax_wdt*0.3) ,minwidth = int(self.tree_tax_wdt*0.3) , anchor = "e")
        self.tree_tax.column('cessamt' , width = int(self.tree_tax_wdt*0.3) ,minwidth = int(self.tree_tax_wdt*0.3) , anchor = "e")

        self.scroll_y_tax.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x_tax.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        self.tree_tax.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)


        self.frm_totals = ttk.Frame( self.frm_row4  , style = "root_main.TFrame")
        self.frm_totals.grid_propagate(True)
        self.lbl_tot_txbl_txt = ttk.Label(self.frm_totals , text = "TTL Taxbl  :"  , style = "window_text_medium.TLabel")
        self.lbl_tot_txbl = ttk.Label(self.frm_totals  , width = 11 , style = "window_lbl_ent.TLabel")

        self.lbl_tot_tax_txt = ttk.Label(self.frm_totals , text = "TTL Tax    :"  , style = "window_text_medium.TLabel")
        self.lbl_tot_tax = ttk.Label(self.frm_totals  , width = 11 , style = "window_lbl_ent.TLabel")

        self.lbl_tot_amt_txt = ttk.Label(self.frm_totals , text = "TTL Amount :"  , style = "window_text_medium.TLabel")
        self.lbl_tot_amt = ttk.Label(self.frm_totals  , width = 11 , style = "window_lbl_ent.TLabel")

        self.lbl_tot_exp = ttk.Label(self.frm_totals , text = "   TTL Expense :"  , style = "window_text_medium.TLabel")
        self.ent_tot_exp = ttk.Entry(self.frm_totals , width = 11 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))

        self.lbl_grd_tot_txt = ttk.Label(self.frm_totals , text = "   Grand Total :"  , style = "window_text_medium.TLabel")
        self.lbl_grd_tot = ttk.Label(self.frm_totals  , width = 11 , style = "window_lbl_ent.TLabel")


        self.tree_frame.pack(side = con.LEFT)

        self.lbl_tot_txbl_txt.grid(row = 0 , column = 0) 
        self.lbl_tot_txbl.grid(row = 0 , column = 1)
        self.lbl_tot_tax_txt.grid(row = 1 , column = 0 , pady = int(self.main_hgt*0.06))
        self.lbl_tot_tax.grid(row = 1 , column = 1)
        self.lbl_tot_amt_txt.grid(row = 2 , column = 0)
        self.lbl_tot_amt.grid(row = 2 , column = 1)
        self.lbl_tot_exp.grid(row = 1 , column = 3)
        self.ent_tot_exp.grid(row = 1 , column = 4)
        self.lbl_grd_tot_txt.grid(row = 2 , column = 3)
        self.lbl_grd_tot.grid(row = 2 , column = 4)
        
        self.frm_totals.pack(side = con.RIGHT)

        #----------------------------------------ROW 4 items ends here-----------------------------------------------------------------------#

        self.btn_frame = ttk.Frame(self.main_frame , style = "root_main.TFrame")

        self.btn_add_dets = ttk.Button(self.btn_frame, state = con.DISABLED ,text = " Add Details "  , style = "window_btn_medium.TButton" , command = lambda : self.show_pur_details(None))
        self.btn_add_dets.bind("<Return>" , self.show_pur_details)
        self.btn_new = ttk.Button(self.btn_frame , text = "New" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.new(None))
        self.btn_new.bind("<Return>" , self.new) 
        self.btn_edit = ttk.Button(self.btn_frame , text = "Edit" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.edit(None))
        self.btn_edit.bind("<Return>" , self.edit)
        self.btn_save = ttk.Button(self.btn_frame , text = "Save" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.save(None))
        self.btn_save.bind("<Return>" , self.save)
        self.btn_cancel = ttk.Button(self.btn_frame , text = "Cancel" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.cancel(None))
        self.btn_cancel.bind("<Return>" , self.cancel)
        self.btn_refresh = ttk.Button(self.btn_frame , text = "Refresh" , width = 7 , style = "window_btn_medium.TButton" ,command = lambda : self.refresh(None))
        self.btn_refresh.bind("<Return>" , self.refresh)

        self.btn_add_dets.grid(row = 0 , column = 0 , padx = int(self.main_wdt*0.05))
        self.btn_new.grid(row = 0 , column = 1 , padx = int(self.main_wdt*0.01))
        self.btn_edit.grid(row = 0 , column = 2 , padx = int(self.main_wdt*0.01))
        self.btn_save.grid(row = 0 , column = 3 , padx = int(self.main_wdt*0.01))
        self.btn_cancel.grid(row = 0 , column = 4 , padx = int(self.main_wdt*0.01))
        self.btn_refresh.grid(row = 0 , column = 5 , padx = int(self.main_wdt*0.01))






        #self.btn_add_dets.grid(row = 0 , column = 0 )
        self.frm_row1.grid(row = 0 , column = 0  )
        self.frm_row2.grid(row = 1 , column = 0 , pady = int(self.main_wdt*0.004))
        self.frm_row3.grid(row = 2 , column = 0 , pady = int(self.main_wdt*0.004))
        self.frm_row4.grid(row = 3 , column = 0 , pady = int(self.main_wdt*0.004))
        self.btn_frame.grid(row = 4 ,column = 0 , sticky = con.E)

        #-----Intial Setting-----------#
        self.btn_save.config(state = con.DISABLED)
        self.btn_add_dets.config( state = con.DISABLED)
        
        #------temporary settings-------#
        #self.btn_add_dets.config(state = con.NORMAL)
        self.combo_supplier.config(state = con.NORMAL)
        self.combo_firms.config(state = con.NORMAL)
        self.ent_pur_date.config(state = con.NORMAL)
        self.ent_inv_no.config(state = con.NORMAL)
        #-temporary settings ends here--#


    def combo_entry_out(self , e):
        e.widget.select_clear()


    """--------------------------Purchase detail functions-----------------------------------------------"""
    def show_pur_details(self , e):
        self.frm_pur_details.place( x = self.main_wdt*0.25 , y = self.main_hgt*0.3)
        self.frm_pur_details.lift()
        self.combo_supplier.focus_set()
    
    def destroy_pur_details(self , e):
        self.frm_pur_details.place_forget()

    def get_suppliers(self,e):
        text = self.combo_supplier.get()
        if text == "":
            sql = "select acc_name from somanath.accounts where acc_type = 'SUPP' order by acc_name"
        else:
            sql = "select acc_name from somanath.accounts where acc_type = 'SUPP' and acc_name regexp '"+text+"' order by acc_name"

        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            resp = req.json()
            values = []
            for each in resp:
                values.append(each['acc_name'])

            self.combo_supplier.config(values = values)

    def get_sup_gst(self,e):
        text = self.combo_supplier.get()

        if text != "":
            sql = "select acc_gstin from somanath.accounts where acc_type = 'SUPP' and acc_name = '"+text+"'"
            req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
            if req.status_code == 200:
                resp = req.json()
                self.lbl_sup_gst.config(text = resp[0]['acc_gstin'])

    def get_firms(self,e):
        
        text = self.combo_firms.get()
        if text == "" :
            sql = "select firm_name from somanath.firms"
            if self.tax_check:
                sql += " where firm_tax != 'CASH' order by firm_name"

        else:
            sql = "select firm_name from somanath.firms where firm_name regexp '"+text+"'"
            if self.tax_check:
                sql += " and firm_tax != 'CASH' order by firm_name"

        

        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            resp = req.json()
            values = []
            for each in resp:
                values.append(each['firm_name'])

            self.combo_firms.config(values = values)

    def get_firm_gst(self,e):
        text = self.combo_firms.get()

        if text != "":
            sql = "select firm_gstin from somanath.firms where firm_name = '"+text+"'"
            req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
            if req.status_code == 200:
                resp = req.json()
                self.lbl_firm_gst.config(text = resp[0]['firm_gstin'])

    def date_format(self,e):
        pass
    """--------------------------Purchase detail functions-----------------------------------------------"""

    def new(self , e):
        self.btn_edit.config(state = con.DISABLED)
        self.btn_new.config(state = con.DISABLED)
        self.btn_save.config(state = con.NORMAL)
        self.btn_add_dets.config(state = con.NORMAL)


    def edit(self , e):
        self.btn_edit.config(state = con.DISABLED)
        self.btn_new.config(state = con.DISABLED)
        self.btn_save.config(state = con.NORMAL)
        self.btn_add_dets.config(state = con.NORMAL)

    def save(self , e):
        self.btn_edit.config(state = con.NORMAL)
        self.btn_new.config(state = con.NORMAL)
        self.btn_save.config(state = con.DISABLED)
        self.btn_add_dets.config(state = con.DISABLED)

    def cancel(self , e):
        self.btn_edit.config(state = con.NORMAL)
        self.btn_new.config(state = con.NORMAL)
        self.btn_save.config(state = con.DISABLED)
        self.btn_add_dets.config(state = con.DISABLED)

    def refresh(self , e):
        pass

    def minimize(self, e):
        self.frm_pur_details.place_forget()
        base_window.minimize(self,e)

    def close(self , e):
        self.frm_pur_details.place_forget()
        base_window.close(self,e)