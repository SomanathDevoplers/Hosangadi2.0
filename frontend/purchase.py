
from ast import Return
from cgitb import text
from sqlite3 import paramstyle
import string
from tkinter import Listbox , constants as con  , messagebox as msg , ttk , Listbox 
from requests import get 
from other_classes import base_window
import datetime


class purchase(base_window):
    
    def __init__(self , root ,frames , dmsn , lbls ,title,validations, others , pur_form , sio):
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , pur_form)
        if base == None:
            return
        base.acc_title.bind("<Button-1>" , self.pack_top)

        self.main_frame.grid_propagate(False)
        self.root_frame = frames[0] 
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.ip = others[0]  
        self.tax_check = others[1] 
        self.root = root
        self.year = others[3]
        self.prod_id = -1
        self.pur_id = -1
        self.prod_gst = -1
        self.prod_cess = -1
        self.stkDiff = -1
        self.selected_sl_no = 0
        self.sl_no = 1
        self.sio = sio
        self.user = others[2]
        self.new_state = False
        self.edit_state = False
        self.added_products = []
        self.selected_tax_meth = None
        self.check_state = False


        #----------------------------------------prod_name toplevel------------------------------------------------------------------------------#
        if root.winfo_screenheight()>1000:
            self.frm_prod_name = ttk.Frame( self.root_frame , height = self.main_hgt*0.594 , width = self.main_wdt*0.232 )#to give white border
        else:
            self.frm_prod_name = ttk.Frame( self.root_frame , height = self.main_hgt*0.608 , width = self.main_wdt*0.237 )#to give white border
        self.frm_prod_name.pack_propagate(False)

        self.frm_prod_name_2 = ttk.Frame( self.frm_prod_name , height = self.main_hgt*0.608-8 , width = self.main_wdt*0.4-8 , style = "root_menu.TFrame")
        self.frm_prod_name_2.grid_propagate(False)

        self.list_prod_name = Listbox(self.frm_prod_name_2 , height = 16 , width = 30 , font = ('Lucida Grande'  , -int(self.main_hgt*0.03) , "bold"))
        self.list_prod_name.bind('<Escape>',self.forget_prod_list)
        self.list_prod_name.bind('<Shift-Tab>',self.forget_prod_list)
        self.list_prod_name.bind('<Tab>',self.get_prod_by_name)
        self.list_prod_name.bind('<Return>',self.get_prod_by_name)
        """self.list_prod_name.bind('<Tab>',enter_to_custname)
        self.list_prod_name.bind('<Return>',enter_to_custname)
        
        self.list_prod_name.bind('<Double-1>',enter_to_custname)"""

        
        self.list_prod_name.grid(row = 1 , column = 0 , padx = 1 , pady = 1)
        self.frm_prod_name_2.pack(pady = 4 , padx = 4)


        

        
        
        #----------------------------------------prod_name toplevel ends here--------------------------------------------------------------------#

        #----------------------------------------prod_stock toplevel-----------------------------------------------------------------------------#
        self.frm_stk_sug = ttk.Frame( self.root_frame , height = self.main_hgt*0.32 , width = self.main_wdt) #to give white border
        self.frm_stk_sug.pack_propagate(False)

        self.frm_stk_sug_2 = ttk.Frame( self.frm_stk_sug , height = self.main_hgt*0.32-8 , width = self.main_wdt-8 , style = "root_menu.TFrame")
        self.frm_stk_sug_2.grid_propagate(False)

        self.lbl_tot_stk_txt = ttk.Label(self.frm_stk_sug_2 , text = " Total stock :" , style = "window_title.TLabel")
        self.lbl_tot_stk = ttk.Label(self.frm_stk_sug_2  , width = 10 , style = "window_lbl_ent.TLabel")

        self.lbl_mrp = ttk.Label(self.frm_stk_sug_2 , text = "  MRP :" , style = "window_title.TLabel")
        self.lbl_mrp_1 = ttk.Label(self.frm_stk_sug_2  , width = 10 , style = "window_lbl_ent.TLabel")
        self.lbl_mrp_2 = ttk.Label(self.frm_stk_sug_2  , width = 10 , style = "window_lbl_ent.TLabel")


        self.btn_upd_prod = ttk.Button(self.frm_stk_sug_2 , text = "Update Product"  , style = "window_btn_medium.TButton" ,command = lambda : self.upd_prod(None))
        self.btn_upd_prod.bind("<Return>" , self.upd_prod)

        self.btn_upd_price = ttk.Button(self.frm_stk_sug_2 , text = "Update SP"  , style = "window_btn_medium.TButton" ,command = lambda : self.upd_price(None))
        self.btn_upd_price.bind("<Return>" , self.upd_price)

        self.btn_sales_sum = ttk.Button(self.frm_stk_sug_2 , text = "Sales Summary" , style = "window_btn_medium.TButton" ,command = lambda : self.sales_summary(None))
        self.btn_sales_sum.bind("<Return>" , self.sales_summary)

        self.frm_tree_old_stock = ttk.Frame(self.frm_stk_sug_2 , width = self.main_wdt-16 , height = int(self.main_hgt*0.214))
        if self.root.winfo_screenheight() < 1000: self.frm_tree_old_stock.config( height = int(self.main_hgt*0.224)) 
        self.frm_tree_old_stock.pack_propagate(False)
    
        self.tree_old_stk = ttk.Treeview(self.frm_tree_old_stock ,selectmode = "browse", takefocus = True , show = "headings" , style = "window.Treeview" , height = 3)
        self.tree_old_stk.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree_old_stk.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.scroll_y_old_stk = ttk.Scrollbar(self.frm_tree_old_stock , orient = con.VERTICAL , command = self.tree_old_stk.yview)
        self.scroll_x_old_stk = ttk.Scrollbar(self.frm_tree_old_stock , orient = con.HORIZONTAL , command = self.tree_old_stk.xview)
        self.tree_old_stk.config(yscrollcommand = self.scroll_y_old_stk.set , xscrollcommand = self.scroll_x_old_stk.set)

        self.tree_old_stk.bind('<Escape>' , self.forget_stk_sug)
        self.tree_old_stk.bind('<Return>' , self.select_rates)
        self.tree_old_stk.bind('<Double-1>' , self.select_rates)


        self.tree_old_stk['columns'] = ( 'date','sup','cp','qty','nml1','nml2','nml3','nml4','htl1','htl2','htl3','htl4','spl1','spl2','spl3','spl4','ang1','ang2','ang3','ang4')

        self.tree_old_stk.heading('date' , text = 'DATE')
        self.tree_old_stk.heading('sup' , text = 'SUPPLIER')
        self.tree_old_stk.heading('cp' , text = 'COST')
        self.tree_old_stk.heading('qty' , text = 'QTY')
        self.tree_old_stk.heading('nml1' , text = 'NRM 1')
        self.tree_old_stk.heading('nml2' , text = 'NRM 2')
        self.tree_old_stk.heading('nml3' , text = 'NRM 3')
        self.tree_old_stk.heading('nml4' , text = 'NRM 4')
        self.tree_old_stk.heading('htl1' , text = 'HTL 1')
        self.tree_old_stk.heading('htl2' , text = 'HTL 2')
        self.tree_old_stk.heading('htl3' , text = 'HTL 3')
        self.tree_old_stk.heading('htl4' , text = 'HTL 4')
        self.tree_old_stk.heading('spl1' , text = 'SPL 1')
        self.tree_old_stk.heading('spl2' , text = 'SPL 2')
        self.tree_old_stk.heading('spl3' , text = 'SPL 3')
        self.tree_old_stk.heading('spl4' , text = 'SPL 4')
        self.tree_old_stk.heading('ang1' , text = 'ANG 1')
        self.tree_old_stk.heading('ang2' , text = 'ANG 2')
        self.tree_old_stk.heading('ang3' , text = 'ANG 3')
        self.tree_old_stk.heading('ang4' , text = 'ANG 4')


        self.tree_old_stk_wdt = self.frm_tree_old_stock.winfo_reqwidth()-self.scroll_y_old_stk.winfo_reqwidth()
        
        self.tree_old_stk.column('date' , width = int(self.tree_old_stk_wdt*0.1)  , anchor = "center")
        self.tree_old_stk.column('sup' , width = int(self.tree_old_stk_wdt*0.25)  , anchor = "w")
        self.tree_old_stk.column('cp' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08)  , anchor = "e")
        self.tree_old_stk.column('qty' , width = int(self.tree_old_stk_wdt*0.1) , minwidth = int(self.tree_old_stk_wdt*0.1), anchor = "e")
        self.tree_old_stk.column('nml1' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08) , anchor = "e")
        self.tree_old_stk.column('nml2' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08), anchor = "e")
        self.tree_old_stk.column('nml3' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08) , anchor = "e")
        self.tree_old_stk.column('nml4' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08) , anchor = "e")
        self.tree_old_stk.column('htl1' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08) , anchor = "e")
        self.tree_old_stk.column('htl2' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08), anchor = "e")
        self.tree_old_stk.column('htl3' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08) , anchor = "e")
        self.tree_old_stk.column('htl4' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08) , anchor = "e")
        self.tree_old_stk.column('ang1' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08) , anchor = "e")
        self.tree_old_stk.column('ang2' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08) , anchor = "e")
        self.tree_old_stk.column('ang3' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08) , anchor = "e")
        self.tree_old_stk.column('ang4' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08) , anchor = "e")
        self.tree_old_stk.column('spl1' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08) , anchor = "e")
        self.tree_old_stk.column('spl2' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08) , anchor = "e")
        self.tree_old_stk.column('spl3' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08) , anchor = "e")
        self.tree_old_stk.column('spl4' , width = int(self.tree_old_stk_wdt*0.08) , minwidth = int(self.tree_old_stk_wdt*0.08) , anchor = "e")


        self.scroll_y_old_stk.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x_old_stk.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        self.tree_old_stk.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)

    
        self.lbl_tot_stk_txt.grid(row = 0 , column = 0 , sticky = con.W)
        self.lbl_tot_stk.grid(row = 0 , column = 1, sticky = con.W)
        self.lbl_mrp.grid(row = 0 , column = 2, sticky = con.W)
        self.lbl_mrp_1.grid(row = 0 , column = 3, sticky = con.W)
        self.lbl_mrp_2.grid(row = 0 , column = 4, sticky = con.W)


        self.btn_upd_prod.grid(row = 0 , column = 5, sticky = con.E)
        self.btn_upd_price.grid(row = 0 , column = 6, sticky = con.E)
        self.btn_sales_sum.grid(row = 0 , column = 7, sticky = con.E)
        self.frm_tree_old_stock.grid(row = 1 , column = 0 , columnspan = 8 , padx = 4 , pady = int(self.main_hgt*0.02))
        self.frm_stk_sug_2.pack(padx = 4 , pady = 4)
        
        #----------------------------------------prod_stock toplevel ends here-------------------------------------------------------------------#
        
        #----------------------------------------purchase_detail_toplevel------------------------------------------------#
        self.frm_pur_details = ttk.Frame( self.root_frame , height = self.main_hgt*0.5 , width = self.main_wdt*0.4) #to give white border
        self.frm_pur_details.pack_propagate(False)

        self.frm_pur_details_2 = ttk.Frame( self.frm_pur_details , height = self.main_hgt*0.5-8 , width = self.main_wdt*0.4-8 , style = "root_menu.TFrame")
        self.frm_pur_details_2.grid_propagate(False)




        self.lbl_sup = ttk.Label(self.frm_pur_details_2 , text = "Supplier      :" , style = "window_title.TLabel")
        self.lbl_sup_gst_txt = ttk.Label(self.frm_pur_details_2 , text = "Supplier GST  :" , style = "window_title.TLabel")
        self.lbl_tax_meth = ttk.Label(self.frm_pur_details_2 , text = "Tax Method    :" , style = "window_title.TLabel")
        self.lbl_firm_name = ttk.Label(self.frm_pur_details_2 , text = "Firm          :" , style = "window_title.TLabel")
        self.lbl_firm_gst_txt = ttk.Label(self.frm_pur_details_2 , text = "Firm GST      :" , style = "window_title.TLabel")
        self.lbl_pur_date = ttk.Label(self.frm_pur_details_2 , text = "Date          :" , style = "window_title.TLabel")
        self.lbl_inv_no = ttk.Label(self.frm_pur_details_2 , text = "Invoice No    :" , style = "window_title.TLabel")
        
        self.combo_supplier = ttk.Combobox(self.frm_pur_details_2 , validate="key", validatecommand=(validations[4], '%P') , state = con.DISABLED , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30 , style = "window_combo.TCombobox") 
        self.combo_supplier.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_supplier.bind("<<ComboboxSelected>>" , self.get_sup_gst)
        self.combo_supplier.bind("<Escape>" , self.destroy_pur_details)
        self.combo_supplier.bind("<Down>" , self.get_suppliers)
        self.combo_supplier.bind("<Button-1>" , self.get_suppliers)
        self.combo_supplier.bind("<KeyRelease>" , self.delete_gstno)

        self.lbl_sup_gst = ttk.Label(self.frm_pur_details_2  , width = 30 , style = "window_lbl_ent.TLabel")

        self.combo_tax_meth = ttk.Combobox(self.frm_pur_details_2 , values = ['In-State' , 'Out-Of-State'] , state = "readonly" ,font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30 , style = "window_combo.TCombobox") 
        self.combo_tax_meth.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_tax_meth.bind("<<ComboboxSelected>>" , self.tax_meth_changed)
        self.combo_tax_meth.bind("<Escape>" , self.destroy_pur_details)

        self.combo_firms = ttk.Combobox(self.frm_pur_details_2 , validate="key", validatecommand=(validations[4], '%P') , state = "readonly" , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30 , style = "window_combo.TCombobox") 
        self.combo_firms.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_firms.bind("<<ComboboxSelected>>" , self.get_firm_gst)
        self.combo_firms.bind("<Escape>" , self.destroy_pur_details)
        self.combo_firms.bind("<Down>" , self.get_firms)
        self.combo_firms.bind("<Button-1>" , self.get_firms)

        self.lbl_firm_gst = ttk.Label(self.frm_pur_details_2  , width = 30 , style = "window_lbl_ent.TLabel")

        self.ent_pur_date = ttk.Entry(self.frm_pur_details_2  , width = 30 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_pur_date.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_pur_date.bind("<Escape>" , self.destroy_pur_details)

        self.ent_inv_no = ttk.Entry(self.frm_pur_details_2  , width = 30 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) )
        self.ent_inv_no.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_inv_no.bind("<Escape>" , self.destroy_pur_details)
        self.ent_inv_no.bind("<Return>" ,self.edit_invoice)

        self.btn_cancel_pur = ttk.Button(self.frm_pur_details_2 , text = "Cancel" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.cancel(None))
        self.btn_cancel_pur.bind("<Return>" , self.cancel)

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
        self.btn_cancel_pur.grid(row = 7 , column = 1, sticky = con.W)

        self.frm_pur_details_2.pack(anchor = con.CENTER , pady = 4)
        #----------------------------------------purchase_detail_toplevel Ends here------------------------------------------------#


        #----------------------------------------ROW 1 Items-----------------------------------------------------------------------#
        self.frm_row1 = ttk.Frame( self.main_frame  , style = "root_main.TFrame")
        self.frm_row1.grid_propagate(True)

        self.lbl_bar = ttk.Label(self.frm_row1 , text = "Barcode"  , style = "window_text_medium.TLabel")
        self.ent_bar = ttk.Entry(self.frm_row1  , width = 13 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[3], '%P'))
        self.ent_bar.bind('<FocusIn>' , self.clear_prod_bar_name)
        self.ent_bar.bind('<Return>' , self.get_prod_by_bar)

        self.lbl_name = ttk.Label(self.frm_row1 , text = "Product Name" , style = "window_text_medium.TLabel")
        self.ent_name = ttk.Entry(self.frm_row1  , width = 30 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[4], '%P'))
        self.ent_name.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_name.bind('<KeyRelease>' , self.get_prod_list)
        self.ent_name.bind('<Down>' , self.focus_prod_list)
        self.ent_name.bind('<Escape>' , self.forget_prod_list)
        self.ent_name.bind('<Shift-Tab>' , self.forget_prod_list)

        self.lbl_taxes = ttk.Label(self.frm_row1 , text = "Tax" , style = "window_text_medium.TLabel")
        self.ent_gst = ttk.Entry(self.frm_row1  , width = 3 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[6], '%P'))
        self.ent_cess = ttk.Entry(self.frm_row1  , width = 3 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[6], '%P'))

        self.lbl_qty = ttk.Label(self.frm_row1 , text = "QTY"  , style = "window_text_medium.TLabel")
        self.ent_qty = ttk.Entry(self.frm_row1  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_qty.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_qty.bind('<KeyRelease>' , self.cal_by_qty)

        self.lbl_cost = ttk.Label(self.frm_row1 , text = "Cost"  , style = "window_text_medium.TLabel")
        self.ent_cost = ttk.Entry(self.frm_row1  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_cost.bind('<KeyRelease>' , self.cal_by_cp)
        self.ent_cost.bind('<FocusOut>' , self.combo_entry_out)

        self.lbl_txb = ttk.Label(self.frm_row1 , text = "Taxble"  , style = "window_text_medium.TLabel")
        self.ent_txb = ttk.Entry(self.frm_row1  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_txb.bind('<KeyRelease>' , self.cal_by_taxbl)
        self.ent_txb.bind('<FocusOut>' , self.combo_entry_out)


        self.lbl_cost_ttl = ttk.Label(self.frm_row1 , text = "TTL Cost"  , style = "window_text_medium.TLabel")
        self.ent_cost_ttl = ttk.Entry(self.frm_row1  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_cost_ttl.bind('<KeyRelease>' , self.cal_by_tcp)
        self.ent_cost_ttl.bind('<FocusOut>' , self.combo_entry_out)


        self.lbl_txb_ttl = ttk.Label(self.frm_row1 , text = "TTL Txbl"  , style = "window_text_medium.TLabel")
        self.ent_txb_ttl = ttk.Entry(self.frm_row1  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_txb_ttl.bind('<KeyRelease>' , self.cal_by_tot_taxbl)
        self.ent_txb_ttl.bind('<FocusOut>' , self.combo_entry_out)


        self.lbl_tax_ttl_txt = ttk.Label(self.frm_row1 , text = "  TTL Tax"  , style = "window_text_medium.TLabel")
        self.ent_gst_ttl = ttk.Entry(self.frm_row1  , width = 8 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_cess_ttl = ttk.Entry(self.frm_row1  , width = 8 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))

        self.lbl_pro_per = ttk.Label(self.frm_row1 , text = "Profit%"  , style = "window_text_medium.TLabel")
        self.ent_pro_per = ttk.Entry(self.frm_row1  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_pro_per.bind('<KeyRelease>' , self.cal_sp)
        self.ent_pro_per.bind('<FocusOut>' , self.combo_entry_out)


        
        self.lbl_bar.grid(row = 0 , column = 0 , sticky =con.W )
        self.lbl_name.grid(row = 0 , column = 1, sticky =con.W)
        self.lbl_taxes.grid(row = 0 , column = 2, sticky =con.W , columnspan = 2)
        self.lbl_qty.grid(row = 0 , column = 4, sticky =con.W)
        self.lbl_cost.grid(row = 0 , column = 5, sticky =con.W)
        self.lbl_txb.grid(row = 0 , column =6, sticky =con.W)
        self.lbl_cost_ttl.grid(row = 0 , column = 7, sticky =con.W)
        self.lbl_txb_ttl.grid(row = 0 , column = 8, sticky =con.W)
        self.lbl_tax_ttl_txt.grid(row = 0 , column = 9, sticky =con.W , columnspan = 2)
        self.lbl_pro_per.grid(row = 0 , column = 11, sticky =con.W)

        self.ent_bar.grid(row = 1 , column = 0, sticky = con.W)
        self.ent_name.grid(row = 1 , column = 1, sticky = con.W)
        self.ent_gst.grid(row = 1 , column = 2, sticky = con.W)
        self.ent_cess.grid(row = 1 , column = 3, sticky = con.W)
        self.ent_qty.grid(row = 1 , column = 4, sticky = con.W)
        self.ent_cost.grid(row = 1 , column = 5, sticky = con.W)
        self.ent_txb.grid(row = 1 , column = 6, sticky =con.W)
        self.ent_cost_ttl.grid(row = 1 , column = 7, sticky = con.W)
        self.ent_txb_ttl.grid(row = 1 , column = 8, sticky = con.W)
        self.ent_gst_ttl.grid(row = 1 , column = 9, sticky = con.W)
        self.ent_cess_ttl.grid(row = 1 , column = 10, sticky = con.W)
        self.ent_pro_per.grid(row = 1 , column = 11, sticky = con.W)


        #----------------------------------------ROW 1 Items Ends here-----------------------------------------------------------------------#

        #----------------------------------------ROW 2 items --------------------------------------------------------------------------------#
        self.frm_row2 = ttk.Frame( self.main_frame  , style = "root_main.TFrame")
        self.frm_row2.grid_propagate(True)


        self.lbl_nml_txt = ttk.Label(self.frm_row2 , text = "NML"  , style = "window_text_medium.TLabel")
        self.lbl_nml1 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_nml2 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_nml3 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_nml4 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")

        self.ent_nml1 = ttk.Entry(self.frm_row2 , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_nml1.bind('<Down>' , self.select_first_stock)
        self.ent_nml1.bind('<KeyRelease>' , self.cal_pro_per)
        self.ent_nml1.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_nml1.bind('<Control-s>' , self.cal_price)
        self.ent_nml1.bind('<Control-S>' , self.cal_price)
        self.ent_nml1.bind('<Return>' , self.selling_price_filler)

        self.ent_nml2 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_nml2.bind('<Down>' , self.select_first_stock)
        self.ent_nml2.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_nml2.bind('<Control-s>' , self.cal_price)
        self.ent_nml2.bind('<Control-S>' , self.cal_price)
        self.ent_nml2.bind('<Return>' , self.selling_price_filler)

        self.ent_nml3 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_nml3.bind('<Down>' , self.select_first_stock)
        self.ent_nml3.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_nml3.bind('<Control-s>' , self.cal_price)
        self.ent_nml3.bind('<Control-S>' , self.cal_price)
        self.ent_nml3.bind('<Return>' , self.selling_price_filler)

        self.ent_nml4 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_nml4.bind('<Down>' , self.select_first_stock)
        self.ent_nml4.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_nml4.bind('<Control-s>' , self.cal_price)
        self.ent_nml4.bind('<Control-S>' , self.cal_price)
        self.ent_nml4.bind('<Return>' , self.selling_price_filler)


        self.lbl_htl_txt = ttk.Label(self.frm_row2 , text = " HTL"  , style = "window_text_medium.TLabel")
        self.lbl_htl1 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_htl2 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_htl3 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_htl4 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")

        self.ent_htl1 = ttk.Entry(self.frm_row2 , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_htl1.bind('<Down>' , self.select_first_stock)
        self.ent_htl1.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_htl1.bind('<Return>' , self.selling_price_filler)
        self.ent_htl1.bind('<Control-s>' , self.cal_price)
        self.ent_htl1.bind('<Control-S>' , self.cal_price)

        self.ent_htl2 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_htl2.bind('<Down>' , self.select_first_stock)
        self.ent_htl2.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_htl2.bind('<Return>' , self.selling_price_filler)
        self.ent_htl2.bind('<Control-s>' , self.cal_price)
        self.ent_htl2.bind('<Control-S>' , self.cal_price)

        self.ent_htl3 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_htl3.bind('<Down>' , self.select_first_stock)
        self.ent_htl3.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_htl3.bind('<Return>' , self.selling_price_filler)
        self.ent_htl3.bind('<Control-s>' , self.cal_price)
        self.ent_htl3.bind('<Control-S>' , self.cal_price)

        self.ent_htl4 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_htl4.bind('<Down>' , self.select_first_stock)
        self.ent_htl4.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_htl4.bind('<Return>' , self.selling_price_filler)
        self.ent_htl4.bind('<Control-s>' , self.cal_price)
        self.ent_htl4.bind('<Control-S>' , self.cal_price)

        self.lbl_spl_txt = ttk.Label(self.frm_row2 , text = " SPL"  , style = "window_text_medium.TLabel")
        self.lbl_spl1 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_spl2 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_spl3 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_spl4 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")

        self.ent_spl1 = ttk.Entry(self.frm_row2 , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_spl1.bind('<Down>' , self.select_first_stock)
        self.ent_spl1.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_spl1.bind('<Return>' , self.selling_price_filler)
        self.ent_spl1.bind('<Control-s>' , self.cal_price)
        self.ent_spl1.bind('<Control-S>' , self.cal_price)

        self.ent_spl2 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_spl2.bind('<Down>' , self.select_first_stock)
        self.ent_spl2.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_spl2.bind('<Return>' , self.selling_price_filler)
        self.ent_spl2.bind('<Control-s>' , self.cal_price)
        self.ent_spl2.bind('<Control-S>' , self.cal_price)

        self.ent_spl3 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_spl3.bind('<Down>' , self.select_first_stock)
        self.ent_spl3.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_spl3.bind('<Return>' , self.selling_price_filler)
        self.ent_spl3.bind('<Control-s>' , self.cal_price)
        self.ent_spl3.bind('<Control-S>' , self.cal_price)

        self.ent_spl4 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_spl4.bind('<Down>' , self.select_first_stock)
        self.ent_spl4.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_spl4.bind('<Return>' , self.selling_price_filler)
        self.ent_spl4.bind('<Control-s>' , self.cal_price)
        self.ent_spl4.bind('<Control-S>' , self.cal_price)

        self.lbl_ang_txt = ttk.Label(self.frm_row2 , text = " ANG"  , style = "window_text_medium.TLabel")
        self.lbl_ang1 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_ang2 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_ang3 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")
        self.lbl_ang4 = ttk.Label(self.frm_row2  , width = 6 , style = "window_lbl_ent.TLabel")

        self.ent_ang1 = ttk.Entry(self.frm_row2 , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_ang1.bind('<Down>' , self.select_first_stock)
        self.ent_ang1.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_ang1.bind('<Return>' , self.selling_price_filler)
        self.ent_ang1.bind('<Control-s>' , self.cal_price)
        self.ent_ang1.bind('<Control-S>' , self.cal_price)

        self.ent_ang2 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_ang2.bind('<Down>' , self.select_first_stock)
        self.ent_ang2.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_ang2.bind('<Return>' , self.selling_price_filler)
        self.ent_ang2.bind('<Control-s>' , self.cal_price)
        self.ent_ang2.bind('<Control-S>' , self.cal_price)

        self.ent_ang3 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_ang3.bind('<Down>' , self.select_first_stock)
        self.ent_ang3.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_ang3.bind('<Return>' , self.selling_price_filler)
        self.ent_ang3.bind('<Control-s>' , self.cal_price)
        self.ent_ang3.bind('<Control-S>' , self.cal_price)

        self.ent_ang4 = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_ang4.bind('<Down>' , self.select_first_stock)
        self.ent_ang4.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_ang4.bind('<Return>' , self.enter_to_treeview)
        self.ent_ang4.bind('<Control-s>' , self.cal_price)
        self.ent_ang4.bind('<Control-S>' , self.cal_price)

        self.lbl_exp = ttk.Label(self.frm_row2 , text = "EXP"  , style = "window_text_medium.TLabel")
        self.ent_exp = ttk.Entry(self.frm_row2  , width = 6 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[6], '%P'))
        self.ent_exp.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_exp.bind('<Return>' , self.selling_price_filler)


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
        self.frm_row3 = ttk.Frame( self.main_frame  , style = "root_menu.TFrame" , height = int(self.main_hgt * 0.315) , width = int(self.main_wdt * 0.995))
        if self.root.winfo_screenheight() < 1000: self.frm_tree_old_stock.config( height = int(self.main_hgt*0.3)) 
        self.frm_row3.pack_propagate(False)
        
        self.tree_pur = ttk.Treeview(self.frm_row3 ,selectmode = "browse", takefocus = True , show = "headings" , style = "window.Treeview")
        self.tree_pur.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree_pur.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.scroll_y_pur = ttk.Scrollbar(self.frm_row3 , orient = con.VERTICAL , command = self.tree_pur.yview)
        self.scroll_x_pur = ttk.Scrollbar(self.frm_row3 , orient = con.HORIZONTAL , command = self.tree_pur.xview)
        self.tree_pur.config(yscrollcommand = self.scroll_y_pur.set , xscrollcommand = self.scroll_x_pur.set)

        

        self.tree_pur['columns'] = ('sl_no','name','gstPer','cp','qty','ttp','tcp','nml1','nml2','nml3','nml4','htl1','htl2','htl3','htl4','spl1','spl2','spl3','spl4','ang1','ang2','ang3','ang4')
        self.tree_pur.heading('sl_no' , text = 'NO')
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
        self.tree_pur.column('sl_no' , width = int(self.tree_pur_wdt*0.033) , anchor = "w")
        self.tree_pur.column('name' , width = int(self.tree_pur_wdt*0.35) , minwidth = int(self.tree_pur_wdt*0.01) , anchor = "w")
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


        self.tree_pur.bind('<Double-Button-1>',self.select_from_treeview)
        self.tree_pur.bind('<Return>',self.select_from_treeview)
        self.tree_pur.bind('<Delete>', self.delete_from_treeview)

        self.scroll_y_pur.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x_pur.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        self.tree_pur.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)


        #----------------------------------------ROW 3 items ends here-----------------------------------------------------------------------#

        #----------------------------------------ROW 4 items --------------------------------------------------------------------------------#
        self.frm_row4 = ttk.Frame( self.main_frame  , style = "root_main.TFrame" , height = int(self.main_hgt * 0.33) , width = int(self.main_wdt * 0.985) )
        self.frm_row4.pack_propagate(False)



        self.tree_frame_gst = ttk.Frame(self.frm_row4 , height = int(self.main_hgt * 0.3) , width = int(self.main_wdt * 0.33) , style = "root_menu.TFrame")
        self.tree_frame_gst.pack_propagate(False)
        self.tree_gst = ttk.Treeview(self.tree_frame_gst ,selectmode = "none", takefocus = True , show = "headings" , style = "window.Treeview")
        self.tree_gst.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree_gst.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.scroll_y_gst = ttk.Scrollbar(self.tree_frame_gst , orient = con.VERTICAL , command = self.tree_gst.yview)
        self.tree_gst.config(yscrollcommand = self.scroll_y_gst.set)

        self.tree_gst['columns'] = ('gstPer','sgst','cgst','igst')
        self.tree_gst.heading('gstPer' , text = 'GST %')
        self.tree_gst.heading('sgst' , text = 'SGST')
        self.tree_gst.heading('cgst' , text = 'CGST')
        self.tree_gst.heading('igst' , text = 'IGST')
        
        self.tree_gst_wdt = self.tree_frame_gst.winfo_reqwidth()-self.scroll_y_gst.winfo_reqwidth()
        self.tree_gst.column('gstPer' , width = int(self.tree_gst_wdt*0.25) ,minwidth = int(self.tree_gst_wdt*0.25) , anchor = "w")
        self.tree_gst.column('sgst' , width = int(self.tree_gst_wdt*0.25) ,minwidth = int(self.tree_gst_wdt*0.25) , anchor = "e")
        self.tree_gst.column('cgst' , width = int(self.tree_gst_wdt*0.25) ,minwidth = int(self.tree_gst_wdt*0.25) , anchor = "e")
        self.tree_gst.column('igst' , width = int(self.tree_gst_wdt*0.25) ,minwidth = int(self.tree_gst_wdt*0.25) , anchor = "e")
        
        self.scroll_y_gst.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.tree_gst.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)





        self.tree_frame_cess = ttk.Frame(self.frm_row4 , height = int(self.main_hgt * 0.3) , width = int(self.main_wdt * 0.165) , style = "root_menu.TFrame")
        self.tree_frame_cess.pack_propagate(False)
        self.tree_cess = ttk.Treeview(self.tree_frame_cess ,selectmode = "none", takefocus = True , show = "headings" , style = "window.Treeview")
        self.tree_cess.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree_cess.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.scroll_y_cess = ttk.Scrollbar(self.tree_frame_cess , orient = con.VERTICAL , command = self.tree_cess.yview)
        self.tree_cess.config(yscrollcommand = self.scroll_y_cess.set)

        self.tree_cess['columns'] = ('cessPer','amt')
        self.tree_cess.heading('cessPer' , text = 'CESS %')
        self.tree_cess.heading('amt' , text = 'AMT')
        
        self.tree_cess_wdt = self.tree_frame_cess.winfo_reqwidth()-self.scroll_y_cess.winfo_reqwidth()
        self.tree_cess.column('cessPer' , width = int(self.tree_cess_wdt*0.5) ,minwidth = int(self.tree_cess_wdt*0.5) , anchor = "w")
        self.tree_cess.column('amt' , width = int(self.tree_cess_wdt*0.5) ,minwidth = int(self.tree_cess_wdt*0.5) , anchor = "e")
        
        self.scroll_y_cess.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.tree_cess.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)





        self.frm_totals = ttk.Frame( self.frm_row4  , style = "root_main.TFrame")
        self.frm_totals.grid_propagate(True)
        self.lbl_tot_txbl_txt = ttk.Label(self.frm_totals , text = "TTL Taxbl  :"  , style = "window_text_medium.TLabel")
        self.lbl_tot_txbl = ttk.Label(self.frm_totals  , width = 11 , style = "window_lbl_ent.TLabel")

        self.lbl_tot_tax_txt = ttk.Label(self.frm_totals , text = "TTL Tax    :"  , style = "window_text_medium.TLabel")
        self.lbl_tot_tax = ttk.Label(self.frm_totals  , width = 11 , style = "window_lbl_ent.TLabel")

        self.lbl_tot_amt_txt = ttk.Label(self.frm_totals , text = "TTL Amount :"  , style = "window_text_medium.TLabel")
        self.lbl_tot_amt = ttk.Label(self.frm_totals  , width = 11 , style = "window_lbl_ent.TLabel")

        self.lbl_cp_filler = ttk.Label(self.frm_totals  , width = 11 , style = "window_lbl_ent.TLabel")

        self.lbl_tot_exp = ttk.Label(self.frm_totals , text = "   TTL Expense :"  , style = "window_text_medium.TLabel")
        self.ent_tot_exp = ttk.Entry(self.frm_totals , width = 11 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[2], '%P'))
        self.ent_tot_exp.bind('<KeyRelease>' , self.cal_expense)
        self.ent_tot_exp.bind('<FocusOut>' , self.combo_entry_out)

        self.lbl_grd_tot_txt = ttk.Label(self.frm_totals , text = "   Grand Total :"  , style = "window_text_medium.TLabel")
        self.lbl_grd_tot = ttk.Label(self.frm_totals  , width = 11 , style = "window_lbl_ent.TLabel")

        self.tree_frame_gst.pack(side = con.LEFT)
        self.tree_frame_cess.pack(side = con.LEFT,  padx = int(self.main_wdt*0.006))


        self.lbl_tot_txbl_txt.grid(row = 0 , column = 0) 
        self.lbl_tot_txbl.grid(row = 0 , column = 1)
        self.lbl_tot_tax_txt.grid(row = 1 , column = 0 , pady = int(self.main_hgt*0.06))
        self.lbl_tot_tax.grid(row = 1 , column = 1)
        self.lbl_tot_amt_txt.grid(row = 2 , column = 0)
        self.lbl_tot_amt.grid(row = 2 , column = 1)
        self.lbl_cp_filler.grid(row = 0 , column = 4)
        self.lbl_tot_exp.grid(row = 1 , column = 3)
        self.ent_tot_exp.grid(row = 1 , column = 4)
        self.lbl_grd_tot_txt.grid(row = 2 , column = 3)
        self.lbl_grd_tot.grid(row = 2 , column = 4)
        
        self.frm_totals.pack(side = con.RIGHT)

        #----------------------------------------ROW 4 items ends here-----------------------------------------------------------------------#

        #----------------------------------------ROW 4 items --------------------------------------------------------------------------------#
        self.frm_row5 = ttk.Frame( self.main_frame  , style = "root_main.TFrame" , width = self.main_wdt , height = int(self.main_hgt*0.05))
        self.frm_row5.pack_propagate(False)

        self.frm_gst_tot = ttk.Frame( self.frm_row5  , style = "root_main.TFrame")
        self.lbl_tot_gst = ttk.Label(self.frm_gst_tot , text = "TOTALS : "  , style = "window_text_medium.TLabel")
        self.lbl_tot_cgst = ttk.Label(self.frm_gst_tot  , width = 10 , style = "window_lbl_ent.TLabel" , justify = con.RIGHT)
        self.lbl_tot_sgst = ttk.Label(self.frm_gst_tot  , width = 10 , style = "window_lbl_ent.TLabel", justify = con.LEFT)
        self.lbl_tot_igst = ttk.Label(self.frm_gst_tot  , width = 10 , style = "window_lbl_ent.TLabel", justify = con.LEFT)

        self.lbl_tot_gst.grid(row = 0 , column = 0)
        self.lbl_tot_cgst.grid(row = 0 , column = 1 , padx = int(self.main_wdt*0.005))
        self.lbl_tot_sgst.grid(row = 0 , column = 2 )
        self.lbl_tot_igst.grid(row = 0 , column = 3 , padx = int(self.main_wdt*0.005))


        self.frm_cess_tot = ttk.Frame( self.frm_row5  , style = "root_main.TFrame")
        self.lbl_tot_cess_txt = ttk.Label(self.frm_cess_tot , text = "  CESS   :"  , style = "window_text_medium.TLabel", justify = con.RIGHT)
        self.lbl_tot_cess = ttk.Label(self.frm_cess_tot  , width = 10 , style = "window_lbl_ent.TLabel")
        
        self.lbl_tot_cess_txt.grid(row = 0 , column = 0)
        self.lbl_tot_cess.grid(row = 0 , column = 1 , padx = int(self.main_wdt*0.005) )

        self.frm_amt_paid = ttk.Frame( self.frm_row5  , style = "root_main.TFrame") 
        self.lbl_full_paid = ttk.Label(self.frm_amt_paid , text = "        "  , style = "window_text_medium.TLabel")
        self.chk_full_paid = ttk.Checkbutton(self.frm_amt_paid  , state = con.DISABLED, text = "Paid :",  style = "window_check.TCheckbutton" , variable = self.check_state , onvalue = 'True' , offvalue = 'False' , command = self.full_paid)
        self.ent_amt_paid = ttk.Entry(self.frm_amt_paid , width = 11 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_amt_paid.bind('<FocusOut>' , self.combo_entry_out)

        self.lbl_full_paid.grid(row = 0 , column = 0)
        self.chk_full_paid.grid(row = 0 , column = 1)
        self.ent_amt_paid.grid(row = 0 , column = 2)

        self.frm_pay_meth = ttk.Frame( self.frm_row5  , style = "root_main.TFrame") 
        self.lbl_pay_meth = ttk.Label(self.frm_pay_meth , text = "       Payment Mode :"  , style = "window_text_medium.TLabel")
        self.combo_pay_meth = ttk.Combobox(self.frm_pay_meth  , text = 'CASH' , values = ['CASH' , 'UPI/NEFT'] , state = "readonly" ,font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 10 , style = "window_combo.TCombobox") 
        self.combo_pay_meth.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_pay_meth.grid(row = 0 , column = 0)
        self.combo_pay_meth.grid(row = 0 , column = 1)

        



        self.frm_gst_tot.pack(side = con.LEFT)
        self.frm_cess_tot.pack(side = con.LEFT)
        self.frm_pay_meth.pack(side = con.LEFT)
        self.frm_amt_paid.pack(side = con.LEFT)
        if self.root.winfo_screenheight()>1000:self.frm_amt_paid.pack(side = con.LEFT , padx = int(self.main_wdt*0.005))
        
        
        


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
        self.frm_row5.grid(row = 4 , column = 0 , pady = int(self.main_wdt*0.004) )
        self.btn_frame.grid(row = 5 ,column = 0 , sticky = con.E , pady = int(self.main_wdt*0.004))


        #------temporary settings-------#
        
        #self.btn_edit.invoke() 
        
        #self.destroy_pur_details(None)
        #self.ent_bar.focus_set()
        #-temporary settings ends here--#

        self.i = 0

        @self.sio.on('hello')
        def hello():
            print('I received a message!')

    def combo_entry_out(self , e):
        e.widget.select_clear()

    """--------------------------Purchase detail functions-----------------------------------------------"""
    def enable_pur_details(self) :
        self.combo_supplier.config(state = con.NORMAL)
        self.combo_firms.config(state = con.NORMAL)
        self.ent_pur_date.config(state = con.NORMAL)
        self.ent_inv_no.config(state = con.NORMAL)
    
    def clear_pur_details(self):
        self.combo_supplier.delete(0,con.END)
        self.lbl_sup_gst.config(text = "")
        self.lbl_firm_gst.config(text = "")
        self.combo_tax_meth.config(state = con.NORMAL)
        self.combo_tax_meth.delete(0,con.END)
        self.combo_tax_meth.config(state = "readonly")
        self.combo_firms.config(state = con.NORMAL)
        self.combo_firms.delete(0,con.END)
        self.combo_firms.config(state = "readonly")
        self.ent_pur_date.delete(0,con.END)
        self.ent_inv_no.delete(0,con.END)

    def disable_pur_details(self):
        self.combo_supplier.config(state = con.DISABLED)
        self.combo_firms.config(state = con.DISABLED)
        self.ent_pur_date.config(state = con.DISABLED)
        self.ent_inv_no.config(state = con.DISABLED)

    def show_pur_details(self , e):
        #self.btn_add_dets.config(state = con.DISABLED)
        self.frm_pur_details.place( x = self.main_wdt*0.25 , y = self.main_hgt*0.3)
        self.frm_pur_details.lift()
        self.combo_supplier.focus_set()
        self.disable_all()

    def destroy_pur_details(self , e):
        

        sup_name = self.combo_supplier.get().upper()
        sup_gst = self.lbl_sup_gst.cget("text")
        self.selected_tax_meth = self.combo_tax_meth.get()
        firm_name = self.combo_firms.get().upper()
        firm_gst = self.lbl_firm_gst.cget("text")
        date = self.ent_pur_date.get().upper()
        inv_no = self.ent_inv_no.get().upper()

        

        if sup_gst == "" or self.selected_tax_meth == "" or date == "" or inv_no == "" :
            msg.showinfo( "Info" , "Enter all Purchase details")
            return

        if sup_gst == 'CASH' and firm_gst != '':
            msg.showinfo("Info" , "Select cash firsm for cash purchase")
            self.combo_firms.focus_set()
            return

        date1 = date.split("/")
        if len(date1)!=3:
            date1 = date.split("-")
            if len(date1) != 3:
                msg.showinfo("Info" , "Enter date in following format \n 'dd-mm-yy' or 'dd/mm/yy ")
                return

        try:
            datetime.datetime(int(date1[2]), int(date1[1]), int(date1[0]))
        except ValueError:
            msg.showinfo("Info" , "Enter correct date")
            self.ent_pur_date.focus_set()
            self.ent_pur_date.select_range(0,con.END)
            return

        
        if len(date1[2])%2 !=0 :
            msg.showinfo("Info" , "Enter correct date")
            self.ent_pur_date.focus_set()
            self.ent_pur_date.select_range(0,con.END)
            return

        if len(date1[0]) == 1:
            date1[0] = '0' + date1[0]

        if len(date1[1]) == 1:
            date1[1] = '0' + date1[1]    

        if len(date1[2]) == 2:
            date1[2] = '20' + date1[2]    

        
    
        if int(datetime.date.today().strftime("%m")) != int(date1[1]) or int(datetime.date.today().strftime("%Y")) != int(date1[2]) :
            ans = msg.askyesno("Info" , "Entered date does not sync with system date\nDo you want to continue?")
            if not ans:
                self.ent_pur_date.focus_set()
                self.ent_pur_date.select_range(0,con.END)
                return

        self.ent_pur_date.delete(0,con.END)
        self.ent_pur_date.insert(0,date1[0] + "-" + date1[1] + "-" + date1[2])
    
        #self.sio.emit("hello")
        
        

        
        params = {
                    "sup_name" : sup_name,
                    "tax_method" : self.selected_tax_meth,
                    "firm_name" : firm_name,
                    "date" : date,
                    "inv_no" : inv_no,
                    "year"  : self.year, 
                    "productsAdded" : False,
                    "editState"  :   False

        }
       
        
        if len(self.added_products) > 0:
            params['productsAdded'] = True 

        if self.edit_state:
            params['editState'] = True            


        
        
        res = get("http://"+self.ip+":5000/purchases/addEditPurDetails"  , params = params)
        
        #treomove if 
        #remove
        #temporary
        if res.status_code == 201:
            msg.showerror("Error" , "This invoice is currently being added")
            return
        if res.status_code == 202:
            msg.showerror("Error" , "This invoice has already been added")
            self.ent_inv_no.select_range(0,con.END)
            self.ent_inv_no.focus_set()
            return

       


        self.frm_pur_details.place_forget()
        self.enable_all()
        self.ent_bar.focus_set()

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
            self.combo_tax_meth.focus_set()

    def get_firms(self,e):
        text = self.combo_firms.get()
        sql = "select firm_name from somanath.firms"
        if self.tax_check:
            sql += " where firm_tax != 'CASH' order by firm_name"


        

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
            self.ent_pur_date.focus_set()

    def delete_gstno(self , e):
        self.lbl_sup_gst.config(text = "")

    def tax_meth_changed(self , e):
        
        if self.added_products != []:
            self.combo_tax_meth.config(state = con.NORMAL)
            meth = self.combo_tax_meth.get()
            self.combo_tax_meth.delete(0,con.END)
            self.combo_tax_meth.insert(0,self.selected_tax_meth)
            self.combo_tax_meth.config(state = "readonly")
            if meth != self.selected_tax_meth:
                msg.showerror("Error" , "Donot change tax method")
            
    def full_paid(self):
        self.ent_amt_paid.delete(0,con.END)
        if self.chk_full_paid.instate(['selected']) == True:
            self.ent_amt_paid.insert(0 , self.lbl_grd_tot.cget("text"))

    """--------------------------Purchase detail functions-----------------------------------------------"""


    """--------------------------Calcualtion functions---------------------------------------------------"""
    def cal_by_qty(self,e):
        if not (e.keycode == 8 or e.keysym in ['0' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '0'] or e.keycode == 190):
            return

        qty = self.ent_qty.get()
        cp = self.ent_cost.get()
        taxbl = self.ent_txb.get()
        tot_cost = self.ent_cost_ttl.get()
        tot_taxbl = self.ent_txb_ttl.get()
        gst_per = float(self.ent_gst.get())
        cess_per = float(self.ent_cess.get())
        ttp = gst_per+cess_per

        if qty == "" or qty == ".":
            self.ent_gst_ttl.config(state = con.NORMAL)
            self.ent_cess_ttl.config(state = con.NORMAL)
            self.ent_cost.delete(0,con.END)
            self.ent_txb.delete(0,con.END)
            self.ent_cost_ttl.delete(0,con.END)
            self.ent_txb_ttl.delete(0,con.END)
            self.ent_gst_ttl.delete(0,con.END)
            self.ent_cess_ttl.delete(0,con.END)
            self.ent_gst_ttl.config(state = con.DISABLED)
            self.ent_cess_ttl.config(state = con.DISABLED)
            return

        qty = float(qty)
        
    
        if cp != "" and cp != ".":
            cp = float(cp)
            taxbl = cp/(1+ttp/100)
            tot_tax = (cp - taxbl) * qty
           
            if gst_per == 0 and cess_per == 0: 
                tot_gst = 0
                tot_cess = 0

            if gst_per == 0 and cess_per != 0:
                tot_gst = 0
                tot_cess = tot_tax 

            if gst_per != 0 and cess_per == 0:
                tot_cess = 0
                tot_gst =  tot_tax 

            if gst_per != 0 and cess_per != 0:
                tot_cess = tot_tax * (cess_per/ttp)
                tot_gst = tot_tax * (gst_per/ttp)

            tot_cost = cp*qty
            tot_taxbl = taxbl*qty


        elif taxbl != "" and taxbl != ".":
            taxbl = float(taxbl)
            cp = taxbl + (gst_per/100 * taxbl) + (cess_per/100 * taxbl)
            tot_cost = cp * qty
            tot_taxbl = taxbl * qty 
            tot_gst = gst_per/100 * taxbl * qty
            tot_cess = cess_per/100 * taxbl * qty

        elif tot_cost != "" and tot_cost != ".":
            tot_cost = float(tot_cost)
            cp = tot_cost/qty
            taxbl = cp/(1+ttp/100)
            tot_tax = (cp - taxbl) *qty

            if gst_per == 0 and cess_per == 0: 
                tot_gst = 0
                tot_cess = 0
            if gst_per == 0 and cess_per != 0:
                tot_gst = 0
                tot_cess =  tot_tax 
            if gst_per != 0 and cess_per == 0:
                tot_cess = 0
                tot_gst =  tot_tax 

            if gst_per != 0 and cess_per != 0:
                tot_cess = tot_tax * (cess_per/ttp)
                tot_gst = tot_tax * (gst_per/ttp)

            tot_taxbl = taxbl*qty

        elif tot_taxbl != "" and tot_taxbl != ".":
            tot_taxbl = float(tot_taxbl)
            taxbl = tot_taxbl / qty
            cp = taxbl + (gst_per/100 * taxbl) + (cess_per/100 * taxbl)
            tot_cost = cp * qty
            tot_gst = gst_per/100 * taxbl * qty
            tot_cess = cess_per/100 * taxbl * qty

        else:
            return


        self.ent_gst_ttl.config(state = con.NORMAL)
        self.ent_cess_ttl.config(state = con.NORMAL)

        self.ent_cost.delete(0,con.END)
        self.ent_txb.delete(0,con.END)
        self.ent_cost_ttl.delete(0,con.END)
        self.ent_txb_ttl.delete(0,con.END)
        self.ent_gst_ttl.delete(0,con.END)
        self.ent_cess_ttl.delete(0,con.END)
        
        self.ent_cost.insert(0, "{:.2f}".format(cp))
        self.ent_txb.insert(0, "{:.2f}".format(taxbl))
        self.ent_cost_ttl.insert(0, "{:.2f}".format(tot_cost))
        self.ent_txb_ttl.insert(0, "{:.2f}".format(tot_taxbl))
        self.ent_gst_ttl.insert(0, "{:.2f}".format(tot_gst))
        self.ent_cess_ttl.insert(0, "{:.2f}".format(tot_cess))

        self.ent_gst_ttl.config(state = con.DISABLED)
        self.ent_cess_ttl.config(state = con.DISABLED)

    def cal_by_cp(self , e):  
        
        if e == None:
            #this segment is to allow select_from_treeview to work
            pass
        elif not (e.keycode == 8 or e.keysym in ['0' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '0'] or e.keycode == 190):
            return


        qty = self.ent_qty.get()
        cp = self.ent_cost.get()
        gst_per = float(self.ent_gst.get())
        cess_per = float(self.ent_cess.get())
        ttp = gst_per+cess_per


        

        if qty == "" or cp == "" or qty == "." or cp == ".":
            self.ent_gst_ttl.config(state = con.NORMAL)
            self.ent_cess_ttl.config(state = con.NORMAL)
            self.ent_txb.delete(0,con.END)
            self.ent_cost_ttl.delete(0,con.END)
            self.ent_txb_ttl.delete(0,con.END)
            self.ent_gst_ttl.delete(0,con.END)
            self.ent_cess_ttl.delete(0,con.END)
            self.ent_gst_ttl.config(state = con.DISABLED)
            self.ent_cess_ttl.config(state = con.DISABLED)
            return

        qty = float(qty)
        cp = float(cp)

        taxbl = cp/(1+ttp/100)
        tot_tax = (cp - taxbl) * qty



        if gst_per == 0 and cess_per == 0: 
            tot_gst = 0
            tot_cess = 0
        if gst_per == 0 and cess_per != 0:
            tot_gst = 0
            tot_cess =  tot_tax
        if gst_per != 0 and cess_per == 0:
            tot_cess = 0
            tot_gst = tot_tax 
        if gst_per != 0 and cess_per != 0:
            tot_cess = tot_tax * (cess_per/ttp)
            tot_gst = tot_tax * (gst_per/ttp)


        tot_cost = cp*qty
        tot_taxbl = taxbl*qty


        self.ent_gst_ttl.config(state = con.NORMAL)
        self.ent_cess_ttl.config(state = con.NORMAL)

        self.ent_qty.delete(0,con.END)
        self.ent_txb.delete(0,con.END)
        self.ent_cost_ttl.delete(0,con.END)
        self.ent_txb_ttl.delete(0,con.END)
        self.ent_gst_ttl.delete(0,con.END)
        self.ent_cess_ttl.delete(0,con.END)
        
        self.ent_qty.insert(0 , "{:.3f}".format(qty))
        self.ent_txb.insert(0, "{:.2f}".format(taxbl))
        self.ent_cost_ttl.insert(0, "{:.2f}".format(tot_cost))
        self.ent_txb_ttl.insert(0, "{:.2f}".format(tot_taxbl))
        self.ent_gst_ttl.insert(0, "{:.2f}".format(tot_gst))
        self.ent_cess_ttl.insert(0, "{:.2f}".format(tot_cess))

        self.ent_gst_ttl.config(state = con.DISABLED)
        self.ent_cess_ttl.config(state = con.DISABLED)

    def cal_by_taxbl(self , e):    
        if not (e.keycode == 8 or e.keysym in ['0' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '0'] or e.keycode == 190):
            return

        qty = self.ent_qty.get()
        taxbl = self.ent_txb.get()
        gst_per = float(self.ent_gst.get())
        cess_per = float(self.ent_cess.get())

        if qty == "" or taxbl == "" or qty == "." or taxbl == ".":
            self.ent_gst_ttl.config(state = con.NORMAL)
            self.ent_cess_ttl.config(state = con.NORMAL)
            self.ent_cost.delete(0,con.END)
            self.ent_cost_ttl.delete(0,con.END)
            self.ent_txb_ttl.delete(0,con.END)
            self.ent_gst_ttl.delete(0,con.END)
            self.ent_cess_ttl.delete(0,con.END)
            self.ent_gst_ttl.config(state = con.DISABLED)
            self.ent_cess_ttl.config(state = con.DISABLED)
            return

        qty = float(qty)
        taxbl = float(taxbl)

        cp = taxbl + (gst_per/100 * taxbl) + (cess_per/100 * taxbl)
        tot_cost = cp * qty
        tot_taxbl = taxbl * qty 
        tot_gst = gst_per/100 * taxbl * qty
        tot_cess = cess_per/100 * taxbl * qty


        self.ent_gst_ttl.config(state = con.NORMAL)
        self.ent_cess_ttl.config(state = con.NORMAL)

        self.ent_qty.delete(0,con.END)
        self.ent_cost.delete(0,con.END)
        self.ent_cost_ttl.delete(0,con.END)
        self.ent_txb_ttl.delete(0,con.END)
        self.ent_gst_ttl.delete(0,con.END)
        self.ent_cess_ttl.delete(0,con.END)
        
        self.ent_qty.insert(0 , "{:.3f}".format(qty))
        self.ent_cost.insert(0, "{:.2f}".format(cp))
        self.ent_cost_ttl.insert(0, "{:.2f}".format(tot_cost))
        self.ent_txb_ttl.insert(0, "{:.2f}".format(tot_taxbl))
        self.ent_gst_ttl.insert(0, "{:.2f}".format(tot_gst))
        self.ent_cess_ttl.insert(0, "{:.2f}".format(tot_cess))

        self.ent_gst_ttl.config(state = con.DISABLED)
        self.ent_cess_ttl.config(state = con.DISABLED)

    def cal_by_tcp(self , e):  
        if not (e.keycode == 8 or e.keysym in ['0' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '0'] or e.keycode == 190):            
            return


        qty = self.ent_qty.get()
        tot_cost = self.ent_cost_ttl.get()
        gst_per = float(self.ent_gst.get())
        cess_per = float(self.ent_cess.get())
        ttp = gst_per+cess_per


        

        if qty == "" or tot_cost == "" or qty == "." or tot_cost == ".":
            self.ent_gst_ttl.config(state = con.NORMAL)
            self.ent_cess_ttl.config(state = con.NORMAL)
            self.ent_cost.delete(0,con.END)
            self.ent_txb.delete(0,con.END)
            self.ent_txb_ttl.delete(0,con.END)
            self.ent_gst_ttl.delete(0,con.END)
            self.ent_cess_ttl.delete(0,con.END)
            self.ent_gst_ttl.config(state = con.DISABLED)
            self.ent_cess_ttl.config(state = con.DISABLED)
            return

        qty = float(qty)
        cp = float(tot_cost)/qty

        taxbl = cp/(1+ttp/100)
        tot_tax = (cp - taxbl) * qty

        if gst_per == 0 and cess_per == 0: 
            tot_gst = 0
            tot_cess = 0
        if gst_per == 0 and cess_per != 0:
            tot_gst = 0
            tot_cess =  tot_tax
        if gst_per != 0 and cess_per == 0:
            tot_cess = 0
            tot_gst =  tot_tax
        if gst_per != 0 and cess_per != 0:
            tot_cess = tot_tax * (cess_per/ttp)
            tot_gst = tot_tax * (gst_per/ttp)


        tot_taxbl = taxbl*qty


        self.ent_gst_ttl.config(state = con.NORMAL)
        self.ent_cess_ttl.config(state = con.NORMAL)

        self.ent_cost.delete(0,con.END)
        self.ent_qty.delete(0,con.END)
        self.ent_txb.delete(0,con.END)
        self.ent_txb_ttl.delete(0,con.END)
        self.ent_gst_ttl.delete(0,con.END)
        self.ent_cess_ttl.delete(0,con.END)
        
        self.ent_cost.insert(0, "{:.2f}".format(cp))
        self.ent_qty.insert(0 , "{:.3f}".format(qty))
        self.ent_txb.insert(0, "{:.2f}".format(taxbl))
        self.ent_txb_ttl.insert(0, "{:.2f}".format(tot_taxbl))
        self.ent_gst_ttl.insert(0, "{:.2f}".format(tot_gst))
        self.ent_cess_ttl.insert(0, "{:.2f}".format(tot_cess))

        self.ent_gst_ttl.config(state = con.DISABLED)
        self.ent_cess_ttl.config(state = con.DISABLED)

    def cal_by_tot_taxbl(self , e):    
        if not (e.keycode == 8 or e.keysym in ['0' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '0'] or e.keycode == 190):
            return

        qty = self.ent_qty.get()
        tot_taxbl = self.ent_txb_ttl.get()
        gst_per = float(self.ent_gst.get())
        cess_per = float(self.ent_cess.get())

        if qty == "" or tot_taxbl == "" or qty == "." or tot_taxbl == ".":
            self.ent_gst_ttl.config(state = con.NORMAL)
            self.ent_cess_ttl.config(state = con.NORMAL)
            self.ent_cost.delete(0,con.END)
            self.ent_cost_ttl.delete(0,con.END)
            self.ent_txb.delete(0,con.END)
            self.ent_gst_ttl.delete(0,con.END)
            self.ent_cess_ttl.delete(0,con.END)
            self.ent_gst_ttl.config(state = con.DISABLED)
            self.ent_cess_ttl.config(state = con.DISABLED)
            return

        qty = float(qty)
        taxbl = float(tot_taxbl)/qty

        cp = taxbl + (gst_per/100 * taxbl) + (cess_per/100 * taxbl)
        tot_cost = cp * qty
        tot_taxbl = taxbl * qty 
        tot_gst = gst_per/100 * taxbl * qty
        tot_cess = cess_per/100 * taxbl * qty


        self.ent_gst_ttl.config(state = con.NORMAL)
        self.ent_cess_ttl.config(state = con.NORMAL)

        self.ent_qty.delete(0,con.END)
        self.ent_cost.delete(0,con.END)
        self.ent_txb.delete(0,con.END)
        self.ent_cost_ttl.delete(0,con.END)
        self.ent_gst_ttl.delete(0,con.END)
        self.ent_cess_ttl.delete(0,con.END)
        
        self.ent_qty.insert(0 , "{:.3f}".format(qty))
        self.ent_cost.insert(0, "{:.2f}".format(cp))
        self.ent_txb.insert(0, "{:.2f}".format(taxbl))
        self.ent_cost_ttl.insert(0, "{:.2f}".format(tot_cost))
        self.ent_gst_ttl.insert(0, "{:.2f}".format(tot_gst))
        self.ent_cess_ttl.insert(0, "{:.2f}".format(tot_cess))

        self.ent_gst_ttl.config(state = con.DISABLED)
        self.ent_cess_ttl.config(state = con.DISABLED)

    def cal_sp(self,e):
        if not (e.keycode == 8 or e.keysym in ['0' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '0'] or e.keycode == 190):
            return

        cp = self.ent_cost.get()
        
        if cp == "":
            msg.showinfo("Info" , "Enter cost price")
            self.ent_pro_per.delete(0, con.END)
            return

        pro = self.ent_pro_per.get()
        if pro == "":
            sp = 0
        else :
            sp = "{:.2f}".format(float(cp)* (1 + float(pro) / 100))
        self.ent_nml1.delete(0,con.END)
        self.ent_nml1.insert(0,sp)
        
    def cal_final_totals(self , new):
        if self.prod_gst != 0:
            i = 0
            tot_cgst = 0
            tot_sgst = 0
            tot_igst = 0
            for each in self.tree_gst.get_children():
                
                sgst = float(self.tree_gst.item(each)['values'][1])
                cgst = float(self.tree_gst.item(each)['values'][2])
                igst = float(self.tree_gst.item(each)['values'][3])

                if int(self.tree_gst.item(each)['values'][0]) == self.prod_gst:
                    prod_tax = round(float(self.ent_gst_ttl.get())/2,2)
                    if not new:
                        prod_tax = -prod_tax
                    

                    if self.combo_tax_meth.get() == "In-State":
                        sgst = sgst + prod_tax 
                        cgst = cgst + prod_tax
                    else:
                        igst = igst + prod_tax *2

                
                    values = [self.prod_gst , "{:.2f}".format(round(sgst,2)) , "{:.2f}".format(round(cgst,2)) , "{:.2f}".format(round(igst,2))]

                    tag = 'b'
                    if i%2 == 0:
                        tag = 'a'

            
                    self.tree_gst.detach(each)

                    self.tree_gst.insert('',i ,tags=(tag,), values =values)
                    

                tot_cgst += cgst
                tot_sgst += sgst
                tot_igst += igst
                i+=1
            
            
            self.lbl_tot_cgst.config(text = "{:.2f}".format(tot_cgst))
            self.lbl_tot_sgst.config(text = "{:.2f}".format(tot_sgst))
            self.lbl_tot_igst.config(text = "{:.2f}".format(tot_igst))






        if self.prod_cess != 0:                                                                                                                                                            
            i = 0
            tot_cess = 0
            for each in self.tree_cess.get_children():
                cess = float(self.tree_cess.item(each)['values'][1])
                
                if int(self.tree_cess.item(each)['values'][0]) == self.prod_cess:
                    prod_tax = round(float(self.ent_cess_ttl.get()),2)
                    if not new:
                        prod_tax = -prod_tax
                    cess = cess + prod_tax
                    values = [self.prod_cess , "{:.2f}".format(cess) ]
                
                    tag = 'b'
                    if i%2 == 0:
                        tag = 'a'

                    self.tree_cess.detach(each)
                    self.tree_cess.insert('',i ,tags=(tag,), values =values)
                       
                i+=1
                tot_cess += cess
    

            self.lbl_tot_cess.config(text = "{:.2f}".format(tot_cess))


        exp = self.ent_tot_exp.get()
        if exp == "" or exp == "." or exp == "-":
            exp = 0
        else : 
            exp = float(exp)
        
        
        x = float(self.lbl_tot_txbl.cget("text"))
        y = float(self.ent_txb_ttl.get())
        if new:
            self.lbl_tot_txbl.config(text = "{:.2f}".format( x + y ))
        else:
            self.lbl_tot_txbl.config(text = "{:.2f}".format( x - y ))

        self.lbl_tot_tax.config(text = "{:.2f}".format(float(self.lbl_tot_sgst.cget("text")) + float(self.lbl_tot_cgst.cget("text")) + float(self.lbl_tot_igst.cget("text")) + float(self.lbl_tot_cess.cget("text"))))
        self.lbl_tot_amt.config(text = "{:.2f}".format(float(self.lbl_tot_txbl.cget("text")) + float(self.lbl_tot_tax.cget("text"))))
        self.lbl_grd_tot.config(text = "{:.2f}".format(float(self.lbl_tot_amt.cget("text")) + exp))

    def cal_expense(self , e):
        exp = self.ent_tot_exp.get() 
        if exp == "" or exp == "." or exp == "-" or exp == "-.":
            exp = 0
        
        self.lbl_grd_tot.config(text = "{:.2f}".format(float(self.lbl_tot_amt.cget("text")) + float(exp)))

    def cal_pro_per(self , e):
        sp = self.ent_nml1.get()
        cp = self.ent_cost.get()

        if sp == "" or sp ==".":
            pro_per = 0
            sp = 0
    
        elif cp == "" or cp ==".":
            pro_per = 0
            cp = 0

        try:
            pro_per = (float(sp) - float(cp)) / float(cp) * 100
        except ZeroDivisionError:
            pro_per = 0


        self.ent_pro_per.delete( 0 , con.END)
        self.ent_pro_per.insert(0 , "{:.2f}".format(round(pro_per , 2)))

    def cal_price(self , e):
      
        val = e.widget.get()

        if val == '.' or val == '':
            val = '0.00'
            self.lbl_cp_filler.config(text = val)
            return

        widget = str(e.widget).split("y")[-1]
        if widget == '':
            val = "{:.2f}".format(round(float(self.lbl_nml1.cget("text")) * float(val) , 3))
        elif widget == '2':
            val = "{:.2f}".format(round(float(self.lbl_nml2.cget("text")) * float(val) , 3))
        elif widget == '3':
            val = "{:.2f}".format(round(float(self.lbl_nml3.cget("text")) * float(val) , 3))
        elif widget == '4':
            val = "{:.2f}".format(round(float(self.lbl_nml4.cget("text")) * float(val) , 3))
        elif widget == '5':
            val = "{:.2f}".format(round(float(self.lbl_htl1.cget("text")) * float(val) , 3))
        elif widget == '6':
            val = "{:.2f}".format(round(float(self.lbl_htl2.cget("text")) * float(val) , 3))
        elif widget == '7':
            val = "{:.2f}".format(round(float(self.lbl_htl3.cget("text")) * float(val) , 3))
        elif widget == '8':
            val = "{:.2f}".format(round(float(self.lbl_htl4.cget("text")) * float(val) , 3))
        elif widget == '9':
            val = "{:.2f}".format(round(float(self.lbl_spl1.cget("text")) * float(val) , 3))
        elif widget == '10':
            val = "{:.2f}".format(round(float(self.lbl_spl2.cget("text")) * float(val) , 3))
        elif widget == '11':
            val = "{:.2f}".format(round(float(self.lbl_spl3.cget("text")) * float(val) , 3))
        elif widget == '12':
            val = "{:.2f}".format(round(float(self.lbl_spl4.cget("text")) * float(val) , 3))
        elif widget == '13':
            val = "{:.2f}".format(round(float(self.lbl_ang1.cget("text")) * float(val) , 3))
        elif widget == '14':
            val = "{:.2f}".format(round(float(self.lbl_ang2.cget("text")) * float(val) , 3))
        elif widget == '15':
            val = "{:.2f}".format(round(float(self.lbl_ang3.cget("text")) * float(val) , 3))
        else:
            val = "{:.2f}".format(round(float(self.lbl_ang4.cget("text")) * float(val) , 3))

        self.lbl_cp_filler.config(text = val)

    """--------------------------Calcualtion functions Ends here-----------------------------------------"""

    """--------------------------Product entry functions ------------------------------------------------"""
    def get_prod_list(self , e):
        #-------backspace----------Aa----------------Zz---------------space---------------0------------------9-----------------.
        if not (e.keycode == 8 or (e.keycode>=65 and e.keycode<=97) or e.keycode == 32 or e.keysym in ['0' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '0'] or e.keycode == 190):
            return

        if self.ent_bar.get() != "":
            return
        text = self.ent_name.get().upper()
        if text == "":
            if e.keycode == 27:
                self.forget_prod_list(None)
            else:
                self.clear_prod_bar_name(None) 
            return


        self.list_prod_name.delete(0,con.END)
        req = get("http://"+self.ip+":4000/getNameAll" , params = {"prod_name" : text}).json()

        for each in req: self.list_prod_name.insert(con.END , each)
        



        if self.root.winfo_screenheight()>1000: self.frm_prod_name.place( x = self.main_wdt*0.113 , y = self.main_hgt*0.123)
        else: self.frm_prod_name.place( x = self.main_wdt*0.106 , y = self.main_hgt*0.128)

        self.frm_prod_name.lift()
    
    def get_prod_by_bar(self , e):
        self.frm_pur_details.place_forget()

        bar = self.ent_bar.get().upper()

        if bar == "":
            return

        self.ent_bar.delete(0,con.END)
        self.ent_bar.insert(0,bar)
        
        
        prod = get("http://"+self.ip+":4000/getProdByBar" , params = {'prod_bar' : ":"+bar+":"}).json()
        if prod == []:
            msg.showinfo("Info" , "Product Not found!")
            self.root.bell()
            return
        prod = prod[0]


        
        #prod_id, prod_bar, prod_name, prod_gst, prod_cess, nml_unit, htl_unit, spl_unit, ang_unit
        self.prod_gst = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select tax_per from somanath.taxes where tax_id = " + str(prod['prod_gst'])  }).json()[0]['tax_per']
        self.prod_cess = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select tax_per from somanath.taxes where tax_id = " + str(prod['prod_cess'])  }).json()[0]['tax_per']      
        if prod['prod_id'] in self.added_products :
            msg.showinfo("Info" , "This product has already been added")
            return
        self.prod_id = prod['prod_id']

        self.ent_name.delete(0,con.END)
        self.ent_name.insert(0,prod['prod_name'])
        self.enable_prod_details()
        self.ent_gst.config(state = con.NORMAL)
        self.ent_gst.delete(0,con.END)
        self.ent_gst.insert(0,self.prod_gst)
        self.ent_gst.config(state = con.DISABLED)

        self.ent_cess.config(state = con.NORMAL)
        self.ent_cess.delete(0,con.END)
        self.ent_cess.insert(0,self.prod_cess)
        self.ent_cess.config(state = con.DISABLED)

        nml = prod['nml_unit'].split(":")[1:-1]
        htl = prod['htl_unit'].split(":")[1:-1]
        spl = prod['spl_unit'].split(":")[1:-1]
        ang = prod['ang_unit'].split(":")[1:-1]

        self.lbl_nml1.config(text = nml[0])
        self.lbl_nml2.config(text = nml[1])
        self.lbl_nml3.config(text = nml[2])
        self.lbl_nml4.config(text = nml[3])
        self.lbl_htl1.config(text = htl[0])
        self.lbl_htl2.config(text = htl[1])
        self.lbl_htl3.config(text = htl[2])
        self.lbl_htl4.config(text = htl[3])
        self.lbl_spl1.config(text = spl[0])
        self.lbl_spl2.config(text = spl[1])
        self.lbl_spl3.config(text = spl[2])
        self.lbl_spl4.config(text = spl[3])
        self.lbl_ang1.config(text = ang[0])
        self.lbl_ang2.config(text = ang[1])
        self.lbl_ang3.config(text = ang[2])
        self.lbl_ang4.config(text = ang[3])


        if e != "called from delete_from_treeview":
            self.get_stk_sug()
            self.ent_qty.focus_set()

    def get_prod_by_name(self , e):
        self.frm_pur_details.place_forget()

        name = self.list_prod_name.get(self.list_prod_name.curselection())
        if name == "":
            return

        
        prod = get("http://"+self.ip+":4000/getProdByName" , params = {'prod_name' : name}).json()
        if prod == []:
            return
        prod = prod[0]
        
        #prod_id, prod_bar, prod_name, prod_gst, prod_cess, nml_unit, htl_unit, spl_unit, ang_unit
        self.prod_gst = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select tax_per from somanath.taxes where tax_id = " + str(prod['prod_gst'])  }).json()[0]['tax_per']
        self.prod_cess = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select tax_per from somanath.taxes where tax_id = " + str(prod['prod_cess'])  }).json()[0]['tax_per']   
        if prod['prod_id'] in self.added_products:
            msg.showinfo("Info" , "This product has already been added")
            return

        self.prod_id = prod['prod_id']

        

        self.ent_bar.delete(0,con.END)
        self.ent_bar.insert(0,prod['prod_bar'].split(":")[1])
        self.ent_name.delete(0,con.END)
        self.ent_name.insert(0,prod['prod_name'])
        self.enable_prod_details()
        self.ent_gst.config(state = con.NORMAL)
        self.ent_gst.delete(0,con.END)
        self.ent_gst.insert(0,self.prod_gst)
        self.ent_gst.config(state = con.DISABLED)

        self.ent_cess.config(state = con.NORMAL)
        self.ent_cess.delete(0,con.END)
        self.ent_cess.insert(0,self.prod_cess)
        self.ent_cess.config(state = con.DISABLED)

        nml = prod['nml_unit'].split(":")[1:-1]
        htl = prod['htl_unit'].split(":")[1:-1]
        spl = prod['spl_unit'].split(":")[1:-1]
        ang = prod['ang_unit'].split(":")[1:-1]

        self.lbl_nml1.config(text = nml[0])
        self.lbl_nml2.config(text = nml[1])
        self.lbl_nml3.config(text = nml[2])
        self.lbl_nml4.config(text = nml[3])
        self.lbl_htl1.config(text = htl[0])
        self.lbl_htl2.config(text = htl[1])
        self.lbl_htl3.config(text = htl[2])
        self.lbl_htl4.config(text = htl[3])
        self.lbl_spl1.config(text = spl[0])
        self.lbl_spl2.config(text = spl[1])
        self.lbl_spl3.config(text = spl[2])
        self.lbl_spl4.config(text = spl[3])
        self.lbl_ang1.config(text = ang[0])
        self.lbl_ang2.config(text = ang[1])
        self.lbl_ang3.config(text = ang[2])
        self.lbl_ang4.config(text = ang[3])

        self.forget_prod_list(None)
        self.ent_qty.focus_set()
        self.get_stk_sug()
        
    def focus_prod_list(self , e):
        if self.list_prod_name.size() > 0: 
            self.list_prod_name.focus_set()
            self.list_prod_name.selection_set(0)

    def forget_prod_list(self,e):
        self.frm_prod_name.place_forget()
        #when shift-tab is pressed focus set to barcode 27 is escape
        if e != None and e.keycode == 27:
            self.ent_name.focus_set()
            return
        if e!= None and e.keycode == 9:
            self.ent_bar.focus_set()

    def get_stk_sug(self ):
        old_stks = get("http://"+self.ip+":5000/getOldStocks" , params = {'prod_id' : self.prod_id , 'year' : self.year , 'max' : 3})

        if old_stks.status_code == 200:
            old_stks = old_stks.json()
            self.lbl_mrp_1.config(text = "{:.2f}".format(float(old_stks['prodMrp1'])))
            self.lbl_mrp_2.config(text = "{:.2f}".format(float(old_stks['prodMrp2'])))
            self.lbl_tot_stk.config(text = "{:.3f}".format(float(old_stks['totQty'])))

            i = 0
            for each in self.tree_old_stk.get_children():
                self.tree_old_stk.delete(each)

            for each in old_stks['stocks']:
                nml = each[4].split(":")[1:-1]
                htl = each[5].split(":")[1:-1]
                spl = each[6].split(":")[1:-1]
                ang = each[7].split(":")[1:-1]

                values = (each[0] , each[1] , "{:.2f}".format(float(each[2])) , "{:.3f}".format(float(each[3])) , nml[0]  , nml[1] , nml[2] , nml[3] , htl[0]  , htl[1] , htl[2] , htl[3] , spl[0]  , spl[1] , spl[2] , spl[3] , ang[0]  , ang[1] , ang[2] , ang[3]  )

                if i%2 == 0:    self.tree_old_stk.insert('','end' ,tags=('a',), values = values)
                else       :    self.tree_old_stk.insert('','end' ,tags=('b',), values = values)

                i+=1



        if self.root.winfo_screenheight()>1000: self.frm_stk_sug.place( x = 0, y = self.main_hgt*0.22)
        else : self.frm_stk_sug.place( x = 0, y = self.main_hgt*0.237)
        
        self.frm_stk_sug.lift()

    def select_first_stock(self , e):
        child = self.tree_old_stk.get_children()
        if len(child) == 0:
            return

        self.tree_old_stk.focus_set()
        self.tree_old_stk.focus(child[0])
        self.tree_old_stk.selection_set(child[0])

    def select_rates(self , e):
        curItem = self.tree_old_stk.focus()
        curItem = self.tree_old_stk.item(curItem)
        curItem = curItem['values']

        self.ent_nml1.delete(0,con.END)
        self.ent_nml2.delete(0,con.END)
        self.ent_nml3.delete(0,con.END)
        self.ent_nml4.delete(0,con.END)

        self.ent_htl1.delete(0,con.END)
        self.ent_htl2.delete(0,con.END)
        self.ent_htl3.delete(0,con.END)
        self.ent_htl4.delete(0,con.END)

        self.ent_spl1.delete(0,con.END)
        self.ent_spl2.delete(0,con.END)
        self.ent_spl3.delete(0,con.END)
        self.ent_spl4.delete(0,con.END)

        self.ent_ang1.delete(0,con.END)
        self.ent_ang2.delete(0,con.END)
        self.ent_ang3.delete(0,con.END)
        self.ent_ang4.delete(0,con.END)


        self.ent_nml1.insert(0,curItem[4])
        self.ent_nml2.insert(0,curItem[5])
        self.ent_nml3.insert(0,curItem[6])
        self.ent_nml4.insert(0,curItem[7])

        self.ent_htl1.insert(0,curItem[8])
        self.ent_htl2.insert(0,curItem[9])
        self.ent_htl3.insert(0,curItem[10])
        self.ent_htl4.insert(0,curItem[11])

        self.ent_spl1.insert(0,curItem[12])
        self.ent_spl2.insert(0,curItem[13])
        self.ent_spl3.insert(0,curItem[14])
        self.ent_spl4.insert(0,curItem[15])

        self.ent_ang1.insert(0,curItem[16])
        self.ent_ang2.insert(0,curItem[17])
        self.ent_ang3.insert(0,curItem[18])
        self.ent_ang4.insert(0,curItem[19])

        self.ent_ang4.focus_set()

    def forget_stk_sug(self , e):
        self.frm_stk_sug.place_forget()

    def selling_price_filler(self, e):
        tot_gst = self.ent_gst_ttl.get()
        if tot_gst == "":
            msg.showinfo("Info" , "Enter Cost Price and QTY")
            self.ent_qty.focus_set()
            self.ent_qty.select_range(0,con.END)
            return
        
        cp = self.ent_cost.get()
        qty = self.ent_qty.get()

        if float(cp) == 0 or float(qty) == 0:
            msg.showinfo("Info" , "Enter Cost Price > 0 and QTY > 0")
            self.ent_qty.focus_set()
            self.ent_qty.select_range(0,con.END)
            return


        nrm1 = self.ent_nml1.get()

        if nrm1 == "":
            msg.showinfo("Info" , "Enter Selling Price ")
            self.ent_nml1.focus_set()
            return

        nrm1 = float(nrm1)
        if nrm1 < 0.001:
            self.ent_nml1.delete(0,con.END)
            msg.showinfo("Selling Price","Enter Correct Selling Price")
            return
        if nrm1 < float(self.ent_cost.get()):
            self.ent_nml1.delete(0,con.END)
            msg.showinfo("Selling Price","Enter Selling Price more than Cost Price")
            return

        nrm1 ="{:.3f}".format(nrm1)
        self.ent_nml1.delete(0,con.END)
        self.ent_nml1.insert(0,nrm1)
        
        nrm2 = self.ent_nml2.get()
        if nrm2 == "":
            nrm2 = nrm1
            self.ent_nml2.insert(0,nrm2)
        
        nrm3 = self.ent_nml3.get()
        if nrm3 == "":
            nrm3 = "{:.3f}".format(float(nrm2))
            self.ent_nml3.insert(0,nrm3)
        
        nrm4 = self.ent_nml4.get()
        if nrm4 == "":
            nrm4 = "{:.3f}".format(float(nrm3))
            self.ent_nml4.insert(0,nrm3)
        

        htl1 = self.ent_htl1.get()
        htl2 = self.ent_htl2.get()
        htl3 = self.ent_htl3.get()
        htl4 = self.ent_htl4.get()
        if htl1 == "" and htl2 =="" and htl3 == "" and htl4 == "":
            htl1 = nrm1
            htl2 = nrm2
            htl3 = nrm3
            htl4 = nrm4
            self.ent_htl1.insert(0,htl1)
            self.ent_htl2.insert(0,htl2)
            self.ent_htl3.insert(0,htl3)
            self.ent_htl4.insert(0,htl4)
        if htl1 =="":
            htl1 = nrm1
            self.ent_htl1.insert(0,htl1)
        if htl2 =="":
            htl2 = "{:.3f}".format(float(htl1))
            self.ent_htl2.insert(0,htl2)
        if htl3 =="":
            htl3 = "{:.3f}".format(float(htl2))
            self.ent_htl3.insert(0,htl3)
        if htl4 =="":
            htl4 = "{:.3f}".format(float(htl3))
            self.ent_htl4.insert(0,htl4)    
        
        spl1 = self.ent_spl1.get()
        spl2 = self.ent_spl2.get()
        spl3 = self.ent_spl3.get()
        spl4 = self.ent_spl4.get()
        if spl1 == "" and spl2 =="" and spl3 == "" and spl4 == "":
            spl1 = htl1
            spl2 = htl2
            spl3 = htl3
            spl4 = htl4
            self.ent_spl1.insert(0,spl1)
            self.ent_spl2.insert(0,spl2)
            self.ent_spl3.insert(0,spl3)
            self.ent_spl4.insert(0,spl4)
        if spl1 =="":
            spl1 = htl1
            self.ent_spl1.insert(0,spl1)
        if spl2 =="":
            spl2 = "{:.3f}".format(float(spl1))
            self.ent_spl2.insert(0,spl2)
        if spl3 =="":
            spl3 = "{:.3f}".format(float(spl2))
            self.ent_spl3.insert(0,spl3)
        if spl4 =="":
            spl4 = "{:.3f}".format(float(spl3))
            self.ent_spl4.insert(0,spl4)

        ang1 = self.ent_ang1.get()
        ang2 = self.ent_ang2.get()
        ang3 = self.ent_ang3.get()
        ang4 = self.ent_ang4.get()
        if ang1 == "" and ang2 =="" and ang3 == "" and ang4 == "":
            ang1 = spl1
            ang2 = spl2
            ang3 = spl3
            ang4 = spl4
            self.ent_ang1.insert(0,ang1)
            self.ent_ang2.insert(0,ang2)
            self.ent_ang3.insert(0,ang3)
            self.ent_ang4.insert(0,ang4)
        if ang1 =="":
            ang1 = spl1
            self.ent_ang1.insert(0,ang1)
        if ang2 =="":
            ang2 = "{:.3f}".format(float(ang1))
            self.ent_ang2.insert(0,ang2)
        if ang3 =="":
            ang3 = "{:.3f}".format(float(ang2))
            self.ent_ang3.insert(0,ang3)
        if ang4 =="":
            ang4 = "{:.3f}".format(float(ang3))
            self.ent_ang4.insert(0,ang4)
        
        self.ent_ang4.focus_set()
        
        return True

    def enter_to_treeview(self, e):
        if not self.selling_price_filler(None):
            return

        cp = float(self.ent_cost.get())
        qty = self.ent_qty.get()

        if qty == "" or qty == ".":
            qty = 0



        if self.stkDiff > 0:
            if float(qty) < self.stkDiff:
                msg.showinfo("Info" , "Enter Qty >=  " + "{:.2f}".format(self.stkDiff))
                self.ent_qty.focus_set()
                return
        else:
            self.stkDiff = 0



        if cp <= 0:
            msg.showerror("Error" , "CP must be greater than 0")
            self.ent_cost.select_range(0,con.END)
            self.ent_cost.focus_set()
            return


        nml1 = self.ent_nml1.get()
        nml2 = self.ent_nml2.get()
        nml3 = self.ent_nml3.get()
        nml4 = self.ent_nml4.get()

        if nml1 == "" or nml1 == "." or nml2 == "" or nml2 == "." or nml3 == "" or nml3 == "." or nml4 == "" or nml4 == ".":
            return
        nml_sp = [float(nml1) , float(nml2) , float(nml3) ,float(nml4)]

        for each in nml_sp:
            if each < cp:
                msg.showerror("Error" , "Enter NML rates greater than COST PRICE")
                self.ent_nml1.focus_set()
                return


        if nml_sp != sorted(nml_sp , reverse = True):
            msg.showerror("Error" , "Enter NML rates in correct order")
            self.ent_nml2.focus_set()
            return
            


        htl1 = self.ent_htl1.get()
        htl2 = self.ent_htl2.get()
        htl3 = self.ent_htl3.get()
        htl4 = self.ent_htl4.get()

        if htl1 == "" or htl1 == "." or htl2 == "" or htl2 == "." or htl3 == "" or htl3 == "." or htl4 == "" or htl4 == ".":
            return
        htl_sp = [float(htl1) , float(htl2) , float(htl3) ,float(htl4)]

        for each in htl_sp:
            if each < cp:
                msg.showerror("Error" , "Enter HTL rates greater than COST PRICE")
                self.ent_htl1.focus_set()
                return
        if htl_sp != sorted(htl_sp, reverse = True):
            msg.showerror("Error" , "Enter HTL rates in correct order")
            self.ent_htl2.focus_set()
            return

                    

            
        spl1 = self.ent_spl1.get()
        spl2 = self.ent_spl2.get()
        spl3 = self.ent_spl3.get()
        spl4 = self.ent_spl4.get()

        if spl1 == "" or spl1 == "." or spl2 == "" or spl2 == "." or spl3 == "" or spl3 == "." or spl4 == "" or spl4 == ".":
            return
        spl_sp = [float(spl1) , float(spl2) , float(spl3) ,float(spl4)]
        for each in spl_sp:
            if each < cp:
                msg.showerror("Error" , "Enter SPL rates greater than COST PRICE")
                self.ent_spl1.focus_set()
                return
        if spl_sp != sorted(spl_sp, reverse = True):
            msg.showerror("Error" , "Enter SPL rates in correct order")
            self.ent_spl2.focus_set()
            return

                    

            
        ang1 = self.ent_ang1.get()
        ang2 = self.ent_ang2.get()
        ang3 = self.ent_ang3.get()
        ang4 = self.ent_ang4.get()

        if ang1 == "" or ang1 == "." or ang2 == "" or ang2 == "." or ang3 == "" or ang3 == "." or ang4 == "" or ang4 == ".":
            return
        ang_sp = [float(ang1) , float(ang2) , float(ang3) ,float(ang4)]
        for each in ang_sp:
            if each < cp:
                msg.showerror("Error" , "Enter ANG rates greater than COST PRICE")
                self.ent_ang1.focus_set()
                return
        if ang_sp != sorted(ang_sp, reverse = True):
            msg.showerror("Error" , "Enter ANG rates in correct order")
            self.ent_ang2.focus_set()
            return
        
        self.added_products.append(self.prod_id)
        
        values = [self.sl_no , self.ent_name.get().upper() , self.prod_gst , "{:.3f}".format(float(self.ent_cost.get())) , "{:.3f}".format(float(qty)) , "{:.3f}".format(float(self.ent_txb_ttl.get())) , "{:.3f}".format(float(self.ent_cost_ttl.get()))]
       
    
        for each in nml_sp:
            values.append("{:.3f}".format(each))
        for each in htl_sp:
            values.append("{:.3f}".format(each))
        for each in spl_sp:
            values.append("{:.3f}".format(each))
        for each in ang_sp:
            values.append("{:.3f}".format(each))

        prod_exp = self.ent_exp.get()
        if prod_exp == "":
            prod_exp = 0

        values.append(prod_exp)
        values.append(self.prod_id)
        values.append(self.prod_cess)
        
        values.append(self.stkDiff)    

        tag = 'b'
        if self.selected_sl_no != 0:
            values[0] = self.selected_sl_no
            if self.selected_sl_no %2 == 0:
                tag = 'a'
            
        elif len(self.added_products) %2 == 0:
            tag = 'a'
            

        
        curItem = self.tree_pur.insert('','end' ,tags=(tag,), values = values)

    
        if self.selected_sl_no != 0:
            self.tree_pur.move(curItem , self.tree_pur.parent(curItem) , self.selected_sl_no - 1)
        else:
            self.sl_no += 1
        
    


        self.cal_final_totals(True)
        self.forget_stk_sug(None)
        self.prod_id = -1
        self.prod_gst = -1
        self.prod_cess = -1
        self.stkDiff = -1
        self.selected_sl_no = 0
        self.ent_bar.config(state = con.NORMAL)
        self.ent_name.config(state = con.NORMAL)

        """"!!!! add products to socket """
        get("http://"+self.ip+":5000/purchases/addPurchaseProduct" , params = {"value" : values} )

        self.ent_bar.focus_set()

    def select_from_treeview(self , e):
        if self.prod_id != -1:
            msg.showwarning("Warning" , "A Product is selected")
            return
        
        
        curItemNo = self.tree_pur.focus()
        values =  self.tree_pur.item(curItemNo)['values']
        #print(values)
        self.added_products.remove(values[24])
        self.selected_sl_no = values[0]
        self.enable_all()
        self.clear_all()
        sql = "select prod_bar from somanath.products where prod_id = " + str(values[24])
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql}).json()
        req = req[0]['prod_bar'].split(":")[1]
        self.ent_bar.insert(0,req)
        
        self.get_prod_by_bar(None)
        self.ent_cost.insert(0,values[3])
        self.ent_qty.insert(0,values[4])
        
        self.cal_by_cp(None)

        if self.edit_state:
            self.stkDiff = float(values[26])
    

        self.ent_nml1.insert(0,values[7])
        self.ent_nml2.insert(0,values[8])
        self.ent_nml3.insert(0,values[9])
        self.ent_nml4.insert(0,values[10])
        self.ent_htl1.insert(0,values[11])
        self.ent_htl2.insert(0,values[12])
        self.ent_htl3.insert(0,values[13])
        self.ent_htl4.insert(0,values[14])
        self.ent_spl1.insert(0,values[15])
        self.ent_spl2.insert(0,values[16])
        self.ent_spl3.insert(0,values[17])
        self.ent_spl4.insert(0,values[18])
        self.ent_ang1.insert(0,values[19])
        self.ent_ang2.insert(0,values[20])
        self.ent_ang3.insert(0,values[21])
        self.ent_ang4.insert(0,values[22])
        self.ent_exp.insert(0,values[23])
        self.cal_final_totals(False)
        self.tree_pur.detach(curItemNo)
        get("http://"+self.ip+":5000/purchases/removePurchaseProduct" , params = {"prod_id" : self.prod_id})
        self.ent_nml1.focus_set()
           
    def delete_from_treeview(self,e):
        curItemNo = self.tree_pur.focus()
        values =  self.tree_pur.item(curItemNo)['values']

        if self.edit_state:
            if float(values[26]) > 0 :
                msg.showinfo("Info","Cannot Delete\nಈ ಐಟೆಮ್ "+ values[26] +"sale ಆಗಿದೆ ")
                return
        
        """Remove
        if self.edit_state:
            msg.showinfo("Info","Delete Continues")
            return
        #Remove"""

        self.added_products.remove(values[24])
        self.enable_all()
        self.clear_all()
        sql = "select prod_bar from somanath.products where prod_id = " + str(values[24])
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql}).json()
        req = req[0]['prod_bar'].split(":")[1]
        self.ent_bar.insert(0,req)
        self.get_prod_by_bar("called from delete_from_treeview")
        self.ent_cost.insert(0,values[3])
        self.ent_qty.insert(0,values[4])
        self.cal_by_cp(None)

        self.ent_nml1.insert(0,values[7])
        self.ent_nml2.insert(0,values[8])
        self.ent_nml3.insert(0,values[9])
        self.ent_nml4.insert(0,values[10])
        self.ent_htl1.insert(0,values[11])
        self.ent_htl2.insert(0,values[12])
        self.ent_htl3.insert(0,values[13])
        self.ent_htl4.insert(0,values[14])
        self.ent_spl1.insert(0,values[15])
        self.ent_spl2.insert(0,values[16])
        self.ent_spl3.insert(0,values[17])
        self.ent_spl4.insert(0,values[18])
        self.ent_ang1.insert(0,values[19])
        self.ent_ang2.insert(0,values[20])
        self.ent_ang3.insert(0,values[21])
        self.ent_ang4.insert(0,values[22])
        self.ent_exp.insert(0,values[23])
        self.cal_final_totals(False)
        get("http://"+self.ip+":5000/purchases/removePurchaseProduct" , params = {"prod_id" : self.prod_id})

        items = self.tree_pur.get_children()
        curIndex = self.tree_pur.index(curItemNo)
        i = 0
        for each in items:
            
            if i > curIndex:
                values = self.tree_pur.item(each)['values']
                values[0] = i
                tag = 'b'
                if i %2 == 0:
                    tag = 'a'
                self.tree_pur.detach(each)
                self.tree_pur.insert('',i,tags=(tag,), values = values)
            i +=1
            
        self.sl_no = len(items)
        
        self.prod_id = -1
        self.prod_gst = -1
        self.prod_cess = -1
        self.stkDiff = -1
        self.selected_sl_no = 0
        self.tree_pur.detach(curItemNo)
        self.ent_bar.focus_set()

    """--------------------------Product entry functions Ends here---------------------------------------"""



    """-------------------------------------Utilities----------------------------------------------------"""
    def enable_all(self):
        self.ent_bar.config(state = con.NORMAL)
        self.ent_name.config(state = con.NORMAL)
        self.ent_tot_exp.config(state = con.NORMAL)
        self.ent_amt_paid.config(state = con.NORMAL)
        self.chk_full_paid.config(state = con.NORMAL)
        self.ent_tot_exp.config(state = con.NORMAL)
        
    def clear_all(self):
        self.enable_prod_details()
        self.ent_bar.delete(0,con.END)
        self.ent_name.delete(0,con.END)
        self.ent_gst.config(state = con.NORMAL)
        self.ent_gst.delete(0,con.END)
        self.ent_gst.config(state = con.DISABLED)
        self.ent_cess.config(state = con.NORMAL)
        self.ent_cess.delete(0,con.END)
        self.ent_cess.config(state = con.DISABLED)
        self.ent_qty.delete(0,con.END)
        self.ent_cost.delete(0,con.END)
        self.ent_txb.delete(0,con.END)
        self.ent_cost_ttl.delete(0,con.END)
        self.ent_txb_ttl.delete(0,con.END)
        self.ent_pro_per.delete(0,con.END)
        self.ent_gst_ttl.config(state = con.NORMAL)
        self.ent_gst_ttl.delete(0,con.END)
        self.ent_gst_ttl.config(state = con.DISABLED)
        self.ent_cess_ttl.config(state = con.NORMAL)
        self.ent_cess_ttl.delete(0,con.END)
        self.ent_cess_ttl.config(state = con.DISABLED)
        
        self.ent_tot_exp.config(state = con.NORMAL)
        self.ent_tot_exp.delete(0,con.END)
        
        self.ent_nml1.delete(0,con.END)
        self.ent_nml2.delete(0,con.END)
        self.ent_nml3.delete(0,con.END)
        self.ent_nml4.delete(0,con.END)
        self.ent_htl1.delete(0,con.END)
        self.ent_htl2.delete(0,con.END)
        self.ent_htl3.delete(0,con.END)
        self.ent_htl4.delete(0,con.END)
        self.ent_spl1.delete(0,con.END)
        self.ent_spl2.delete(0,con.END)
        self.ent_spl3.delete(0,con.END)
        self.ent_spl4.delete(0,con.END)
        self.ent_ang1.delete(0,con.END)
        self.ent_ang2.delete(0,con.END)
        self.ent_ang3.delete(0,con.END)
        self.ent_ang4.delete(0,con.END)

        self.lbl_nml1.config(text = "")
        self.lbl_nml2.config(text = "")
        self.lbl_nml3.config(text = "")
        self.lbl_nml4.config(text = "")
        self.lbl_htl1.config(text = "")
        self.lbl_htl2.config(text = "")
        self.lbl_htl3.config(text = "")
        self.lbl_htl4.config(text = "")
        self.lbl_spl1.config(text = "")
        self.lbl_spl2.config(text = "")
        self.lbl_spl3.config(text = "")
        self.lbl_spl4.config(text = "")
        self.lbl_ang1.config(text = "")
        self.lbl_ang2.config(text = "")
        self.lbl_ang3.config(text = "")
        self.lbl_ang4.config(text = "")

        self.ent_exp.delete(0,con.END)
        self.lbl_cp_filler.config(text = "")

    def disable_all(self):   
        self.ent_bar.config(state = con.DISABLED)
        self.ent_name.config(state = con.DISABLED)
        #self.ent_tot_exp.config(state = con.DISABLED)
        self.ent_amt_paid.config(state = con.DISABLED)
        self.chk_full_paid.config(state = con.DISABLED)
       
    def enable_prod_details(self):
        self.ent_qty.config(state = con.NORMAL)
        self.ent_cost.config(state = con.NORMAL)
        self.ent_txb.config(state = con.NORMAL)
        self.ent_cost_ttl.config(state = con.NORMAL)
        self.ent_txb_ttl.config(state = con.NORMAL)
        self.ent_pro_per.config(state = con.NORMAL)

        self.ent_nml1.config(state = con.NORMAL)
        self.ent_nml2.config(state = con.NORMAL)
        self.ent_nml3.config(state = con.NORMAL)
        self.ent_nml4.config(state = con.NORMAL)
        self.ent_htl1.config(state = con.NORMAL)
        self.ent_htl2.config(state = con.NORMAL)
        self.ent_htl3.config(state = con.NORMAL)
        self.ent_htl4.config(state = con.NORMAL)
        self.ent_spl1.config(state = con.NORMAL)
        self.ent_spl2.config(state = con.NORMAL)
        self.ent_spl3.config(state = con.NORMAL)
        self.ent_spl4.config(state = con.NORMAL)
        self.ent_ang1.config(state = con.NORMAL)
        self.ent_ang2.config(state = con.NORMAL)
        self.ent_ang3.config(state = con.NORMAL)
        self.ent_ang4.config(state = con.NORMAL)

        self.ent_exp.config(state = con.NORMAL)
        
    def disable_prod_details(self):
        self.ent_qty.config(state = con.DISABLED)
        self.ent_cost.config(state = con.DISABLED)
        self.ent_txb.config(state = con.DISABLED)
        self.ent_cost_ttl.config(state = con.DISABLED)
        self.ent_txb_ttl.config(state = con.DISABLED)
        self.ent_pro_per.config(state = con.DISABLED)

        self.ent_nml1.config(state = con.DISABLED)
        self.ent_nml2.config(state = con.DISABLED)
        self.ent_nml3.config(state = con.DISABLED)
        self.ent_nml4.config(state = con.DISABLED)
        self.ent_htl1.config(state = con.DISABLED)
        self.ent_htl2.config(state = con.DISABLED)
        self.ent_htl3.config(state = con.DISABLED)
        self.ent_htl4.config(state = con.DISABLED)
        self.ent_spl1.config(state = con.DISABLED)
        self.ent_spl2.config(state = con.DISABLED)
        self.ent_spl3.config(state = con.DISABLED)
        self.ent_spl4.config(state = con.DISABLED)
        self.ent_ang1.config(state = con.DISABLED)
        self.ent_ang2.config(state = con.DISABLED)
        self.ent_ang3.config(state = con.DISABLED)
        self.ent_ang4.config(state = con.DISABLED)

        self.ent_exp.config(state = con.DISABLED)
        
    def new_tree(self):
    
        self.clear_all_tree()
        
        gst = []
        cess = []

        req = get("http://"+self.ip+":6000/taxes/getTaxList").json()
        
        for each in req:
            if each['tax_type'] == '0':
                gst.append(each['tax_per'])
            else:
                cess.append(each['tax_per'])

        gst.sort()
        cess.sort()

        i = 0
        for each in gst:
            if i % 2 == 0: tag = 'a'
            else: tag = 'b'
            self.tree_gst.insert('','end' ,tags=(tag,), values = (each , "0.00" , "0.00" , "0.00"))
            i += 1


        i = 0
        for each in cess:
            if i % 2 == 0: tag = 'a'
            else: tag = 'b'
            self.tree_cess.insert('','end' ,tags=(tag,), values = (each  , "0.00"))
            i += 1
        
        self.ent_bar.focus_set()

    def clear_all_tree(self):
        
        for each in self.tree_old_stk.get_children():
            self.tree_old_stk.delete(each)

        for each in self.tree_pur.get_children():
            self.tree_pur.delete(each)

        for each in self.tree_gst.get_children():
            self.tree_gst.delete(each)

        for each in self.tree_cess.get_children():
            self.tree_cess.delete(each)

    def clear_prod_bar_name(self , e):
        self.clear_all()
        self.disable_prod_details()
        self.forget_prod_list(None)
        self.forget_stk_sug(None)

    def enter_new_details(self):
        if self.new_state:
            self.combo_tax_meth.config(state = con.NORMAL)
            self.combo_tax_meth.insert(0, "In-State")
            self.combo_tax_meth.config(state = "readonly")
            self.ent_pur_date.insert(0, datetime.date.today().strftime("%d") + "-" +datetime.date.today().strftime("%m") + "-" + datetime.date.today().strftime("%Y"))

        self.lbl_tot_cgst.config(text = "0.00")
        self.lbl_tot_sgst.config(text = "0.00")
        self.lbl_tot_igst.config(text = "0.00")
        self.lbl_tot_cess.config(text = "0.00")
        self.lbl_tot_txbl.config(text = "0.00")
        self.lbl_tot_tax.config(text = "0.00")
        self.lbl_tot_amt.config(text = "0.00")
        self.lbl_grd_tot.config(text = "0.00")
        
    """-------------------------------------Utilities Ends here------------------------------------------"""

    """-------------------------------------socket event handlers----------------------------------------"""

    


    """-------------------------------------socket event handlers ends here------------------------------"""

    def upd_price(self , e):
        pass

    def upd_prod(self , e):
        pass
        
    def sales_summary(self , e):
        pass

    def new(self , e):
        self.btn_edit.config(state = con.DISABLED)
        self.btn_new.config(state = con.DISABLED)
        self.btn_save.config(state = con.NORMAL)
        self.btn_add_dets.config(state = con.NORMAL)
        self.btn_cancel.config(state = con.NORMAL)
        #self.enable_all()

        self.combo_pay_meth.config(state = con.NORMAL)
        self.combo_pay_meth.delete(0,con.END)
        self.combo_pay_meth.insert(0,'CASH')
        self.combo_pay_meth.config(state = "readonly")
        self.clear_all()
        self.new_tree()
        self.new_state = True
        self.edit_state = False
        self.enable_pur_details()
        self.clear_pur_details()
        self.show_pur_details(None)
        self.enter_new_details()

        """self.combo_supplier.insert(0,"3 STAR CANDLE HOUSE")
        self.lbl_sup_gst.config(text = "123123123")
        self.combo_firms.config(state = con.NORMAL)
        self.combo_firms.insert(0,"SOMANATH CASH")
        self.combo_firms.config(state = "readonly")
        self.ent_inv_no.insert(0,"123")

           
        self.ent_bar.insert(0,"S00033")
        self.ent_bar.focus_set()"""

    def edit(self , e):
        self.clear_all()
        self.new_tree()
        self.btn_edit.config(state = con.DISABLED)
        self.btn_new.config(state = con.DISABLED)
        self.btn_save.config(state = con.NORMAL)
        self.btn_cancel.config(state = con.NORMAL)
        self.btn_add_dets.config(state = con.NORMAL)
        self.new_state = False
        self.edit_state = True
        self.enable_pur_details()
        self.clear_pur_details()
        self.disable_pur_details()
        self.show_pur_details(None)  
        self.ent_inv_no.config(state = con.NORMAL)  

    def edit_invoice(self, e):
        if self.edit_state:
            pur_id = self.ent_inv_no.get().upper()
            if pur_id == "" :
                msg.showinfo( "Info" , "Edit ಮಾಡುಕೆ ಇರುವ ಬಿಲ್ ನಂಬರ್ ಹಾಕಿ ಎಂಟರ್(Enter) ಒತ್ತಿ ")
                return
            sql = "SELECT pur_id, pur_acc, pur_firm_id, pur_inv, pur_prod_id, pur_prod_qty, pur_exp, date_format(pur_date,'%d-%m-%Y') as pur_date, tax_method, insert_time, insert_id FROM somanath20"+self.year+".purchases where pur_id = '"+ self.year +"_"+pur_id +"'"
            req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
            if req.status_code == 200:
                resp = req.json()
                if len(resp) == 0:
                    msg.showinfo( "Info" , "ಬಿಲ್ ನಂಬರ್ "+pur_id+" save ಇಲ್ಲಾ")
                    self.ent_inv_no.select_range(0,con.END)
                    return
                
                sql1 = "SELECT acc_name , acc_gstin FROM somanath.accounts where acc_id ='" + str(resp[0]["pur_acc"]) +"'"
                req1 = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql1})
                if req1.status_code == 200:
                    ok_cancel = msg.askokcancel("ಪ್ರಶ್ನೆ"," Invoice ನಂಬರ್ \t:"+ resp[0]['pur_inv'] +" \n Supplier \t:"+ req1.json()[0]['acc_name'] +" \n BILL DATE \t:"+ resp[0]["pur_date"] +" \n\n\t ಇದ್ ಎಡಿಟ್ ಮಾಡುಕೆ OK ಒತ್ತಿ \n\n ಬ್ಯಾಡಾ ಅಂಬಾಗ ಇದ್ಧರೇ CANCEL ಒತ್ತಿ \n")
                    if ok_cancel == False:
                        return
                    #edit_begins
                    self.pur_id = resp[0]['pur_id']
                    sql = "select firm_name , firm_gstin from somanath.firms where firm_id = " + str(resp[0]['pur_firm_id'])
                    reqFirm = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})

                    resp[0]['pur_firm_name'] = reqFirm.json()[0]['firm_name']
                    resp[0]['pur_acc_name'] = req1.json()[0]['acc_name'] 
                    

                    
                    req = get("http://"+self.ip+":5000/purchases/edit" , params = resp[0]) 
                    if req.status_code == 201:
                        msg.showinfo("Info" , "ಸ್ವಲ್ಪ ಸಮಯದ ನಂತರ ಮತ್ತೆ  ಪ್ರಯತ್ನಿಸಿ")
                        return

                    resp[0]['pur_firm_gst'] = reqFirm.json()[0]['firm_gstin'] 
                    resp[0]['pur_acc_gst'] = req1.json()[0]['acc_gstin']  

                    tax_method = resp[0]['tax_method']
                    if tax_method == 'OUT':
                        tax_method = 'Out-Of-State'
                    else:
                        tax_method = 'In-State'

                    self.enable_pur_details()
                    self.clear_pur_details()


                    self.combo_supplier.insert(0,resp[0]['pur_acc_name'])
                    self.lbl_sup_gst.config(text = resp[0]['pur_acc_gst'])

                    self.combo_firms.config(state = con.NORMAL)
                    self.combo_firms.delete(0,con.END)
                    self.combo_firms.insert(0,resp[0]['pur_firm_name'])
                    self.combo_firms.config(state = con.DISABLED)
                    self.lbl_firm_gst.config(text = resp[0]['pur_firm_gst'])

                    self.combo_tax_meth.config(state = con.NORMAL)
                    self.combo_tax_meth.delete(0,con.END)
                    self.combo_tax_meth.insert(0,tax_method)
                    self.combo_tax_meth.config(state = "readonly")

                    self.ent_inv_no.delete(0,con.END)
                    self.ent_inv_no.insert(0, resp[0]['pur_inv'])
                    
                    self.ent_pur_date.delete(0,con.END)
                    self.ent_pur_date.insert(0 , resp[0]['pur_date'])
                    self.frm_pur_details.place_forget()
                    self.enable_all()


                    stocks = req.json()

                    reqgst = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select tax_per from somanath.taxes where tax_type = '0'"}).json()
                    reqcess = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select tax_per from somanath.taxes where tax_type = '1'"}).json()

                    

                    gst_tot= {}
                    cess_tot = {}
                    self.added_products = []
                    tot_taxbl_amt = 0
                    
                    for each in reqgst:
                        gst_tot[each['tax_per']] = [0,0,0]

                    for each in reqcess:
                        cess_tot[each['tax_per']] = 0


                    

                    self.lbl_grd_tot.config(text = stocks['trans'][0])
                    self.ent_amt_paid.config(state = con.NORMAL)
                    self.ent_tot_exp.config(state = con.NORMAL)
                    self.ent_amt_paid.insert(0 , stocks['trans'][1])
                    self.ent_tot_exp.insert( 0 ,  "{:.2f}".format(round(float(resp[0]['pur_exp']) , 2)))
                    #self.destroy_pur_details(None)

                    self.combo_pay_meth.config(state = con.NORMAL)
                    self.combo_pay_meth.delete(0 , con.END)
                    if stocks['trans'][2] == 'CASH':
                        self.combo_pay_meth.insert(0 , "CASH")
                    else:
                        self.combo_pay_meth.insert(0 , "UPI/NEFT")
                    self.combo_pay_meth.config(state = "readonly")


                        

                    del stocks['trans']


                    sl_no = 1
                    for each in stocks:
                        tag = 'b'
                        if sl_no %2 == 0:
                            tag = 'a'

                        gst = float(stocks[each][4]) *  (stocks[each][1]/100)
                    
                        if tax_method == 'In-State':    
                            cgst = gst_tot[stocks[each][1]][0] + gst/2
                            sgst = cgst
                            igst = 0

                        else: 
                            cgst = 0
                            sgst = 0
                            igst = gst_tot[stocks[each][1]][2] + gst

                        gst_tot[stocks[each][1]] = [cgst , sgst , igst]
                            
                    
                        cess_tot[stocks[each][23]] = (float(stocks[each][4]) *  (stocks[each][23]/100)) +float( cess_tot[stocks[each][23]])
                        
                        tot_taxbl_amt += float(stocks[each][4])
                        self.added_products.append(int(each))

                        values = (sl_no , stocks[each][0] , stocks[each][1] , stocks[each][2] , stocks[each][3], stocks[each][4], stocks[each][5] , stocks[each][6] , stocks[each][7], stocks[each][8], stocks[each][9], stocks[each][10], stocks[each][11], stocks[each][12], stocks[each][13] , stocks[each][14] , stocks[each][15] , stocks[each][16] , stocks[each][17] , stocks[each][18] , stocks[each][19] , stocks[each][20] , stocks[each][21] , stocks[each][22] , each , stocks[each][23] , stocks[each][24])
                        self.tree_pur.insert('','end',tags=(tag,), values = values)
                        sl_no +=1

                
                    self.sl_no = sl_no

                    
                    for each in self.tree_gst.get_children():
                        self.tree_gst.delete(each)

                    tot_cgst = 0
                    tot_sgst = 0
                    tot_igst = 0
                    tot_cess = 0
                    i = 0
                    for each in gst_tot:
                        tag = 'b'
                        if i %2 == 0:
                            tag = 'a'
                        values = [ each , "{:.2f}".format(round( gst_tot[each][0] , 3)) , "{:.2f}".format(round( gst_tot[each][1] , 3)) ,"{:.2f}".format(round( gst_tot[each][2] , 3))   ]
                        self.tree_gst.insert('','end',tags=(tag,), values = values)
                        i+=1
                        tot_cgst+= float(values[1])
                        tot_sgst+= float(values[2])
                        tot_igst+= float(values[3])

                    for each in self.tree_cess.get_children():
                        self.tree_cess.delete(each)
                    i = 0
                    for each in cess_tot:
                        tag = 'b'
                        if i % 2 == 0:
                            tag = 'a'
                        values = [ each , "{:.2f}".format(round( cess_tot[each] , 3)) ]
                        self.tree_cess.insert('','end',tags=(tag,), values = values)
                        i+=1
                        tot_cess += float(values[1])

            tot_tax = "{:.2f}".format(round(tot_cgst + tot_sgst + tot_igst + tot_cess,2))
            tot_cgst = "{:.2f}".format(round(tot_cgst,2))
            tot_sgst = "{:.2f}".format(round(tot_sgst,2))
            tot_igst = "{:.2f}".format(round(tot_igst,2))
            tot_cess = "{:.2f}".format(round(tot_cess,2))
            tot_taxbl_amt = "{:.2f}".format(round(tot_taxbl_amt,2))
            tot_amt = "{:.2f}".format(float(tot_taxbl_amt) + float(tot_tax))


            self.lbl_tot_cgst.config(text = tot_cgst)
            self.lbl_tot_sgst.config(text = tot_sgst)
            self.lbl_tot_igst.config(text = tot_igst)
            self.lbl_tot_cess.config(text = tot_cess)
            self.lbl_tot_tax.config(text = tot_tax)
            self.lbl_tot_txbl.config(text = tot_taxbl_amt)
            self.lbl_tot_amt.config(text = tot_amt)


            self.combo_firms.config(state = con.DISABLED)
            self.combo_tax_meth.config(state = con.DISABLED)
        
            return #if req.statu_code !=200


                          
        else:
            self.frm_pur_details.place_forget()
            self.enable_all()
             
    def save(self , e):
        if self.prod_id != -1:
            msg.showinfo("Info" , "Add selected product before saving")
            return

        if self.added_products == []:
            msg.showinfo("Info" , "No Products Added")
            return
        
        amt_paid = self.ent_amt_paid.get()

        if amt_paid == "" or amt_paid == ".":
            msg.showinfo("Info" , "Add Amount Paid")
            return

        msgstr = "Check the following details : \n\n Firm Name\t: "+self.combo_firms.get()+" \n Supplier Name\t: "+self.combo_supplier.get()+"\n Supplier GST\t: "+self.lbl_sup_gst.cget("text")+"\n Invoice No\t: "+self.ent_inv_no.get()+"\n Invoice Date\t: "+self.ent_pur_date.get()+"\n Total Taxbl\t: "+self.lbl_tot_txbl.cget("text")+"\n Total GST\t: "+"{:.2f}".format(float(self.lbl_tot_tax.cget("text")) - float(self.lbl_tot_cess.cget("text")))+"\n Grand Total\t: "+self.lbl_grd_tot.cget("text") + "\n Payment Mode\t: "+self.combo_pay_meth.get()
        if not msg.askokcancel("Info" , msgstr):
            return


        exp = self.ent_tot_exp.get()
        if exp == "-" or exp == "" or exp ==".":
            exp = 0
        
        params = {
            "db_year" : self.year,
            "pur_exp" : "{:.2f}".format(round(float(exp),2)),
            "pur_inv" : self.ent_inv_no.get(),
            "amt_paid" : "{:.2f}".format(round(float(amt_paid),2)),
            "pur_bal" : "{:.2f}".format(float(float(self.lbl_grd_tot.cget("text")) - float(amt_paid))) , 
            "pay_meth" : self.combo_pay_meth.get(),
            "grand_total" : "{:.2f}".format(round(float(self.lbl_grd_tot.cget("text"))),2),
            "user_name" : self.user,
            "edit_state" : self.edit_state,
            "pur_id" : self.pur_id

        }


        res = get("http://"+self.ip+":5000/purchases/save" , params = params)
        if res.status_code == 201:
            msg.showerror("Error" , "Someone else is currently saving a bill Try again")
            return

        
        self.clear_all_tree()
        self.btn_edit.config(state = con.NORMAL)
        self.btn_new.config(state = con.NORMAL)
        self.btn_save.config(state = con.DISABLED)
        self.btn_add_dets.config(state = con.DISABLED)
        self.new_state = False
        self.edit_state = False
        self.prod_id = -1
        self.pur_id = -1
        self.prod_gst = -1
        self.prod_cess = -1
        self.sl_no = 1
        self.selected_sl_no = 0
        self.stkDiff = -1
        self.added_products = []
        self.selected_tax_meth = None
        self.check_state = False
        self.forget_prod_list(None)
        self.frm_pur_details.place_forget()
        self.forget_stk_sug(None)
        self.clear_all()
        self.disable_prod_details()
        self.lbl_tot_sgst.config(text = "")
        self.lbl_tot_cgst.config(text = "")
        self.lbl_tot_igst.config(text = "")
        self.lbl_tot_cess.config(text = "")
        self.lbl_tot_txbl.config(text = "")
        self.lbl_tot_tax.config(text = "")
        self.lbl_tot_amt.config(text = "")
        self.lbl_grd_tot.config(text = "")
        self.ent_amt_paid.delete(0,con.END)
        self.disable_all()
        self.clear_pur_details()
        self.disable_pur_details()

    def cancel(self , e):
        if self.pur_id != -1:
            msg.showinfo("Info" , "ಎಡಿಟ್ ಮಾಡಿದ ಬಿಲ್ ಮೊದಲು SAVE ಮಾಡ್ಕೊಳ್ಳಿ")
            return

        ans = msg.askokcancel("Info" , "Do you want to cancel?\n All the products added will be lost!!")
        if not ans:
            return
        self.btn_edit.config(state = con.NORMAL)
        self.btn_new.config(state = con.NORMAL)
        self.btn_save.config(state = con.DISABLED)
        self.btn_cancel.config(state = con.DISABLED)
        self.btn_add_dets.config(state = con.DISABLED)
        self.forget_prod_list(None)
        self.frm_pur_details.place_forget()
        self.forget_stk_sug(None)
        self.clear_all()
        self.clear_all_tree()
        self.ent_amt_paid.delete(0,con.END)
        self.clear_pur_details()
        self.disable_pur_details()
        self.disable_all()
        self.new_state = False
        self.edit_state = False
        self.prod_id = -1
        self.pur_id = -1
        self.sl_no = 1
        self.prod_gst = -1
        self.prod_cess = -1
        self.selected_sl_no = 0
        self.stkDiff = -1
        self.added_products = []
        self.selected_tax_meth = None
        self.check_state = False
        self.ent_tot_exp.delete(0,con.END)
        self.disable_prod_details()
        self.lbl_tot_sgst.config(text = "")
        self.lbl_tot_cgst.config(text = "")
        self.lbl_tot_igst.config(text = "")
        self.lbl_tot_cess.config(text = "")
        self.lbl_tot_txbl.config(text = "")
        self.lbl_tot_tax.config(text = "")
        self.lbl_tot_amt.config(text = "")
        self.lbl_grd_tot.config(text = "")
        get("http://"+self.ip+":5000/purchases/cancelPurchase" )
                
    def refresh(self , e):
        pass
    
    def minimize(self, e):
        self.forget_prod_list(None)
        self.frm_pur_details.place_forget()
        self.forget_stk_sug(None)
        base_window.minimize(self,e)

    def close(self , e):
        if self.new_state or self.edit_state:
            msg.showinfo("Info" , " ಮೊದಲು ಬಿಲ್ SAVE ಇಲ್ಲ CANCEL ಮಾಡ್ಕೊಳ್ಳಿ")
            return
        self.forget_prod_list(None)
        self.frm_pur_details.place_forget()
        self.forget_stk_sug(None)
        base_window.close(self,e)
        

    
    
    