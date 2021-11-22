from tkinter import ttk , constants as con , Text , filedialog

from base_window import base_window
from PIL import Image , ImageTk
from image_viewer import image_viewer
#firm_id, firm_tax, firm_name, firm_suffix, firm_email, firm_mobile, firm_website, firm_address, firm_gstin, firm_pan, firm_bank, firm_accno, firm_ifsc, insert_time, firm_upid, firm_upiqr, firm_logo, firm_photo, insert_id, update_time, update_id
class firm(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations,others):
        base_window.__init__(self , root ,frames , dmsn , lbls ,title)
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.combo_values = ["REGULAR" , "COMPOSITION" , "CASH"]
        self.image_qr = None
        self.image_logo = None
        self.image_photo = None
        self.others = others


        self.lbl_firm_tax = ttk.Label(self.main_frame , text = "Tax Method        :" , style = "window_text_medium.TLabel")
        self.lbl_firm_name = ttk.Label(self.main_frame , text = "Firm Name         :" , style = "window_text_medium.TLabel")
        self.lbl_firm_suff_txt = ttk.Label(self.main_frame , text = "Firm Suffix       :" , style = "window_text_medium.TLabel")
        self.lbl_firm_email = ttk.Label(self.main_frame , text = "Firm Email        :" , style = "window_text_medium.TLabel")
        self.lbl_firm_mob = ttk.Label(self.main_frame , text = "Firm Mobile       :" , style = "window_text_medium.TLabel")
        self.lbl_firm_web = ttk.Label(self.main_frame , text = "Firm Website      :" , style = "window_text_medium.TLabel")
        self.lbl_firm_address = ttk.Label(self.main_frame , text = "Firm Address      :" , style = "window_text_medium.TLabel")
        self.lbl_firm_gstin = ttk.Label(self.main_frame , text = "Firm GSTIN        :" , style = "window_text_medium.TLabel")
        self.lbl_firm_pan = ttk.Label(self.main_frame , text = "Firm PAN          :" , style = "window_text_medium.TLabel")
        self.lbl_firm_bank = ttk.Label(self.main_frame , text = "Firm Bank Name    :" , style = "window_text_medium.TLabel")
        self.lbl_firm_ifsc = ttk.Label(self.main_frame , text = "Firm Bank IFSC    :" , style = "window_text_medium.TLabel")
        self.lbl_firm_accno = ttk.Label(self.main_frame , text = "Firm Bank AC/NO   :" , style = "window_text_medium.TLabel")
        self.lbl_firm_upiid = ttk.Label(self.main_frame , text = "Firm UPI ID       :" , style = "window_text_medium.TLabel")
        self.lbl_firm_upiqr_txt = ttk.Label(self.main_frame , text = "Firm UPI QR       :" , style = "window_text_medium.TLabel")
        self.lbl_firm_logo_txt = ttk.Label(self.main_frame , text = "Firm Logo         :" , style = "window_text_medium.TLabel")
        self.lbl_firm_photo_txt = ttk.Label(self.main_frame , text = "Firm Photo        :" , style = "window_text_medium.TLabel")

        self.combo_tax = ttk.Combobox(self.main_frame  ,values = self.combo_values, font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30) 
        self.combo_tax.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_tax.insert(0,self.combo_values[0])
        self.ent_firm_name = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_firm_name.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_firm_suff = ttk.Label(self.main_frame , width = 30,  style = "window_lbl_ent.TLabel")
        self.ent_firm_email = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_firm_email.bind("<FocusOut>" , self.combo_entry_out)

        self.ent_firm_mob = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_firm_mob.bind("<FocusOut>" , self.combo_entry_out)

        self.ent_firm_web = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_firm_web.bind("<FocusOut>" , self.combo_entry_out)

        self.ent_firm_address = Text(self.main_frame  , width = 30 , height = 4 ,  font = ('Lucida Grande' , -int(self.main_hgt*0.03)))
        self.ent_firm_gstin = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_firm_gstin.bind("<FocusOut>" , self.combo_entry_out)

        self.ent_firm_pan = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_firm_pan.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_firm_bank = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_firm_bank.bind("<FocusOut>" , self.combo_entry_out)
        
        self.ent_firm_ifsc = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_firm_ifsc.bind("<FocusOut>" , self.combo_entry_out)

        self.ent_firm_accno = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_firm_accno.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_firm_upiid = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_firm_upiid.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_firm_upiqr = ttk.Label(self.main_frame  , width = 30 , background = "#fff", justify = con.RIGHT ,relief = con.SOLID , borderwidth = 1 , border = 1 , font = ('Lucida Grande' , -int(self.main_hgt*0.03)))
        self.btn_firm_upiqr_brw = ttk.Button(self.main_frame , text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_qr(None))
        self.btn_firm_upiqr_brw.bind("<Return>" , self.file_dialog_qr)
        self.btn_firm_upiqr_vw = ttk.Button(self.main_frame , text = "View" , style = "window_btn_medium.TButton" ,command = lambda : self.view_qr(None))
        self.btn_firm_upiqr_vw.bind("<Return>" , self.view_qr)
        
        self.lbl_firm_logo = ttk.Label(self.main_frame  , width = 30 , style = "window_lbl_ent.TLabel")
        self.btn_firm_logo_brw = ttk.Button(self.main_frame , text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_logo(None))
        self.btn_firm_logo_brw.bind("<Return>" , self.file_dialog_logo)
        self.btn_firm_logo_vw = ttk.Button(self.main_frame , text = "View" , style = "window_btn_medium.TButton" ,command = lambda : self.view_logo(None))
        self.btn_firm_logo_vw.bind("<Return>" , self.view_logo)

        self.lbl_firm_photo = ttk.Label(self.main_frame  , width = 30, style = "window_lbl_ent.TLabel")
        self.btn_firm_photo_brw = ttk.Button(self.main_frame , text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_photo(None))
        self.btn_firm_photo_brw.bind("<Return>" , self.file_dialog_photo)
        self.btn_firm_photo_vw = ttk.Button(self.main_frame , text = "View" , style = "window_btn_medium.TButton" ,command = lambda : self.view_photo(None))
        self.btn_firm_photo_vw.bind("<Return>" , self.view_photo)

        

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

        

        self.tree['columns'] = ('id','sfx','name')
        self.tree.heading('id' , text = 'ID')
        self.tree.heading('sfx' , text = 'Sfx')
        self.tree.heading('name' , text = 'name')
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


        self.lbl_firm_tax.grid(row = 0 , column = 0 , pady = int(self.main_hgt*0.01))
        self.combo_tax.grid(row = 0 , column = 1 )
        self.lbl_firm_name.grid(row = 1 , column = 0 , pady = int(self.main_hgt*0.012))
        self.ent_firm_name.grid(row = 1 , column = 1 , sticky = con.W)
        self.lbl_firm_suff_txt.grid(row = 2 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_firm_suff.grid(row = 2 , column = 1 , sticky = con.W)
        self.lbl_firm_email.grid(row = 3 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_email.grid(row = 3 , column = 1 , sticky = con.W)
        self.lbl_firm_mob.grid(row = 4 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_mob.grid(row = 4 , column = 1 , sticky = con.W)
        self.lbl_firm_web.grid(row = 5 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_web.grid(row = 5 , column = 1 , sticky = con.W)
        self.lbl_firm_address.grid(row = 6 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_address.grid(row = 6 , column = 1 , sticky = con.W)
        self.lbl_firm_gstin.grid(row = 7 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_gstin.grid(row = 7 , column = 1 , sticky = con.W)
        self.lbl_firm_pan.grid(row = 8 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_pan.grid(row = 8 , column = 1 , sticky = con.W)
        self.lbl_firm_bank.grid(row = 9 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_bank.grid(row = 9 , column = 1 , sticky = con.W)
        self.lbl_firm_ifsc.grid(row = 10 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_ifsc.grid(row = 10 , column = 1 , sticky = con.W)
        self.lbl_firm_accno.grid(row = 11 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_accno.grid(row = 11 , column = 1 , sticky = con.W)
        self.lbl_firm_upiid.grid(row = 12 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_upiid.grid(row = 12 , column = 1 , sticky = con.W)
        self.lbl_firm_upiqr_txt.grid(row = 13 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_firm_upiqr.grid(row = 13 , column = 1 , sticky = con.W)
        self.btn_firm_upiqr_brw.grid(row = 13 , column = 2)
        self.btn_firm_upiqr_vw.grid(row = 13 , column = 3 , padx = int(self.main_wdt*0.002))
        self.lbl_firm_logo_txt.grid(row = 14 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_firm_logo.grid(row = 14 , column = 1 , sticky = con.W)
        self.btn_firm_logo_brw.grid(row = 14 , column = 2)
        self.btn_firm_logo_vw.grid(row = 14 , column = 3 , padx = int(self.main_wdt*0.002))
        self.lbl_firm_photo_txt.grid(row = 15 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_firm_photo.grid(row = 15 , column = 1 , sticky = con.W)
        self.btn_firm_photo_brw.grid(row = 15 , column = 2)
        self.btn_firm_photo_vw.grid(row = 15 , column = 3 , padx = int(self.main_wdt*0.002))

        self.tree_frame.grid(row = 0 , column = 4 , rowspan = 15 , padx = int(self.main_wdt*0.01))
        self.scroll_y.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        #self.tree_header_frame.pack(anchor = con.N , side = con.LEFT , fill = con.Y)
        self.tree.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)

        self.btn_frame.grid(row = 15 , column = 4 , sticky = con.E)
        self.btn_new.grid(row = 0 , column = 0 , padx = int(self.main_wdt*0.01))
        self.btn_edit.grid(row = 0 , column = 1 , padx = int(self.main_wdt*0.01))
        self.btn_save.grid(row = 0 , column = 2 , padx = int(self.main_wdt*0.01))

        self.tree_wdt = self.tree_frame.winfo_reqwidth()-self.scroll_y.winfo_reqwidth()
        
        self.tree.column('id' , width = int(self.tree_wdt*0.15) ,minwidth = int(self.tree_wdt*0.15) , anchor = "w")
        self.tree.column('sfx' , width = int(self.tree_wdt*0.15) , minwidth = int(self.tree_wdt*0.15) , anchor = "w")
        self.tree.column('name' , width = int(self.tree_wdt*0.70) , minwidth = int(self.tree_wdt*0.70) , anchor = "w")

    def combo_entry_out(self , e):
        e.widget.select_clear()

    def file_dialog_qr(self , e):
        file = filedialog.askopenfilename(initialdir = self.others[0]+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        if file!= "":
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]
            self.lbl_firm_upiqr.config(text = text)
            self.image_qr = ImageTk.PhotoImage(Image.open(file))
        else:
            self.lbl_firm_upiqr.config(text = "")
        

    def file_dialog_logo(self , e):
        file = filedialog.askopenfilename(initialdir = self.others[0]+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        if file!= "":
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]
            self.lbl_firm_logo.config(text = text)
            self.image_logo = ImageTk.PhotoImage(Image.open(file))
        else:
            self.lbl_firm_logo.config(text = "")

    def file_dialog_photo(self , e):
        file = filedialog.askopenfilename(initialdir = self.others[0]+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        if file!= "":
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]

            self.lbl_firm_photo.config(text = text)
            self.image_photo = ImageTk.PhotoImage(Image.open(file))
        else:
            self.lbl_firm_photo.config(text = "")

    def view_qr(self , e):
        if self.image_qr != None or self.lbl_firm_upiqr.cget("text") != "":
            image_viewer(self.image_qr,"QR Code Image")
    
    def view_logo(self , e):
        if self.image_logo != None or self.lbl_firm_logo.cget("text") != "":
            image_viewer(self.image_logo,"Logo Image")

    def view_photo(self , e):
        if self.image_photo != None or self.lbl_firm_photo.cget("text") != "":
            image_viewer(self.image_photo,"Photo Image")

    def new(self , e):
        pass

    def edit(self , e):
        pass

    def save(self , e):
        pass