from tkinter import ttk , constants as con , Text , filedialog

from base_window import base_window
from PIL import Image , ImageTk
from image_viewer import image_viewer

#acc_id, acc_type, acc_name, acc_email, acc_add, acc_mob1, acc_mob2, acc_gstin, acc_accno, acc_ifsc, acc_cus_type, insert_time, insert_id, update_time, update_id

class acc(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations,others):
        base_window.__init__(self , root ,frames , dmsn , lbls ,title)
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.others = others
        self.acc_img = None
        self.rad_acc = None
        self.rad_cus_type = None

        self.lbl_acc_type = ttk.Label(self.main_frame , text = "A/C Holder Type   :" , style = "window_text_medium.TLabel")
        self.lbl_acc_name = ttk.Label(self.main_frame , text = "A/C Holder Name   :" , style = "window_text_medium.TLabel")
        self.lbl_acc_email = ttk.Label(self.main_frame , text = "A/C Holder Email  :" , style = "window_text_medium.TLabel")
        self.lbl_acc_address = ttk.Label(self.main_frame , text = "A/C Holder Address:" , style = "window_text_medium.TLabel")
        self.lbl_acc_mob1 = ttk.Label(self.main_frame , text = "A/C Holder Mob1   :" , style = "window_text_medium.TLabel")
        self.lbl_acc_mob2 = ttk.Label(self.main_frame , text = "A/C Holder Mob2   :" , style = "window_text_medium.TLabel")
        self.lbl_acc_gst = ttk.Label(self.main_frame , text = "A/C Holder GST    :" , style = "window_text_medium.TLabel")
        self.lbl_acc_acno = ttk.Label(self.main_frame , text = "A/C Holder A/C no :" , style = "window_text_medium.TLabel")
        self.lbl_acc_ifsc = ttk.Label(self.main_frame , text = "A/C Holder IFSC   :" , style = "window_text_medium.TLabel")
        self.lbl_acc_ctype = ttk.Label(self.main_frame , text = "Customer Type     :" , style = "window_text_medium.TLabel")
        self.lbl_acc_img_txt = ttk.Label(self.main_frame , text = "A/C Holder Image  :" , style = "window_text_medium.TLabel")

        self.rad_cust = ttk.Radiobutton(self.main_frame , value = 0 , variable = self.rad_acc , style = "window_radio.TRadiobutton" , text = "Customer")
        self.rad_supp = ttk.Radiobutton(self.main_frame , value = 1 , variable = self.rad_acc , style = "window_radio.TRadiobutton" , text = "Supplier")
        self.ent_acc_name = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)))
        self.ent_acc_name.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_acc_email = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_acc_email.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_acc_address = Text(self.main_frame  , width = 30 , height = 4 ,  font = ('Lucida Grande' , -int(self.main_hgt*0.03)))
        self.ent_acc_mob1 = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_acc_mob1.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_acc_mob2 = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_acc_mob2.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_acc_gst = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_acc_gst.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_acc_acno = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_acc_acno.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_acc_ifsc = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_acc_ifsc.bind("<FocusOut>" , self.combo_entry_out)
        self.frm_rad_cust = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.rad_cust_nrm = ttk.Radiobutton(self.frm_rad_cust , value = 0 , variable = self.rad_cus_type , style = "window_radio.TRadiobutton" , text = "NRM")
        self.rad_cust_htl = ttk.Radiobutton(self.frm_rad_cust , value = 1 , variable = self.rad_cus_type , style = "window_radio.TRadiobutton" , text = "HTL")
        self.rad_cust_spl = ttk.Radiobutton(self.frm_rad_cust , value = 2 , variable = self.rad_cus_type , style = "window_radio.TRadiobutton" , text = "SPL")
        self.rad_cust_ang = ttk.Radiobutton(self.frm_rad_cust , value = 3 , variable = self.rad_cus_type , style = "window_radio.TRadiobutton" , text = "ANG")
        self.lbl_acc_img = ttk.Label(self.main_frame  , width = 30 , style = "window_lbl_ent.TLabel")

        self.btn_acc_img_brw = ttk.Button(self.main_frame , text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_acc(None))
        self.btn_acc_img_brw.bind("<Return>" , self.file_dialog_acc)
        self.btn_acc_img_view = ttk.Button(self.main_frame , text = " View " , style = "window_btn_medium.TButton" ,command = lambda : self.view_acc(None))
        self.btn_acc_img_view.bind("<Return>" , self.view_acc)

        if root.winfo_screenheight()>1000:
            self.tree_frame = ttk.Frame(self.main_frame , height = int(self.main_hgt*0.853) , width = int(self.main_wdt*0.45) , style = "root_menu.TFrame")
        else:
            self.tree_frame = ttk.Frame(self.main_frame , height = int(self.main_hgt*0.863) , width = int(self.main_wdt*0.45) , style = "root_menu.TFrame")
        self.tree_frame.pack_propagate(False)
        self.tree_frame.grid_propagate(False)

        self.frm_rad_acc = ttk.Frame(self.tree_frame , style = "root_main.TFrame")
        self.ent_acc_search = ttk.Entry(self.frm_rad_acc  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.chk_cust = ttk.Checkbutton(self.frm_rad_acc , text = "Customers" , style = "window_check.TCheckbutton")
        self.chk_supp = ttk.Checkbutton(self.frm_rad_acc , text = "Suppliers" , style = "window_check.TCheckbutton")

        self.tree = ttk.Treeview(self.tree_frame ,selectmode = "browse", takefocus = True , show = "headings" , style = "window.Treeview")
        self.tree.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.scroll_y = ttk.Scrollbar(self.tree_frame , orient = con.VERTICAL , command = self.tree.yview)
        self.scroll_x = ttk.Scrollbar(self.tree_frame , orient = con.HORIZONTAL , command = self.tree.xview)
        self.tree.config(yscrollcommand = self.scroll_y.set , xscrollcommand = self.scroll_x.set)

        

        self.tree['columns'] = ('id','type','name')
        self.tree.heading('id' , text = 'ID')
        self.tree.heading('type' , text = 'Type')
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

        self.lbl_acc_type.grid(row = 0 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_name.grid(row = 1 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_email.grid(row = 2 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_address.grid(row = 3 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_mob1.grid(row = 4 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_mob2.grid(row = 5 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_gst.grid(row = 6 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_acno.grid(row = 7 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_ifsc.grid(row = 8 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_ctype.grid(row = 9 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_img_txt.grid(row = 10 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))


        self.rad_cust.grid(row = 0 , column = 1)
        self.rad_supp.grid(row = 0 , column = 2)
        self.ent_acc_name.grid(row = 1 , column = 1 , columnspan = 2)
        self.ent_acc_email.grid(row = 2 , column = 1 , columnspan = 2)
        self.ent_acc_address.grid(row = 3 , column = 1 , columnspan = 2)
        self.ent_acc_mob1.grid(row = 4 , column = 1 , columnspan = 2)
        self.ent_acc_mob2.grid(row = 5 , column = 1 , columnspan = 2)
        self.ent_acc_gst.grid(row = 6 , column = 1 , columnspan = 2)
        self.ent_acc_acno.grid(row = 7 , column = 1 , columnspan = 2)
        self.ent_acc_ifsc.grid(row = 8 , column = 1 , columnspan = 2)
        self.frm_rad_cust.grid(row = 9 , column = 1 , columnspan = 2)
        self.rad_cust_nrm.grid(row = 0 , column = 0, padx = int(self.main_wdt*0.01))
        self.rad_cust_htl.grid(row = 0 , column = 1, padx = int(self.main_wdt*0.01))
        self.rad_cust_spl.grid(row = 0 , column = 2, padx = int(self.main_wdt*0.01))
        self.rad_cust_ang.grid(row = 0 , column = 3, padx = int(self.main_wdt*0.01))
        self.lbl_acc_img.grid(row = 10 , column = 1 , columnspan = 2)
        self.btn_acc_img_brw.grid(row = 11 , column = 1)
        self.btn_acc_img_view.grid(row = 11 , column = 2)
        
        self.tree_frame.grid(row = 0 , column = 6 , rowspan = 15 , padx = int(self.main_wdt*0.01) , pady = int(self.main_hgt*0.035))
        self.frm_rad_acc.pack(anchor = con.NW )
        self.ent_acc_search.grid(row = 0 , column = 0 , sticky = con.W)
        if root.winfo_screenheight()>1000:
            self.chk_cust.grid(row = 0 , column = 1 , sticky = con.E , padx = int(self.main_hgt*0.0538))
        else:
            self.chk_cust.grid(row = 0 , column = 1 , sticky = con.E , padx = int(self.main_hgt*0.04955))
        self.chk_supp.grid(row = 0 , column = 2 , sticky = con.E)

        self.scroll_y.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        #self.tree_header_frame.pack(anchor = con.N , side = con.LEFT , fill = con.Y)
        self.tree.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)

        self.btn_frame.grid(row = 20 , column = 6 , sticky = con.E)
        self.btn_new.grid(row = 0 , column = 0 , padx = int(self.main_wdt*0.01))
        self.btn_edit.grid(row = 0 , column = 1 , padx = int(self.main_wdt*0.01))
        self.btn_save.grid(row = 0 , column = 2 , padx = int(self.main_wdt*0.01))

        self.tree_wdt = self.tree_frame.winfo_reqwidth()-self.scroll_y.winfo_reqwidth()
        
        self.tree.column('id' , width = int(self.tree_wdt*0.15) ,minwidth = int(self.tree_wdt*0.15) , anchor = "w")
        self.tree.column('type' , width = int(self.tree_wdt*0.15) , minwidth = int(self.tree_wdt*0.15) , anchor = "w")
        self.tree.column('name' , width = int(self.tree_wdt*0.70) , minwidth = int(self.tree_wdt*0.70) , anchor = "w")



    def new(self , e):
        pass

    def edit(self , e):
        pass

    def save(self , e):
        pass

    def combo_entry_out(self , e):
        e.widget.select_clear()

    def file_dialog_acc(self , e):
        file = filedialog.askopenfilename(initialdir = self.others[0]+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        if file!= "":
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]
            self.lbl_acc_img.config(text = text)
            self.acc_img = ImageTk.PhotoImage(Image.open(file)) 
        else:
            self.lbl_acc_img.config(text = "")


    def view_acc(self , e):
        if self.acc_img != None or self.lbl_acc_img.cget("text") != "":
            image_viewer(self.acc_img,"QR Code Image")