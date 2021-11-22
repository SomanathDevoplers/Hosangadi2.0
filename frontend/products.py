#prod_id, prod_bar, prod_cat, prod_hsn, prod_kan, prod_min_qty, prod_date, prod_mrp, prod_sup, prod_tax1, prod_tax2, prod_unit_type, nml_unit, htl_unit, spl_unit, ang_unit, insert_time, insert_id, update_time, update_id

from tkinter import Toplevel, ttk , constants as con , Text , filedialog
from base_window import base_window
from PIL import Image , ImageTk
from image_viewer import image_viewer

class prods(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations,others):
        base_window.__init__(self , root ,frames , dmsn , lbls ,title)
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.img_kan = None                                                                             #kannada image
        self.img_prod_high = None                                                                       #high quality image
        self.img_prod_low = None                                                                        #low quality image
        self.rad_unit = None    
        self.others = others                                                                        #units radio
                                                                                 
        
        self.lbl_bar = ttk.Label(self.main_frame , text = "Barcode    :" , style = "window_text_medium.TLabel")
        self.lbl_cat = ttk.Label(self.main_frame , text = "  Category :" , style = "window_text_medium.TLabel")
        self.lbl_name = ttk.Label(self.main_frame , text = "Name       :" , style = "window_text_medium.TLabel")
        self.lbl_hsn = ttk.Label(self.main_frame , text = "HSN        :" , style = "window_text_medium.TLabel")
        self.lbl_shelf = ttk.Label(self.main_frame , text = "  Shelf No :" , style = "window_text_medium.TLabel")
        self.lbl_kan_txt = ttk.Label(self.main_frame , text = "Kannada    :" , style = "window_text_medium.TLabel")
        self.lbl_min_qty = ttk.Label(self.main_frame , text = "Min Qty    :" , style = "window_text_medium.TLabel")
        self.lbl_exp = ttk.Label(self.main_frame , text = "Expiry   :" , style = "window_text_medium.TLabel")
        self.lbl_desc = ttk.Label(self.main_frame , text = "Description:" , style = "window_text_medium.TLabel")
        self.lbl_img1_txt = ttk.Label(self.main_frame , text = "Image 1    :" , style = "window_text_medium.TLabel")
        self.lbl_img2_txt = ttk.Label(self.main_frame , text = "Image 2    :" , style = "window_text_medium.TLabel")
        self.lbl_sup = ttk.Label(self.main_frame , text = "Supplier   :" , style = "window_text_medium.TLabel")
        self.lbl_tax1 = ttk.Label(self.main_frame , text = "GST        :" , style = "window_text_medium.TLabel")
        self.lbl_tax2 = ttk.Label(self.main_frame , text = "CESS     :" , style = "window_text_medium.TLabel")
        self.lbl_mrp1 = ttk.Label(self.main_frame , text = "MRP 1  :" , style = "window_text_medium.TLabel")
        self.lbl_mrp2 = ttk.Label(self.main_frame , text = "MRP 2  :" , style = "window_text_medium.TLabel")
        self.lbl_unit = ttk.Label(self.main_frame , text = "Unit     :" , style = "window_text_medium.TLabel")
        self.lbl_nrm = ttk.Label(self.main_frame , text = "Units NRM  :" , style = "window_text_medium.TLabel")
        self.lbl_htl = ttk.Label(self.main_frame , text = "Units HTL  :" , style = "window_text_medium.TLabel")
        self.lbl_spl = ttk.Label(self.main_frame , text = "Units SPL  :" , style = "window_text_medium.TLabel")
        self.lbl_ang = ttk.Label(self.main_frame , text = "Units ANG  :" , style = "window_text_medium.TLabel")



        self.btn_add_bar = ttk.Button(self.main_frame ,text = " Add "  , style = "window_btn_medium.TButton" , command = lambda : self.show_top_bar(None))
        self.btn_add_bar.bind("<Return>" , self.show_top_bar)

        self.ent_name = ttk.Entry(self.main_frame  , width = 30 ,  font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_name.bind("<FocusOut>" , self.combo_entry_out)

        self.btn_add_cat = ttk.Button(self.main_frame  ,text = " Add "  , style = "window_btn_medium.TButton" , command = lambda : self.show_top_cat(None))
        self.btn_add_cat.bind("<Return>" , self.show_top_cat)

        self.ent_hsn = ttk.Entry(self.main_frame  , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_hsn.bind("<FocusOut>" , self.combo_entry_out)

        self.ent_shelf = ttk.Entry(self.main_frame  , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_shelf.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_kan = ttk.Label(self.main_frame  , width = 30 , style = "window_lbl_ent.TLabel")
        self.btn_kan_add = ttk.Button(self.main_frame , text = "Add Img" , style = "window_btn_medium.TButton" ,command = lambda : self.add_image(None))
        self.btn_kan_add.bind("<Return>" , self.add_image)
        self.btn_kan_brw = ttk.Button(self.main_frame , text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_kan(None))
        self.btn_kan_brw.bind("<Return>" , self.file_dialog_kan)
        self.btn_kan_vw = ttk.Button(self.main_frame , text = "View" , style = "window_btn_medium.TButton" ,command = lambda : self.view_kan(None))
        self.btn_kan_vw.bind("<Return>" , self.view_kan)

        self.ent_min_qty = ttk.Entry(self.main_frame  , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_min_qty.bind("<FocusOut>" , self.combo_entry_out)

        self.ent_exp = ttk.Entry(self.main_frame  , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_exp.bind("<FocusOut>" , self.combo_entry_out)

        self.ent_desc = Text(self.main_frame  , width = 30 , height = 4 ,  font = ('Lucida Grande' , -int(self.main_hgt*0.03)) )

        self.lbl_img1 = ttk.Label(self.main_frame  , width = 30 , style = "window_lbl_ent.TLabel")
        self.btn_img1_brw = ttk.Button(self.main_frame , text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_img1(None))
        self.btn_img1_brw.bind("<Return>" , self.file_dialog_img1)
        self.btn_img1_vw = ttk.Button(self.main_frame , text = "View" , style = "window_btn_medium.TButton" ,command = lambda : self.view_img1(None))
        self.btn_img1_vw.bind("<Return>" , self.view_img1)

        self.lbl_img2 = ttk.Label(self.main_frame  , width = 30 , style = "window_lbl_ent.TLabel")
        self.btn_img2_brw = ttk.Button(self.main_frame , text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_img2(None))
        self.btn_img2_brw.bind("<Return>" , self.file_dialog_img2)
        self.btn_img2_vw = ttk.Button(self.main_frame , text = "View" , style = "window_btn_medium.TButton" ,command = lambda : self.view_img2(None))
        self.btn_img2_vw.bind("<Return>" , self.view_img2)

        self.btn_add_sup = ttk.Button(self.main_frame  ,text = " Add "  , style = "window_btn_medium.TButton" , command = lambda : self.show_top_sup(None))
        self.btn_add_sup.bind("<Return>" , self.show_top_sup)

        self.combo_unit = ttk.Combobox(self.main_frame  , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 6) 
        self.combo_unit.bind("<FocusOut>" , self.combo_entry_out)

        self.combo_tax1 = ttk.Combobox(self.main_frame  , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 6) 
        self.combo_tax1.bind("<FocusOut>" , self.combo_entry_out)

        self.combo_tax2 = ttk.Combobox(self.main_frame  , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 6) 
        self.combo_tax2.bind("<FocusOut>" , self.combo_entry_out)


        self.ent_mrp1 = ttk.Entry(self.main_frame  , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_mrp1.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_mrp2 = ttk.Entry(self.main_frame  , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_mrp2.bind("<FocusOut>" , self.combo_entry_out)

        self.frm_nrm = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.ent_nrm1 = ttk.Entry(self.frm_nrm  , width = 6 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_nrm1.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_nrm2 = ttk.Entry(self.frm_nrm  , width = 6 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_nrm2.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_nrm3 = ttk.Entry(self.frm_nrm  , width = 6 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_nrm3.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_nrm4 = ttk.Entry(self.frm_nrm  , width = 6 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_nrm4.bind("<FocusOut>" , self.combo_entry_out)

        self.frm_htl = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.chk_htl = ttk.Checkbutton(self.frm_htl  , style = "window_check.TCheckbutton")
        self.ent_htl1 = ttk.Entry(self.frm_htl  , width = 6 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_htl1.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_htl2 = ttk.Entry(self.frm_htl  , width = 6 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_htl2.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_htl3 = ttk.Entry(self.frm_htl  , width = 6 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_htl3.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_htl4 = ttk.Entry(self.frm_htl  , width = 6 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_htl4.bind("<FocusOut>" , self.combo_entry_out)

        self.frm_ang = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.chk_ang = ttk.Checkbutton(self.frm_ang  , style = "window_check.TCheckbutton")
        self.ent_ang1 = ttk.Entry(self.frm_ang  , width = 6 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_ang1.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_ang2 = ttk.Entry(self.frm_ang  , width = 6 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_ang2.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_ang3 = ttk.Entry(self.frm_ang  , width = 6 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_ang3.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_ang4 = ttk.Entry(self.frm_ang  , width = 6 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_ang4.bind("<FocusOut>" , self.combo_entry_out)

        self.frm_spl = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.chk_spl = ttk.Checkbutton(self.frm_spl  , style = "window_check.TCheckbutton")
        self.ent_spl1 = ttk.Entry(self.frm_spl  , width = 6 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_spl1.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_spl2 = ttk.Entry(self.frm_spl  , width = 6 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_spl2.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_spl3 = ttk.Entry(self.frm_spl  , width = 6 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_spl3.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_spl4 = ttk.Entry(self.frm_spl  , width = 6 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_spl4.bind("<FocusOut>" , self.combo_entry_out)


        if root.winfo_screenheight()>1000:
            self.tree_frame = ttk.Frame(self.main_frame , height = int(self.main_hgt*0.844) , width = int(self.main_wdt*0.45) , style = "root_menu.TFrame")
        else:
            self.tree_frame = ttk.Frame(self.main_frame , height = int(self.main_hgt*0.858) , width = int(self.main_wdt*0.46) , style = "root_menu.TFrame")
        self.tree_frame.pack_propagate(False)
        self.tree_frame.grid_propagate(False)

        self.frm_chk_cat = ttk.Frame(self.tree_frame , style = "root_main.TFrame")
        self.chk_cat = ttk.Checkbutton(self.frm_chk_cat , text = "Category :" , style = "window_check.TCheckbutton")
        self.combo_cat1 = ttk.Combobox(self.frm_chk_cat  , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 22 , style = "window_combo.TCombobox") 
        self.combo_cat1.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_cat2 = ttk.Combobox(self.frm_chk_cat  , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 22) 
        self.combo_cat2.bind("<FocusOut>" , self.combo_entry_out)

        self.frm_chk_sup = ttk.Frame(self.tree_frame , style = "root_main.TFrame")
        self.chk_sup = ttk.Checkbutton(self.frm_chk_sup , text = "Supplier :" , style = "window_check.TCheckbutton")
        self.combo_sup1 = ttk.Combobox(self.frm_chk_sup  , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 22) 
        self.combo_sup1.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_sup2 = ttk.Combobox(self.frm_chk_sup  , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 22) 
        self.combo_sup2.bind("<FocusOut>" , self.combo_entry_out)
        


        self.ent_prod_search = ttk.Entry(self.tree_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
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



        self.lbl_bar.grid(row = 0 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_name.grid(row = 1 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_hsn.grid(row = 2 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_kan_txt.grid(row = 3 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_min_qty.grid(row = 5 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_desc.grid(row = 6 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_img1_txt.grid(row = 7 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_img2_txt.grid(row = 9 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_sup.grid(row = 11 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_tax1.grid(row = 12 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_nrm.grid(row = 13 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_htl.grid(row = 14 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_spl.grid(row = 15 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_ang.grid(row = 16 , column = 0 , pady = int(self.main_hgt*0.01))


        self.btn_add_bar.grid(row = 0 , column = 1 , sticky= con.W)
        self.lbl_cat.grid(row = 0 , column = 2 , sticky = con.E)
        self.btn_add_cat.grid(row = 0 , column = 3)
        self.ent_name.grid(row = 1 , column = 1 , columnspan = 3)
        self.ent_hsn.grid(row = 2 , column = 1 , sticky = con.W)
        self.lbl_shelf.grid(row = 2 , column = 2 , sticky = con.E)
        self.ent_shelf.grid(row = 2 , column = 3 )
        self.lbl_kan.grid(row = 3 , column = 1 , columnspan = 3)
        self.btn_kan_add.grid(row = 4 , column = 1 , sticky = con.W)
        self.btn_kan_brw.grid(row = 4 , column = 2 )
        self.btn_kan_vw .grid(row = 4 , column = 3 , sticky = con.E)
        self.ent_min_qty.grid(row = 5 , column = 1 , sticky = con.W)
        self.lbl_exp.grid(row = 5 , column = 2 , sticky = con.E)
        self.ent_exp.grid(row = 5 , column = 3 , sticky = con.E)
        self.ent_desc.grid(row = 6 , column = 1 , columnspan = 3)
        self.lbl_img1.grid(row = 7 , column = 1 , columnspan = 3)
        self.btn_img1_brw.grid(row = 8 , column = 1 , sticky = con.W)
        self.btn_img1_vw.grid(row = 8 , column = 2 , sticky = con.W)
        self.lbl_img2.grid(row = 9 , column = 1 , columnspan = 3)
        self.btn_img2_brw.grid(row = 10 , column = 1 , sticky = con.W)
        self.btn_img2_vw.grid(row = 10 , column = 2 , sticky = con.W)
        self.btn_add_sup.grid(row = 11 , column = 1 , sticky = con.W)
        self.lbl_unit.grid(row = 11 , column = 2 , sticky = con.E)
        self.combo_unit.grid(row = 11 , column = 3 , sticky = con.E)
        self.combo_tax1.grid(row = 12 , column = 1 , sticky = con.W)
        self.lbl_tax2.grid(row = 12 , column = 2 , sticky = con.E)
        self.combo_tax2.grid(row = 12 , column = 3 , sticky = con.E)

        self.frm_nrm.grid(row = 13 , column = 1 , columnspan = 3 , sticky = con.W)
        self.ent_nrm1.grid(row = 0, column = 1)
        self.ent_nrm2.grid(row = 0, column = 2)
        self.ent_nrm3.grid(row = 0, column = 3)
        self.ent_nrm4.grid(row = 0, column = 4)
        
        self.frm_htl.grid(row = 14 , column = 1 , columnspan = 3, sticky = con.W)
        self.ent_htl1.grid(row = 0, column = 1)
        self.ent_htl2.grid(row = 0, column = 2)
        self.ent_htl3.grid(row = 0, column = 3)
        self.ent_htl4.grid(row = 0, column = 4)
        self.chk_htl.grid(row = 0, column = 5 , padx = int(self.main_wdt*0.01))

        self.frm_ang.grid(row = 15 , column = 1 , columnspan = 3, sticky = con.W)
        self.ent_ang1.grid(row = 0, column = 1)
        self.ent_ang2.grid(row = 0, column = 2)
        self.ent_ang3.grid(row = 0, column = 3)
        self.ent_ang4.grid(row = 0, column = 4)
        self.chk_ang.grid(row = 0, column = 5 , padx = int(self.main_wdt*0.01))

        self.frm_spl.grid(row = 16 , column = 1 , columnspan = 3, sticky = con.W)
        self.ent_spl1.grid(row = 0, column = 1)
        self.ent_spl2.grid(row = 0, column = 2)
        self.ent_spl3.grid(row = 0, column = 3)
        self.ent_spl4.grid(row = 0, column = 4)
        self.chk_spl.grid(row = 0, column = 5 , padx = int(self.main_wdt*0.01))

        self.tree_frame.grid(row = 0 , column = 6 , rowspan = 15 , padx = int(self.main_wdt*0.01) , pady = int(self.main_hgt*0.01))
        self.frm_chk_cat.pack()
        self.chk_cat.grid(row = 0, column = 1)
        self.combo_cat1.grid(row = 0, column = 2, padx = int(self.main_wdt*0.002))
        self.combo_cat2.grid(row = 0, column = 3)
        self.frm_chk_sup.pack()
        self.chk_sup.grid(row = 0, column = 1)
        self.combo_sup1.grid(row = 0, column = 2, padx = int(self.main_wdt*0.002) , pady = int(self.main_hgt*0.005))
        self.combo_sup2.grid(row = 0, column = 3)

        self.scroll_y.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        self.tree.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)

        self.btn_frame.grid(row = 15 ,column = 6 , sticky = con.E)
        self.btn_new.grid(row = 0 , column = 0 , padx = int(self.main_wdt*0.01))
        self.btn_edit.grid(row = 0 , column = 1 , padx = int(self.main_wdt*0.01))
        self.btn_save.grid(row = 0 , column = 2 , padx = int(self.main_wdt*0.01))


        self.tree_wdt = self.tree_frame.winfo_reqwidth()-self.scroll_y.winfo_reqwidth()
        
        self.tree.column('id' , width = int(self.tree_wdt*0.2) ,minwidth = int(self.tree_wdt*0.2) , anchor = "w")
        self.tree.column('name' , width = int(self.tree_wdt*0.80) , minwidth = int(self.tree_wdt*0.80) , anchor = "w")


    def combo_entry_out(self , e):
        e.widget.select_clear()
    
    def show_top_bar(self,e):
        self.top_bar = Toplevel()
        self.top_bar.geometry("+"+str(int(self.main_wdt/3))+"+"+str(int(self.main_hgt/3)))
        self.top_bar.focus_set()
        self.top_bar.overrideredirect(True)
        self.top_bar.bind("<FocusOut>" , self.focus_top_bar)
        self.top_bar.bind("<Escape>" , self.destroy_top_bar)
        
        self.frm_barcode = ttk.Frame(self.top_bar  , style = "root_menu.TFrame")
        self.btn_gen_bar = ttk.Button(self.frm_barcode , text = "Genarate Barcode"  , style = "window_btn_medium.TButton" ,command = lambda : self.generate(None))
        self.btn_gen_bar.bind("<Return>" , self.generate)
        self.ent_bar = Text(self.frm_barcode  , width = 30 , height = 4 ,  font = ('Lucida Grande' , -int(self.main_hgt*0.03)) )
        self.btn_gen_bar.pack()
        self.ent_bar.pack()
        self.frm_barcode.pack()

    def focus_top_bar(self , e):
        self.top_bar.bell()
        self.top_bar.deiconify()

    def destroy_top_bar(self , e):
        self.top_bar.destroy()

    def show_top_cat(self,e):
        self.top_cat = Toplevel()
        self.top_cat.geometry("+"+str(int(self.main_wdt/3))+"+"+str(int(self.main_hgt/3)))
        self.top_cat.focus_set()
        self.top_cat.overrideredirect(True)
        self.top_cat.bind("<FocusOut>" , self.focus_top_cat)
        self.top_cat.bind("<Escape>" , self.destroy_top_cat)
        
        self.frm_category = ttk.Frame(self.top_cat  , style = "root_menu.TFrame")
        self.combo_cat = ttk.Combobox(self.top_cat  , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 29) 
        self.combo_cat.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_cat = Text(self.frm_category  , width = 30 , height = 4 ,  font = ('Lucida Grande' , -int(self.main_hgt*0.03)))
        self.combo_cat.pack()
        self.ent_cat.pack()
        self.frm_category.pack()

    def focus_top_cat(self , e):
        self.top_cat.bell()
        self.top_cat.deiconify()

    def destroy_top_cat(self , e):
        self.top_cat.destroy()

    def show_top_sup(self,e):
        self.top_sup = Toplevel()
        self.top_sup.geometry("+"+str(int(self.main_wdt/3))+"+"+str(int(self.main_hgt/3)))
        self.top_sup.focus_set()
        self.top_sup.overrideredirect(True)
        self.top_sup.bind("<FocusOut>" , self.focus_top_sup)
        self.top_sup.bind("<Escape>" , self.destroy_top_sup)
        
        self.frm_supplier = ttk.Frame(self.top_sup  , style = "root_menu.TFrame")
        self.combo_sup = ttk.Combobox(self.top_sup  , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 29) 
        self.combo_sup.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_sup = Text(self.frm_supplier  , width = 30 , height = 4 ,  font = ('Lucida Grande' , -int(self.main_hgt*0.03)))
        self.combo_sup.pack()
        self.ent_sup.pack()
        self.frm_supplier.pack()

    def focus_top_sup(self , e):
        self.top_sup.bell()
        self.top_sup.deiconify()

    def destroy_top_sup(self , e):
        self.top_sup.destroy()

    def file_dialog_kan(self , e):
        file = filedialog.askopenfilename(initialdir = self.others[0]+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        if file!= "":
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]

            self.lbl_kan.config(text = text)
            self.image_kan = ImageTk.PhotoImage(Image.open(file))
        else:
            self.lbl_kan.config(text = "")

    def view_kan(self , e):
        if self.image_kan != None or self.lbl_kan.cget("text") != "":
            image_viewer(self.image_kan,"QR Code Image")

    def add_image(self , e):
        pass

    def generate(self,e):
        pass

    def close(self , e):
        try:
            self.top_bar.destroy()
        except AttributeError:
            pass
            
        try:
            self.top_cat.destroy()
        except AttributeError:
            pass

        try:
            self.top_sup.destroy()
        except AttributeError:
            pass

        base_window.close(self,e)
    
    def minimize(self, e):
        try:
            self.top_bar.destroy()
        except AttributeError:
            pass
            
        try:
            self.top_cat.destroy()
        except AttributeError:
            pass

        try:
            self.top_sup.destroy()
        except AttributeError:
            pass

        base_window.minimize(self,e)
        

    def file_dialog_img1(self , e):
        file = filedialog.askopenfilename(initialdir = self.others[0]+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        if file!= "":
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]

            self.lbl_img1.config(text = text)
            self.img_prod_low = ImageTk.PhotoImage(Image.open(file))
        else:
            self.lbl_img1.config(text = "")

    def view_img1(self , e):
        if self.img_prod_low != None or self.lbl_img1.cget("text") != "":
            image_viewer(self.img_prod_low,"QR Code Image")

    def file_dialog_img2(self , e):
        file = filedialog.askopenfilename(initialdir = self.others[0]+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        if file!= "":
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]

            self.lbl_img2.config(text = text)
            self.img_prod_low = ImageTk.PhotoImage(Image.open(file))
        else:
            self.lbl_img2.config(text = "")

    def view_img2(self , e):
        if self.img_prod_low != None or self.lbl_img2.cget("text") != "":
            image_viewer(self.img_prod_low,"QR Code Image")

    def new(self , e):
        pass

    def edit(self , e):
        pass

    def save(self , e):
        pass