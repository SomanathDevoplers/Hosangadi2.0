from forms import acc
from pyperclip import copy as copy_text
from tkinter import  StringVar, constants as con  , messagebox as msg , ttk , Listbox , Text , IntVar
from requests import get , post
from other_classes import base_window
import datetime
import time
import json
from  tkdocviewer import DocViewer
import os



class sales(base_window):

    def __init__(self , root ,frames , dmsn , lbls ,title,validations, others , sales_form , sio , accounts_form):
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , sales_form)
        if base == None:
            return
        
        self.sio = sio
        self.form_id = others[5]

        self.args = [root ,frames , dmsn , lbls ,title,validations, others , sales_form , sio , accounts_form]
        self.main_frame.grid_propagate(False)
        self.root_frame = frames[0] 
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.screen_height = root.winfo_screenheight()
    
        self.ip = others[0]  
        self.tax_check = others[1] 
        self.root = root
        self.user = others[2]
        self.year = others[3] 


        self.rad_cust_mob = IntVar()
        self.rad_printer = IntVar()
        self.rad_even_odd = IntVar()
        self.rad_select_window = IntVar()
        self.check_gst = StringVar()
        self.t1 = 0
        self.t2 = 0
        self.control = False


        self.new_state = False
        self.edit_state = False
        self.after_save = False
        self.cust_id = -1
        
        self.for_page_change = {}
        self.sale_id = ""
        self.added_products = {}
        self.sl_no = 0

        self.selected_sl_no = 0
        self.prod_id = -1
        self.prod_gst = -1
        self.prod_cess = -1
        self.prod_units = []
        self.prod_sp = []
        self.prod_cp = 0
        self.stk_id = ""
        self.max_qty = 0
        
        self.firm_tot = []
        self.billInfo = {}
        self.voucher = {}
        self.displayed_pdf = ""
        self.rendered_page_count = 0
        self.change_page_count = False
        self.location = os.path.expanduser("~")

        #----------------------------------------cust_name toplevel------------------------------------------------------------------------------#
        if self.screen_height > 1000:
            self.frm_cust_name = ttk.Frame( self.main_frame , height = self.main_hgt*0.594 , width = self.main_wdt*0.227 )#to give white border
        else:
            self.frm_cust_name = ttk.Frame( self.main_frame , height = self.main_hgt*0.608 , width = self.main_wdt*0.228 )#to give white border

        self.frm_cust_name.pack_propagate(False)
        self.frm_cust_name_2 = ttk.Frame( self.frm_cust_name , height = self.main_hgt*0.608-8 , width = self.frm_cust_name.winfo_reqwidth()-8 , style = "root_menu.TFrame")
        self.frm_cust_name_2.grid_propagate(False)

        self.list_cust_name = Listbox(self.frm_cust_name_2 , height = 16 , width = 30 , font = ('Lucida Grande'  , -int(self.main_hgt*0.03) , "bold"))
        self.list_cust_name.bind('<Escape>',self.forget_cust_list)
        self.list_cust_name.bind('<Shift-Tab>',self.forget_cust_list)
        self.list_cust_name.bind('<FocusIn>' , self.clear_cust_details)
        self.list_cust_name.bind('<Tab>',self.get_cust_details)
        self.list_cust_name.bind('<Return>',self.get_cust_details)
        self.list_cust_name.bind('<Double-Button-1>',self.get_cust_details)
        
        
        self.list_cust_name.grid(row = 1 , column = 0 , padx = 1 , pady = 1)
        self.frm_cust_name_2.pack(pady = 4 , padx = 4)

        #----------------------------------------cust_name toplevel ends here--------------------------------------------------------------------#



        #----------------------------------------prod_name toplevel------------------------------------------------------------------------------#
        if self.screen_height>1000:
            self.frm_prod_name = ttk.Frame( self.main_frame , height = self.main_hgt*0.594 , width = self.main_wdt*0.247 )#to give white border
        else:
            self.frm_prod_name = ttk.Frame( self.main_frame , height = self.main_hgt*0.608 , width = self.main_wdt*0.252 )#to give white border
        self.frm_prod_name.pack_propagate(False)

        self.frm_prod_name_2 = ttk.Frame( self.frm_prod_name , height = self.main_hgt*0.608-8 , width = self.frm_prod_name.winfo_screenwidth()-8 , style = "root_menu.TFrame")
        self.frm_prod_name_2.grid_propagate(False)

        self.list_prod_name = Listbox(self.frm_prod_name_2 , height = 16 , width = 32 , font = ('Lucida Grande'  , -int(self.main_hgt*0.03) , "bold"))
        self.list_prod_name.bind('<Escape>',self.forget_prod_list)
        self.list_prod_name.bind('<Shift-Tab>',self.forget_prod_list)
        self.list_prod_name.bind('<Tab>',self.get_prod_by_name)
        self.list_prod_name.bind('<Double-Button-1>',self.get_prod_by_name)
        self.list_prod_name.bind('<Return>',self.get_prod_by_name)
       

        
        self.list_prod_name.grid(row = 1 , column = 0 , padx = 1 , pady = 1)
        self.frm_prod_name_2.pack(pady = 4 , padx = 4)

        
        
        #----------------------------------------prod_name toplevel ends here--------------------------------------------------------------------#








        #----------------------------------------stk_sug toplevel------------------------------------------------------------------------------#

        if self.screen_height > 1000:
            self.frm_stk_sug = ttk.Frame( self.main_frame , height = self.main_hgt*0.34 , width = self.main_wdt*0.577) #to give white border
            self.frm_stk_sug.pack_propagate(False)

            self.frm_stk_sug_2 = ttk.Frame( self.frm_stk_sug , height = self.main_hgt*0.34-8 , width = self.main_wdt*0.577-8 , style = "root_menu.TFrame")
            self.frm_stk_sug_2.grid_propagate(False)
        else:
            self.frm_stk_sug = ttk.Frame( self.main_frame , height = self.main_hgt*0.35 , width = self.main_wdt*0.58) #to give white border
            self.frm_stk_sug.pack_propagate(False)

            self.frm_stk_sug_2 = ttk.Frame( self.frm_stk_sug , height = self.main_hgt*0.35-8 , width = self.main_wdt*0.58-8 , style = "root_menu.TFrame")
            self.frm_stk_sug_2.grid_propagate(False)


        self.lbl_mrp = ttk.Label(self.frm_stk_sug_2 , text = " MRP    :" , style = "window_title.TLabel")
        self.lbl_mrp_1 = ttk.Label(self.frm_stk_sug_2  , width = 8 , style = "window_lbl_ent.TLabel")
        self.lbl_mrp_2 = ttk.Label(self.frm_stk_sug_2  , width = 8 , style = "window_lbl_ent.TLabel")

        self.lbl_tot_stk_txt = ttk.Label(self.frm_stk_sug_2 , text = "Total stock:" , style = "window_title.TLabel")
        self.lbl_tot_stk = ttk.Label(self.frm_stk_sug_2  , width = 10 , style = "window_lbl_ent.TLabel")

        self.lbl_units_txt = ttk.Label(self.frm_stk_sug_2 , text = " UNITS  :" , style = "window_title.TLabel")
        self.lbl_units = ttk.Label(self.frm_stk_sug_2 , style = "window_title.TLabel")


        self.frm_tree_old_stock = ttk.Frame(self.frm_stk_sug_2 , width = self.main_wdt*0.577-16 , height = int(self.main_hgt*0.214))
        if self.screen_height < 1000: self.frm_tree_old_stock.config( height = int(self.main_hgt*0.224)) 
        self.frm_tree_old_stock.pack_propagate(False)
    
        self.tree_old_stk = ttk.Treeview(self.frm_tree_old_stock ,selectmode = "browse", takefocus = True , show = "headings" , style = "window.Treeview" , height = 6)
        self.tree_old_stk.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree_old_stk.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.scroll_y_old_stk = ttk.Scrollbar(self.frm_tree_old_stock , orient = con.VERTICAL , command = self.tree_old_stk.yview)
        self.scroll_x_old_stk = ttk.Scrollbar(self.frm_tree_old_stock , orient = con.HORIZONTAL , command = self.tree_old_stk.xview)
        self.tree_old_stk.config(yscrollcommand = self.scroll_y_old_stk.set , xscrollcommand = self.scroll_x_old_stk.set)

        self.tree_old_stk.bind('<Escape>' , self.focus_prod_qty)
        self.tree_old_stk.bind('<Return>' , self.select_first_stock)
        self.tree_old_stk.bind('<Double-1>' , self.select_first_stock)


        self.tree_old_stk['columns'] = ( 'date','sup','firm','qty','cp','sp')

        self.tree_old_stk.heading('date' , text = 'DATE')
        self.tree_old_stk.heading('sup' , text = 'SUPPLIER')
        self.tree_old_stk.heading('firm' , text = 'FIRM')
        self.tree_old_stk.heading('qty' , text = 'QTY')
        self.tree_old_stk.heading('cp' , text = 'CP')
        self.tree_old_stk.heading('sp' , text = 'SP')


        self.tree_old_stk_wdt = self.frm_tree_old_stock.winfo_reqwidth()-self.scroll_y_old_stk.winfo_reqwidth()
        
        self.tree_old_stk.column('date' , width = int(self.tree_old_stk_wdt*0.16)  , anchor = "w")
        self.tree_old_stk.column('sup' , width = int(self.tree_old_stk_wdt*0.37)  , anchor = "w")
        self.tree_old_stk.column('firm' , width = int(self.tree_old_stk_wdt*0.08)  , anchor = "e")
        self.tree_old_stk.column('qty' , width = int(self.tree_old_stk_wdt*0.13) , anchor = "e")
        self.tree_old_stk.column('cp' , width = int(self.tree_old_stk_wdt*0.13)   , anchor = "e")
        self.tree_old_stk.column('sp' , width = int(self.tree_old_stk_wdt*0.13)   , anchor = "e")

        
        self.scroll_y_old_stk.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x_old_stk.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        self.tree_old_stk.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)

    
        
        self.lbl_mrp.grid(row = 0 , column = 0, sticky = con.W , pady = int(self.main_hgt *0.01))
        self.lbl_mrp_1.grid(row = 0 , column = 1, sticky = con.W)
        self.lbl_mrp_2.grid(row = 0 , column = 2, sticky = con.W)

        self.lbl_tot_stk_txt.grid(row = 0 , column = 3 , sticky = con.E)
        self.lbl_tot_stk.grid(row = 0 , column = 4, sticky = con.E)

        self.lbl_units_txt.grid(row = 1 , column = 0, sticky = con.W )
        self.lbl_units.grid(row = 1 , column = 1 , columnspan = 4 , sticky = con.W) 


       
        self.frm_tree_old_stock.grid(row = 2 , column = 0 , columnspan = 8 , padx = 4 , pady = int(self.main_hgt*0.02))
        self.frm_stk_sug_2.pack(padx = 4 , pady = 4)



        #----------------------------------------stk_sug toplevel ends here--------------------------------------------------------------------#






        #====================================Right main sales window ==================================================================================================#

        self.frm_right = ttk.Frame( self.main_frame , height = int(self.main_hgt) , width = int(self.main_wdt * 0.4) , style= "root_main.TFrame")
        self.frm_right.pack_propagate(False)


        #====================================customer window=======================================================================#
        self.frm_cust_2 = ttk.Frame( self.frm_right , height = int(self.main_hgt) , width = int(self.main_wdt * 0.4)) #to give white border
        self.frm_cust_2.pack_propagate(False)

        self.frm_cust = ttk.Frame( self.frm_cust_2 , height = int(self.main_hgt) - 8 , width = int(self.main_wdt * 0.4)-8 , style = "root_main.TFrame")
        self.frm_cust.grid_propagate(False)

    
        self.lbl_cust_type_txt = ttk.Label(self.frm_cust , text = " Type    :    " , style = "window_text_medium.TLabel")
        self.lbl_cust_type = ttk.Label(self.frm_cust , width = 26 , justify = con.LEFT, style = "window_text_medium.TLabel")        

        self.lbl_cust_bal_txt = ttk.Label(self.frm_cust , text = " Cur Bal :    "  , style = "window_text_medium.TLabel")
        self.lbl_cust_bal = ttk.Label(self.frm_cust  , width = 30 , style = "window_lbl_ent.TLabel")


        self.lbl_cust_mob1_txt = ttk.Label(self.frm_cust , text = " MOB 1   :    " , style = "window_text_medium.TLabel")
        self.lbl_cust_mob1 = ttk.Label(self.frm_cust  , width = 20 , style = "window_lbl_ent.TLabel")
        self.btn_copy_mob1 = ttk.Button(self.frm_cust , text = "Copy" , width = 5 , style = "window_btn_medium.TButton" ,command = lambda : self.copy_mob1(None))
        #self.btn_copy_mob1.bind("<Return>" , self.copy_mob1) 
        self.rad_cust_mob1 = ttk.Radiobutton(self.frm_cust , state = con.DISABLED, value = 0 , variable = self.rad_cust_mob , style = "window_radio.TRadiobutton" )
        

        self.lbl_cust_mob2_txt = ttk.Label(self.frm_cust , text = " MOB 2   :    "  , style = "window_text_medium.TLabel")
        self.lbl_cust_mob2 = ttk.Label(self.frm_cust  , width = 20 , style = "window_lbl_ent.TLabel")
        self.btn_copy_mob2 = ttk.Button(self.frm_cust , text = "Copy" , width = 5 , style = "window_btn_medium.TButton" ,command = lambda : self.copy_mob2(None))
        #self.btn_copy_mob2.bind("<Return>" , self.copy_mob2) 
        self.rad_cust_mob2 = ttk.Radiobutton(self.frm_cust , state = con.DISABLED, value = 1 , variable = self.rad_cust_mob , style = "window_radio.TRadiobutton")


        self.lbl_cust_addr_txt = ttk.Label(self.frm_cust , text = " Address :    "  , style = "window_text_medium.TLabel")
        self.lbl_cust_addr = Text(self.frm_cust  , state = con.DISABLED, width = 30 , height = 4 ,  font = ('Lucida Grande' , -int(self.main_hgt*0.03)))

        self.btn_send = ttk.Button(self.frm_cust ,state = con.DISABLED, text = "Send" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.send(None))
        self.btn_send.bind("<Return>" , self.send)

        self.btn_upd_cust = ttk.Button(self.frm_cust  , state = con.DISABLED, text = "Update Customer" , width = 17 , style = "window_btn_medium.TButton" ,command = lambda : self.upd_cust(None))
        self.btn_upd_cust.bind("<Return>" , self.upd_cust)

        self.lbl_cust_type_txt.grid(row = 0 , column = 0 , pady = int(self.main_hgt * 0.03))
        self.lbl_cust_type.grid(row = 0 , column = 1 , columnspan = 2)

        self.lbl_cust_bal_txt.grid(row = 1 , column = 0 , pady = int(self.main_hgt * 0.03))
        self.lbl_cust_bal.grid(row = 1 , column = 1 , columnspan = 2)

        self.lbl_cust_mob1_txt.grid(row = 2 , column = 0 , pady = int(self.main_hgt * 0.03))
        self.lbl_cust_mob1.grid(row = 2 , column = 1 , sticky = con.W)
        self.btn_copy_mob1.grid(row = 2 , column = 2 , sticky = con.W)
        self.rad_cust_mob1.grid(row = 2 , column = 3 , sticky = con.E)

        self.lbl_cust_mob2_txt.grid(row = 3 , column = 0 , pady = int(self.main_hgt * 0.03))
        self.lbl_cust_mob2.grid(row = 3 , column = 1 , sticky = con.W)
        self.btn_copy_mob2.grid(row = 3 , column = 2 , sticky = con.W)
        self.rad_cust_mob2.grid(row = 3 , column = 3 , sticky = con.E)

        self.lbl_cust_addr_txt.grid(row = 4 , column = 0 , pady = int(self.main_hgt * 0.08))
        self.lbl_cust_addr.grid(row = 4 , column = 1 , columnspan = 2)

        self.btn_upd_cust.grid(row = 5 , column = 1 , sticky = con.W , pady = int(self.main_hgt * 0.03) )
        self.btn_send.grid(row = 5 , column = 2 , sticky = con.E)

        self.frm_cust.pack(pady = 4)
        #====================================customer window End Here==============================================================#

        #====================================sales report window======================================================================#
        self.frm_cashflow_2 = ttk.Frame( self.frm_right , height = int(self.main_hgt )  , width = int(self.main_wdt * 0.4)) #to give white border
        self.frm_cashflow_2.pack_propagate(False)

        self.frm_cashflow = ttk.Frame( self.frm_cashflow_2 , height = int(self.main_hgt ) - 8 , width = int(self.main_wdt * 0.4)-8 , style = "root_main.TFrame")
        self.frm_cashflow.grid_propagate(False)


        self.lbl_cust_cashflow = ttk.Label(self.frm_cashflow , text = " Name :" , style = "window_text_medium.TLabel")
        self.combo_cust_cashflow = ttk.Combobox(self.frm_cashflow , validate="key", validatecommand=(validations[4], '%P') , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 38 , style = "window_combo.TCombobox") 
        self.combo_cust_cashflow.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_cust_cashflow.bind("<Down>" , self.get_customers)
        self.combo_cust_cashflow.bind("<Button-1>" , self.get_customers)


        self.lbl_from_cashflow = ttk.Label(self.frm_cashflow , text = " From :" , style = "window_text_medium.TLabel")
        self.ent_from_cashflow = ttk.Entry(self.frm_cashflow  , width = 10 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_from_cashflow.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_to_cashflow = ttk.Label(self.frm_cashflow , text = "To:" , style = "window_text_medium.TLabel")
        self.ent_to_cashflow = ttk.Entry(self.frm_cashflow  , width = 10,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_to_cashflow.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_limit_cashflow = ttk.Label(self.frm_cashflow , text = " Last :" , style = "window_text_medium.TLabel")
        self.ent_limit_cashflow = ttk.Entry(self.frm_cashflow  , width = 10 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[2], '%P'))
        self.ent_limit_cashflow.bind("<FocusOut>" , self.combo_entry_out)

        self.btn_get_cashflow = ttk.Button(self.frm_cashflow , text = "Get Reports" , width = 12 , style = "window_btn_medium.TButton" ,command = lambda : self.get_cashflow(None) )
        self.btn_get_cashflow.bind("<Return>" , self.get_cashflow)



        if self.screen_height > 1000 : self.frm_tree_cashflow = ttk.Frame(self.frm_cashflow , width = self.main_wdt*0.4-16 , height = int(self.main_hgt*0.65))
        else:self.frm_tree_cashflow = ttk.Frame(self.frm_cashflow , width = self.main_wdt*0.4-16 , height = int(self.main_hgt*0.65))
        self.frm_tree_cashflow.pack_propagate(False)
        self.tree_cashflow = ttk.Treeview(self.frm_tree_cashflow ,selectmode = "browse", takefocus = True , show = "headings" , style = "window.Treeview" , height = 6)
        self.tree_cashflow.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree_cashflow.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.scroll_y_cashflow = ttk.Scrollbar(self.frm_tree_cashflow , orient = con.VERTICAL , command = self.tree_cashflow.yview)
        self.scroll_x_cashflow = ttk.Scrollbar(self.frm_tree_cashflow , orient = con.HORIZONTAL , command = self.tree_cashflow.xview)
        self.tree_cashflow.config(yscrollcommand = self.scroll_y_cashflow.set , xscrollcommand = self.scroll_x_cashflow.set)

        self.tree_cashflow['columns'] = ( 'date','billno','billamt','amtpaid','bal')

        self.tree_cashflow.heading('date' , text = 'DATE')
        self.tree_cashflow.heading('billno' , text = 'BNO')
        self.tree_cashflow.heading('billamt' , text = 'AMT')
        self.tree_cashflow.heading('amtpaid' , text = 'PAID')
        self.tree_cashflow.heading('bal' , text = 'BAL')
    
        self.tree_cashflow_wdt = self.tree_cashflow.winfo_reqwidth()-self.scroll_y_cashflow.winfo_reqwidth()

        
        if self.screen_height > 1000:
            self.tree_cashflow.column('date' , width = int(self.tree_cashflow_wdt*0.145)  , anchor = "w")
            self.tree_cashflow.column('billno' , width = int(self.tree_cashflow_wdt*0.1)  , anchor = "center")
            self.tree_cashflow.column('billamt' , width = int(self.tree_cashflow_wdt*0.16)  , anchor = "e")
            self.tree_cashflow.column('amtpaid' , width = int(self.tree_cashflow_wdt*0.16) , anchor = "e")
            self.tree_cashflow.column('bal' , width = int(self.tree_cashflow_wdt*0.16)   , anchor = "e")
        
        else:
            self.tree_cashflow.column('date' , width = int(self.tree_cashflow_wdt*0.105)  , anchor = "w")
            self.tree_cashflow.column('billno' , width = int(self.tree_cashflow_wdt*0.08)  , anchor = "center")
            self.tree_cashflow.column('billamt' , width = int(self.tree_cashflow_wdt*0.11)  , anchor = "e")
            self.tree_cashflow.column('amtpaid' , width = int(self.tree_cashflow_wdt*0.1) , anchor = "e")
            self.tree_cashflow.column('bal' , width = int(self.tree_cashflow_wdt*0.11)   , anchor = "e")



        self.scroll_y_cashflow.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x_cashflow.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        self.tree_cashflow.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)



        self.lbl_cust_cashflow.grid(row = 0 , column = 0 , pady = int(self.main_hgt*0.01))
        self.combo_cust_cashflow.grid(row = 0 , column = 1 , columnspan = 5 , sticky= con.W )

        self.lbl_from_cashflow.grid(row = 1 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_from_cashflow.grid(row = 1 , column = 1 , sticky= con.W )

        self.lbl_to_cashflow.grid(row = 1 , column = 2 , sticky= con.W)
        self.ent_to_cashflow.grid(row = 1 , column = 3 , sticky= con.W)

        self.lbl_limit_cashflow.grid(row = 2 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_limit_cashflow.grid(row = 2 , column = 1 , sticky= con.W)

        self.btn_get_cashflow.grid(row = 3 , column = 2 , sticky = con.W , columnspan = 2)

        self.frm_tree_cashflow.grid(row = 4 , column = 0 , columnspan = 5 )

        self.frm_cashflow.pack(pady = 4)





        #====================================sales report window======================================================================#
        self.frm_sales_rep_2 = ttk.Frame( self.frm_right , height = int(self.main_hgt )  , width = int(self.main_wdt * 0.4)) #to give white border
        self.frm_sales_rep_2.pack_propagate(False)

        self.frm_sales_rep = ttk.Frame( self.frm_sales_rep_2 , height = int(self.main_hgt ) - 8 , width = int(self.main_wdt * 0.4)-8 , style = "root_main.TFrame")
        self.frm_sales_rep.grid_propagate(False)


        self.lbl_cust_sales_rep = ttk.Label(self.frm_sales_rep , text = " Name :" , style = "window_text_medium.TLabel")
        self.combo_cust_sales_rep = ttk.Combobox(self.frm_sales_rep , validate="key", validatecommand=(validations[4], '%P') , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 38 , style = "window_combo.TCombobox") 
        self.combo_cust_sales_rep.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_cust_sales_rep.bind("<Down>" , self.get_customers)
        self.combo_cust_sales_rep.bind("<Button-1>" , self.get_customers)


        self.lbl_from_sales_rep = ttk.Label(self.frm_sales_rep , text = " From :" , style = "window_text_medium.TLabel")
        self.ent_from_sales_rep = ttk.Entry(self.frm_sales_rep  , width = 10 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_from_sales_rep.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_limit_sales_rep = ttk.Label(self.frm_sales_rep , text = " Last :" , style = "window_text_medium.TLabel")
        self.ent_limit_sales_rep = ttk.Entry(self.frm_sales_rep  , width = 10 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[2], '%P'))
        self.ent_limit_sales_rep.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_to_sales_rep = ttk.Label(self.frm_sales_rep , text = " To :" , style = "window_text_medium.TLabel")
        self.ent_to_sales_rep = ttk.Entry(self.frm_sales_rep  , width = 10,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_to_sales_rep.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_bill_sales_rep = ttk.Label(self.frm_sales_rep , text = " Bill :" , style = "window_text_medium.TLabel")
        self.ent_bill_sales_rep = ttk.Entry(self.frm_sales_rep  , width = 10,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_bill_sales_rep.bind("<FocusOut>" , self.combo_entry_out)


        self.btn_get_sales_rep = ttk.Button(self.frm_sales_rep , text = "Get Reports" , width = 12 , style = "window_btn_medium.TButton" ,command = lambda : self.get_sales_rep(None) )
        self.btn_get_sales_rep.bind("<Return>" , self.btn_get_sales_rep)



        if self.screen_height > 1000 : self.frm_tree_sales_rep = ttk.Frame(self.frm_sales_rep , width = self.main_wdt*0.4-16 , height = int(self.main_hgt*0.65))
        else:self.frm_tree_sales_rep = ttk.Frame(self.frm_sales_rep , width = self.main_wdt*0.4-16 , height = int(self.main_hgt*0.65))
        self.frm_tree_sales_rep.pack_propagate(False)
        self.tree_sales_rep = ttk.Treeview(self.frm_tree_sales_rep ,selectmode = "browse", takefocus = True , show = "headings" , style = "window.Treeview" , height = 6)
        self.scroll_y_sales_rep = ttk.Scrollbar(self.frm_tree_sales_rep , orient = con.VERTICAL , command = self.tree_sales_rep.yview)
        self.scroll_x_sales_rep = ttk.Scrollbar(self.frm_tree_sales_rep , orient = con.HORIZONTAL , command = self.tree_sales_rep.xview)
        self.tree_sales_rep.config(yscrollcommand = self.scroll_y_sales_rep.set , xscrollcommand = self.scroll_x_sales_rep.set)

        self.tree_sales_rep['columns'] = ( 'name','qty','sp','date')

        self.tree_sales_rep.heading('name' , text = 'PRODUCT NAME')
        self.tree_sales_rep.heading('qty' , text = 'QTY')
        self.tree_sales_rep.heading('sp' , text = 'SP')
        self.tree_sales_rep.heading('date' , text = 'DATE')
     
        self.tree_sales_rep.tag_configure('cat1' , background = "#0D0D07" , foreground = "#d9cc99")
        self.tree_sales_rep.tag_configure('cat2' , background = "#05478A" , foreground = "#d9cc99")#417376
        self.tree_sales_rep_wdt = self.tree_sales_rep.winfo_reqwidth()-self.scroll_y_sales_rep.winfo_reqwidth()

        
        if self.screen_height > 1000:
            self.tree_sales_rep.column('name' , width = int(self.tree_sales_rep_wdt*0.5)  , anchor = "w")
            self.tree_sales_rep.column('qty' , width = int(self.tree_sales_rep_wdt*0.15)  , anchor = "center")
            self.tree_sales_rep.column('sp' , width = int(self.tree_sales_rep_wdt*0.15)  , anchor = "e")
            self.tree_sales_rep.column('date' , width = int(self.tree_sales_rep_wdt*0.15) , anchor = "e")

        
        else:
            self.tree_sales_rep.column('name' , width = int(self.tree_sales_rep_wdt*0.35)  , anchor = "w")
            self.tree_sales_rep.column('qty' , width = int(self.tree_sales_rep_wdt*0.15)  , anchor = "e")
            self.tree_sales_rep.column('sp' , width = int(self.tree_sales_rep_wdt*0.15)  , anchor = "e")
            self.tree_sales_rep.column('date' , width = int(self.tree_sales_rep_wdt*0.15) , anchor = "e")



        self.scroll_y_sales_rep.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x_sales_rep.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        self.tree_sales_rep.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)



        self.lbl_cust_sales_rep.grid(row = 0 , column = 0 , pady = int(self.main_hgt*0.01))
        self.combo_cust_sales_rep.grid(row = 0 , column = 1 , columnspan = 5 , sticky= con.W )

        self.lbl_from_sales_rep.grid(row = 1 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_from_sales_rep.grid(row = 1 , column = 1 , sticky= con.W )

        self.lbl_to_sales_rep.grid(row = 1 , column = 2 , sticky= con.W)
        self.ent_to_sales_rep.grid(row = 1 , column = 3 , sticky= con.W)

        self.lbl_limit_sales_rep.grid(row = 2 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_limit_sales_rep.grid(row = 2 , column = 1 , sticky= con.W)

        self.lbl_bill_sales_rep.grid(row = 2 , column = 2 , sticky= con.W)
        self.ent_bill_sales_rep.grid(row = 2 , column = 3 , sticky= con.W)

        self.btn_get_sales_rep.grid(row = 3 , column = 1 , sticky = con.E , columnspan = 2)
        self.frm_tree_sales_rep.grid(row = 4 , column = 0,  columnspan = 4 ) 
        self.frm_sales_rep.pack(pady = 4)


        #====================================sales report window End Here==============================================================#


        #====================================bill print window==========================================================================#
        self.frm_pdf_2 = ttk.Frame( self.frm_right , height = int(self.main_hgt ) , width = int(self.main_wdt * 0.4)) #to give white border
        self.frm_pdf_2.pack_propagate(False)

        self.frm_pdf = ttk.Frame( self.frm_pdf_2 , height = int(self.main_hgt ) - 8 , width = int(self.main_wdt * 0.4)-8 , style = "root_main.TFrame")
        self.frm_pdf.grid_propagate(False)

        self.lbl_vch_bill_no_txt = ttk.Label(self.frm_pdf , text = "BillNo:" , style = "window_text_medium.TLabel")

        self.lbl_vch_bill_no = ttk.Label(self.frm_pdf , width = 7 , justify = con.LEFT, style = "window_text_medium.TLabel") 

        self.lbl_cust_vch = ttk.Label(self.frm_pdf , text = " Name :" , style = "window_text_medium.TLabel")

        self.combo_cust_vch = ttk.Combobox(self.frm_pdf , validate="key", state = con.NORMAL, validatecommand=(validations[4], '%P') , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 38 , style = "window_combo.TCombobox") 
        self.combo_cust_vch.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_cust_vch.bind("<<ComboboxSelected>>" , self.get_customer_vch_details)
        self.combo_cust_vch.bind("<KeyRelease>" , self.retrict_vch_entry)
        self.combo_cust_vch.bind("<Down>" , self.get_customers)
        self.combo_cust_vch.bind("<Button-1>" , self.get_customers)

        self.lbl_cash_paid = ttk.Label(self.frm_pdf , text = " CASH :"  , style = "window_text_medium.TLabel")
        self.ent_cash_paid = ttk.Entry(self.frm_pdf  , width = 7 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[2], '%P'))
        self.ent_cash_paid.bind("<KeyRelease>",self.cal_vch_bal)
        self.ent_cash_paid.bind("<FocusOut>" , self.combo_entry_out)
        
        self.lbl_bank_paid = ttk.Label(self.frm_pdf , text = " BANK :"  , style = "window_text_medium.TLabel")
        self.ent_bank_paid = ttk.Entry(self.frm_pdf  , width = 7 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[2], '%P'))
        self.ent_bank_paid.bind("<KeyRelease>",self.cal_vch_bal)
        self.ent_bank_paid.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_tot_paid_txt = ttk.Label(self.frm_pdf , text = "TotPaid: " , style = "window_text_medium.TLabel")
        self.lbl_tot_paid = ttk.Label(self.frm_pdf  , width = 7 , style = "window_lbl_ent.TLabel")

        self.lbl_old_bal_txt = ttk.Label(self.frm_pdf , text = " Old Bal:" , style = "window_text_medium.TLabel")
        self.lbl_old_bal = ttk.Label(self.frm_pdf  , width = 8 , style = "window_lbl_ent.TLabel")

        self.lbl_bill_amt_txt = ttk.Label(self.frm_pdf , text = " BillAmt:" , style = "window_text_medium.TLabel")
        self.lbl_bill_amt = ttk.Label(self.frm_pdf  , width = 8 , style = "window_lbl_ent.TLabel")

        self.lbl_fin_bal_txt = ttk.Label(self.frm_pdf , text = " Fin Bal:" , style = "window_text_medium.TLabel")
        self.lbl_fin_bal = ttk.Label(self.frm_pdf  , width = 8 , style = "window_lbl_ent.TLabel")

        self.btn_save_vch = ttk.Button(self.frm_pdf , text = "SAVE" , width = 10 , style = "window_btn_medium.TButton" ,command = lambda : self.save_vch(None),state=con.DISABLED)
        self.btn_save_vch.bind("<Return>" , self.save_vch)
        self.btn_vch = ttk.Button(self.frm_pdf , text = "VCH ONLY" , width = 10 , style = "window_btn_medium.TButton" ,command = lambda : self.print_only_vch(None),state=con.DISABLED)
        self.btn_vch.bind("<Return>" , self.print_only_vch)
        self.btn_vch_bill = ttk.Button(self.frm_pdf , text = "VCH + BILL" , width = 10 , style = "window_btn_medium.TButton" ,command = lambda : self.print_both(None), state=con.DISABLED)
        self.btn_vch_bill.bind("<Return>" , self.print_both)

        if self.screen_height > 1000:self.frm_line = ttk.Frame( self.frm_pdf , height = 4 , width = int(self.main_wdt * 0.395)) 
        else:self.frm_line = ttk.Frame( self.frm_pdf , height = 4 , width = int(self.main_wdt * 0.393)) 

        self.lbl_pdf_bill_no = ttk.Label(self.frm_pdf , text = "BillNo:" , style = "window_text_medium.TLabel")
        self.ent_pdf_bill_no = ttk.Entry(self.frm_pdf  , width = 7 , state = con.NORMAL ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_pdf_bill_no.bind("<Return>" , self.bill_pdf_only)
        
        self.lbl_page_range = ttk.Label(self.frm_pdf , text = "Range:" , style = "window_text_medium.TLabel")
        self.ent_page_range = ttk.Entry(self.frm_pdf  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_page_range.bind('<KeyRelease>' , self.show_page_range)
        

        self.rad_odd_only = ttk.Radiobutton(self.frm_pdf , text = "Odd " ,  value = 0 , variable = self.rad_even_odd , style = "window_radio_med.TRadiobutton", state = con.DISABLED ,  command = self.show_odd_pages)
        self.rad_even_only = ttk.Radiobutton(self.frm_pdf , text = "Even ", value = 1 , variable = self.rad_even_odd , style = "window_radio_med.TRadiobutton", state = con.DISABLED ,  command = self.show_even_pages)
        self.rad_printer_1 = ttk.Radiobutton(self.frm_pdf , text = "EPSON  ", value = 0 , variable = self.rad_printer , style = "window_radio_med.TRadiobutton", state = con.DISABLED, command = self.select_page)
        self.rad_printer_2 = ttk.Radiobutton(self.frm_pdf , text = "SHREYANS", value = 1 , variable = self.rad_printer , style = "window_radio_med.TRadiobutton", state = con.DISABLED, command = self.select_page)
        
        if self.screen_height > 1000: self.frm_bill = ttk.Frame( self.frm_pdf , height = int(self.main_hgt *0.659 ) , width = int(self.main_wdt * 0.225))
        else : self.frm_bill = ttk.Frame( self.frm_pdf , height = int(self.main_hgt *0.55 ) , width = int(self.main_wdt * 0.315))
        self.frm_bill.pack_propagate(False)


        self.pdf = DocViewer(self.frm_bill ,  scrollbars = "vertical")
        self.pdf.bind('<<DocumentFinished>>' , self.pdf_loaded)
        self.pdf.pack(fill = con.BOTH ,expand = 1 )
        
        #self.print_btn_frame = ttk.Frame(self.frm_pdf , style = "root_main.TFrame")
        self.btn_bill_only = ttk.Button(self.frm_pdf , text = "BILL" , state = con.DISABLED , width = 5 , style = "window_btn_medium.TButton" ,command = lambda : self.print_only_bill(None))
        self.btn_bill_only.bind("<Return>" , self.print_only_bill)
        self.btn_print_bill = ttk.Button(self.frm_pdf , text = "PRINT", state = con.DISABLED , width = 5, style = "window_btn_medium.TButton" ,command = lambda : self.print(None))
        self.btn_print_bill.bind("<Return>" , self.print)

        self.chk_gst_bill = ttk.Checkbutton(self.frm_pdf  , state = con.DISABLED, text = "GST",  style = "window_check.TCheckbutton" , variable = self.check_gst , onvalue = 'True' , offvalue = 'False')
    
        #self.lbl_vch_bill_no_txt.grid(row = 0 , column = 0 , pady = int(self.main_hgt*0.01))
        #self.lbl_vch_bill_no.grid(row = 0 , column = 1)
        self.lbl_cust_vch.grid(row = 0 , column = 0)
        self.combo_cust_vch.grid(row = 0 , column = 1 , columnspan = 4 , sticky= con.W , pady = int(self.main_hgt*0.01))


        self.lbl_cash_paid.grid(row = 1 , column = 0, pady = int(self.main_hgt*0.01))
        self.ent_cash_paid.grid(row = 1 , column = 1)
        self.lbl_old_bal_txt.grid(row = 1 , column = 2 )
        self.lbl_old_bal.grid(row = 1 , column = 3  , sticky = con.W)
        self.btn_save_vch.grid(row = 1 , column = 4 , sticky = con.E)

        self.lbl_bank_paid.grid(row = 2 , column = 0, pady = int(self.main_hgt*0.01))
        self.ent_bank_paid.grid(row = 2 , column = 1)
        self.lbl_bill_amt_txt.grid(row = 2 , column = 2)
        self.lbl_bill_amt.grid(row = 2 , column = 3 , sticky = con.W)
        self.btn_vch.grid(row = 2 , column = 4 ,  sticky = con.E)


        self.lbl_tot_paid_txt.grid(row = 3 , column = 0, pady = int(self.main_hgt*0.01))
        self.lbl_tot_paid.grid(row = 3 , column = 1)
        self.lbl_fin_bal_txt.grid(row = 3 , column = 2)
        self.lbl_fin_bal.grid(row = 3 , column = 3 ,  sticky = con.W)
        self.btn_vch_bill.grid(row = 3 , column = 4 , sticky = con.E)

        self.frm_line.grid(row = 4 , column = 0 , columnspan = 5)


        self.lbl_pdf_bill_no.grid(row = 5 , column = 0, pady = int(self.main_hgt*0.01))
        self.ent_pdf_bill_no.grid(row = 5 , column = 1)
        self.lbl_page_range.grid(row = 5 , column = 3)
        self.ent_page_range.grid(row = 5 , column = 4)

        self.rad_odd_only.grid(row = 6 , column = 0, pady = int(self.main_hgt*0.01))
        self.rad_even_only.grid(row = 6 , column = 1)
        self.chk_gst_bill.grid(row = 6 , column = 3)
        #self.rad_printer_1.grid(row = 6 , column = 3)
        #self.rad_printer_2.grid(row = 6 , column = 4)

        if self.screen_height>1000:
            self.frm_bill.grid(row = 7 , column = 0 , columnspan =  4 , rowspan = 2)
            self.btn_bill_only.grid(row = 7 , column = 4 , sticky = con.S)
            self.btn_print_bill.grid(row = 8 , column = 4 , sticky = con.S)

        else:
            self.frm_bill.grid(row = 7 , column = 0 , columnspan = 5)
            #self.print_btn_frame.grid(row = 8 , column = 1  , sticky = con.W,  pady = int(self.main_hgt*0.01))
            self.btn_bill_only.grid(row = 8 , column = 1  , sticky = con.W,  pady = int(self.main_hgt*0.01))
            self.btn_print_bill.grid(row = 8 , column = 3  , sticky = con.W,  pady = int(self.main_hgt*0.01))


        self.frm_pdf.pack(pady = 4)
        #====================================bill print window End Here==================================================================#


        #self.frm_cust_2.pack()
        #self.frm_sales_2.pack()
        #self.frm_vch_2.pack()
        #self.frm_pdf_2.pack()


        #====================================Right main sales window End Here==============================================================================================#








        #====================================left main sales window==================================================================#

        self.frm_sales_2 = ttk.Frame( self.main_frame , height = self.main_hgt , width = int(self.main_wdt * 0.6)) #to give white border
        self.frm_sales_2.pack_propagate(False)

        self.frm_sales = ttk.Frame( self.frm_sales_2 , height = self.main_hgt - 8 , width = int(self.main_wdt * 0.6)-8 , style = "root_main.TFrame")
        self.frm_sales.grid_propagate(False)


        #===============================row 1 sales window========================================================#
        self.frm_row1 = ttk.Frame( self.frm_sales  , style = "root_main.TFrame")
        self.frm_row1.grid_propagate(True)

        self.lbl_bill_no = ttk.Label(self.frm_row1 , text = " Bill :"  , style = "window_text_medium.TLabel")
        self.ent_bill_no = ttk.Entry(self.frm_row1  , width = 7 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[6], '%P'))
        self.ent_bill_no.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_bill_no.bind("<Return>",self.get_invoice_details)

        self.lbl_bill_date = ttk.Label(self.frm_row1 , text = " Date :"  , style = "window_text_medium.TLabel")
        self.ent_bill_date = ttk.Entry(self.frm_row1  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[8], '%P'))
        self.ent_bill_date.bind("<FocusOut>" , self.check_date)

        self.lbl_cust_name = ttk.Label(self.frm_row1 , text = "  Customer :"  , style = "window_text_medium.TLabel")
        self.ent_cust_name = ttk.Entry(self.frm_row1  , width = 30 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[4], '%P'))
        self.ent_cust_name.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_cust_name.bind('<KeyRelease>' , self.get_cust_list)
        self.ent_cust_name.bind('<Down>' , self.focus_cust_list)
        self.ent_cust_name.bind('<Escape>' , self.forget_cust_list)
        self.ent_cust_name.bind('<Shift-Tab>' , self.forget_cust_list)
        self.ent_cust_name.bind('<FocusIn>' , self.forget_stk_sug)

    
        self.lbl_bill_no.grid(row = 0 , column = 0 )
        self.ent_bill_no.grid(row = 0 , column = 1 )

        self.lbl_bill_date.grid(row = 0 , column = 2 )
        self.ent_bill_date.grid(row = 0 , column = 3 )

        self.lbl_cust_name.grid(row = 0 , column = 4)
        self.ent_cust_name.grid(row = 0 , column = 5)

        #===============================row 1 sales window ends here==============================================#



        #===============================row 2 sales window========================================================#
        self.frm_row2 = ttk.Frame( self.frm_sales  , style = "root_main.TFrame")
        self.frm_row2.grid_propagate(True)

        """self.lbl_prod = ttk.Label(self.frm_row2 , text = " Product Name/Barcode   "  , style = "window_text_medium.TLabel")
        self.lbl_prod_hsn = ttk.Label(self.frm_row2 , text = " HSN "  , style = "window_text_medium.TLabel")
        self.lbl_prod_qty = ttk.Label(self.frm_row2 , text = " QTY "  , style = "window_text_medium.TLabel")
        self.lbl_prod_sp = ttk.Label(self.frm_row2 , text = " SP "  , style = "window_text_medium.TLabel")
        self.lbl_prod_total = ttk.Label(self.frm_row2 , text = " TOTAL  "  , style = "window_text_medium.TLabel")"""

        self.lbl_row2_spacer = ttk.Label(self.frm_row2 , text = " "  , style = "window_text_medium.TLabel")
        self.ent_prod = ttk.Entry(self.frm_row2  , width = 33 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[4], '%P'))
        self.ent_prod.bind('<FocusOut>' , self.combo_entry_out)
        self.ent_prod.bind('<KeyRelease>' , self.get_prod_list)
        self.ent_prod.bind('<Down>' , self.focus_prod_list)
        self.ent_prod.bind('<Escape>' , self.forget_prod_list)
        self.ent_prod.bind('<Shift-Tab>' , self.forget_prod_list)
        self.ent_prod.bind('<FocusIn>' , self.focus_prod)
        self.ent_prod.bind('<Return>' , self.get_prod_by_bar)

        
        self.ent_prod_qty = ttk.Entry(self.frm_row2  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_prod_qty.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_prod_qty.bind("<KeyRelease>" , self.cal_by_qty)
        self.ent_prod_qty.bind('<Down>' , self.focus_first_stock)
        self.ent_prod_qty.bind('<Return>' , self.enter_to_treeview)



        self.ent_prod_sp = ttk.Entry(self.frm_row2  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_prod_sp.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_prod_sp.bind("<KeyRelease>" , self.cal_by_sp)
        self.ent_prod_sp.bind('<Down>' , self.focus_first_stock)
        self.ent_prod_sp.bind('<Return>' , self.enter_to_treeview)



        self.ent_prod_total = ttk.Entry(self.frm_row2  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)))

        self.ent_prod_hsn = ttk.Entry(self.frm_row2  , width = 10 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[2], '%P'))
        self.ent_prod_hsn.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_prod_hsn.bind("<KeyRelease>" , self.cal_by_hsn)
        self.ent_prod_hsn.bind('<Down>' , self.focus_first_stock)
        self.ent_prod_hsn.bind('<Return>' , self.enter_to_treeview)




        """
        self.lbl_prod.grid(row = 0 , column = 1)
        self.lbl_prod_hsn.grid(row = 0 , column = 2)
        self.lbl_prod_qty.grid(row = 0 , column = 3)
        self.lbl_prod_sp.grid(row = 0 , column = 4)
        self.lbl_prod_total.grid(row = 0 , column = 5)"""
        
        if self.screen_height>1000:
            self.lbl_row2_spacer.grid(row = 0 , column = 0)

        self.ent_prod.grid(row = 0 , column = 1)
        self.ent_prod_qty.grid(row = 0 , column = 2)
        self.ent_prod_sp.grid(row = 0 , column = 3)
        self.ent_prod_total.grid(row = 0 , column = 4)
        self.ent_prod_hsn.grid(row = 0 , column = 5)
        
        


        #===============================row 2 sales window ends here==============================================#





        #===============================row 3 sales window========================================================#
        self.frm_row3 = ttk.Frame( self.frm_sales  , style = "root_main.TFrame")
        self.frm_row3.pack_propagate(True)


        self.tree_sales = ttk.Treeview(self.frm_row3 ,selectmode = "browse", takefocus = True , show = "headings" , style = "window.Treeview" , height = 8)
        self.tree_sales.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree_sales.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.tree_sales.tag_configure('avail' , background = "#53eb90" , foreground = "#000")
        self.tree_sales.tag_configure('nonAvail' , background = "#D10000" , foreground = "#000")
        self.tree_sales.tag_configure('edit' , background = "#419EDC" , foreground = "#000")


        self.tree_sales.tag_configure('SSM' , background = "#00A0CC" , foreground = "#D9CC9C")
        self.tree_sales.tag_configure('SCM' , background = "#D10000" , foreground = "#D9CC9C")
        self.tree_sales.tag_configure('SEM' , background = "#417376" , foreground = "#D9CC9C")#417376


        self.scroll_y_sales = ttk.Scrollbar(self.frm_row3 , orient = con.VERTICAL , command = self.tree_sales.yview)
        self.scroll_x_sales = ttk.Scrollbar(self.frm_row3 , orient = con.HORIZONTAL , command = self.tree_sales.xview)
        self.tree_sales.config(yscrollcommand = self.scroll_y_sales.set , xscrollcommand = self.scroll_x_sales.set)

        self.tree_sales.bind('<Delete>' , self.delete_from_treeview)
        self.tree_sales.bind('<Double-Button-1>' , self.select_from_treeview)
        self.tree_sales.bind('<Return>' , self.delete_from_treeview)

        self.tree_sales['columns'] = ( 'slNo', 'prodName'  , 'qty' , 'sp' , 'total' ,'hsn')
        self.tree_sales.heading('slNo' , text = 'NO')
        self.tree_sales.heading('prodName' , text = 'PRODUCT NAME')
        self.tree_sales.heading('qty' , text = 'QTY')
        self.tree_sales.heading('sp' , text = 'SP')
        self.tree_sales.heading('total' , text = 'TOTAL')
        self.tree_sales.heading('hsn' , text = 'HSN')

        
        self.tree_sales_wdt = self.tree_sales.winfo_reqwidth()-self.scroll_y_sales.winfo_reqwidth()
    
        if self.screen_height>1000:
            self.tree_sales.column('slNo' , width = int(self.tree_sales_wdt*0.045)  , anchor = "center")
            self.tree_sales.column('prodName' , width = int(self.tree_sales_wdt*0.38)  , anchor = "w")
            self.tree_sales.column('qty' , width = int(self.tree_sales_wdt*0.122) , minwidth = int(self.tree_sales_wdt*0.1), anchor = "e")
            self.tree_sales.column('sp' , width = int(self.tree_sales_wdt*0.122) , minwidth = int(self.tree_sales_wdt*0.08) , anchor = "e")
            self.tree_sales.column('total' , width = int(self.tree_sales_wdt*0.122) , minwidth = int(self.tree_sales_wdt*0.08), anchor = "e")
            self.tree_sales.column('hsn' , width = int(self.tree_sales_wdt*0.122) , minwidth = int(self.tree_sales_wdt*0.08)  , anchor = "e")
        else:
            self.lbl_row2_spacer.config(text = "")
            self.tree_sales.column('slNo' , width = int(self.tree_sales_wdt*0.034)  , anchor = "center")
            self.tree_sales.column('prodName' , width = int(self.tree_sales_wdt*0.265)  , anchor = "w")
            self.tree_sales.column('qty' , width = int(self.tree_sales_wdt*0.088) , minwidth = int(self.tree_sales_wdt*0.01), anchor = "e")
            self.tree_sales.column('sp' , width = int(self.tree_sales_wdt*0.088) , minwidth = int(self.tree_sales_wdt*0.01) , anchor = "e")
            self.tree_sales.column('total' , width = int(self.tree_sales_wdt*0.088) , minwidth = int(self.tree_sales_wdt*0.01), anchor = "e")
            self.tree_sales.column('hsn' , width = int(self.tree_sales_wdt*0.088) , minwidth = int(self.tree_sales_wdt*0.01)  , anchor = "e")


        self.scroll_y_sales.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x_sales.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        self.tree_sales.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)

        #===============================row 3 sales window ends here==============================================#





        #===============================row 3 sales window========================================================#
        
        self.frm_row4 = ttk.Frame( self.frm_sales  , style = "root_main.TFrame" )
        #self.frm_row4.grid_propagate(True)


        self.frm_select_window = ttk.Frame( self.frm_row4  , style = "root_main.TFrame" )
        self.rad_cust = ttk.Radiobutton(self.frm_select_window , text = "Customer Details", value = 0 , variable = self.rad_select_window , style = "window_radio_med.TRadiobutton" ,command = lambda : self.select_window(None))
        self.rad_vch_bill = ttk.Radiobutton(self.frm_select_window , text = "VCH & Print Preview" ,  value = 1 , variable = self.rad_select_window , style = "window_radio_med.TRadiobutton" ,command = lambda : self.select_window(None))
        self.rad_stocks = ttk.Radiobutton(self.frm_select_window , text = "Sales Report", value = 2 , variable = self.rad_select_window , style = "window_radio_med.TRadiobutton" ,command = lambda : self.select_window(None))
        self.rad_cashflow = ttk.Radiobutton(self.frm_select_window , text = "Cashflow", value = 3 , variable = self.rad_select_window , style = "window_radio_med.TRadiobutton",command = lambda : self.select_window(None))
        self.rad_cust.grid(row = 0 , column = 0  , sticky = con.W , pady = int(self.main_hgt*0.01))
        self.rad_vch_bill.grid(row = 1 , column = 0  , sticky = con.W, pady = int(self.main_hgt*0.01))
        self.rad_stocks.grid(row = 2 , column = 0  , sticky = con.W, pady = int(self.main_hgt*0.01))
        self.rad_cashflow.grid(row = 3 , column = 0  , sticky = con.W, pady = int(self.main_hgt*0.01))




        self.frm_totals = ttk.Frame( self.frm_row4  , style = "root_main.TFrame" )
        self.lbl_total_txt = ttk.Label(self.frm_totals , text = "                Totals  : "  , style = "window_text_medium.TLabel")
        
        self.lbl_total_amt = ttk.Label(self.frm_totals  , width = 10 , style = "window_lbl_ent.TLabel")
        self.lbl_total_hsn = ttk.Label(self.frm_totals  , width = 10 , style = "window_lbl_ent.TLabel")


        #self.lbl_grd_tot_txt = ttk.Label(self.frm_totals , text = "  Total :"  , style = "window_text_medium.TLabel")
        #self.lbl_grd_tot = ttk.Label(self.frm_totals  , width = 10 , style = "window_lbl_ent.TLabel")

        #if self.screen_height<1000:
            #self.lbl_total_txt.config(text = "                Totals  : ")
            #self.lbl_grd_tot.config( width = 11)
        
        self.lbl_total_txt.grid(row = 0 , column = 0 )
        self.lbl_total_amt.grid(row = 0 , column = 1 )
        self.lbl_total_hsn.grid(row = 0 , column = 2 )


        #self.lbl_grd_tot_txt.grid(row = 2 , column = 1)
        #self.lbl_grd_tot.grid(row = 2 , column = 2)

        

        self.frm_select_window.pack(side = con.LEFT , padx = int(self.main_wdt * 0.01))
        self.frm_totals.pack(side = con.RIGHT)

        #===============================row  sales window ends here==============================================#


        #===============================btn frame================================================================#

        self.btn_frame = ttk.Frame(self.frm_sales , style = "root_main.TFrame")

        self.btn_new = ttk.Button(self.btn_frame , text = "New" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.new(None))
        self.btn_new.bind("<Return>" , self.new) 
        self.btn_edit = ttk.Button(self.btn_frame , text = "Edit" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.edit(None))
        self.btn_edit.bind("<Return>" , self.edit)
        self.btn_save = ttk.Button(self.btn_frame , text = "Save" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.save(None) , state = con.DISABLED)
        self.btn_save.bind("<Return>" , self.save)
        self.btn_cancel = ttk.Button(self.btn_frame , text = "Cancel" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.cancel(None) , state = con.DISABLED)
        self.btn_cancel.bind("<Return>" , self.cancel)

        self.btn_new.grid(row = 0 , column = 0 , padx = int(self.main_wdt*0.01))
        self.btn_edit.grid(row = 0 , column = 1 , padx = int(self.main_wdt*0.01))
        self.btn_save.grid(row = 0 , column = 2 , padx = int(self.main_wdt*0.01))
        self.btn_cancel.grid(row = 0 , column = 3 , padx = int(self.main_wdt*0.01))


        #===============================btn frame Ends here=======================================================#




        self.frm_row1.grid(row = 0 , column = 0 , pady = int(self.main_wdt * 0.01))
        self.frm_row2.grid(row = 1 , column = 0)
        self.frm_row3.grid(row = 2 , column = 0)
        self.frm_row4.grid(row = 3 , column = 0)
        self.btn_frame.grid(row = 4 , column = 0 , sticky = con.E , pady = int(self.main_hgt*0.02))

        self.frm_sales.pack(pady = 4)
        
        
        #====================================left main sales window End Here==========================================================#


        self.frm_sales_rep_2.grid(row = 0 , column = 0)
        self.frm_cashflow_2.grid(row = 0 , column = 0)
        self.frm_cust_2.grid(row = 0 , column = 0)
        self.frm_pdf_2.grid(row = 0 , column = 0)

        self.rad_select_window.set(1)
        self.frm_sales_2.grid(row = 0 , column = 0 , rowspan = 2)
        self.frm_right.grid(row = 1 , column = 1 )
        self.forget_stk_sug(None)
      
        self.btn_new.focus_set()
    
    """-------------------------------------Customer Functions------------------------------------------"""
    

    def get_cust_list(self , e):
        #-------backspace----------Aa----------------Zz---------------space---------------0------------------9-----------------.
        if not (e.keycode == 8  or (e.keycode>=65 and e.keycode<=97) or e.keycode == 32 or e.keysym in ['0' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '0'] or e.keycode == 190):
            return

        text = self.ent_cust_name.get().upper()
        if text == "":
            self.forget_cust_list(None)
            self.clear_cust_details(None)
            return


        self.list_cust_name.delete(0,con.END)
        req = get("http://"+self.ip+":4000/getCustName" , params = {"cust_name" : text}).json()

        for each in req: self.list_cust_name.insert(con.END , each)
        
        if self.screen_height > 1000: self.frm_cust_name.place( x = int(self.main_wdt * 0.364) , y = int(self.main_hgt * 0.065))
        else: self.frm_cust_name.place( x = int(self.main_wdt * 0.367) , y = int(self.main_hgt * 0.071))

        self.frm_cust_name.lift()
        self.clear_cust_details(None)

    def focus_cust_list(self , e):
        if self.list_cust_name.size() > 0: 
            self.list_cust_name.focus_set()
            self.list_cust_name.selection_set(0)
            self.clear_cust_details(None)

    def forget_cust_list(self,e):
        self.frm_cust_name.place_forget()
        #when shift-tab is pressed focus set to barcode 27 is escape
        if e != None and e.keycode == 27:
            self.ent_cust_name.focus_set()
            return
        if e!= None and e.keycode == 9:
            self.ent_bill_date.focus_set()
            pass

    def get_cust_details(self , e):
        name = self.list_cust_name.get(self.list_cust_name.curselection())
        if name == "":
            return

        self.ent_cust_name.delete(0 , con.END)
        self.ent_cust_name.insert(0 , name)

        sql = "select accounts.acc_id, acc_cus_type,  acc_cls_bal_firm1 + acc_cls_bal_firm2 + acc_cls_bal_firm3 as acc_cls_bal  ,  acc_mob1, acc_mob2, acc_add from somanath.accounts , somanath20"+ self.year +".acc_bal where acc_name ='"+ name + "' and accounts.acc_id = acc_bal.acc_id "
        cust = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql }).json()
        if cust == []:
            return
        cust = cust[0]
       
        self.acc_title.config(text = name)
        

        self.cust_id = cust['acc_id']
        self.frm_cust_name.place_forget()
        self.lbl_cust_type.config(text = cust['acc_cus_type'])
        self.cust_type = cust['acc_cus_type']
        
        self.lbl_cust_bal.config(text = "{:.2f}".format(round(float(cust['acc_cls_bal']),2)))
        self.lbl_cust_mob1.config(text = cust['acc_mob1'])
        self.lbl_cust_mob2.config(text = cust['acc_mob2'])
        self.lbl_cust_addr.config(state = con.NORMAL)
        self.lbl_cust_addr.delete(0.0 , con.END)
        self.lbl_cust_addr.insert(0.0 , cust['acc_add'])
        self.lbl_cust_addr.config(state = con.DISABLED)
        self.rad_cust_mob.set(-1)
        self.rad_cust_mob1.config(state = con.DISABLED)
        self.rad_cust_mob2.config(state = con.DISABLED)
        self.btn_copy_mob1.config(state = con.NORMAL)
        self.btn_copy_mob2.config(state = con.NORMAL)


        if cust['acc_mob1'] != '' and cust['acc_mob2'] != '':
            self.rad_cust_mob1.config(state = con.NORMAL)
            self.rad_cust_mob2.config(state = con.NORMAL)
            self.rad_cust_mob.set(-1)

        if cust['acc_mob1'] != '' and cust['acc_mob2'] == '':
            self.rad_cust_mob1.config(state = con.NORMAL)
            self.rad_cust_mob.set(0)

        if cust['acc_mob1'] == '' and cust['acc_mob2'] != '':
            self.rad_cust_mob2.config(state = con.NORMAL)
            self.rad_cust_mob.set(1)

        
        params = {
                'sale_id'   : self.sale_id , 
                'sale_date' : self.ent_bill_date.get() , 
                'cust_name' : name, 
                'form_id'   : self.form_id
        }

        req = get("http://"+self.ip+":5000/sales/addEditNewSalesDetails" , params = params).json()
        self.sale_id = req['saleId']

        self.btn_send.config(state = con.NORMAL)
        self.btn_upd_cust.config(state = con.NORMAL)


        #correct
        self.frm_cust_2.lift()
        self.rad_select_window.set(0)
        self.enable_prod()
        self.ent_prod.focus()

    def clear_cust_details(self , e):
        self.lbl_cust_type.config(text = "")
        self.lbl_cust_bal.config(text = "")
        self.lbl_cust_mob1.config(text = "")
        self.lbl_cust_mob2.config(text = "")
        self.lbl_cust_addr.config(state = con.NORMAL)
        self.lbl_cust_addr.delete(0.0 , con.END)
        self.lbl_cust_addr.config(state = con.DISABLED)
        self.rad_cust_mob.set(-1)
        self.btn_send.config(state = con.DISABLED)
        self.btn_upd_cust.config(state = con.DISABLED)
        self.btn_copy_mob1.config(state = con.DISABLED)
        self.btn_copy_mob2.config(state = con.DISABLED)
        self.disable_prod()
        
    def copy_mob1(self , e):
        copy_text(self.lbl_cust_mob1.cget("text"))
        
    def copy_mob2(self , e):
        copy_text(self.lbl_cust_mob2.cget("text"))

    def upd_cust(self , e):
        arglist = [ self.args[0] , self.args[1] , self.args[2] , self.args[3] , "Accounts" ,  [self.args[5][0] , self.args[5][4] , self.args[5][7] , self.args[5][9] , self.args[5][3]] , [self.args[6][4] , self.args[6][0] , self.args[6][1] , self.args[6][2] , self.args[6][3]] , self.args[9] , self.cust_id ]
        acc(arglist[0] , arglist[1] , arglist[2] , arglist[3] , arglist[4] , arglist[5] , arglist[6] , arglist[7] , arglist[8]  )
        
        

    def send(self , e):
        if self.rad_cust_mob.get():
            #@mob yake
            mob = self.lbl_cust_mob2.cget("text")
        if not self.rad_cust_mob.get():
            mob = self.lbl_cust_mob1.cget("text")


    """-------------------------------------------------------------------------------------------------"""

    
    """-------------------------------------Product Functions-------------------------------------------"""

    def get_prod_list(self , e): 
        #-------backspace----------Aa----------------Zz---------------space---------------0------------------9-----------------.--------------------------enter
        if not (e.keycode == 8 or (e.keycode>=65 and e.keycode<=97) or e.keycode == 32 or e.keysym in ['0' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '0'] or e.keycode == 190 or e.keycode == 13):
            return


        text = self.ent_prod.get().upper()
        if text == "":
            self.forget_prod_list(None)
            return
            

        x = 0.00000
        if len(text) == 1:
            self.t1 = time.time()
            self.forget_prod_list(None)
            self.control = False

        if len(text) == 2:
            self.t2 = time.time()
            x = self.t2 - self.t1
            self.t1 = time.time()
            if (x) < 0.1:
                self.control = False
            else:
                self.control = True


        if len(text) == 3:
            self.t3 = time.time()
            x = self.t3 - self.t2
            self.t1 = time.time()
            if (x) > 0.5:
                self.control = True
        

        if self.control:
            self.list_prod_name.delete(0,con.END)
            req = get("http://"+self.ip+":4000/getNameFew" , params = {"prod_name" : text}).json()
            
            
            if len(req) >0:
                for each in req: self.list_prod_name.insert(con.END , each)

                if self.screen_height > 1000:self.frm_prod_name.place( x = int(self.main_wdt * 0.025) , y = int(self.main_hgt * 0.124))
                else: self.frm_prod_name.place( x = int(self.main_wdt * 0.019) , y = int(self.main_hgt * 0.135))

                self.frm_prod_name.lift()

    def focus_prod_list(self , e):
        if self.list_prod_name.size() > 0: 
            self.list_prod_name.focus_set()
            self.list_prod_name.selection_set(0)

    def forget_prod_list(self,e):
        self.frm_prod_name.place_forget()
        #when shift-tab is pressed focus set to barcode | 27 is escape
        if e != None and e.keycode == 27:
            self.ent_prod.focus_set()
            return
        if e!= None and e.keycode == 9:
            self.ent_prod.focus_set()

    def get_prod_by_bar(self , e):
        bar = self.ent_prod.get()
        if bar == "" :
            return

        prod = get("http://"+self.ip+":4000/getProdByBar" , params = {'prod_bar' : ":"+bar+":"}).json()

        if len(prod) == 0:
            msg.showinfo("Info" , "ಈ Barcode Add ಇಲ್ಲ")
            self.ent_prod.delete(0 , con.END)
        else:
            self.ent_prod.delete(0 , con.END)
            self.ent_prod.insert(0 , prod[0]['prod_name'])
            self.get_prod_by_name(None)
        
    def get_prod_by_name(self , e):
        stk_id = []
        loc = []
        
        if e == None:
            name = self.ent_prod.get()
        else:
            name = self.list_prod_name.get(self.list_prod_name.curselection())
            if name == "":
                return

        prod = get("http://"+self.ip+":4000/getProdByName" , params = {'prod_name' : name}).json()
        if prod == []:
            return
        prod = prod[0]

        if str(prod['prod_id']) in self.added_products:
            found_sl_no = ""
            for each in self.added_products[str(prod['prod_id'])][1]:
                if each == '':
                    for each in self.added_products[str(prod['prod_id'])][0] : found_sl_no += " " + str(each) +" ,"
                    msg.showinfo("Info","ಈ Item ADD ಮಾಡಲಾಗಿದೆ \n \n ಕ್ರಮ ಸಂಖ್ಯೆ  : " + found_sl_no[:-1] + " \n \n  ಅದನ್ನೇ CHANGE ಮಾಡಿ")
                    self.ent_prod.delete(0,con.END)
                    self.ent_prod.focus_set()
                    self.frm_prod_name.place_forget()
                    return
            

            for each in self.added_products[str(prod['prod_id'])][0] : found_sl_no += " " + str(each) +" ,"
            msg.showinfo("Info","ಈ Item ADD ಮಾಡಲಾಗಿದೆ \n \n ಕ್ರಮ ಸಂಖ್ಯೆ  : " + str(found_sl_no)[:-1] + " \n \n  ಅದನ್ನೇ CHANGE ಮಾಡಿ")
            stk_id =  self.added_products[str(prod['prod_id'])][1]
            loc = self.added_products[str(prod['prod_id'])][0]
                


        self.prod_gst = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select tax_per from somanath.taxes where tax_id = " + str(prod['prod_gst'])  }).json()[0]['tax_per']
        self.prod_cess = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select tax_per from somanath.taxes where tax_id = " + str(prod['prod_cess'])  }).json()[0]['tax_per']   
        

        self.prod_id = prod['prod_id']

        cust_type = self.lbl_cust_type.cget("text").lower()
        self.prod_units = prod[cust_type +"_unit"].split(":")[1:-1]

        self.ent_prod.delete(0,con.END)
        self.ent_prod.insert(0, name)

        self.get_stk_sug(stk_id , loc)

    def get_stk_sug(self , stk_id , loc):
        cust_type = self.lbl_cust_type.cget("text").lower()
        stocks = get("http://"+self.ip+":5000/sales/getSalesStocks" , params = {'prod_id' : self.prod_id , 'year' : self.year , 'spType' : cust_type , 'form_id'   : self.form_id}).json()
        
        if stocks == []:
            msg.showinfo("Info" , "stock ಖಾಲಿಯಾಗಿದೆ")
            self.selected_sl_no = 0
            self.prod_id = -1
            self.prod_gst = -1
            self.prod_cess = -1
            self.prod_units = []
            self.prod_sp = []
            self.prod_cp = 0
            self.stk_id = ""
            self.max_qty = 0
            self.ent_prod.focus_set()
            self.ent_prod.select_range(0 , con.END)
            return

        for each in self.tree_old_stk.get_children():
            self.tree_old_stk.delete(each)

        tot_stk_qty = round(stocks[0]['stk_tot_qty'] , 3)

       

        i = 0
        for each in stocks:
            if i%2 == 0: tag = 'a'
            else: tag = 'b'

            global_stocks = get("http://"+self.ip+":5000/getGlobalStocks" , params = {'prod_id' :self.prod_id , 'form_id'   : self.form_id}).json() 

            if each['stk_id'] in stk_id :
                continue

            prod_qty = round(each['stk_prod_qty'],3)

            if each['stk_id'] in global_stocks:
                prod_qty = round(prod_qty - float(global_stocks[each['stk_id']]) , 3)
                if prod_qty <= 0:
                    continue

            sp = each['stk_sp_'+cust_type].split(":")[1:-1]
            units = each[cust_type+'_unit'].split(":")[1:-1]
            values = (  each['pur_date']  , each['acc_name'] , each['firm_suffix'] , "{:.3f}".format(prod_qty) , "{:.2f}".format(round(each['stk_cost'],2)) , sp[0] , sp , units  , each['stk_id'])
            self.tree_old_stk.insert('','end' ,tags=(tag,), values = values)
            i+=1

        if i == 0:
            sl_no = ""
            for each in loc:
                sl_no += " " + str(each) + " ,"

            if sl_no != "":
                msg.showinfo("Info","ಈ Item ADD ಮಾಡಲಾಗಿದೆ \n \n ಕ್ರಮ ಸಂಖ್ಯೆ  : " + sl_no[:-1] + " \n \n  ಅದನ್ನೇ CHANGE ಮಾಡಿ")
            else:
                msg.showinfo("Info","ಈ Item ಬೇರೆ ಬಿಲ್ ನಲ್ಲಿ   ADD ಮಾಡಲಾಗಿದೆ \n \n  ಹಾಗಾಗಿ ಸ್ಟಾಕ್ ಖಾಲಿಯಾಗಿದೆ")

            self.selected_sl_no = 0
            self.prod_id = -1
            self.prod_gst = -1
            self.prod_cess = -1
            self.prod_units = []
            self.prod_sp = []
            self.prod_cp = 0
            self.stk_id = ""
            self.max_qty = 0
            self.ent_prod.focus_set()
            self.ent_prod.delete(0 , con.END)
            return

        firstItem = self.tree_old_stk.get_children()[0]
        firstItem = self.tree_old_stk.item(firstItem)['values']

        self.prod_units = firstItem[7].split()
        self.prod_sp = firstItem[6].split()
        self.prod_cp = float(firstItem[4])

        for each in global_stocks:
            tot_stk_qty -= round(float(global_stocks[each]),3)

        if len(stk_id) == 0:
            self.stk_id = ""
            self.max_qty = tot_stk_qty
        else:
            self.stk_id = str(firstItem[8])[0:2]+"_"+str(firstItem[8])[2:]
            self.max_qty = float(firstItem[3])

        self.lbl_tot_stk.config( text = "{:.3f}".format(tot_stk_qty) + " " + stocks[0]['prod_unit_type']) 
        self.lbl_mrp_1.config(text = "{:.2f}".format(round((stocks[0]['prod_mrp']),2)))
        self.lbl_mrp_2.config(text = "{:.2f}".format(round((stocks[0]['prod_mrp_old']),2)))
        self.lbl_units.config(text = self.prod_units[0] + "  ,  " + self.prod_units[1] + "  ,  " + self.prod_units[2] + "  ,  " + self.prod_units[3] )

        self.forget_prod_list(None)

        if self.screen_height >1000 : self.frm_stk_sug.place(x = int(self.main_wdt * 0.004) , y = self.main_hgt* 0.165)
        else : self.frm_stk_sug.place(x = int(self.main_wdt * 0.006) , y = self.main_hgt* 0.188)
        self.frm_stk_sug.lift()

        self.enable_prod_details()
        self.clear_prod_details()

        self.ent_prod_total.config(state = con.NORMAL)
        self.ent_prod_total.delete(0,con.END)
        self.ent_prod_total.insert(0,"{:.2f}".format(round( float(self.prod_sp[0]) * 1 , 2)))
        self.ent_prod_total.config(state = con.DISABLED)

        self.ent_prod_sp.insert(0 ,self.prod_sp[0])
        if self.max_qty >= 1:
            self.ent_prod_qty.insert(0 , "1.000")
        else:
            self.ent_prod_qty.insert(0 , self.max_qty)

        self.ent_prod_qty.select_range(0,con.END)
        self.ent_prod_qty.focus_set()

        pro_per ="{:.2f}".format(round((((float(self.prod_sp[0])/self.prod_cp ) - 1) * 100 ) , 3))
        self.ent_prod_hsn.insert( 0,pro_per)

    def forget_stk_sug(self , e):
        self.frm_stk_sug.place_forget()

    def focus_first_stock(self , e):
        child = self.tree_old_stk.get_children()
        if len(child) == 0:
            return

        self.tree_old_stk.focus_set()
        self.tree_old_stk.focus(child[0])
        self.tree_old_stk.selection_set(child[0])

    def select_first_stock(self , e):
        curItem = self.tree_old_stk.focus()
        curItem = self.tree_old_stk.item(curItem)
        curItem = curItem['values']
        if len(curItem) == 0:
            return

        self.prod_sp = curItem[6].split()
        self.prod_cp = round(float(curItem[4]),3)
        self.max_qty = round(float(curItem[3]),3)
        self.stk_id = str(curItem[8])[0:2] + "_" + str(curItem[8])[2:]
        

        qty = self.ent_prod_qty.get()
        if qty == "" or qty == ".":
            qty = 0
        

        if float(qty) > self.max_qty:
            qty = self.max_qty

        self.ent_prod_qty.delete(0,con.END)
        self.ent_prod_qty.insert(0 , "{:.3f}".format(round(float(qty),3)))

        self.ent_prod_total.config(state = con.NORMAL)
        self.ent_prod_total.delete(0,con.END)
        self.ent_prod_total.insert(0,"{:.2f}".format(round( float(self.prod_sp[0]) * float(qty) , 2)))
        self.ent_prod_total.config(state = con.DISABLED)

        self.ent_prod_sp.delete(0,con.END)
        self.ent_prod_sp.insert(0 , self.prod_sp[0])
        
        pro_per ="{:.2f}".format(round((((float(self.prod_sp[0])/self.prod_cp ) - 1) * 100 ) , 3))
        self.ent_prod_hsn.delete(0,con.END)
        self.ent_prod_hsn.insert( 0,pro_per)

        self.ent_prod_qty.select_range(0,con.END)
        self.ent_prod_qty.focus_set()

    def focus_prod(self , e):
        self.clear_prod_details()
        self.disable_prod_details()
        self.forget_cust_list(None)
        self.forget_stk_sug(None)

    def focus_prod_qty(self , e):
        self.ent_prod_qty.focus_set()
        self.ent_prod_qty.select_range(0 , con.END)

    def enter_to_treeview(self , e):
        sp = self.ent_prod_sp.get()
        qty = self.ent_prod_qty.get()
        name = self.ent_prod.get()
        
        try:
            float(qty)
        except ValueError:
            msg.showinfo("Info" , "ENTER QTY")
            return



        if float(qty) > float(self.max_qty):
            msg.showinfo("Info" , "ENTER QTY < " + "{:.3f}".format(round(self.max_qty,3)))
            self.ent_prod_qty.delete(0,con.END)
            self.ent_prod_qty.insert(0 , "{:.3f}".format(round(self.max_qty,3)))
            self.ent_prod_qty.focus_set()
            self.ent_prod_qty.select_range(0,con.END)
            return
        self.ent_prod_total.config(state = con.NORMAL)
        tot = self.ent_prod_total.get()
        self.ent_prod_total.config(state = con.DISABLED)

        if float(tot)   <= 0:
            msg.showinfo("Info" , " SP ಮತ್ತು QTY ಹಾಕಿ ")
            return
        try:
            qty = "{:.3f}".format(round(float(qty),3))
            sp = "{:.2f}".format(round(float(sp),2))
            hsn = "{:.2f}".format(round((float(sp) - float(self.prod_cp) ) * float(qty) , 2))
        except ValueError:
            msg.showinfo('Info' , " QTY , SP , HSN ಚೆಕ್ ಮಾಡಿ ")
            self.ent_prod_qty.focus_set()
            return
            
        if float(qty) <= 0 or float(sp) <= 0:
            msg.showinfo('Info' ," QTY , SP 0 ಕಿಂತ ಹೆಚ್ಚು ಹಾಕಿ ")
            self.ent_prod_qty.focus_set()
            return

    
        
           

        
        if self.selected_sl_no != 0:
            tag = 'b'
            if self.selected_sl_no %2 == 0:
                tag = 'a'

            values = (self.selected_sl_no , name , qty , sp , tot , hsn , self.prod_units , self.prod_sp , self.prod_cp , self.max_qty , self.prod_gst , self.prod_cess , self.stk_id , self.prod_id)
            self.tree_sales.insert('', self.selected_sl_no - 1 ,tags=(tag,), values = values)

            if str(self.prod_id) in self.added_products:
                self.added_products[str(self.prod_id)][0].append(self.selected_sl_no)
                self.added_products[str(self.prod_id)][1].append(self.stk_id)
            else:
                self.added_products[str(self.prod_id)] = [[self.selected_sl_no] , [self.stk_id]]
            
        else:
            tag = 'a'
            if self.sl_no %2 == 0:
                tag = 'b'
            self.sl_no += 1

            values = (self.sl_no , name , qty , sp , tot , hsn , self.prod_units , self.prod_sp , self.prod_cp , self.max_qty , self.prod_gst , self.prod_cess , self.stk_id , self.prod_id)
            self.tree_sales.focus(self.tree_sales.insert('','end',tags=(tag,), values = values))

            if str(self.prod_id) in self.added_products:
                self.added_products[str(self.prod_id)][0].append(self.sl_no)
                self.added_products[str(self.prod_id)][1].append(self.stk_id)
            else:
                self.added_products[str(self.prod_id)] = [[self.sl_no] , [self.stk_id]]



        self.cal_totals(values , True)

        self.selected_sl_no = 0
        self.prod_id = -1
        self.prod_gst = -1
        self.prod_cess = -1
        self.prod_units = []
        self.prod_sp = []
        self.prod_cp = 0
        self.stk_id = ""
        self.max_qty = 0

        
        self.ent_prod.delete(0 , con.END)
        self.ent_prod.focus_set()
        values = list(values)

        units = "\"["
        for each in values[6]:
             units += '"' + "{:.3f}".format(float(each)) + '",' 
        units = units[0:-1] + "]\""

        sp = "\"["
        for each in values[7]:
             sp += '"' + "{:.2f}".format(float(each)) + '",'
        sp = sp[0:-1] + "]\""

        values[6] = str(values[6])
        values[7] = str(values[7])
        
        get("http://"+self.ip+":5000/sales/addSalesProduct" , params = {"product" : values , 'sale_id' : self.sale_id , 'form_id'   : self.form_id} )

        


    def select_from_treeview(self , e):
        if self.prod_id != -1:
            msg.showwarning("Warning" , "A Product is selected")
            return
        
        if self.after_save:
            return
    
    
        curItemNo = self.tree_sales.focus()
        if not (curItemNo in self.tree_sales.get_children()):
            return

        values =  self.tree_sales.item(curItemNo)['values']

        tags =  self.tree_sales.item(curItemNo)['tags'][0]
        #values = (self.selectd_sl_no , name , qty , sp , tot , hsn , self.prod_units , self.prod_sp , self.prod_cp , self.max_qty , self.prod_gst , self.prod_cess , self.stk_id , self.prod_id)
 
        self.selected_sl_no = int(values[0])
        self.prod_id = int(values[13])
        self.prod_gst = round(float(values[10]),1)
        self.prod_cess = round(float(values[11]),1)
        self.prod_units = values[6].split()
        self.prod_sp = values[7].split()
        self.prod_cp = float(values[8])
        self.max_qty = float(values[9])
        self.stk_id = values[12]
        
        if tags == 'nonAvail':
            self.max_qty = round(float(values[14]),3)
        
        if self.stk_id != "":
            self.stk_id = str(values[12])[0:2]+"_"+str(values[12])[2:]


        if self.added_products[str(values[13])][1][0] == '':
            del self.added_products[str(values[13])]
        else:
            self.added_products[str(values[13])][0].remove(values[0])
            self.added_products[str(values[13])][1].remove(self.stk_id)

            if len(self.added_products[str(values[13])][0]) == 0:
                del self.added_products[str(values[13])]


        
        self.clear_prod_details()
        self.enable_prod_details()
        self.ent_prod.delete(0 , con.END)
        self.ent_prod.insert(0 , values[1])
        self.ent_prod_qty.insert(0 , values[2])
        self.ent_prod_sp.insert(0 , values[3])
        self.ent_prod_total.config(state = con.NORMAL)
        self.ent_prod_total.delete(0 , con.END)
        self.ent_prod_total.insert(0 , values[4])
        self.ent_prod_total.config(state = con.DISABLED)
        self.ent_prod_hsn.insert(0 , values[5])
        self.ent_prod_qty.focus_set()

        self.tree_sales.detach(curItemNo)


        self.cal_totals(values , False)
        values = list(values)
        values[12] = self.stk_id

        if tags == 'edit':
            new = False
        else:
            new = True

        get("http://"+self.ip+":5000/sales/removeSalesProduct" , params = {"product" : values , 'sale_id' : self.sale_id , 'newBill' : new , 'db_year' : self.year , 'form_id'   : self.form_id})

        if tags == 'edit':
            self.clear_prod_details()
            self.enable_prod_details()
            #self.ent_prod.insert(0 , values[1])
            self.list_prod_name.delete(0 , con.END)
            self.list_prod_name.insert( 0 , values[1])
            self.get_prod_by_name(None)
            #self.ent_prod_qty.delete(0,con.END)
            #self.ent_prod_qty.insert(0 , values[2])
            self.ent_prod_qty.select_range(0,con.END)
            self.ent_prod_qty.focus_set()
            

    def delete_from_treeview(self,e):
        if self.after_save:
            return

        curItemNo = self.tree_sales.focus()
        values =  self.tree_sales.item(curItemNo)['values']
        if len(values) == 0:
            return

        tags = self.tree_sales.item(curItemNo)['tags'][0]
        delete_values = values

        #values = (self.sl_no , name , qty , sp , tot , hsn , self.prod_units , self.prod_sp , self.prod_cp , self.max_qty , self.prod_gst , self.prod_cess , self.stk_id , self.prod_id)
        stk_id = ''
        if values[12] != '':
            stk_id = str(values[12])[0:2]+"_"+str(values[12])[2:]
        sl_no_delete = values[0]
        if self.added_products[str(values[13])][1][0] == '':
            del self.added_products[str(values[13])]
        else:
            self.added_products[str(values[13])][0].remove(values[0])
            self.added_products[str(values[13])][1].remove(stk_id)

            if len(self.added_products[str(values[13])][0]) == 0:
                del self.added_products[str(values[13])]

        self.cal_totals(values , False)
       
        items = self.tree_sales.get_children()
        curIndex = self.tree_sales.index(curItemNo)
        i = 0
        for each in items:
            if i > curIndex:
                values = self.tree_sales.item(each)['values']
                tags = self.tree_sales.item(each)['tags'][0]

                values[0] = i
                tag = 'b'
                if i %2 == 0:
                    tag = 'a'

                if tags != 'a' and tags != 'b':
                    tag = tags

                self.tree_sales.detach(each)
                self.tree_sales.insert('',i,tags=(tag,), values = values)
            i +=1

        self.sl_no = len(items) - 1

        self.tree_sales.detach(curItemNo)
        
        for each in self.added_products:
            j = 0
            for i in self.added_products[str(each)][0]:
                if i > sl_no_delete:
                    self.added_products[str(each)][0][j] =  self.added_products[str(each)][0][j] - 1
                j += 1

        self.selected_sl_no = 0
        self.prod_id = -1
        self.prod_gst = -1
        self.prod_cess = -1
        self.prod_units = []
        self.prod_sp = []
        self.prod_cp = 0
        self.stk_id = ""
        self.max_qty = 0

        self.ent_prod.focus_set()
        delete_values = list(delete_values)
        if stk_id == '':
            stk_id = 'stkId'
        delete_values[12] = stk_id
        if tags == 'edit':
            new = False
        else:
            new = True
        
        

        get("http://"+self.ip+":5000/sales/removeSalesProduct" , params = {"product" : delete_values , 'sale_id' : self.sale_id , 'newBill' : new , 'db_year' : self.year , 'form_id'   : self.form_id} )

    """-------------------------------------------------------------------------------------------------"""

    """-------------------------------------calculation Functions---------------------------------------"""

    def cal_by_qty(self , e):
        qty = self.ent_prod_qty.get()
        sp = self.ent_prod_sp.get()
        if qty == "" or qty == ".":
            qty = 0

        if sp == "" or sp == "." :
            sp = 0

        qty = float(qty)

        if qty > float(self.max_qty):
            msg.showinfo("Info" , "ENTER QTY < " + "{:.3f}".format(round(self.max_qty,3)))
            self.ent_prod_qty.delete(0,con.END)
            self.ent_prod_qty.insert(0 , "{:.3f}".format(round(self.max_qty,3)))
            self.ent_prod_qty.focus_set()
            self.ent_prod_qty.select_range(0,con.END)
            return


        if qty >= float(self.prod_units[3]):
            sp = self.prod_sp[3]
        elif qty >= float(self.prod_units[2]):
            sp = self.prod_sp[2]
        elif qty >= float(self.prod_units[1]):
            sp = self.prod_sp[1]
        else:
            sp = self.prod_sp[0]


        sp = round(float(sp) , 3)
        self.ent_prod_sp.delete(0 , con.END)
        self.ent_prod_sp.insert( 0 , "{:.2f}".format(sp))

        pro_per ="{:.2f}".format(round((((float(sp)/float(self.prod_cp) ) - 1) * 100 ) , 3))

        self.ent_prod_hsn.delete(0,con.END)
        self.ent_prod_hsn.insert(0, pro_per)

        total = "{:.2f}".format(round(sp*qty,3))

        self.ent_prod_total.config(state = con.NORMAL)
        self.ent_prod_total.delete(0,con.END)
        self.ent_prod_total.insert(0, total)
        self.ent_prod_total.config(state = con.DISABLED)
   
    def cal_by_sp(self , e):
        qty = self.ent_prod_qty.get()
        sp = self.ent_prod_sp.get()
        
        if qty == "" or qty == ".":
            qty = 0

        if sp == "" or sp == "." :
            sp = 0

        total = "{:.2f}".format(round(float(sp)*float(qty),3))

        self.ent_prod_total.config(state = con.NORMAL)
        self.ent_prod_total.delete(0,con.END)
        self.ent_prod_total.insert(0, total)
        self.ent_prod_total.config(state = con.DISABLED)

        pro_per ="{:.2f}".format(round((((float(sp)/float(self.prod_cp) ) - 1) * 100 ) , 3))

        self.ent_prod_hsn.delete(0,con.END)
        self.ent_prod_hsn.insert(0, pro_per)

    def cal_by_hsn(self , e):
        qty = self.ent_prod_qty.get()
        hsn = self.ent_prod_hsn.get()
        
        if qty == "" or qty == ".":
            qty = 0


        if hsn == "" or hsn == "." or hsn == '-' or hsn == '-.':
            hsn = 0

        
        sp = "{:.2f}".format(round((1 + float(hsn)/100) * float(self.prod_cp) , 2))

        total = "{:.2f}".format(round(float(sp)*float(qty),3))

        self.ent_prod_total.config(state = con.NORMAL)
        self.ent_prod_total.delete(0,con.END)
        self.ent_prod_total.insert(0, total)
        self.ent_prod_total.config(state = con.DISABLED)

        self.ent_prod_sp.delete(0,con.END)
        self.ent_prod_sp.insert(0, sp)
      
    def cal_totals(self , values , addOrDel):
        tot = self.lbl_total_amt.cget("text")
        hsn = self.lbl_total_hsn.cget("text")

        if addOrDel:
            self.lbl_total_amt.config( text = "{:.2f}".format( round( float(tot) + float(values[4]) , 2) ))
            self.lbl_total_hsn.config( text = "{:.2f}".format( round( float(hsn) + float(values[5]) , 2) ))
        else:
            self.lbl_total_amt.config( text = "{:.2f}".format( round( float(tot) - float(values[4]) , 2) ))
            self.lbl_total_hsn.config( text = "{:.2f}".format( round( float(hsn) - float(values[5]) , 2) ))

    def cal_vch_bal(self,e):
        try:
            y = float(self.ent_bank_paid.get())
        except ValueError:          
            y = 0

        try:
            x = float(self.ent_cash_paid.get())
        except ValueError:          
            x = 0

        
        tot_paid = round( y + x ,2 )
        self.lbl_tot_paid.config( text = "{:.2f}".format(tot_paid))
        self.lbl_fin_bal.config( text ="{:.2f}".format(round(float(self.lbl_old_bal.cget('text')) + float(self.lbl_bill_amt.cget('text')) - tot_paid,2)))
       
    

    """-------------------------------------------------------------------------------------------------"""

    """-------------------------------------Utilities----------------------------------------------------"""


    def combo_entry_out(self , e):
        e.widget.select_clear()

    def enable_all_details(self):
        self.ent_bill_no.config(state = con.NORMAL)
        self.ent_bill_date.config(state = con.NORMAL)
        self.ent_cust_name.config(state = con.NORMAL)
        
    def clear_all_details(self):
        self.ent_bill_no.delete(0 , con.END)
        self.ent_bill_date.delete(0 , con.END)
        self.ent_cust_name.delete(0 , con.END)
        self.lbl_total_amt.config(text = "")
        self.lbl_total_hsn.config(text = "")
        #self.lbl_grd_tot.config(text = "")
     
    def disable_all_details(self):
        self.ent_bill_no.config(state = con.DISABLED)
        self.ent_bill_date.config(state = con.DISABLED)
        self.ent_cust_name.config(state = con.DISABLED)

    def enable_prod(self):
        self.ent_prod.delete(0,con.END)
        self.ent_prod.config(state = con.NORMAL)

    def disable_prod(self):
        self.ent_prod.delete(0,con.END)
        self.ent_prod.config(state = con.DISABLED)
        self.forget_prod_list(None)
        self.forget_stk_sug(None)

    def enable_prod_details(self):
        self.ent_prod_sp.config(state = con.NORMAL)
        self.ent_prod_hsn.config(state = con.NORMAL)
        self.ent_prod_qty.config(state = con.NORMAL)

    def clear_prod_details(self):
        self.ent_prod_qty.delete(0,con.END)
        self.ent_prod_sp.delete(0,con.END)
        self.ent_prod_total.config(state = con.NORMAL)
        self.ent_prod_total.delete(0,con.END)
        self.ent_prod_total.config(state = con.DISABLED)
        self.ent_prod_hsn.delete( 0 ,con.END)
     
    def disable_prod_details(self):
        self.ent_prod_qty.config(state = con.DISABLED)
        self.ent_prod_sp.config(state = con.DISABLED)
        self.ent_prod_hsn.config(state = con.DISABLED)
        self.ent_prod_qty.config(state = con.DISABLED)

    def check_date(self , e):
        date = self.ent_bill_date.get().upper()

        date1 = date.split("/")
        if len(date1)!=3:
            date1 = date.split("-")
            if len(date1) != 3:
                msg.showinfo("Info" , "Enter date in following format \n 'dd-mm-yy' or 'dd/mm/yy ")
                self.ent_bill_date.focus_set()
                self.ent_bill_date.select_range(0,con.END)
                return

        try:
            datetime.datetime(int(date1[2]), int(date1[1]), int(date1[0]))
        except ValueError:
            msg.showinfo("Info" , "Enter correct date")
            self.ent_bill_date.focus_set()
            self.ent_bill_date.select_range(0,con.END)
            return

        
        if len(date1[2])%2 !=0 :
            msg.showinfo("Info" , "Enter correct date")
            self.ent_bill_date.focus_set()
            self.ent_bill_date.select_range(0,con.END)
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
                self.ent_bill_date.focus_set()
                self.ent_bill_date.select_range(0,con.END)
                return

        self.ent_bill_date.delete(0,con.END)
        self.ent_bill_date.insert(0,date1[0] + "-" + date1[1] + "-" + date1[2])        
        self.ent_bill_date.select_clear()

        if self.sale_id != "" and self.lbl_cust_type.cget("text") != "":
            params = {
                    'sale_id'   : self.sale_id , 
                    'sale_date' : self.ent_bill_date.get() , 
                    'cust_name' : self.ent_cust_name.get().upper(), 
                    'form_id'   : self.form_id
            }

            req = get("http://"+self.ip+":5000/sales/addEditNewSalesDetails" , params = params).json()
            self.sale_id = req['saleId']

    def clear_all_tree(self):
        for each in self.tree_sales.get_children():
            self.tree_sales.delete(each)

    """--------------------------------------------------------------------------------------------------"""

    """--------------------------------------sales form functions----------------------------------------"""

    def new(self , e):
        self.btn_edit.config(state = con.DISABLED)
        self.btn_new.config(state = con.DISABLED)
        self.btn_save.config(state = con.NORMAL)
        self.btn_cancel.config(state = con.NORMAL)


        self.enable_all_details()
        self.clear_all_details()
        self.clear_all_tree()
        self.enable_vch_details()
        self.clear_vch_details()
        self.disable_vch_details()
        self.ent_pdf_bill_no.delete(0 , con.END)
        self.enable_print_details()
        self.clear_print_details()
        self.disable_print_details()
        self.combo_cust_vch.delete(0, con.END)
        self.combo_cust_vch.config(state = con.DISABLED)
        self.btn_vch.config(state = con.DISABLED)
        self.btn_vch_bill.config(state = con.DISABLED)
        self.btn_save_vch.config(state = con.DISABLED)

        self.ent_pdf_bill_no.config(state  = con.NORMAL)
        self.ent_pdf_bill_no.delete(0 , con.END)
        self.ent_pdf_bill_no.config(state  = con.DISABLED)


        self.new_state = True
        self.edit_state = False
        self.after_save = False

        self.t1 = 0
        self.t2 = 0
        self.control = False
        self.cust_id = -1
        

        self.sale_id = ""
        self.added_products = {}
        self.sl_no = 0

        self.selected_sl_no = 0
        self.prod_id = -1
        self.prod_gst = -1
        self.prod_cess = -1
        self.prod_units = []
        self.prod_sp = []
        self.prod_cp = 0
        self.stk_id = ""
        self.max_qty = 0
        
        self.firm_tot = []
        self.billInfo = {}
        self.voucher = {}
        self.displayed_pdf = ""
        self.rendered_page_count = 0
        self.change_page_count = False

       
        self.ent_bill_no.config(state = con.DISABLED)
        
        self.disable_prod()
        self.disable_prod_details()
        self.ent_bill_date.insert(0, datetime.date.today().strftime("%d") + "-" +datetime.date.today().strftime("%m") + "-" + datetime.date.today().strftime("%Y"))
        self.lbl_total_amt.config(text = '0.00')
        self.lbl_total_hsn.config(text = '0.00')
        #self.lbl_grd_tot.config(text = '0.00')
        self.ent_cust_name.focus_set()

    def edit(self,e):
        self.edit_state = True
        self.ent_bill_no.config(state= con.NORMAL)
        self.ent_bill_no.focus_set()
        self.btn_vch.config(state = con.DISABLED)
        self.btn_vch_bill.config(state = con.DISABLED)
        self.btn_save_vch.config(state = con.DISABLED)

        self.ent_pdf_bill_no.config(state  = con.NORMAL)
        self.ent_pdf_bill_no.delete(0 , con.END)
        self.ent_pdf_bill_no.config(state  = con.DISABLED)

    def save(self , e):

        if self.prod_id != -1:
            msg.showwarning("Warning" , "A Product is selected")
            return

        child = self.tree_sales.get_children()

        if len(child) == 0:
            msg.showinfo("Info" , "Enter Products")
            self.ent_bill_date.focus_set()
            return

        bill_date = self.ent_bill_date.get()
        
        if bill_date == "":
            msg.showinfo("Info" , "Enter Bill date ")
            self.ent_bill_date.focus_set()
            return



        req = get("http://"+self.ip+":5000/sales/save" , params = {'sale_id' : self.sale_id , 'year' : self.year , 'cust_id': self.cust_id, 'sale_date' : bill_date , 'user_name': self.user , 'form_id'   : self.form_id })
        if (req.status_code == 201):
            msg.showinfo('Try Again',"Some other is being saved please wait!")
            return

        #320 means some products are not available
        elif (req.status_code == 320):
            non_avail = req.json()
            child = self.tree_sales.get_children()
            non_avail_child = []

            for each in child:
                values = self.tree_sales.item(each)['values']
                stk_id = values[12]
                prod_id = str(values[13]) 
                 
                if stk_id == '':
                    stk_id = 'stkId'
                else:
                    stk_id =  str(values[12])[0:2]+"_"+str(values[12])[2:]
                
                if prod_id in non_avail:
                    if stk_id in non_avail[prod_id]:
                        values.append(non_avail[prod_id][stk_id][11])
                        if stk_id == 'stkId':
                            stk_id = ''

                        values[12] = stk_id
                        
                        non_avail_child.append(each)
                        self.tree_sales.detach(each)
                        self.tree_sales.insert('','end',tags=('nonAvail'), values = values)

            for each in child:
                if each not in non_avail_child:
                    values = self.tree_sales.item(each)['values']
                    self.tree_sales.detach(each)
                    self.tree_sales.insert('','end',tags=('avail'), values = values)

        elif(req.status_code == 200):
            for each in self.tree_sales.get_children():
                values =  self.tree_sales.item(each)['values']
                tags =  self.tree_sales.item(each)['tags'][0]
                stk_id = values[12]
                if stk_id == '':
                    stk_id = 'stkId'
                else:
                    stk_id = str(values[12])[0:2]+"_"+str(values[12])[2:]

                values[12] = stk_id
                if tags == 'edit': new = False
                else: new = True
                get("http://"+self.ip+":5000/sales/removeSalesProduct" , params = {"product" : values , 'sale_id' : self.sale_id , 'newBill' : new , 'db_year' : self.year , 'form_id'   : self.form_id} )


            get("http://"+self.ip+":5000/sales/cancelSales" , params = {"sale_id" : self.sale_id , 'form_id'   : self.form_id})
            self.btn_edit.config(state = con.DISABLED)
            self.btn_new.config(state = con.DISABLED)
            self.btn_save.config(state = con.DISABLED)
            self.btn_cancel.config(state = con.DISABLED)

            

            self.disable_all_details()

            self.enable_prod_details()
            self.clear_prod_details()
            self.disable_prod_details()

            self.enable_prod()
            self.disable_prod()

            self.forget_cust_list(None)
            self.forget_stk_sug(None)
            self.forget_prod_list(None)

            self.clear_all_tree()
            json_req = req.json()
            saved_products = json_req['salesSaveData']
            saved_bill_no = json_req['BillNumber']
            
            i = 0
            hsn = 0
            total = 0
            invoiceData = {}
            self.firm_tot = []

            for each in saved_products:
                if saved_products[each]['sales_prod_id'] == ":":
                    self.firm_tot.append(saved_products[each]['firm_total'])
                    continue 
                
                if each not in ['1' , '2' , '3']:
                    return

                
                prod_id = saved_products[each]['sales_prod_id'].split(":")[1:-1]
                pur_id = saved_products[each]['sales_pur_id'].split(":")[1:-1]
                prod_qty = saved_products[each]['sales_prod_qty'].split(":")[1:-1]
                prod_sp = saved_products[each]['sales_prod_sp'].split(":")[1:-1]
                prod_cp = saved_products[each]['cost_price'].split(":")[1:-1]
                prod_gst = saved_products[each]['gst_value'].split(":")[1:-1]
                prod_cess = saved_products[each]['cess_value'].split(":")[1:-1]
                prod_name = saved_products[each]['prod_name'].split(":")[1:-1]
                self.firm_tot.append(saved_products[each]['firm_total'])

                

                j = 0
                for pid in prod_id:
                    i+=1
                    mrp = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select prod_mrp,prod_name_kan from somanath.products where prod_id = " + pid }).json()
                    values = (i , prod_name[j] , "{:.3f}".format(round(float(prod_qty[j]) , 3))  , "{:.3f}".format(round(float(prod_sp[j]) , 3)) , "{:.3f}".format(round(float(prod_sp[j]) , 3) * round(float(prod_qty[j]) , 3)) ,  "{:.3f}".format((round(float(prod_sp[j]),3) - round(float(prod_cp[j]),3) )* round(float(prod_qty[j]) , 3)) , mrp[0]['prod_mrp'] ,prod_gst[j] , prod_cess[j] , pur_id[j], each , prod_id[j] )
                    hsn += float(values[5])
                    total += float(values[4])
                    
                    if int(each)%3 == 1:
                        tag = 'SSM'
                    elif int(each)%3 == 2:
                        tag = 'SCM'
                    else:
                        tag = 'SEM'
                    if prod_name[j] in invoiceData:
                        x = invoiceData[prod_name[j]]
                        tot = float(values[4]) + x[3]
                        qty = x[2] + float(prod_qty[j])
                        sp = round(tot / qty,3)
                        invoiceData[prod_name[j]] = [x[0],sp,qty,tot,x[4]]
                    else:
                        MRP = float(mrp[0]['prod_mrp'])
                        if ( MRP <= float(prod_sp[j]) ):
                            MRP = 0
                        invoiceData[prod_name[j]] = [ MRP , float(prod_sp[j]) , float(prod_qty[j]) , float(values[4]),mrp[0]['prod_name_kan'] ]

                    j +=1
                    self.tree_sales.insert('','end',tags=(tag), values = values)

            self.ent_cust_name.config(state = con.NORMAL)
            self.billInfo = json.dumps(invoiceData)
            oldBal = False
            self.voucher =json.dumps({})
            
            self.lbl_total_amt.config( text = "{:.2f}".format( round( float(total), 2) ))
            self.lbl_total_hsn.config( text = "{:.2f}".format( round( float(hsn), 2) ))
            grand_total =  "{:.2f}".format(float(self.lbl_total_amt.cget("text")))
            #self.lbl_grd_tot.config(text = grand_total )
            self.ent_bill_no.config(state = con.NORMAL)
            self.ent_bill_no.delete(0 , con.END)
            self.ent_bill_no.insert(0 , saved_bill_no)
            self.ent_bill_no.config(state = con.DISABLED)


            f = open("C:\\Program Files\\Hosangadi2.0\\invoiceData.txt", "w")
            f.write(self.billInfo)
            f.close()
            invoiceDataFile = {'upload_file': ("C:\\Program Files\\Hosangadi2.0\\invoiceData.txt", open('C:\\Program Files\\Hosangadi2.0\\invoiceData.txt','r'), 'text')}
            pdf = post("http://"+self.ip+":7000/sales/invoice" ,files = invoiceDataFile ,  params = {'billNo' : saved_bill_no, 'Date' : bill_date, 'customerName': self.ent_cust_name.get().title() ,'billTotal': grand_total, 'oldBal' : oldBal, 'oldBalData':self.voucher,'page':self.rad_printer.get()})
            self.for_page_change = {'billNo' : saved_bill_no, 'Date' : bill_date, 'customerName': self.ent_cust_name.get().title() ,'billTotal': grand_total, 'oldBal' : oldBal, 'oldBalData':self.voucher}
            self.displayed_pdf = self.location+"\\Desktop\\Invoices\\invoice.pdf"
            open(self.displayed_pdf,"wb").write(pdf.content)  
            self.pdf.display_file(self.displayed_pdf)
            self.change_page_count = True
            self.rad_even_odd.set(-1)


            #enable bill_print right frame
            self.enable_vch_details()
            bank = 0
            cash = 0
            if self.edit_state:
                bank = round(float(self.ent_bank_paid.get()),2)
                cash = round(float(self.ent_cash_paid.get()),2)
            self.clear_vch_details()
            self.combo_cust_vch.insert(0,self.ent_cust_name.get())
            self.lbl_old_bal.config(text = self.lbl_cust_bal.cget('text'))
            self.lbl_bill_amt.config(text = grand_total)
            if not self.edit_state:
                self.ent_bank_paid.insert(0,bank)
                self.ent_cash_paid.insert(0,cash)
            else:
                self.ent_bank_paid.insert(0,bank)
                self.ent_cash_paid.insert(0,cash)
            self.lbl_tot_paid.config(text = "{:.2f}".format(round(bank + cash,2)) )    
            self.lbl_fin_bal.config(text =  "{:.2f}".format(round(float(grand_total) + float(self.lbl_cust_bal.cget('text')) - bank - cash,2)) )
            
            self.ent_pdf_bill_no.config(state = con.NORMAL)
            self.ent_pdf_bill_no.delete(0 , con.END)
            self.ent_pdf_bill_no.insert(0 , saved_bill_no)
            self.ent_pdf_bill_no.config(state = con.DISABLED)
            self.ent_cust_name.config(state = con.DISABLED)



            

            self.combo_cust_vch.config(state = con.DISABLED)
            self.btn_save_vch.config(state= con.NORMAL)
            self.frm_pdf_2.lift()
            self.rad_select_window.set(1)

            self.t1 = 0
            self.t2 = 0
            self.control = False


            self.new_state = False
            self.after_save = True
            self.cust_id = -1
            

            self.sale_id = ""
            self.added_products = {}
            self.sl_no = 0

            self.selected_sl_no = 0
            self.prod_id = -1
            self.prod_gst = -1
            self.prod_cess = -1
            self.prod_units = []
            self.prod_sp = []
            self.prod_cp = 0
            self.stk_id = ""
            self.max_qty = 0

    def cancel(self , e):
        """if self.edit_state:
            if self.ent_bill_no.get() == '':
                self.ent_bill_no.config(state= con.DISABLED)
                self.btn_new.config(state= con.NORMAL)
                return
            else:
                msg.showinfo("Info" , "ಎಡಿಟ್ ಮಾಡಿದ ಬಿಲ್ ಮೊದಲು SAVE ಮಾಡ್ಕೊಳ್ಳಿ")
                return"""

        ans = msg.askokcancel("Info" , "Do you want to cancel?\n All the products added will be lost!!")
        if not ans:
            self.ent_prod.focus_set()
            return


        for each in self.tree_sales.get_children():
            values =  self.tree_sales.item(each)['values']
            stk_id = values[12]
            if stk_id == '':
                stk_id = 'stkId'
            else:
                stk_id = str(values[12])[0:2]+"_"+str(values[12])[2:]

            values[12] = stk_id
            get("http://"+self.ip+":5000/sales/removeSalesProduct" , params = {"product" : values , 'sale_id' : self.sale_id ,  'newBill' : 'True' , 'db_year' : self.year , 'form_id'   : self.form_id} )



        get("http://"+self.ip+":5000/sales/cancelSales" , params = {"sale_id" : self.sale_id , 'form_id'   : self.form_id})

        self.btn_edit.config(state = con.NORMAL)
        self.btn_new.config(state = con.NORMAL)
        self.btn_save.config(state = con.DISABLED)
        self.btn_cancel.config(state = con.DISABLED)

        self.acc_title.config(text = "Sales Entry")


        self.t1 = 0
        self.t2 = 0
        self.control = False
        self.cust_id = -1


        self.sale_id = ""
        self.added_products = {}
        self.sl_no = 0

        self.selected_sl_no = 0
        self.prod_id = -1
        self.prod_gst = -1
        self.prod_cess = -1
        self.prod_units = []
        self.prod_sp = []
        self.prod_cp = 0
        self.stk_id = ""
        self.max_qty = 0

        self.firm_tot = []
        self.billInfo = {}
        self.voucher = {}
        self.displayed_pdf = ""
        self.rendered_page_count = 0
        self.change_page_count = False

        self.new_state = False
        self.edit_state = False
        self.after_save = False




        self.enable_all_details()
        self.clear_all_details()
        self.disable_all_details()

        self.enable_prod_details()
        self.clear_prod_details()
        self.disable_prod_details()

        self.enable_prod()
        self.disable_prod()

        self.forget_cust_list(None)
        self.forget_stk_sug(None)
        self.forget_prod_list(None)
        self.clear_all_tree()

        self.clear_vch_details()
        self.ent_pdf_bill_no.config(state  = con.NORMAL)
        self.combo_cust_vch.config(state = con.NORMAL)
        self.clear_cust_details(None)

    def select_page(self):
        f = open("C:\\Program Files\\Hosangadi2.0\\invoiceData.txt", "w")
        f.write(self.billInfo)
        f.close()
        invoiceDataFile = {'upload_file': ("C:\\Program Files\\Hosangadi2.0\\invoiceData.txt", open('C:\\Program Files\\Hosangadi2.0\\invoiceData.txt','r'), 'text')}
        pdf = post("http://"+self.ip+":7000/sales/invoice" , files = invoiceDataFile , params = {'billNo' :self.for_page_change['billNo'], 'Date' : self.for_page_change['Date'],'customerName': self.for_page_change['customerName'] , 'billTotal': self.for_page_change['billTotal'] , 'oldBal' : self.for_page_change['oldBal'] , 'oldBalData':self.for_page_change['oldBalData'],'page': self.rad_printer.get()})
        self.displayed_pdf = self.location+"\\Desktop\\Invoices\\invoice.pdf"
        open(self.displayed_pdf,"wb").write(pdf.content)  
        self.pdf.display_file(self.displayed_pdf)
        self.change_page_count = True
        #self.rad_even_odd.set(-1)


    def select_window(self , e):
        selected = self.rad_select_window.get()

        if selected == 0:
            self.frm_cust_2.lift()
        elif selected == 1:
            self.frm_pdf_2.lift()
        elif selected == 2:
            self.frm_sales_rep_2.lift()
        else:
            self.frm_cashflow_2.lift()

    def minimize(self, e):
        self.forget_prod_list(None)
        self.forget_stk_sug(None)
        self.forget_cust_list(None)
        base_window.minimize(self,e)

    def close(self , e):
        if self.after_save:
            msg.showinfo("Info" , " ಮೊದಲು ವೌಚರ್ SAVE ಮಾಡ್ಕೊಳ್ಳಿ")
            self.pack_top(None)
            return

        if self.new_state or self.edit_state:
            msg.showinfo("Info" , " ಮೊದಲು ಬಿಲ್ SAVE ಇಲ್ಲ CANCEL ಮಾಡ್ಕೊಳ್ಳಿ")
            self.pack_top(None)
            return
        self.frm_stk_sug.destroy()
        self.frm_prod_name.destroy()
        self.frm_cust_name.destroy()
        base_window.close(self,e)


    """--------------------------------------------------------------------------------------------------"""

    """--------------------------------------voucher bill functions----------------------------------------"""

    def retrict_vch_entry(self , e):
        self.ent_cash_paid.delete(0 , con.END)
        self.ent_bank_paid.delete(0 , con.END)
        self.lbl_tot_paid.config(text = "")
        self.lbl_old_bal.config(text = "")
        self.lbl_bill_amt.config(text = "")
        self.lbl_fin_bal.config(text = "")
        self.ent_cash_paid.config(state = con.DISABLED)
        self.ent_bank_paid.config(state = con.DISABLED)
        self.ent_pdf_bill_no.delete(0 , con.END)
        self.ent_page_range.delete(0 , con.END)
        self.rad_even_odd.set(0)
        self.rad_printer.set(0)
        self.ent_page_range.config(state = con.DISABLED)
        self.rad_odd_only.config(state = con.DISABLED)
        self.rad_even_only.config(state = con.DISABLED)
        self.rad_printer_1.config(state = con.DISABLED)
        self.rad_printer_2.config(state = con.DISABLED)
        self.chk_gst_bill.config(state = con.DISABLED)

        self.btn_print_bill.config(state = con.DISABLED)
        self.btn_bill_only.config(state = con.DISABLED)

        self.btn_save_vch.config(state = con.DISABLED)
        self.clear_print_details()
        self.disable_print_details()
        
        if self.combo_cust_vch.get() == "":
            self.ent_pdf_bill_no.config(state = con.NORMAL)

    def enable_vch_details(self):
        self.combo_cust_vch.config(state = con.NORMAL)
        self.ent_cash_paid.config(state = con.NORMAL)
        self.ent_bank_paid.config(state = con.NORMAL)

    def clear_vch_details(self):
        self.combo_cust_vch.delete(0 , con.END)
        self.ent_cash_paid.delete(0 , con.END)
        self.ent_bank_paid.delete(0 , con.END)
        self.lbl_tot_paid.config(text = "")
        self.lbl_old_bal.config(text = "")
        self.lbl_bill_amt.config(text = "")
        self.lbl_fin_bal.config(text = "")

    def disable_vch_details(self):
        #self.combo_cust_vch.config(state = con.DISABLED)
        self.ent_cash_paid.config(state = con.DISABLED)
        self.ent_bank_paid.config(state = con.DISABLED)
        self.ent_pdf_bill_no.config(state = con.DISABLED)

    def enable_print_details(self):
        #self.ent_pdf_bill_no.config(state = con.NORMAL)
        self.ent_page_range.config(state = con.NORMAL)
        self.rad_odd_only.config(state = con.NORMAL)
        self.rad_even_only.config(state = con.NORMAL)
        self.rad_printer_1.config(state = con.NORMAL)
        #self.rad_printer_2.config(state = con.NORMAL)
        self.chk_gst_bill.config(state = con.NORMAL)

        self.btn_print_bill.config(state = con.NORMAL)
        self.btn_bill_only.config(state = con.NORMAL)

    def clear_print_details(self):
        self.ent_pdf_bill_no.delete(0 , con.END)
        self.ent_page_range.delete(0 , con.END)
        self.rad_even_odd.set(0)
        self.rad_printer.set(0)
        self.pdf.erase()

    def disable_print_details(self):
        #self.ent_pdf_bill_no.config(state = con.DISABLED)
        self.ent_page_range.config(state = con.DISABLED)
        self.rad_odd_only.config(state = con.DISABLED)
        self.rad_even_only.config(state = con.DISABLED)
        self.rad_printer_1.config(state = con.DISABLED)
        self.rad_printer_2.config(state = con.DISABLED)
        self.btn_print_bill.config(state = con.DISABLED)
        self.btn_bill_only.config(state = con.DISABLED)
        self.chk_gst_bill.config(state = con.DISABLED)

    def get_customers(self,e):
        text = e.widget.get()
        
        if text == "":
            sql = "select acc_name from somanath.accounts where acc_type = 'CUST' order by acc_name"
        else:
            sql = "select acc_name from somanath.accounts where acc_type = 'CUST' and acc_name regexp '"+text+"' order by acc_name"

        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            resp = req.json()
            values = []
            for each in resp:
                values.append(each['acc_name'])

            e.widget.config(values = values)

    def get_customer_vch_details(self , e):
        name = self.combo_cust_vch.get()
        if name == "":
            return

        self.ent_cash_paid.focus_set()
        sql = "select accounts.acc_id, acc_cus_type,  acc_cls_bal_firm1 + acc_cls_bal_firm2 + acc_cls_bal_firm3 as acc_cls_bal  ,  acc_mob1, acc_mob2, acc_add from somanath.accounts , somanath20"+ self.year +".acc_bal where acc_name ='"+ name + "' and accounts.acc_id = acc_bal.acc_id "
        cust = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql }).json()
        if cust == []:
            return
        cust = cust[0]
        self.enable_vch_details()
        self.clear_vch_details()
        self.lbl_old_bal.config(text = "{:.2f}".format(round(float(cust['acc_cls_bal']),2)))
        self.combo_cust_vch.insert(0 , name)
        self.ent_bank_paid.insert(0,"0.00")
        self.ent_cash_paid.insert(0,"0.00")
        self.ent_cash_paid.select_range( 0 ,con.END)
        self.ent_cash_paid.focus_set()
        self.lbl_tot_paid.config(text = "0.00")
        self.lbl_bill_amt.config(text =  "0.00")
        self.lbl_fin_bal.config(text = "{:.2f}".format(round(float(cust['acc_cls_bal']),2)) )
        self.ent_pdf_bill_no.config(state = con.NORMAL)
        self.ent_pdf_bill_no.delete(0 , con.END)
        self.ent_pdf_bill_no.config(state = con.DISABLED)
        self.btn_save_vch.config(state = con.NORMAL)
        self.clear_print_details()
        self.disable_print_details()

    def print_both(self , e):
        self.enable_print_details()
        self.clear_print_details()
        f = open("C:\\Program Files\\Hosangadi2.0\\invoiceData.txt", "w")
        f.write(self.billInfo)
        f.close()
        invoiceDataFile = {'upload_file': ("C:\\Program Files\\Hosangadi2.0\\invoiceData.txt", open('C:\\Program Files\\Hosangadi2.0\\invoiceData.txt','r'), 'text')}
        pdf = post("http://"+self.ip+":7000/sales/invoice",files = invoiceDataFile , params = {'billNo' : self.ent_bill_no.get(), 'Date' : self.ent_bill_date.get(), 'customerName': self.ent_cust_name.get().title() , 'billTotal': self.voucher['bill_amt'] , 'oldBal' : True , 'oldBalData':json.dumps(self.voucher),'page':self.rad_printer.get()})
        self.for_page_change = {'billNo' : self.ent_bill_no.get(), 'Date' : self.ent_bill_date.get(), 'customerName': self.ent_cust_name.get().title() , 'billTotal': self.voucher['bill_amt'] , 'oldBal' : True , 'oldBalData':json.dumps(self.voucher)}
        self.displayed_pdf = self.location+"\\Desktop\\Invoices\\invoice.pdf"
        open(self.displayed_pdf,"wb").write(pdf.content)  
        self.pdf.display_file(self.displayed_pdf)
        self.change_page_count = True
        self.rad_even_odd.set(-1)

    def print_only_vch(self , e):
        self.enable_print_details()
        self.clear_print_details()
        pdf = get("http://"+self.ip+":7000/sales/voucherPrint" , params = {'Date' : str(datetime.datetime.today().strftime('%d-%m-%Y')), 'customerName': self.combo_cust_vch.get().title() , 'oldBalData':json.dumps(self.voucher)} , allow_redirects = True)
        self.displayed_pdf = self.location+"\\Desktop\\Invoices\\voucher.pdf"
        open(self.displayed_pdf ,"wb").write(pdf.content)
        self.pdf.display_file(self.displayed_pdf)
        self.change_page_count = False
        self.rad_even_odd.set(-1)

    def print_only_bill(self , e):
        self.enable_print_details()
        self.clear_print_details()
        if len(self.ent_bill_date.get()) == 0:
            date = self.voucher['bill_date']
            cust = self.voucher['cust_name']
            bill_no = self.voucher['bill_no']
        else:
            date = self.ent_bill_date.get()
            cust = self.ent_cust_name.get().title()
            bill_no = self.ent_bill_no.get()

        f = open("C:\\Program Files\\Hosangadi2.0\\invoiceData.txt", "w")
        f.write(self.billInfo)
        f.close()


        invoiceDataFile = {'upload_file': ("C:\\Program Files\\Hosangadi2.0\\invoiceData.txt", open('C:\\Program Files\\Hosangadi2.0\\invoiceData.txt','r'), 'text')}
        pdf = post("http://"+self.ip+":7000/sales/invoice" , files = invoiceDataFile, params = {'billNo' : bill_no, 'Date' : date, 'customerName':  cust , 'billTotal': self.voucher['bill_amt'] , 'oldBal' : False , 'oldBalData':json.dumps(self.voucher),'page':self.rad_printer.get()})
        self.for_page_change = {'billNo' : bill_no, 'Date' : date, 'customerName': cust , 'billTotal': self.voucher['bill_amt'] , 'oldBal' : False , 'oldBalData':json.dumps(self.voucher)}
        self.displayed_pdf = self.location+"\\Desktop\\Invoices\\invoice.pdf"
        open(self.displayed_pdf,"wb").write(pdf.content)  
        self.pdf.display_file(self.displayed_pdf)
        self.change_page_count = True
        self.rad_even_odd.set(-1)

    def print(self , e):
        #After Print function
        #Reset sales Bill


        if not self.pdf.rendered_page_count:
            msg.showinfo("Info" , "Enter correct Page Number")
            return

        range = self.ent_page_range.get()
        files = {'file': open(self.displayed_pdf, 'rb')}

        post("http://"+self.ip+":7000/PrintInvoice" , params = {'range' : range , 'even_odd' : self.rad_even_odd.get() , 'total_pages' : self.rendered_page_count} , files = files)


        self.btn_edit.config(state = con.NORMAL)
        self.btn_new.config(state = con.NORMAL)
        self.btn_save.config(state = con.DISABLED)
        self.btn_cancel.config(state = con.DISABLED)

        self.acc_title.config(text = "Sales Entry")


        self.t1 = 0
        self.t2 = 0
        self.control = False

        self.new_state = False
        self.edit_state = False
        self.after_save = False
        self.cust_id = -1
        

        self.sale_id = ""
        self.added_products = {}
        self.sl_no = 0

        self.selected_sl_no = 0
        self.prod_id = -1
        self.prod_gst = -1
        self.prod_cess = -1
        self.prod_units = []
        self.prod_sp = []
        self.prod_cp = 0
        self.stk_id = ""
        self.max_qty = 0

        self.firm_tot = []
        self.billInfo = {}
        self.voucher = {}
        """self.for_page_change = {}
        self.displayed_pdf = ""
        self.rendered_page_count = 0
        self.change_page_count = False
        #self.ent_pdf_bill_no.delete(0,con.END)
        #self.pdf.erase()"""


        self.enable_all_details()
        self.clear_all_details()
        self.disable_all_details()

        self.enable_prod_details()
        self.clear_prod_details()
        self.disable_prod_details()

        self.enable_prod()
        self.disable_prod()

        self.forget_cust_list(None)
        self.forget_stk_sug(None)
        self.forget_prod_list(None)
        self.clear_all_tree()

        self.enable_vch_details()
        self.clear_vch_details()
        self.disable_vch_details()
        #self.enable_print_details()
        #self.clear_print_details()
        #self.disable_print_details()
        self.clear_cust_details(None)
        self.btn_save_vch.config(state = con.DISABLED)
        self.btn_vch.config(state = con.DISABLED)
        self.btn_vch_bill.config(state = con.DISABLED)
        self.combo_cust_vch.config(state = con.DISABLED)
        self.combo_cust_vch.config(state = con.NORMAL)
        self.combo_cust_vch.delete(0,con.END)
        self.ent_pdf_bill_no.config(state = con.NORMAL)

    def save_vch(self ,e):
        billNo = self.ent_pdf_bill_no.get()
        cash = self.ent_cash_paid.get()   
        bank = self.ent_bank_paid.get()
        name = self.combo_cust_vch.get().upper()  
        date = self.ent_bill_date.get()   

        try:
            cash = float(cash)
        except ValueError:
            cash = 0

        try:
            bank = float(bank)
        except ValueError:
            bank = 0

        if billNo == "" and bank + cash == 0:
            msg.showinfo("Info" , " ENTER AMOUNT PAID ")
            self.ent_cash_paid.focus_set()
            self.ent_cash_paid.select_range(0 , con.END)
            return

        if billNo == "":
            params = { 
                        'dbYear':self.year,
                        'bank':bank,
                        'cash':cash,
                        'name':name,
                        'billNo':'',
                        'billDate': str(datetime.datetime.today().strftime('%d-%m-%Y')),
                        'firm1':'',
                        'firm2':'',
                        'firm3':'',
                        'user_name':self.user,
                        'editState' : ''
                    } 
        else:
            params = { 
                        'dbYear':self.year,
                        'bank':bank,
                        'cash':cash,
                        'name':name,
                        'billNo':billNo,
                        'billDate':date,
                        'firm1':self.firm_tot[0],
                        'firm2':self.firm_tot[1],
                        'firm3':self.firm_tot[2],
                        'user_name':self.user,
                        'form_id'   : self.form_id,
                        'editState' : self.edit_state
                    }

        voucher = get("http://"+self.ip+":5000/sales/voucher" , params = params).json()
        self.voucher = voucher
        if self.after_save:
            self.btn_vch_bill.config(state = con.NORMAL)
        self.btn_vch.config(state = con.NORMAL)
        self.btn_save_vch.config(state = con.DISABLED)
        
        
        self.ent_pdf_bill_no.delete(0 , con.END)
        self.ent_page_range.delete(0 , con.END)
        self.rad_even_odd.set(0)
        self.rad_printer.set(0)
        self.disable_vch_details()
        self.enable_print_details()
        
        self.ent_pdf_bill_no.config(state = con.NORMAL)

        self.edit_state = False
        self.new_state = False
        self.after_save = False
        self.btn_new.config(state = con.NORMAL)
        self.btn_edit.config(state = con.NORMAL)

    """--------------------------------------------------------------------------------------------------"""

    """--------------------------------------edit bill functions----------------------------------------"""
    def get_invoice_details(self,e):
        bill_no = self.ent_bill_no.get()
        
        
    

        if bill_no == '' or bill_no == '.':
            msg.showwarning("ಬಿಲ್ ನಂಬರ್","ಎಡಿಟ್ ಮಾಡುಕ್ ಇದ್ದ್ ಬಿಲ್ ನಂಬರ್ ಹಾಕಿ \n ಎಡಿಟ್ ಮಾಡುಕ್ ಇಲ್ಲದಿರೆ CANCEL ಬಟನ್ ಒತ್ತಿ")
            return
        
        sql = "SELECT date_format(sale_date,'%d-%m-%Y') as sale_date,acc_name,somanath.accounts.acc_id,acc_cus_type,acc_mob1,acc_mob2,acc_add,acc_cls_bal_firm1,acc_cls_bal_firm2,acc_cls_bal_firm3, acc_cls_bal_firm1 + acc_cls_bal_firm2 + acc_cls_bal_firm3 as cust_bal FROM somanath20"+self.year+".sales,somanath20"+self.year+".acc_bal ,somanath.accounts where sales_id = '"+self.year+"_"+bill_no+"' and  somanath20"+self.year+".sales.sales_acc = somanath.accounts.acc_id and somanath20"+self.year+".sales.sales_acc = somanath20"+self.year+".acc_bal.acc_id limit 1;"
        
        cust = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql }).json()
        
        if len(cust) == 0:
            self.ent_bill_no.delete(0,con.END)
            self.ent_bill_no.focus_set()
            msg.showwarning("ಬಿಲ್ ನಂಬರ್","ಎಡಿಟ್ ಮಾಡುಕ್ ಇದ್ದ್ ಬಿಲ್ ನಂಬರ್ ಹಾಕಿ \n ಎಡಿಟ್ ಮಾಡುಕ್ ಇಲ್ಲದಿರೆ CANCEL ಬಟನ್ ಒತ್ತಿ")
            return
        
        ans = msg.askyesno("ಇದೆಯಾ" , "ಗಿರಾಕಿ : "+cust[0]['acc_name']+"\n ಬಿಲ್ ತಾರಿಕ್: "+cust[0]['sale_date']+"\n ಎಡಿಟ್ ಮಾಡುಕ್ ಹೊದ್ ಇದ್ ಅಲ್ಲದಿರೆ NO ವತ್ತಿ")
        if not ans:
            self.ent_bill_no.select_range(0,con.END)
            self.ent_bill_no.focus_set()
            self.btn_cancel.invoke()
            return
        
        self.sale_id = self.year+"_"+bill_no
      
        edit_data = get("http://"+self.ip+":5000/sales/edit" , params = {'billNo' : self.sale_id ,'dbYear':self.year , 'user' : self.user  , 'sale_date' : cust[0]['sale_date'] , 'cust_name' : cust[0]['acc_name'] , 'form_id'   : self.form_id})

        if edit_data.status_code == 201:
            msg.showerror("ERROR" , "ಈ BILL ಬೇರೆ ಕಡೆ EDIT ಮಾಡುತ್ತಿದ್ದಾರೆ")
            self.ent_bill_no.select_range(0,con.END)
            self.ent_bill_no.focus_set()
            return    

   
        self.btn_edit.config(state = con.DISABLED)
        edit_data = edit_data.json()

        self.btn_new.config(state= con.DISABLED)
        self.enable_all_details()
        self.ent_bill_no.config(state = con.DISABLED)
        self.ent_cust_name.delete(0,con.END)
        self.ent_cust_name.insert(0,cust[0]['acc_name'])
        self.ent_bill_date.delete(0,con.END)
        self.ent_bill_date.insert(0,cust[0]['sale_date'])


    
        self.lbl_total_amt.config( text = edit_data['total'])
        self.lbl_total_hsn.config( text = edit_data['total_hsn'])
        #self.lbl_grd_tot.config( text = "{:.2f}".format(float(edit_data['total'])) )
        child = self.tree_sales.get_children()
        for each in child:
            self.tree_sales.delete(each)
        
        self.added_products = {}
        self.prod_id = -1
        self.cust_id = cust[0]['acc_id']
        
        self.sl_no = int(edit_data['slNO'])
   
        self.selected_sl_no = 0
        self.prod_gst = -1
        self.prod_cess = -1
        self.prod_units = []
        self.prod_sp = []
        self.prod_cp = 0
        self.stk_id = ""
        self.max_qty = 0

        self.t1 = 0
        self.t2 = 0
        self.control = False


        


        self.new_state = False
        self.after_save = False
        

  

        
        self.firm_tot = []
        self.billInfo = {}
        self.voucher = {}
        self.displayed_pdf = ""
        self.rendered_page_count = 0
        self.change_page_count = False
        
        for each in edit_data['values']:
            self.tree_sales.insert('','end',tags=('edit'), values = tuple(each))
            if each[13] in self.added_products:
                self.added_products[each[13]][0].append(int(each[0]))
                self.added_products[each[13]][1].append(each[12])
            else:
                self.added_products[each[13]] = [int(each[0])] , [each[12]]   

        
        sql = "SELECT (amt_paid_firm1_cash+amt_paid_firm2_cash+amt_paid_firm3_cash) as amt_paid_cash , (amt_paid_firm1_bank+amt_paid_firm2_bank+amt_paid_firm3_bank) as amt_paid_bank,(trans_amt_firm1+trans_amt_firm2+trans_amt_firm3) - (amt_paid_firm1_cash+amt_paid_firm2_cash+amt_paid_firm3_cash+amt_paid_firm1_bank+amt_paid_firm2_bank+amt_paid_firm3_bank) as tot_bal, trans_amt_firm1 - (amt_paid_firm1_cash+amt_paid_firm1_bank) as tot_bal_firm1, trans_amt_firm2 - (amt_paid_firm2_cash+amt_paid_firm2_bank) as tot_bal_firm2, trans_amt_firm3 - (amt_paid_firm3_cash+amt_paid_firm3_bank) as tot_bal_firm3 FROM somanath20"+self.year+".cashflow_sales where trans_sales = '"+self.year+"_"+bill_no+"';"
        bal_diff = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql }).json()
        
        sql = "UPDATE somanath20"+self.year+".acc_bal SET acc_cls_bal_firm1 ="+"{:.2f}".format(round(float( cust[0]['acc_cls_bal_firm1']) - float(bal_diff[0]['tot_bal_firm1']),2 )) +", acc_cls_bal_firm2 ="+"{:.2f}".format(round(float( cust[0]['acc_cls_bal_firm2']) - float(bal_diff[0]['tot_bal_firm2']),2 )) +", acc_cls_bal_firm3 ="+"{:.2f}".format(round(float( cust[0]['acc_cls_bal_firm3']) - float(bal_diff[0]['tot_bal_firm3']),2 )) +" where acc_id ="+ str(cust[0]['acc_id'])+";"
        get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql })
        
        self.ent_prod.config(state = con.NORMAL)
        self.lbl_cust_type.config(text = cust[0]['acc_cus_type'])
        self.lbl_cust_mob1.config(text = cust[0]['acc_mob1'])
        self.lbl_cust_mob2.config(text = cust[0]['acc_mob2'])
        self.lbl_cust_addr.config(state = con.NORMAL)
        self.lbl_cust_addr.delete(0.0 , con.END)
        self.lbl_cust_addr.insert(0.0 , cust[0]['acc_add'])
        self.lbl_cust_addr.config(state = con.DISABLED)
        self.acc_title.config(text = cust[0]['acc_name'])

        self.lbl_cust_bal.config(text= "{:.2f}".format( float(cust[0]['cust_bal']) - float(bal_diff[0]['tot_bal']) ) )
        self.frm_cust_2.lift() 
        self.rad_select_window.set(0)
        self.enable_vch_details()
        self.ent_bank_paid.delete(0 , con.END)
        self.ent_bank_paid.insert(0 , bal_diff[0]['amt_paid_bank'])
        self.ent_cash_paid.delete(0 , con.END)
        self.ent_cash_paid.insert(0 , bal_diff[0]['amt_paid_cash'])
        self.lbl_tot_paid.config(text = "{:.2f}".format( float( bal_diff[0]['amt_paid_cash']) + float(bal_diff[0]['amt_paid_bank']) ) )
        self.lbl_old_bal.config(text = "{:.2f}".format(float(cust[0]['cust_bal']) - float(bal_diff[0]['tot_bal'])) )
        self.lbl_bill_amt.config(text = "{:.2f}".format(float(edit_data['total'])) )
        self.lbl_fin_bal.config(text = "{:.2f}".format(float(cust[0]['cust_bal']) - float(bal_diff[0]['tot_bal']) + float(edit_data['total']) - float(bal_diff[0]['amt_paid_bank']) - float(bal_diff[0]['amt_paid_cash'])) )
        self.combo_cust_vch.delete(0,con.END)
        self.combo_cust_vch.insert(0,cust[0]['acc_name'])
        self.combo_cust_vch.config(state= con.DISABLED)
        self.btn_save_vch.config(state = con.DISABLED)
        self.disable_vch_details()
        self.disable_print_details()
        self.btn_save.config( state = con.NORMAL)
    """----------------------------------------print bill functions-------------------------------------------"""
    def bill_pdf_only(self,e):
        x = self.ent_pdf_bill_no.get().split(' ')
        bill_number = self.year+"_"+ self.ent_pdf_bill_no.get()
        db_year = self.year
        if len(x)>1:
            bill_number = x[0]+'_'+x[1]
            db_year = x[0]
        
        sql = "SELECT  sales_ref,acc_name , sales_prod_id , sales_prod_qty , sales_prod_sp , date_format(sale_date,'%d-%m-%Y') as Date  , discount, acc_cls_bal_firm1 + acc_cls_bal_firm2 + acc_cls_bal_firm3 as remaining_bal,trans_amt_firm1+trans_amt_firm2+trans_amt_firm3 as bill_amt,amt_paid_firm1_cash+amt_paid_firm2_cash+amt_paid_firm3_cash+amt_paid_firm1_bank+amt_paid_firm2_bank+amt_paid_firm3_bank as amountPaid"
        sql += " FROM somanath20"+db_year+".sales, somanath.accounts, somanath20"+db_year+".acc_bal, somanath20"+db_year+".cashflow_sales where somanath20"+db_year+".sales.sales_id = '"+str(bill_number)+"'" 
        sql += " and somanath20"+db_year+".sales.sales_acc = somanath.accounts.acc_id  and somanath20"+db_year+".acc_bal.acc_id = somanath20"+db_year+".sales.sales_acc and somanath20"+db_year+".cashflow_sales.trans_sales = somanath20"+db_year+".sales.sales_id order by  sales_ref;"
      
        bill_data = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql }).json()
        self.enable_vch_details()
        self.clear_vch_details()
        self.disable_vch_details()

        if bill_data == []:
            msg.showinfo("INFO" , "ಈ ಬಿಲ್ ಇಲ್ಲ")
            self.ent_pdf_bill_no.config( state = con.NORMAL)
            self.ent_pdf_bill_no.focus_set()
            self.ent_pdf_bill_no.select_range( 0 , con.END)
            return 

        self.enable_print_details()
        self.clear_print_details()
        self.ent_pdf_bill_no.config( state = con.NORMAL)
        
        

        prod_qty = []
        prod_sp = []
        name_mrp = {}
        firm = []
        j = 0
        for each in bill_data:
            prodQty = each['sales_prod_qty'].split(':')[1:-1]
            prodSp = each['sales_prod_sp'].split(':')[1:-1]
            firm.append([each['sales_ref'],len(prodSp)])
            i = 0
            for prodId in each['sales_prod_id'].split(':')[1:-1]:
                prod_qty.append(prodQty[i])
                prod_sp.append(prodSp[i])
                name_mrp[j] = get("http://"+self.ip+":7000/onlySql" , params = {'sql' : "SELECT prod_name,prod_mrp,prod_name_kan,tax_per FROM somanath.products,somanath.taxes where tax_id=prod_gst and prod_id ="+ prodId }).json()
                i+=1
                j+=1
        invoiceData = {}
        i = 0
        grandTotal = 0
        ssm_count = 0
        sem_count = 0
        scm_count = 0
        actual_invoice = [0,0,0]
        for each in firm:
            if each[0].split("_")[0] == "SSM":
                ssm_count = each[1]
                actual_invoice[0] = each[0]
            elif each[0].split("_")[0] == "SEM":
                sem_count = each[1]
                actual_invoice[2] = each[0]
            else:
                scm_count = each[1]
                actual_invoice[1] = each[0]
        for each in name_mrp:
            firm_id = actual_invoice[0]
            if scm_count>0:
                firm_id = actual_invoice[1]
            elif sem_count > 0:
                firm_id = actual_invoice[2]
            if name_mrp[each][0]['prod_name'] in invoiceData:
                x = invoiceData[name_mrp[each][0]['prod_name']]
                tot = float(prod_qty[i])*float(prod_sp[i]) + x[3]
                qty = x[2] + float(prod_qty[i])
                sp = round(tot / qty,2)
                grandTotal += tot
                invoiceData[name_mrp[each][0]['prod_name']] = [x[0],sp,qty,tot,x[4],x[5],x[6]]
            else:
                MRP = float(name_mrp[each][0]['prod_mrp'])
                if ( MRP <= float(prod_sp[i]) ):
                    MRP = 0
                tot = float(prod_qty[i])*float(prod_sp[i])
                grandTotal += tot
                invoiceData[name_mrp[each][0]['prod_name']] = [ MRP , float(prod_sp[i]) , float(prod_qty[i]) , tot, name_mrp[each][0]['prod_name_kan'], name_mrp[each][0]['tax_per'], firm_id]
            i += 1
            if firm_id == actual_invoice[0]:
                ssm_count -= 1
            elif firm_id == actual_invoice[1]:
                scm_count -= 1
            else:
                sem_count -= 1

        voucher = {
            'bill_amt' : grandTotal,
            'old_bal' : float(bill_data[0]['remaining_bal'])  - ( grandTotal - float(bill_data[0]['amountPaid']) ) ,
            'amountPaid': bill_data[0]['amountPaid'],
            'remaining_bal': bill_data[0]['remaining_bal'],
            'bill_date': bill_data[0]['Date'],
            'cust_name': bill_data[0]['acc_name'],
            'bill_no' : self.ent_pdf_bill_no.get()
        } 
        self.voucher =  voucher
        self.billInfo = json.dumps(invoiceData)
        f = open("C:\\Program Files\\Hosangadi2.0\\invoiceData.txt", "w")
        f.write(self.billInfo)
        f.close()
        invoiceDataFile = {'upload_file': ("C:\\Program Files\\Hosangadi2.0\\invoiceData.txt", open('C:\\Program Files\\Hosangadi2.0\\invoiceData.txt','r'), 'text')}
        pdf = post("http://"+self.ip+":7000/sales/invoice" , files = invoiceDataFile , params = {'billNo' : self.ent_pdf_bill_no.get(), 'Date' : bill_data[0]['Date'], 'customerName': bill_data[0]['acc_name'] , 'billTotal': grandTotal , 'oldBal' : True , 'oldBalData':json.dumps(voucher),'page': self.rad_printer.get(), 'gst': self.check_gst.get()})
        self.for_page_change = {'billNo' : self.ent_pdf_bill_no.get(), 'Date' : bill_data[0]['Date'], 'customerName': bill_data[0]['acc_name'] , 'billTotal': grandTotal , 'oldBal' : True , 'oldBalData':json.dumps(voucher)}
        self.displayed_pdf = self.location+"\\Desktop\\Invoices\\invoice.pdf"
        open(self.displayed_pdf,"wb").write(pdf.content)  
        self.pdf.display_file(self.displayed_pdf)
        self.change_page_count = True
        self.btn_vch.config(state = con.DISABLED)
        self.btn_vch_bill.config(state = con.DISABLED)
        self.rad_even_odd.set(-1)
         
    def show_even_pages(self):
        i = self.rendered_page_count
        even_page_string = ""
        
        for k in range(1,i+1):
            if k%2 == 0:
                even_page_string += str(k)+','
        
        self.pdf.display_file(self.displayed_pdf , pages = even_page_string[0:-1] )
        self.change_page_count = False
        self.ent_page_range.delete(0 , con.END)
 
    def show_odd_pages(self):
        i = self.rendered_page_count
        odd_page_string = ""
        
        for k in range(1,i+1):
            if k%2 == 1:
                odd_page_string += str(k)+','
        self.pdf.display_file(self.displayed_pdf , pages = odd_page_string[0:-1] )
        self.change_page_count = False
        self.ent_page_range.delete(0 , con.END)

    def show_page_range(self , e):
        range = self.ent_page_range.get()
        self.pdf.display_file(self.displayed_pdf , pages = range)
        self.change_page_count = False
        self.rad_even_odd.set(-1)

    def pdf_loaded(self , e):
        if self.change_page_count:
            self.rendered_page_count = self.pdf.rendered_page_count  

    """--------------------------------------------------------------------------------------------------"""

    """---------------------------------------- reports functions----------------------------------------"""
    def get_cashflow(self , e):
        
        child = self.tree_cashflow.get_children()
        for each in child:
            self.tree_cashflow.delete(each)

        cust_name = self.combo_cust_cashflow.get()
        limit = self.ent_limit_cashflow.get()
        
        if cust_name == "":
            msg.showerror("Error" , "Select Customer")
            self.combo_cust_cashflow.select_range(0,con.END)
            self.combo_cust_cashflow.focus_set()
            return

        if cust_name!= "":
            if cust_name not in self.combo_cust_cashflow['values']:
                msg.showerror("Error" , "Select Name from the list")
                self.combo_cust_cashflow.select_range(0,con.END)
                self.combo_cust_cashflow.focus_set()
                return

        from_date = self.ent_from_cashflow.get()
        to_date = self.ent_to_cashflow.get()


        if limit == "":
            date1 = from_date.split("/")
            if len(date1)!=3:
                date1 = from_date.split("-")
                if len(date1) != 3:
                    msg.showinfo("Info" , "Enter date in following format \n 'dd-mm-yy' or 'dd/mm/yy ")
                    self.ent_from_cashflow.delete(0,con.END)
                    self.ent_from_cashflow.focus_set()
                    return

            try:
                datetime.datetime(int(date1[2]), int(date1[1]), int(date1[0]))
            except ValueError:
                msg.showinfo("Info" , "Enter correct date")
                self.ent_from_cashflow.delete(0,con.END)
                self.ent_from_cashflow.focus_set()
                return

            
            if len(date1[2])%2 !=0 :
                msg.showinfo("Info" , "Enter correct date")
                self.ent_from_cashflow.delete(0,con.END)
                self.ent_from_cashflow.focus_set()
                return

            if len(date1[0]) == 1:
                date1[0] = '0' + date1[0]

            if len(date1[1]) == 1:
                date1[1] = '0' + date1[1]    

            if len(date1[2]) == 2:
                date1[2] = '20' + date1[2]    

            
            self.ent_from_cashflow.delete(0,con.END)
            self.ent_from_cashflow.insert(0,date1[0] + "-" + date1[1] + "-" + date1[2])        
            self.ent_from_cashflow.select_clear()
            from_date = date1[2] + "-" + date1[1] + "-" + date1[0]




        if to_date != "":
            date1 = to_date.split("/")
            if len(date1)!=3:
                date1 = to_date.split("-")
                if len(date1) != 3:
                    msg.showinfo("Info" , "Enter date in following format \n 'dd-mm-yy' or 'dd/mm/yy ")
                    self.ent_to_cashflow.delete(0,con.END)
                    self.ent_to_cashflow.focus_set()
                    return

            try:
                datetime.datetime(int(date1[2]), int(date1[1]), int(date1[0]))
            except ValueError:
                msg.showinfo("Info" , "Enter correct date")
                self.ent_to_cashflow.delete(0,con.END)
                self.ent_to_cashflow.focus_set()
                return

            
            if len(date1[2])%2 !=0 :
                msg.showinfo("Info" , "Enter correct date")
                self.ent_to_cashflow.delete(0,con.END)
                self.ent_to_cashflow.focus_set()
                return

            if len(date1[0]) == 1:
                date1[0] = '0' + date1[0]

            if len(date1[1]) == 1:
                date1[1] = '0' + date1[1]    

            if len(date1[2]) == 2:
                date1[2] = '20' + date1[2]    

            
            self.ent_to_cashflow.delete(0,con.END)
            self.ent_to_cashflow.insert(0,date1[0] + "-" + date1[1] + "-" + date1[2])        
            self.ent_to_cashflow.select_clear()

            to_date = date1[2] + "-" + date1[1] + "-" + date1[0]




        if limit != "":
            from_date = ''
            to_date = ''
        else:
            limit = 10000000
        req = get("http://"+self.ip+":6000/reports/getCashflowSales" , params = { "acc_name" : cust_name , "limit" : limit ,'sdate' : from_date ,'edate' :to_date,'db' : self.year  }) 


        data = req.json()
        if len(data) > 0:
            dByear = str(data.pop())



            acc_id = data.pop()
            data.reverse()
            max_date = data[0]['transdate']
            sql = "SELECT sum((trans_amt_firm1+trans_amt_firm2+trans_amt_firm3)-(amt_paid_firm1_cash+amt_paid_firm2_cash+amt_paid_firm3_cash+amt_paid_firm1_bank+amt_paid_firm2_bank+amt_paid_firm3_bank)) as diff FROM somanath20"+dByear+".cashflow_sales where trans_acc = "+ str(acc_id) +" and trans_date < '"+str(datetime.datetime.strptime(data[0]['transdate'], '%d-%b-%y')).split()[0]+"'"
            

            for each in data:
                if each['transdate'] == max_date:
                    sql += " and trans_id != '" + each['trans_id'] + "'"
                else:
                    break
            
            bal_diff = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql }).json()[0]['diff']
            if bal_diff == "" or bal_diff == None:
                bal_diff = 0
            
            sql = "SELECT acc_opn_bal_firm1+acc_opn_bal_firm2+acc_opn_bal_firm3 as open_bal FROM somanath20"+dByear+".acc_bal where acc_id ="+ str(acc_id)

           


            opn_bal1 = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql }).json()[0]['open_bal']
            if opn_bal1 == "" or opn_bal1 == None:
                opn_bal = 0 + bal_diff
            opn_bal = round(opn_bal1 + bal_diff,2)
            self.tree_cashflow.insert('','end',tags=('a'), values = ['-' , '-' , '-' , '-' , "{:.2f}".format(round(opn_bal,2))])
            

            i = 0
            for each in data:
                opn_bal += float(each['bal'])
                tags = 'b'
                if i%2 == 0:
                    tags = 'a'
                sale_id =  each['trans_sales']
                if sale_id == None:
                    sale_id = "-"
                else:
                    sale_id = sale_id.split("_")[1]

                
                self.tree_cashflow.insert('','end',tags=(tags ), values = [each['transdate'], sale_id, "{:.2f}".format(round(float(each['trans_amt']),2)) ,  "{:.2f}".format(round(float(each['amt_paid']),2))  ,  "{:.2f}".format(round(opn_bal,2))])
                i +=1

    def get_sales_rep(self , e):
        child = self.tree_sales_rep.get_children()
        for each in child:
            self.tree_sales_rep.delete(each)

        inv_no = self.ent_bill_sales_rep.get()
        if inv_no !="":
            self.combo_cust_sales_rep.delete(0 , con.END)
            self.ent_limit_sales_rep.delete(0 , con.END)
            self.ent_from_sales_rep.delete(0 , con.END)
            self.ent_to_sales_rep.delete(0 , con.END)
            try:
                inv = inv_no.split("-")[1]
                dbYear = inv_no.split("-")[0]
            except IndexError:
                dbYear= self.year
                inv = inv_no
            req = get("http://"+self.ip+":6000/reports/getCustomersales" , params = { "acc_name" : '' , "limit" : '' ,'sdate' :'','edate' :'','invNo' : inv ,'db' : dbYear })


        else:
            cust_name = self.combo_cust_sales_rep.get()
            limit = self.ent_limit_sales_rep.get()
            from_date = self.ent_from_sales_rep.get()
            to_date = self.ent_to_sales_rep.get()

            if cust_name == "" and inv_no == "":
                msg.showerror("Error" , "Select Customer or enter BILL NO")
                self.combo_cust_sales_rep.select_range(0,con.END)
                self.combo_cust_sales_rep.focus_set()
                return

            if cust_name!= "":
                if cust_name not in self.combo_cust_sales_rep['values']:
                    msg.showerror("Error" , "Select Name from the list")
                    self.combo_cust_sales_rep.select_range(0,con.END)
                    self.combo_cust_sales_rep.focus_set()
                    return

            if limit == "":
                date1 = from_date.split("/")
                if len(date1)!=3:
                    date1 = from_date.split("-")
                    if len(date1) != 3:
                        msg.showinfo("Info" , "Enter date in following format \n 'dd-mm-yy' or 'dd/mm/yy ")
                        self.ent_from_sales_rep.delete(0,con.END)
                        self.ent_from_sales_rep.focus_set()
                        return

                try:
                    datetime.datetime(int(date1[2]), int(date1[1]), int(date1[0]))
                except ValueError:
                    msg.showinfo("Info" , "Enter correct date")
                    self.ent_from_sales_rep.delete(0,con.END)
                    self.ent_from_sales_rep.focus_set()
                    return

                
                if len(date1[2])%2 !=0 :
                    msg.showinfo("Info" , "Enter correct date")
                    self.ent_from_sales_rep.delete(0,con.END)
                    self.ent_from_sales_rep.focus_set()
                    return

                if len(date1[0]) == 1:
                    date1[0] = '0' + date1[0]

                if len(date1[1]) == 1:
                    date1[1] = '0' + date1[1]    

                if len(date1[2]) == 2:
                    date1[2] = '20' + date1[2]    

                
                self.ent_from_sales_rep.delete(0,con.END)
                self.ent_from_sales_rep.insert(0,date1[0] + "-" + date1[1] + "-" + date1[2])        
                self.ent_from_sales_rep.select_clear()
                from_date = date1[2] + "-" + date1[1] + "-" + date1[0]

            if to_date != "":
                date1 = to_date.split("/")
                if len(date1)!=3:
                    date1 = to_date.split("-")
                    if len(date1) != 3:
                        msg.showinfo("Info" , "Enter date in following format \n 'dd-mm-yy' or 'dd/mm/yy ")
                        self.ent_to_sales_rep.delete(0,con.END)
                        self.ent_to_sales_rep.focus_set()
                        return

                try:
                    datetime.datetime(int(date1[2]), int(date1[1]), int(date1[0]))
                except ValueError:
                    msg.showinfo("Info" , "Enter correct date")
                    self.ent_to_sales_rep.delete(0,con.END)
                    self.ent_to_sales_rep.focus_set()
                    return

                
                if len(date1[2])%2 !=0 :
                    msg.showinfo("Info" , "Enter correct date")
                    self.ent_to_sales_rep.delete(0,con.END)
                    self.ent_to_sales_rep.focus_set()
                    return

                if len(date1[0]) == 1:
                    date1[0] = '0' + date1[0]

                if len(date1[1]) == 1:
                    date1[1] = '0' + date1[1]    

                if len(date1[2]) == 2:
                    date1[2] = '20' + date1[2]    

                
                self.ent_to_sales_rep.delete(0,con.END)
                self.ent_to_sales_rep.insert(0,date1[0] + "-" + date1[1] + "-" + date1[2])        
                self.ent_to_sales_rep.select_clear()

                to_date = date1[2] + "-" + date1[1] + "-" + date1[0]

            req = get("http://"+self.ip+":6000/reports/getCustomersales" , params = { "acc_name" : cust_name , "limit" : limit ,'sdate' :from_date,'edate' :to_date,'invNo' : '' ,'db' : self.year })


            
        if req.status_code == 201:
            msg.showinfo("Info" , "Not Found")
            return
        else:
            array_of_items = []
            data = req.json()
            if len(data) >0:
                for each in data:
                    x = data[each]
                    array_of_items.append([x[-1],x[-2],x[0][1],x[0][0],x[0][2]])
                array_of_items.sort(key=lambda x: x[0])

                ##array_of_items = [[1, 'HASI MENASU', '0.250', '60.000', '21-Nov-20'], [1, 'ONION S', '1.000', '65.000', '21-Nov-20'], [2, 'SUGAR', '1.000', '38.000', '17-Nov-20'], [4, 'DAZZY ENDOR 2RS', 71, '2.000', '25-Nov-20'], [5, 'MENASU .', '0.250', '320.000', '25-Nov-20'], [6, 'MOONG MAHARAJA GOLD', '0.500', '100.000', '18-Nov-20'], [6, 'HURULI KALU', 2, '45.000', '21-Nov-20'], [9, 'RAVA B', '1.000', '32.000', '18-Nov-20'], [11, 'DEVAGIRI 250G', '1.000', '65.000', '20-Nov-20'], [18, 'RAJ NJOY HALDI CHANDAN 5*100G', '1.000', '73.000', '17-Nov-20'], [26, 'GIL PRESTO 20RS 3+1N', '0.250', '80.000', '25-Nov-20'], [28, 'ULLAS 12RS', 2, '10.000', '25-Nov-20'], [41, 'NANDINI CURD 200G', 4, '13.000', '25-Nov-20'], [41, 'NANDINI MILK 500ML', 4, '22.000', '25-Nov-20']]
                y = 0
                sorted_array = []
                category_array = []


                x = array_of_items[0][0]
                for each in array_of_items:
                    y = each[0]
                    if x == y: category_array.append( each[1:] )
                    else: 
                        category_array.sort(key=lambda x: x[0][0])
                        sorted_array.append(category_array)
                        category_array = []
                        category_array.append( each[1:] )
                        x = each[0]
                    y = x
                category_array.sort(key=lambda x: x[0][0])
                sorted_array.append(category_array)    
                i =0
                for each in sorted_array:
                    tags = 'cat1'
                    if i%2 == 0:
                        tags = 'cat2'
                    for x in each:
                        qty = "{:.3f}".format(round( float(x[1]) ,3))
                        self.tree_sales_rep.insert('','end',tags =(tags ,), values = [x[0] , qty , x[2] , x[3]])
                    i += 1

    """--------------------------------------------------------------------------------------------------"""