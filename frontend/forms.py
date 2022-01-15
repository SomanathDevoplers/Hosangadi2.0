import io
from tkinter import Text , constants as con , filedialog , ttk , messagebox as msg , StringVar , IntVar
from requests import get , post
from PIL import Image,ImageTk
import os
from base_window import base_window
from image_viewer import image_viewer



#firm_id, firm_tax, firm_name, firm_suffix, firm_email, firm_mobile, firm_website, firm_address, firm_gstin, firm_pan, firm_bank, firm_accno, firm_ifsc, insert_time, firm_upid, firm_upiqr, firm_logo, firm_photo, insert_id, update_time, update_id
class firm(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations,others , firm_form):
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , firm_form)
        
        if base == None:
            return
            
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.image_qr = None
        self.image_logo = None
        self.image_photo = None
        self.image_qr_loc = ""
        self.image_logo_loc = ""
        self.image_photo_loc = ""
        self.home_dir = others[0]
        self.ip = others[1]                                      #home dir , ipaddr 
        self.tax_check = others[2]
        self.user = others[3]
        self.selected_firm_id = -1
        self.root_frame = frames[0]

        if self.tax_check:
            self.combo_values = ["REGULAR" , "COMPOSITION"]
        else:
            self.combo_values = ["REGULAR" , "COMPOSITION" , "CASH"]
        
        self.new_state = False
        self.edit_state = False



        self.lbl_firm_tax = ttk.Label(self.main_frame , text = "Tax Method        :" , style = "window_text_medium.TLabel")
        self.lbl_firm_name = ttk.Label(self.main_frame , text = "Firm Name         :" , style = "window_text_medium.TLabel")
        self.lbl_firm_suff_txt = ttk.Label(self.main_frame , text = "Firm Suffix       :" , style = "window_text_medium.TLabel")
        self.lbl_firm_email = ttk.Label(self.main_frame , text = "Firm Email        :" , style = "window_text_medium.TLabel")
        self.lbl_firm_mob = ttk.Label(self.main_frame , text = "Firm Mobile       :" , style = "window_text_medium.TLabel")
        self.lbl_firm_web = ttk.Label(self.main_frame , text = "Firm Website      :" , style = "window_text_medium.TLabel")
        self.lbl_firm_gstin = ttk.Label(self.main_frame , text = "Firm GSTIN        :" , style = "window_text_medium.TLabel")
        self.lbl_firm_pan = ttk.Label(self.main_frame , text = "Firm PAN          :" , style = "window_text_medium.TLabel")
        self.lbl_firm_bank = ttk.Label(self.main_frame , text = "Firm Bank Name    :" , style = "window_text_medium.TLabel")
        self.lbl_firm_ifsc = ttk.Label(self.main_frame , text = "Firm Bank IFSC    :" , style = "window_text_medium.TLabel")
        self.lbl_firm_accno = ttk.Label(self.main_frame , text = "Firm Bank A/C NO  :" , style = "window_text_medium.TLabel")
        self.lbl_firm_upiid = ttk.Label(self.main_frame , text = "Firm UPI ID       :" , style = "window_text_medium.TLabel")
        self.lbl_firm_upiqr_txt = ttk.Label(self.main_frame , text = "Firm UPI QR       :" , style = "window_text_medium.TLabel")
        self.lbl_firm_logo_txt = ttk.Label(self.main_frame , text = "Firm Logo         :" , style = "window_text_medium.TLabel")
        self.lbl_firm_photo_txt = ttk.Label(self.main_frame , text = "Firm Photo        :" , style = "window_text_medium.TLabel")
        self.lbl_firm_address = ttk.Label(self.main_frame , text = "Firm Address      :" , style = "window_text_medium.TLabel")

        self.combo_tax = ttk.Combobox(self.main_frame  ,values = self.combo_values , state = con.DISABLED , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 30) 
        self.combo_tax.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_firm_name = ttk.Entry(self.main_frame  , width = 30 , state = con.DISABLED  ,font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[4], '%P'))
        #self.ent_firm_name.bind("<FocusOut>" , self.check_name)

        self.ent_firm_suff = ttk.Entry(self.main_frame  , width = 30 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[3], '%P'))
        self.ent_firm_suff.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_firm_email = ttk.Entry(self.main_frame  , width = 30 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_firm_email.bind("<FocusOut>" , self.combo_entry_out)

        self.ent_firm_mob = ttk.Entry(self.main_frame  , width = 30 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[7], '%P'))
        self.ent_firm_mob.bind("<FocusOut>" , self.combo_entry_out)

        self.ent_firm_web = ttk.Entry(self.main_frame  , width = 30 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)))
        self.ent_firm_web.bind("<FocusOut>" , self.combo_entry_out)

        self.ent_firm_address = Text(self.main_frame  , state = con.DISABLED, width = 30 , height = 4 ,  font = ('Lucida Grande' , -int(self.main_hgt*0.03)) )

        self.ent_firm_gstin = ttk.Entry(self.main_frame  , width = 30, state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) ,  validate="key", validatecommand=(validations[3], '%P'))
        self.ent_firm_gstin.bind("<FocusOut>" , self.check_gstin)

        self.ent_firm_pan = ttk.Entry(self.main_frame  , width = 30 , state = con.DISABLED,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[3], '%P'))
        self.ent_firm_pan.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_firm_bank = ttk.Entry(self.main_frame  , width = 30 , state = con.DISABLED,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)), validate="key", validatecommand=(validations[0], '%P'))
        self.ent_firm_bank.bind("<FocusOut>" , self.combo_entry_out)
        
        self.ent_firm_ifsc = ttk.Entry(self.main_frame  , width = 30 , state = con.DISABLED,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)), validate="key", validatecommand=(validations[0], '%P'))
        self.ent_firm_ifsc.bind("<FocusOut>" , self.combo_entry_out)

        self.ent_firm_accno = ttk.Entry(self.main_frame  , width = 30, state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_firm_accno.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_firm_upiid = ttk.Entry(self.main_frame  , width = 30 , state = con.DISABLED,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)))
        self.ent_firm_upiid.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_firm_upiqr = ttk.Label(self.main_frame  , width = 30 , background = "#fff", justify = con.RIGHT ,relief = con.SOLID , borderwidth = 1 , border = 1 , font = ('Lucida Grande' , -int(self.main_hgt*0.03)))
        self.btn_firm_upiqr_brw = ttk.Button(self.main_frame , state = con.DISABLED, text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_qr(None))
        self.btn_firm_upiqr_brw.bind("<Return>" , self.file_dialog_qr)
        self.btn_firm_upiqr_vw = ttk.Button(self.main_frame  , state = con.DISABLED, text = "View" , style = "window_btn_medium.TButton" ,command = lambda : self.view_qr(None))
        self.btn_firm_upiqr_vw.bind("<Return>" , self.view_qr)
        
        self.lbl_firm_logo = ttk.Label(self.main_frame  , width = 30 , style = "window_lbl_ent.TLabel")
        self.btn_firm_logo_brw = ttk.Button(self.main_frame , state = con.DISABLED, text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_logo(None))
        self.btn_firm_logo_brw.bind("<Return>" , self.file_dialog_logo)
        self.btn_firm_logo_vw = ttk.Button(self.main_frame , state = con.DISABLED, text = "View" , style = "window_btn_medium.TButton" ,command = lambda : self.view_logo(None))
        self.btn_firm_logo_vw.bind("<Return>" , self.view_logo)

        self.lbl_firm_photo = ttk.Label(self.main_frame  , width = 30, style = "window_lbl_ent.TLabel")
        self.btn_firm_photo_brw = ttk.Button(self.main_frame , state = con.DISABLED, text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_photo(None))
        self.btn_firm_photo_brw.bind("<Return>" , self.file_dialog_photo)
        self.btn_firm_photo_vw = ttk.Button(self.main_frame , state = con.DISABLED, text = "View" , style = "window_btn_medium.TButton" ,command = lambda : self.view_photo(None))
        self.btn_firm_photo_vw.bind("<Return>" , self.view_photo)

        

        if root.winfo_screenheight()>1000:
            self.tree_frame = ttk.Frame(self.main_frame , height = int(self.main_hgt*0.865) , width = int(self.main_wdt*0.45) , style = "root_menu.TFrame")
        else:
            self.tree_frame = ttk.Frame(self.main_frame , height = int(self.main_hgt*0.871) , width = int(self.main_wdt*0.45) , style = "root_menu.TFrame")
        self.tree_frame.pack_propagate(False)
        self.tree_frame.grid_propagate(False)

        #self.tree_header_frame = ttk.Frame(self.tree_frame)

        self.tree = ttk.Treeview(self.tree_frame ,selectmode = "browse", takefocus = True , show = "headings" , style = "window.Treeview" )
        self.tree.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.scroll_y = ttk.Scrollbar(self.tree_frame , orient = con.VERTICAL , command = self.tree.yview)
        self.scroll_x = ttk.Scrollbar(self.tree_frame , orient = con.HORIZONTAL , command = self.tree.xview)
        self.tree.config(yscrollcommand = self.scroll_y.set , xscrollcommand = self.scroll_x.set)

        

        self.tree['columns'] = ('id','sfx','name')
        self.tree.heading('id' , text = 'ID')
        self.tree.heading('sfx' , text = 'Sfx')
        self.tree.heading('name' , text = 'name')

        self.tree.bind('<Double-Button-1>',self.select_tree)
        self.tree.bind('<Return>',self.select_tree)
        #self.tree['show'] = 'headings'


        """for i in range(100):
            if i%2 == 0:
                self.tree.insert('','end' ,tags=('a',), values = ("SMS"+str(i) , "Vijay" , "Somanath Stores" ))
            else:
                self.tree.insert('','end' ,tags=('b',), values = ("SMS"+str(i) , "Vijay", "Somanath Stores" ))"""

        self.btn_frame = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.btn_new = ttk.Button(self.btn_frame , text = "New" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.new(None))
        self.btn_new.bind("<Return>" , self.new) 
        self.btn_edit = ttk.Button(self.btn_frame ,state = con.DISABLED ,  text = "Edit" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.edit(None))
        self.btn_edit.bind("<Return>" , self.edit)
        self.btn_save = ttk.Button(self.btn_frame , state = con.DISABLED, text = "Save" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.save(None))
        self.btn_save.bind("<Return>" , self.save)
        self.btn_refresh = ttk.Button(self.btn_frame , text = "Refresh" , width = 7 , style = "window_btn_medium.TButton" ,command = lambda : self.refresh(None))
        self.btn_refresh.bind("<Return>" , self.refresh)
        self.btn_cancel = ttk.Button(self.btn_frame , state = con.DISABLED, text = "Cancel" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.cancel(None))
        self.btn_cancel.bind("<Return>" , self.cancel)


        self.lbl_firm_tax.grid(row = 0 , column = 0 , pady = int(self.main_hgt*0.01))
        self.combo_tax.grid(row = 0 , column = 1 )
        self.lbl_firm_name.grid(row = 1 , column = 0 , pady = int(self.main_hgt*0.012))
        self.ent_firm_name.grid(row = 1 , column = 1 , sticky = con.W)
        self.lbl_firm_suff_txt.grid(row = 2 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_suff.grid(row = 2 , column = 1 , sticky = con.W)
        self.lbl_firm_email.grid(row = 3 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_email.grid(row = 3 , column = 1 , sticky = con.W)
        self.lbl_firm_mob.grid(row = 4 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_mob.grid(row = 4 , column = 1 , sticky = con.W)
        self.lbl_firm_web.grid(row = 5 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_web.grid(row = 5 , column = 1 , sticky = con.W)
        self.lbl_firm_gstin.grid(row = 6 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_gstin.grid(row = 6 , column = 1 , sticky = con.W)
        self.lbl_firm_pan.grid(row = 7 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_pan.grid(row = 7 , column = 1 , sticky = con.W)
        self.lbl_firm_bank.grid(row = 8 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_bank.grid(row = 8 , column = 1 , sticky = con.W)
        self.lbl_firm_ifsc.grid(row = 9 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_ifsc.grid(row = 9 , column = 1 , sticky = con.W)
        self.lbl_firm_accno.grid(row = 10 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_accno.grid(row = 10 , column = 1 , sticky = con.W)
        self.lbl_firm_upiid.grid(row = 11 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_upiid.grid(row = 11 , column = 1 , sticky = con.W)
        self.lbl_firm_upiqr_txt.grid(row = 12 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_firm_upiqr.grid(row = 12 , column = 1 , sticky = con.W)
        self.btn_firm_upiqr_brw.grid(row = 12 , column = 2)
        self.btn_firm_upiqr_vw.grid(row = 12 , column = 3 , padx = int(self.main_wdt*0.002))
        self.lbl_firm_logo_txt.grid(row = 13 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_firm_logo.grid(row = 13 , column = 1 , sticky = con.W)
        self.btn_firm_logo_brw.grid(row = 13 , column = 2)
        self.btn_firm_logo_vw.grid(row = 13 , column = 3 , padx = int(self.main_wdt*0.002))
        self.lbl_firm_photo_txt.grid(row = 14 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_firm_photo.grid(row = 14 , column = 1 , sticky = con.W)
        self.btn_firm_photo_brw.grid(row = 14 , column = 2)
        self.btn_firm_photo_vw.grid(row = 14 , column = 3 , padx = int(self.main_wdt*0.002))
        self.lbl_firm_address.grid(row = 15 , column = 0 , pady = int(self.main_hgt*0.01))
        self.ent_firm_address.grid(row = 15 , column = 1 , sticky = con.W)
        


        self.tree_frame.grid(row = 0 , column = 4 , rowspan = 16 , padx = int(self.main_wdt*0.01))
        self.scroll_y.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        #self.tree_header_frame.pack(anchor = con.N , side = con.LEFT , fill = con.Y)
        self.tree.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)

        self.btn_frame.grid(row = 16 , column = 4 , sticky = con.E)
        self.btn_new.grid(row = 0 , column = 0 , padx = int(self.main_wdt*0.01))
        self.btn_edit.grid(row = 0 , column = 1 , padx = int(self.main_wdt*0.01))
        self.btn_save.grid(row = 0 , column = 2 , padx = int(self.main_wdt*0.01))
        self.btn_refresh.grid(row = 0 , column = 3 , padx = int(self.main_wdt*0.01))

        self.tree_wdt = self.tree_frame.winfo_reqwidth()-self.scroll_y.winfo_reqwidth()
        
        self.tree.column('id' , width = int(self.tree_wdt*0.15) ,minwidth = int(self.tree_wdt*0.15) , anchor = "w")
        self.tree.column('sfx' , width = int(self.tree_wdt*0.15) , minwidth = int(self.tree_wdt*0.15) , anchor = "w")
        self.tree.column('name' , width = int(self.tree_wdt*0.70) , minwidth = int(self.tree_wdt*0.70) , anchor = "w")

        self.btn_new.focus_set()
        self.firm_list()

    def combo_entry_out(self , e):
        e.widget.select_clear()

    def file_dialog_qr(self , e):
        file = filedialog.askopenfilename(initialdir = self.home_dir[0]+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        
        if file!= "":
            ext = file.split(".")[-1]
            if ext != 'jpg' and ext != 'png' and ext != 'jpeg' and ext != 'bmp':
                msg.showerror("error","Select only images \n (eg :- *.png or *.jpg or *.bmp or *.jpeg)")
                return
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]
            self.lbl_firm_upiqr.config(text = text)
            self.image_qr = ImageTk.PhotoImage(Image.open(file))
        else:
            self.lbl_firm_upiqr.config(text = "")

        self.image_qr_loc = file
        
    def file_dialog_logo(self , e):
        file = filedialog.askopenfilename(initialdir = self.home_dir[0]+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        
        if file!= "":
            ext = file.split(".")[-1]
            if ext != 'jpg' and ext != 'png' and ext != 'jpeg' and ext != 'bmp':
                msg.showerror("error","Select only images \n (eg :- *.png or *.jpg or *.bmp or *.jpeg)")
                return
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]
            self.lbl_firm_logo.config(text = text)
            self.image_logo = ImageTk.PhotoImage(Image.open(file))
        else:
            self.lbl_firm_logo.config(text = "")
        
        self.image_logo_loc = file
            
    def file_dialog_photo(self , e):
        file = filedialog.askopenfilename(initialdir = self.home_dir[0]+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        
        if file!= "":   
            ext = file.split(".")[-1]
            if ext != 'jpg' and ext != 'png' and ext != 'jpeg' and ext != 'bmp':
                msg.showerror("error","Select only images \n (eg :- *.png or *.jpg or *.bmp or *.jpeg)")
                return
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]

            self.image_photo = ImageTk.PhotoImage(Image.open(file))
            self.lbl_firm_photo.config(text = text)
        else:
            self.lbl_firm_photo.config(text = "")

        self.image_photo_loc = file
            
    def view_qr(self , e):
        if self.image_qr != None and self.lbl_firm_upiqr.cget("text") != "":
            image_viewer(self.image_qr_loc,"Logo" ,  self.root_frame)
    
    def view_logo(self , e):
        if self.image_logo != None and self.lbl_firm_logo.cget("text") != "":
            image_viewer(self.image_logo_loc,"Logo" ,  self.root_frame)

    def view_photo(self , e):
        if self.image_photo != None and self.lbl_firm_photo.cget("text") != "":
            image_viewer(self.image_photo_loc,"Photo" , self.root_frame )

    def new(self , e):
        self.btn_new.config(state = con.DISABLED)
        self.btn_edit.config(state = con.DISABLED)
        self.btn_save.config(state = con.NORMAL)
        self.btn_cancel.config(state = con.NORMAL)

        self.new_state = True
        self.edit_state = False

        self.enable_all()
        self.clear_all()

        self.combo_tax.focus_set()

    def edit(self , e):
        self.btn_new.config(state = con.DISABLED)
        self.btn_edit.config(state = con.DISABLED)
        self.btn_save.config(state = con.NORMAL)
        self.btn_cancel.config(state = con.NORMAL)

        self.new_state = False
        self.edit_state = True

        img_qr = self.lbl_firm_upiqr.cget("text")
        img_photo = self.lbl_firm_photo.cget("text")
        img_logo = self.lbl_firm_logo.cget("text")

        firm_dir = os.path.join(os.path.expanduser('~'),"Images" , "firms")                                                     #delete all older firm images in the folder

        for f in os.listdir(firm_dir):
            os.remove(os.path.join(firm_dir, f))
    

        if img_qr != "":
            self.image_qr_loc = os.path.join(firm_dir , "qr." + img_qr.split(".")[-1])
            imgpil = ImageTk.getimage(self.image_qr)
            imgpil.save( self.image_qr_loc , img_qr.split(".")[-1])

        if img_photo != "":
            self.image_photo_loc = os.path.join(firm_dir , "photo." + img_photo.split(".")[-1])
            imgpil = ImageTk.getimage(self.image_photo)
            imgpil.save( self.image_photo_loc , img_photo.split(".")[-1])
        
        if img_logo != "":
            self.image_logo_loc = os.path.join(firm_dir , "logo." + img_logo.split(".")[-1])
            imgpil = ImageTk.getimage(self.image_logo)
            imgpil.save( self.image_logo_loc , img_logo.split(".")[-1])


        self.enable_all()
        self.ent_firm_name.focus_set()

    def save(self , e):  
        tax_method = self.combo_tax.get()
        firm_name = self.ent_firm_name.get().upper()
        firm_suffix = self.ent_firm_suff.get().upper()
        firm_email = self.ent_firm_email.get()
        firm_mobile = self.ent_firm_mob.get()
        firm_website = self.ent_firm_web.get()
        firm_address = self.ent_firm_address.get(0.0 , 10.30).upper()
        firm_gst = self.ent_firm_gstin.get().upper()
        firm_pan = self.ent_firm_pan.get().upper()
        firm_bank = self.ent_firm_bank.get().upper()
        firm_ifsc = self.ent_firm_ifsc.get().upper()
        firm_acno = self.ent_firm_accno.get().upper()
        firm_upiid = self.ent_firm_upiid.get()

        if tax_method == "CASH":
            firm_gst = "" 
            
        if tax_method == "" or tax_method not in self.combo_values:
            msg.showinfo("Info" , "Select tax method")
            return

        if firm_name == "":
            msg.showinfo("Info" , "Add firm Name")
            return

        if len(firm_suffix) != 3:
            msg.showinfo("Info" , "Firm Suffix must be 3 characters")
            self.ent_firm_suff.select_range(0,con.END)
            self.ent_firm_suff.focus_set()
            return

        if tax_method != "CASH" and (firm_gst == "" or firm_pan == ""):
            msg.showinfo("Info" , "GST and PAN no cannot be empty")
            self.ent_firm_gstin.select_range(0,con.END)
            self.ent_firm_gstin.focus_set()
            return

        

        if tax_method == "REGULAR":
            tax_method = "REGU"
        
        if tax_method == "COMPOSITION":
            tax_method = "COMP"

        

        parameters = {
            "firm_id" : "" , 
            "user_name" : self.user ,
            "firm_type" : tax_method ,
            "firm_name" : firm_name , 
            "firm_suffix" : firm_suffix ,
            "firm_email" : firm_email ,
            "firm_mobile" : firm_mobile ,
            "firm_website" : firm_website ,
            "firm_address" : firm_address ,
            "firm_gst" :  firm_gst,
            "firm_pan" :  firm_pan,
            "firm_bank" :  firm_bank ,
            "firm_ifsc" :  firm_ifsc ,
            "firm_acno" :  firm_acno,
            "firm_upiid" : firm_upiid,
            "firm_qr" : False , 
            "firm_logo" : False , 
            "firm_photo" : False ,
            }

        files = []


        if self.image_qr_loc != "":
            original = Image.open(self.image_qr_loc)
            temp = self.image_qr_loc.split(".")
            type = temp[-1]

            if type != "png":
                temp.pop(len(temp)-1)
                
                self.image_qr_loc = os.path.join(self.home_dir , "Images" , "tempImages" , "qr.png")
                original.save(self.image_qr_loc , format = "png")

            files.append(('images', (self.image_qr_loc, open(self.image_qr_loc, 'rb'), 'images/png')))
            parameters['firm_qr'] = True



        if self.image_logo_loc != "":
            original = Image.open(self.image_logo_loc)
            temp = self.image_logo_loc.split(".")
            type = temp[-1]

            if type != "png":
                temp.pop(len(temp)-1)
                
                self.image_logo_loc = os.path.join(self.home_dir , "Images" , "tempImages" , "logo.png")
                original.save(self.image_logo_loc , format = "png")

            files.append(('images', (self.image_logo_loc, open(self.image_logo_loc, 'rb'), 'image/png')))
            parameters['firm_logo'] = True

        if self.image_photo_loc != "":
            original = Image.open(self.image_photo_loc)
            temp = self.image_photo_loc.split(".")
            type = temp[-1]

            if type != "png":
                temp.pop(len(temp)-1)
                self.image_photo_loc = os.path.join(self.home_dir , "Images" , "tempImages" , "photo.png")
                original.save(self.image_photo_loc , format = "png")

            files.append(('images', (self.image_photo_loc, open(self.image_photo_loc, 'rb'), 'image/png')))
            parameters['firm_photo'] = True


        
        if self.edit_state:
            parameters['firm_id'] = self.selected_firm_id  

        req = post("http://"+self.ip+":6000/firms/Save" , params = parameters , files = files) 
            
                                                                                                   
                                                      
        if req.status_code == 201:
            msg.showerror("Error" , "One of these columns is not unique : \n\t1.Firm Name \n\t2.Firm Suffix \n\t3.Firm GSTIN \n\t4.Firm PAN")
            return

        
                

            
        


        self.clear_all()
        self.disable_all()
        self.firm_list()
        self.btn_cancel.config(state = con.DISABLED)
        self.btn_new.config(state = con.NORMAL)
        self.btn_save.config(state = con.DISABLED)
        self.btn_edit.config(state = con.DISABLED)
        
    def cancel(self , e):
        self.btn_new.config(state = con.NORMAL)
        self.btn_edit.config(state = con.DISABLED)
        self.btn_save.config(state = con.DISABLED)
        self.btn_cancel.config(state = con.DISABLED)

        self.clear_all()
        self.disable_all()

        self.new_state = False
        self.edit_state = False

    def refresh(self,e):
        self.firm_list()

    def enable_all(self):
        self.combo_tax.config(state = con.NORMAL)
        self.ent_firm_name.config(state = con.NORMAL)
        self.ent_firm_suff.config(state = con.NORMAL)
        self.ent_firm_email.config(state = con.NORMAL)
        self.ent_firm_mob.config(state = con.NORMAL)
        self.ent_firm_web.config(state = con.NORMAL)
        self.ent_firm_address.config(state = con.NORMAL)
        self.ent_firm_gstin.config(state = con.NORMAL)
        self.ent_firm_pan.config(state = con.NORMAL)
        self.ent_firm_bank.config(state = con.NORMAL)
        self.ent_firm_ifsc.config(state = con.NORMAL)
        self.ent_firm_accno.config(state = con.NORMAL)
        self.ent_firm_upiid.config(state = con.NORMAL)
        self.btn_firm_upiqr_brw.config(state = con.NORMAL)
        self.btn_firm_upiqr_vw.config(state = con.NORMAL)
        self.btn_firm_logo_brw.config(state = con.NORMAL)
        self.btn_firm_logo_vw.config(state = con.NORMAL)
        self.btn_firm_photo_brw.config(state = con.NORMAL)
        self.btn_firm_photo_vw.config(state = con.NORMAL)
    
    def disable_all(self):
        self.combo_tax.config(state = con.DISABLED)
        self.ent_firm_name.config(state = con.DISABLED)
        self.ent_firm_suff.config(state = con.DISABLED)
        self.ent_firm_email.config(state = con.DISABLED)
        self.ent_firm_mob.config(state = con.DISABLED)
        self.ent_firm_web.config(state = con.DISABLED)
        self.ent_firm_address.config(state = con.DISABLED)
        self.ent_firm_gstin.config(state = con.DISABLED)
        self.ent_firm_pan.config(state = con.DISABLED)
        self.ent_firm_bank.config(state = con.DISABLED)
        self.ent_firm_ifsc.config(state = con.DISABLED)
        self.ent_firm_accno.config(state = con.DISABLED)
        self.ent_firm_upiid.config(state = con.DISABLED)
        self.btn_firm_upiqr_brw.config(state = con.DISABLED)
        self.btn_firm_upiqr_vw.config(state = con.DISABLED)
        self.btn_firm_logo_brw.config(state = con.DISABLED)
        self.btn_firm_logo_vw.config(state = con.DISABLED)
        self.btn_firm_photo_brw.config(state = con.DISABLED)
        self.btn_firm_photo_vw.config(state = con.DISABLED)

    def clear_all(self):
        self.combo_tax.delete(0,con.END)
        self.ent_firm_name.delete(0,con.END)
        self.ent_firm_suff.delete(0,con.END)
        self.ent_firm_email.delete(0,con.END)
        self.ent_firm_mob.delete(0,con.END)
        self.ent_firm_web.delete(0,con.END)
        self.ent_firm_address.delete(0.0,10.100)
        self.ent_firm_gstin.delete(0,con.END)
        self.ent_firm_pan.delete(0,con.END)
        self.ent_firm_bank.delete(0,con.END)
        self.ent_firm_ifsc.delete(0,con.END)
        self.ent_firm_accno.delete(0,con.END)
        self.ent_firm_upiid.delete(0,con.END)
        self.lbl_firm_upiqr.config(text = "")
        self.lbl_firm_logo.config(text = "")
        self.lbl_firm_photo.config(text = "")

        self.selected_firm_id = -1
        self.image_qr_loc = ""
        self.image_logo_loc = ""
        self.image_photo_loc = ""

    def firm_list(self):
        req = get("http://"+self.ip+":6000/firms/getFirmList" , params = {"tax_check" : self.tax_check})
        
        for each in self.tree.get_children():
            self.tree.delete(each)

        if req.status_code == 200:
            resp = req.json()
            tag_index = 0
            for each in resp:
                if tag_index%2:
                    tag = 'a'
                else:
                    tag = 'b'
                tag_index += 1
                self.tree.insert('','end' ,tags=(tag,), values = (each['firm_id'] , each['firm_suffix'] , each['firm_name']))

    def select_tree(self , e):
        
        self.btn_firm_upiqr_vw.config(state = con.DISABLED)
        self.btn_firm_photo_vw.config(state = con.DISABLED)
        self.btn_firm_logo_vw.config(state = con.DISABLED)
        self.btn_new.config(state = con.NORMAL)

        try:
            cur_item = self.tree.focus()
            cur_item = self.tree.item(cur_item)
            cur_item = cur_item['values']

            req = get("http://"+self.ip+":6000/firms/getSelectedFirm" , params = {"firm_id" : cur_item[0]})
            
            if req.status_code == 200:
                
                resp = req.json()[0]
                
                self.enable_all()
                self.clear_all()
                
                if resp['firm_tax'] == "REGU":
                    self.combo_tax.insert(0 , "REGULAR")
                
                elif resp['firm_tax'] == "CASH":
                    self.combo_tax.insert(0 , "CASH")
                
                else:
                    self.combo_tax.insert(0 , "COMPOSITION")

                self.ent_firm_name.insert(0 , resp['firm_name'])
                self.ent_firm_suff.insert(0 , resp['firm_suffix'])
                self.ent_firm_email.insert(0 , resp['firm_email'])
                self.ent_firm_mob.insert(0 , resp['firm_mobile'])
                self.ent_firm_web.insert(0 , resp['firm_website'])
                self.ent_firm_address.insert(0.0 , resp['firm_address'])
                self.ent_firm_gstin.insert(0 , resp['firm_gstin'])
                self.ent_firm_pan.insert(0 , resp['firm_pan'])
                self.ent_firm_bank.insert(0 , resp['firm_bank'])
                self.ent_firm_ifsc.insert(0 , resp['firm_ifsc'])
                self.ent_firm_accno.insert(0 , resp['firm_accno'])
                self.ent_firm_upiid.insert(0 , resp['firm_upid'])
                
                self.disable_all()

                if resp['firm_upiqr'] == 'True':
                    self.lbl_firm_upiqr.config(text = "qr.png")
                    file = get("http://"+self.ip+":6000/images/firms/"+str(cur_item[0])+"/qr.png")
                    self.image_qr = ImageTk.PhotoImage(Image.open(io.BytesIO(file.content)))
                    #self.btn_firm_upiqr_vw.config(state = con.NORMAL)
                
                if resp['firm_logo'] == 'True':
                    self.lbl_firm_logo.config(text = "logo.png")
                    file = get("http://"+self.ip+":6000/images/firms/"+str(cur_item[0])+"/logo.png")
                    self.image_logo = ImageTk.PhotoImage(Image.open(io.BytesIO(file.content)))
                    #self.btn_firm_logo_vw.config(state = con.NORMAL)
                
                if resp['firm_photo'] == 'True':
                    self.lbl_firm_photo.config(text = "photo.png")
                    file = get("http://"+self.ip+":6000/images/firms/"+str(cur_item[0])+"/photo.png")
                    self.image_photo = ImageTk.PhotoImage(Image.open(io.BytesIO(file.content)))
                    #self.btn_firm_photo_vw.config(state = con.NORMAL)

                self.btn_edit.config(state = con.NORMAL)
                self.selected_firm_id = resp['firm_id']
                
        except IndexError:
            pass

    def check_name(self, e):
        self.ent_firm_name.select_clear()
        name = self.ent_firm_name.get().upper()
        temp = name.split()
        name = ""

        i = 0
        for each in temp:
            if i == 0:
                name += each
            else:
                name += " "+each
            i+=1

        
        sql = "select firm_name from somanath.firms where firm_name = '"+ name +"'"
        
        if not self.new_state:
            sql += " and firm_id != "+ str(self.selected_firm_id)
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            if len(req.json())>0:
                msg.showinfo("Error" , "This firm name exists")
                self.ent_firm_name.select_range(0 , con.END)
                self.ent_firm_name.focus_set()
                self.btn_refresh.invoke()
                return


        self.ent_firm_name.delete(0,con.END)
        self.ent_firm_name.insert(0,name)
       
    def check_gstin(self, e):
        self.ent_firm_gstin.select_clear()
        tax = self.combo_tax.get()
        if  tax != "REGULAR" and tax != "COMPOSITION":
           return
        gstin = self.ent_firm_gstin.get().upper()
        gstin = gstin.split()[0]
        if len(gstin)!= 15:
           msg.showerror("Info" , "GSTIN MUST BE 15 CHARECTARS")
           self.ent_firm_gstin.select_from(0,con.END)
           self.ent_firm_gstin.focus_set()
           return
        self.ent_firm_pan.delete(0,con.END)
        self.ent_firm_pan.insert(0,gstin[2:12])
        self.ent_firm_gstin.delete(0,con.END)
        self.ent_firm_gstin.insert(0,gstin)









class taxes(base_window):  
    def __init__(self , root ,frames , dmsn , lbls ,title,validations,ip,user , tax_form):
        
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , tax_form)
        if base == None:
            return
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.rad_tax = StringVar()
        self.ip = ip
        self.user = user
        self.edit_state = False
        self.selected_tax = -1
        
        self.lbl_tax_type = ttk.Label(self.main_frame , text = "Tax Type         :" , style = "window_text_medium.TLabel")
        self.lbl_tax_per = ttk.Label(self.main_frame , text = "Tax Percentage   :" , style = "window_text_medium.TLabel")
        
        self.ent_tax_per = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'),state='disabled')
        self.ent_tax_per.bind("<FocusOut>" , self.combo_entry_out)
        self.rad_tax_gst = ttk.Radiobutton(self.main_frame , variable = self.rad_tax , value = 0 , style = "window_radio.TRadiobutton" , text = "GST")
        self.rad_tax_cess = ttk.Radiobutton(self.main_frame , variable = self.rad_tax , value = 1 , style = "window_radio.TRadiobutton" , text = "CESS")



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
        self.tree.bind('<Double-Button-1>',self.select_tree)
        self.tree.bind('<Return>',self.select_tree)

        """for i in range(100):
            if i%2 == 0:
                self.tree.insert('','end' ,tags=('a',), values = ("SMS"+str(i) , "Vijay" , "Somanath Stores" ))
            else:
                self.tree.insert('','end' ,tags=('b',), values = ("SMS"+str(i) , "Vijay", "Somanath Stores" ))"""

        self.btn_frame = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.btn_new = ttk.Button(self.btn_frame , text = "New" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.new(None))
        self.btn_new.bind("<Return>" , self.new) 
        self.btn_edit = ttk.Button(self.btn_frame , state  = con.DISABLED , text = "Edit" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.edit(None))
        self.btn_new.bind("<Return>" , self.edit)
        self.btn_save = ttk.Button(self.btn_frame , state = con.DISABLED , text = "Save" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.save(None))
        self.btn_save.bind("<Return>" , self.save)
        self.btn_refresh = ttk.Button(self.btn_frame , text = "Refresh" , width = 7 , style = "window_btn_medium.TButton" ,command = lambda : self.refresh(None))
        self.btn_refresh.bind("<Return>" , self.refresh)

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
        self.btn_refresh.grid(row = 0 , column = 3 , padx = int(self.main_wdt*0.01))

        self.tree_wdt = self.tree_frame.winfo_reqwidth()-self.scroll_y.winfo_reqwidth()
        
        self.tree.column('id' , width = int(self.tree_wdt*0.15) ,minwidth = int(self.tree_wdt*0.15) , anchor = "w")
        self.tree.column('type' , width = int(self.tree_wdt*0.15) , minwidth = int(self.tree_wdt*0.15) , anchor = "w")
        self.tree.column('per' , width = int(self.tree_wdt*0.70) , minwidth = int(self.tree_wdt*0.70) , anchor = "w")
        
        self.get_tax_list()

    def new(self , e):
        self.ent_tax_per.configure(state="normal")
        self.ent_tax_per.delete(0,'end')
        self.btn_new["state"]='disabled'
        self.btn_edit["state"]='disabled'
        self.btn_save["state"]='enable'
        self.ent_tax_per.focus_set()
        self.edit_state = False
        self.rad_tax_cess.config(state = con.NORMAL)
        self.rad_tax_gst.config(state = con.NORMAL)
        self.selected_tax = -1
        self.rad_tax.set('3')
        
    def edit(self , e):
        self.ent_tax_per.configure(state="normal")
        self.btn_new["state"]='disabled'
        self.btn_edit["state"]='disabled'
        self.btn_save["state"]='enable'
        self.edit_state = True
        self.ent_tax_per.focus_set()

    def get_tax_list(self):
        req = get("http://"+self.ip+":6000/taxes/getTaxList")
        for each in self.tree.get_children():
            self.tree.delete(each)

        if req.status_code == 200:
            resp = req.json()
            tag_index = 0
            for each in resp:
                if tag_index%2:
                    tag = 'a'
                else:
                    tag = 'b'
                tag_index += 1
                if each['tax_type']=="0":x="GST"
                else:x="CESS"
                self.tree.insert('','end' ,tags=(tag,), values = (each['tax_id'] , x , each['tax_per']))
        
    def save(self , e):
        tax_per = self.ent_tax_per.get()
        if tax_per == "":
            msg.showinfo("Info" , "Add Tax percentage")
            return

        tax_type = self.rad_tax.get()
        if tax_type not in ('0','1'):
            msg.showinfo("Info", "Select GST/CESS")
            return

        parameters = {
        "tax_per"   : tax_per ,
        "tax_type"  : tax_type,
        "user_name" : self.user ,
        "tax_id"    : ""
        }


    
        
        
    
        if self.edit_state:
            parameters['tax_id'] = self.selected_tax
            

        req = post("http://"+self.ip+":6000/taxes/save" , params = parameters )
        
        if req.status_code == 201:
            msg.showinfo("Info","Entered value exist")
            self.ent_tax_per.select_range(0,con.END)
            self.ent_tax_per.focus_set()
            self.btn_refresh.invoke()
            return

        self.ent_tax_per.delete(0, 'end')
        self.ent_tax_per.config(state=con.DISABLED)
        self.btn_new.config(state = con.NORMAL)
        self.btn_edit.config(state=con.DISABLED)
        self.btn_save.config(state=con.DISABLED)
        self.rad_tax_cess.config(state=con.DISABLED)
        self.rad_tax_gst.config(state=con.DISABLED)
        self.get_tax_list()
        self.edit_state = False

    def refresh(self,e):
        self.get_tax_list()

    def combo_entry_out(self , e):
        e.widget.select_clear()
       
    def select_tree(self , e):
        self.btn_new["state"]='enable'
        self.btn_edit["state"]='enable'
        self.btn_save["state"]='disabled'
        try:
            cur_item = self.tree.focus()
            cur_item = self.tree.item(cur_item)
            cur_item = cur_item['values']
            self.selected_tax = cur_item[0]
            req = get("http://"+self.ip+":6000/taxes/getSelectedTax" , params = { "tax_id" : cur_item[0]})
            if req.status_code == 200:
                resp = req.json()[0]
                self.ent_tax_per.config(state=con.NORMAL)
                self.ent_tax_per.delete(0, 'end')
                self.ent_tax_per.insert(0,resp['tax_per'])
                self.ent_tax_per.config(state=con.DISABLED)
                
                if resp['tax_type'] == '0':
                    self.rad_tax.set(0)
                else:
                    self.rad_tax.set(1)

                self.rad_tax_cess.config(state = con.DISABLED)
                self.rad_tax_gst.config(state = con.DISABLED)

        except IndexError:
            self.btn_new["state"]='enable'
            self.btn_edit["state"]='disabled'









class categories(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations,others , cat_from):
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , cat_from)
        if base == None:
            return
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.homeDir = others[0]
        self.image_cat = None
        self.image_cat_loc = None
        self.edit_state = False
        self.new_state = False
        self.ip = others[1]
        self.user = others[2]
        self.selected_cat_id = -1
        self.root_frame = frames[0]



        self.lbl_cat_name = ttk.Label(self.main_frame , text = "Category Name    :" , style = "window_text_medium.TLabel")
        self.ent_cat_name = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_cat_name.bind("<FocusOut>" , self.check_name)
        self.ent_cat_name.config(state=con.DISABLED)
        self.lbl_cat_txt = ttk.Label(self.main_frame , text = "Category Image   :" , style = "window_text_medium.TLabel")
        self.lbl_cat_img = ttk.Label(self.main_frame  , width = 30 , style = "window_lbl_ent.TLabel")

        self.btn_cat_img_brw = ttk.Button(self.main_frame , text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_cat(None))
        self.btn_cat_img_brw.bind("<Return>" , self.file_dialog_cat)
        self.btn_cat_img_brw.config(state=con.DISABLED)
        self.btn_cat_img_view = ttk.Button(self.main_frame , text = "View" , style = "window_btn_medium.TButton" ,command = lambda : self.view_cat(None))
        self.btn_cat_img_view.bind("<Return>" , self.view_cat)
        self.btn_cat_img_view.config(state=con.DISABLED)
        

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
        self.tree.bind('<Double-Button-1>',self.select_tree)
        self.tree.bind('<Return>',self.select_tree)

        self.btn_frame = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.btn_new = ttk.Button(self.btn_frame , text = "New" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.new(None))
        self.btn_new.config(state = con.NORMAL)
        self.btn_new.bind("<Return>" , self.new) 
        self.btn_edit = ttk.Button(self.btn_frame , text = "Edit" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.edit(None))
        self.btn_edit.bind("<Return>" , self.edit)
        self.btn_edit.config(state = con.DISABLED)
        self.btn_save = ttk.Button(self.btn_frame , text = "Save" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.save(None))
        self.btn_save.bind("<Return>" , self.save)
        self.btn_refresh = ttk.Button(self.btn_frame , text = "Refresh" , width = 7 , style = "window_btn_medium.TButton" ,command = lambda : self.refresh(None))
        self.btn_refresh.bind("<Return>" , self.refresh)
        self.btn_save.config(state = con.DISABLED)

    
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
        self.btn_refresh.grid(row = 0 , column = 3 , padx = int(self.main_wdt*0.01))

        self.tree_wdt = self.tree_frame.winfo_reqwidth()-self.scroll_y.winfo_reqwidth()
        
        self.tree.column('id' , width = int(self.tree_wdt*0.2) ,minwidth = int(self.tree_wdt*0.2) , anchor = "w")
        self.tree.column('name' , width = int(self.tree_wdt*0.8) , minwidth = int(self.tree_wdt*0.6) , anchor = "w")
        
        self.get_cat_list()

    def new(self , e):
        self.btn_new.config(state=con.DISABLED)
        self.btn_edit.config(state=con.DISABLED)
        self.btn_save.config(state=con.NORMAL)
       
        self.selected_cat_id = -1
        self.edit_state = False
        self.new_state = True
        
        self.enable_all()
        self.clear_all()
        self.ent_cat_name.focus_set()

    def edit(self , e):
        self.btn_new.config(state=con.DISABLED)
        self.btn_edit.config(state=con.DISABLED)
        self.btn_save.config(state=con.NORMAL)

        self.edit_state = True
        self.new_state = False
        

        cat_img = self.lbl_cat_img.cget("text")

        cat_dir = os.path.join(os.path.expanduser('~'),"Images" , "categories")                                                     #delete all older firm images in the folder

        for f in os.listdir(cat_dir):
            os.remove(os.path.join(cat_dir, f))

        if cat_img != "":
            self.image_cat_loc = os.path.join(cat_dir , "photo." + cat_img.split(".")[-1])
            imgpil = ImageTk.getimage(self.image_cat)
            imgpil.save( self.image_cat_loc , cat_img.split(".")[-1])

        self.enable_all()
        self.ent_cat_name.focus_set()
    
    def get_cat_list(self):
        req = get("http://"+self.ip+":6000/cat/getCatList")
        for each in self.tree.get_children():
            self.tree.delete(each)

        if req.status_code == 200:
            resp = req.json()
            tag_index = 0
            for each in resp:
                if tag_index%2:
                    tag = 'a'
                else:
                    tag = 'b'
                tag_index += 1
                self.tree.insert('','end' ,tags=(tag,), values = (each['cat_id'] ,each['cat_name']))
        
    def save(self , e):
        cat_name = self.ent_cat_name.get().upper()

        if cat_name == '':
            msg.showinfo("Info", "Enter Category name")
            self.ent_cat_name.select_range(0,con.END)
            self.ent_cat_name.focus_set()
            return
        

        
        files = []            

        parameters = {
                    'cat_id': "",
                    'cat_name' : cat_name,
                    'user_name':self.user,
                    'cat_image':False 
                }


            
        if self.image_cat_loc != "" and self.image_cat_loc != None:
            original = Image.open(self.image_cat_loc)
            temp = self.image_cat_loc.split(".")
            typeLow = temp[-1]

            if typeLow != "png":
                temp.pop(len(temp)-1)
            
            self.image_cat_loc = os.path.join(self.homeDir , "Images" , "tempImages" , "image.png")
            original.save(self.image_cat_loc , format = "png")


            files.append(('images', (self.image_cat_loc, open(self.image_cat_loc, 'rb'), 'image/png')))
            parameters['cat_image'] = True

            



        
        if self.edit_state:            
            parameters['cat_id'] = self.selected_cat_id

        req = post("http://"+self.ip+":6000/cat/save" , params = parameters , files = files)
        if req.status_code == 201:
            msg.showerror("Error" , "This Category has been added")
            return

        self.clear_all()
        self.disable_all()

        self.btn_new.config(state=con.NORMAL)
        self.btn_edit.config(state=con.DISABLED)
        self.btn_save.config(state=con.DISABLED)
        self.get_cat_list()
        self.edit_state = False
        self.new_state = False

    def refresh(self,e):
        self.get_cat_list()

    def combo_entry_out(self , e):
        e.widget.select_clear()

    def file_dialog_cat(self , e):
        file = filedialog.askopenfilename(initialdir = self.homeDir+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        if file!= "":
            ext = file.split(".")[-1]
            if ext != 'jpg' and ext != 'png' and ext != 'jpeg' and ext != 'bmp':
                msg.showerror("error","Select only images \n (eg :- *.png or *.jpg or *.bmp or *.jpeg)")
                return
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]
            self.lbl_cat_img.config(text = text)
            self.image_cat = ImageTk.PhotoImage(Image.open(file))
        else:
            self.lbl_cat_img.config(text = "")

        self.image_cat_loc = file   

    def view_cat(self , e):
        if self.image_cat != None and self.lbl_cat_img.cget("text") != "":
            image_viewer(self.image_cat_loc,"Category" , self.root_frame)

    def select_tree(self , e):
        self.btn_new.config(state=con.NORMAL)
        self.btn_edit.config(state=con.NORMAL)
        self.btn_save.config(state=con.DISABLED)
        

        


        try:
            cur_item = self.tree.focus()
            cur_item = self.tree.item(cur_item)
            cur_item = cur_item['values']
            

            req = get("http://"+self.ip+":6000/cat/getSelectedCat" , params = { "cat_id" : cur_item[0]})
            if req.status_code == 200:
                resp = req.json()[0]
                self.enable_all()
                self.clear_all()
    
                self.ent_cat_name.insert(0,resp['cat_name'])
                self.selected_cat_id = resp['cat_id']
                self.disable_all()
                if resp['cat_image'] == 'True':
                    self.lbl_cat_img.config(text = "photo.png")
                    file = get("http://"+self.ip+":6000/images/categories/"+str(cur_item[0])+"/photo.png")
                    self.image_cat = ImageTk.PhotoImage(Image.open(io.BytesIO(file.content)))
                    #self.btn_cat_img_view.config(state = con.NORMAL)


                


        except IndexError:
            self.btn_new.config(state=con.NORMAL)
            self.btn_edit.config(state=con.DISABLED)
    
    def check_name(self, e):
        self.ent_cat_name.select_clear()
        name = self.ent_cat_name.get().upper()
        temp = name.split()
        name = ""

        i = 0
        for each in temp:
            if i == 0:
                name += each
            else:
                name += " "+each
            i+=1

        
        sql = "select cat_name from somanath.categories where cat_name = '"+ name +"'"
        
        if not self.new_state:
            sql += " and cat_id != "+ str(self.selected_cat_id)
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            if len(req.json())>0:
                msg.showinfo("Error" , "This category name exists")
                self.ent_cat_name.select_range(0 , con.END)
                self.ent_cat_name.focus_set()
                return


        self.ent_cat_name.delete(0,con.END)
        self.ent_cat_name.insert(0,name)

    def enable_all(self):
        self.ent_cat_name.config(state = con.NORMAL)

        self.btn_cat_img_brw.config(state = con.NORMAL)
        self.btn_cat_img_view.config(state = con.NORMAL)

    def clear_all(self):
        self.image_cat = None
        self.image_cat_loc = ""
        self.selected_cat_id = -1
        self.lbl_cat_img.config(text = "")
        self.ent_cat_name.delete(0,con.END)

    def disable_all(self):
        self.ent_cat_name.config(state = con.DISABLED)
        self.btn_cat_img_brw.config(state = con.DISABLED)
        self.btn_cat_img_view.config(state = con.DISABLED)

      







class emp(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations,others , emp_form):
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , emp_form)
        if base == None:
            return
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.emp_img = None
        self.emp_img_loc = ""
        self.selected_emp = -1
        self.others = others
        self.root_frame = frames[0]
        self.new_state = False
        self.edit_state = False
        self.user = others[2]
        self.ip = others[1]
        self.home_dir = others[0]


        self.lbl_emp_name = ttk.Label(self.main_frame , text = "Employ Name      :" , style = "window_text_medium.TLabel")
        self.lbl_emp_add = ttk.Label(self.main_frame , text = "Employ Address   :" , style = "window_text_medium.TLabel")
        self.lbl_emp_mob = ttk.Label(self.main_frame , text = "Employ Mob       :" , style = "window_text_medium.TLabel")
        self.lbl_emp_acc = ttk.Label(self.main_frame , text = "Employ AC/NO     :" , style = "window_text_medium.TLabel")
        self.lbl_emp_ifsc = ttk.Label(self.main_frame , text = "Employ IFSC      :" , style = "window_text_medium.TLabel")
        self.lbl_emp_img_txt = ttk.Label(self.main_frame , text = "Employ Photo     :" , style = "window_text_medium.TLabel")

        self.ent_emp_name = ttk.Entry(self.main_frame  , width = 30 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_emp_name.bind("<FocusOut>" , self.check_name)
        self.ent_emp_mob = ttk.Entry(self.main_frame  , width = 30 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[2], '%P'))
        self.ent_emp_mob.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_emp_acc = ttk.Entry(self.main_frame  , width = 30 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_emp_acc.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_emp_ifsc = ttk.Entry(self.main_frame  , width = 30 , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_emp_ifsc.bind("<FocusOut>" , self.combo_entry_out)
        self.lbl_emp_img =  ttk.Label(self.main_frame  , width = 30 , style = "window_lbl_ent.TLabel")
        self.ent_emp_add = Text(self.main_frame  , width = 30 , height = 4 ,  font = ('Lucida Grande' , -int(self.main_hgt*0.03)))

        self.btn_emp_photo_brw = ttk.Button(self.main_frame , state = con.DISABLED , text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_photo(None))
        self.btn_emp_photo_brw.bind("<Return>" , self.file_dialog_photo)
        self.btn_emp_photo_vw = ttk.Button(self.main_frame , state = con.DISABLED , text = " View " , style = "window_btn_medium.TButton" ,command = lambda : self.view_photo(None))
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

        self.tree.bind('<Double-Button-1>',self.select_tree)
        self.tree.bind('<Return>',self.select_tree)

        self.tree['columns'] = ('id','name')
        self.tree.heading('id' , text = 'ID')
        self.tree.heading('name' , text = 'Name')
        #self.tree['show'] = 'headings'



        self.btn_frame = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.btn_new = ttk.Button(self.btn_frame , text = "New" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.new(None))
        self.btn_new.bind("<Return>" , self.new) 
        self.btn_edit = ttk.Button(self.btn_frame , text = "Edit" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.edit(None))
        self.btn_edit.bind("<Return>" , self.edit)
        self.btn_save = ttk.Button(self.btn_frame , text = "Save" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.save(None))
        self.btn_save.bind("<Return>" , self.save)
        self.btn_refresh = ttk.Button(self.btn_frame , text = "Refresh" , width = 7 , style = "window_btn_medium.TButton" ,command = lambda : self.refresh(None))
        self.btn_refresh.bind("<Return>" , self.refresh)

        self.tree_wdt = self.tree_frame.winfo_reqwidth()-self.scroll_y.winfo_reqwidth()
        
        self.tree.column('id' , width = int(self.tree_wdt*0.2) ,minwidth = int(self.tree_wdt*0.15) , anchor = "w")
        self.tree.column('name' , width = int(self.tree_wdt*0.8) , minwidth = int(self.tree_wdt*0.70) , anchor = "w")


        self.lbl_emp_name.grid(row = 0 , column = 0 , pady = int(self.main_hgt*0.03) , padx = int(self.main_wdt*0.01))
        self.lbl_emp_mob.grid(row = 1 , column = 0 , pady = int(self.main_hgt*0.03))
        self.lbl_emp_acc.grid(row = 2 , column = 0 , pady = int(self.main_hgt*0.03))
        self.lbl_emp_ifsc.grid(row = 3 , column = 0 , pady = int(self.main_hgt*0.03))
        self.lbl_emp_add.grid(row = 4 , column = 0 , pady = int(self.main_hgt*0.03))
        self.lbl_emp_img_txt.grid(row = 5 , column = 0 , pady = int(self.main_hgt*0.03))

        self.ent_emp_name.grid(row = 0 , column = 1 , padx = int(self.main_hgt*0.01) , columnspan = 2)
        self.ent_emp_mob.grid(row = 1 , column = 1  , columnspan = 2)
        self.ent_emp_acc.grid(row = 2 , column = 1 , columnspan = 2)
        self.ent_emp_ifsc.grid(row = 3 , column = 1 , columnspan = 2)
        self.ent_emp_add.grid(row = 4 , column = 1 , columnspan = 2)
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
        self.btn_refresh.grid(row = 0 , column = 3 , padx = int(self.main_wdt*0.01))

        self.emp_list()

    def combo_entry_out(self , e):
        e.widget.select_clear()

    def file_dialog_photo(self , e):
        file = filedialog.askopenfilename(initialdir = self.others[0]+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        if file!= "":
            ext = file.split(".")[-1]
            if ext != 'jpg' and ext != 'png' and ext != 'jpeg' and ext != 'bmp':
                msg.showerror("error","Select only images \n (eg :- *.png or *.jpg or *.bmp or *.jpeg)")
                return
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]
            self.lbl_emp_img.config(text = text)
            self.emp_img = ImageTk.PhotoImage(Image.open(file))
        else:
            self.lbl_emp_img.config(text = "")
            

        self.emp_img_loc = file

        

    def view_photo(self , e):
        if self.emp_img != None or self.lbl_emp_img.cget("text") != "":
            image_viewer(self.emp_img_loc,"Employee" , self.root_frame)

    def enable_all(self ):
        self.ent_emp_name.config(state = con.NORMAL)
        self.ent_emp_mob.config(state = con.NORMAL)
        self.ent_emp_acc.config(state = con.NORMAL)
        self.ent_emp_ifsc.config(state = con.NORMAL)
        self.ent_emp_add.config(state = con.NORMAL)
        self.btn_emp_photo_brw.config(state = con.NORMAL)
        self.btn_emp_photo_vw.config(state = con.NORMAL)
        
    def disable_all(self ):
        self.ent_emp_name.config(state = con.DISABLED)
        self.ent_emp_mob.config(state = con.DISABLED)
        self.ent_emp_acc.config(state = con.DISABLED)
        self.ent_emp_ifsc.config(state = con.DISABLED)
        self.ent_emp_add.config(state = con.DISABLED)
        self.btn_emp_photo_brw.config(state = con.DISABLED)
        self.btn_emp_photo_vw.config(state = con.DISABLED)

    def clear_all(self ):
        self.ent_emp_name.delete(0,con.END)
        self.ent_emp_mob.delete(0,con.END)
        self.ent_emp_acc.delete(0,con.END)
        self.ent_emp_ifsc.delete(0,con.END)
        self.ent_emp_add.delete(0.0,con.END)
        self.lbl_emp_img.config(text = "")

        self.emp_img = None
        self.emp_img_loc = ""
        self.selected_emp = -1

    def new(self , e):
        self.edit_state = False
        self.new_state = True

        self.btn_new.config(state = con.DISABLED)
        self.btn_edit.config(state = con.DISABLED)
        self.btn_save.config(state = con.NORMAL)
        

        self.new_state = True
        self.edit_state = False

        self.enable_all()
        self.clear_all()

        self.ent_emp_name.focus_set()

    def edit(self , e):
        self.btn_new.config(state = con.DISABLED)
        self.btn_edit.config(state = con.DISABLED)
        self.btn_save.config(state = con.NORMAL)
        #self.btn_cancel.config(state = con.NORMAL)

        self.new_state = False
        self.edit_state = True

        emp_photo = self.lbl_emp_img.cget("text")
        emp_dir = os.path.join(os.path.expanduser('~'),"Images" , "accounts")                                                     #delete all older firm images in the folder

        for f in os.listdir(emp_dir):
            os.remove(os.path.join(emp_dir, f))
    

        if emp_photo != "":
            self.emp_img_loc = os.path.join(emp_dir , "photo." + emp_photo.split(".")[-1])
            imgpil = ImageTk.getimage(self.emp_img)
            imgpil.save( self.emp_img_loc , emp_photo.split(".")[-1])

        self.enable_all()
        self.ent_emp_name.focus_set()

    def save(self , e):
        name = self.ent_emp_name.get()
        mob = self.ent_emp_mob.get()
        acno = self.ent_emp_acc.get()
        ifsc = self.ent_emp_ifsc.get()
        add =   self.ent_emp_add.get(0.0 , 10.30).upper()

        if name == "":
            msg.showinfo("Info" , "Enter Name")
            self.ent_emp_name.focus_set()
            return
        
        parameters = {
            "emp_id"    : "",
            "user_name" : self.user ,
            "emp_name"  : name , 
            "emp_mob"   : mob,
            "emp_acno"  : acno , 
            "emp_ifsc"  : ifsc , 
            "emp_add"   : add,    
            "emp_img" : False  
        }


        files = []

        if self.emp_img_loc != "" and  self.emp_img_loc != None:
            original = Image.open(self.emp_img_loc)
            temp = self.emp_img_loc.split(".")
            type = temp[-1]

            if type != "png":
                temp.pop(len(temp)-1)
                self.emp_img_loc = os.path.join(self.home_dir , "Images" , "tempImages" , "employee.png")
                original.save(self.emp_img_loc , format = "png")

            files.append(('images', (self.emp_img_loc, open(self.emp_img_loc, 'rb'), 'image/png')))
            parameters['emp_img'] = True


        

        

        if self.edit_state:
            parameters['emp_id'] = self.selected_emp

        req = post("http://"+self.ip+":6000/employs/save" , params = parameters , files = files)

        if req.status_code == 201:
            msg.showerror("Error" , "This employee has been added")
            return

        self.clear_all()
        self.disable_all()
        self.emp_list()
        
        self.btn_new.config(state = con.NORMAL)
        self.btn_save.config(state = con.DISABLED)
        self.btn_edit.config(state = con.DISABLED)

    def refresh(self,e):
        self.emp_list()

    def emp_list(self):
        req = get("http://"+self.ip+":6000/employs/getEmpList")
        
        for each in self.tree.get_children():
            self.tree.delete(each)

        if req.status_code == 200:
            resp = req.json()
            tag_index = 0
            for each in resp:
                if tag_index%2:
                    tag = 'a'
                else:
                    tag = 'b'
                tag_index += 1
                self.tree.insert('','end' ,tags=(tag,), values = (each['emp_id'] , each['emp_name']))

    def check_name(self, e):
        self.ent_emp_name.select_clear()
        name = self.ent_emp_name.get().upper()
        temp = name.split()
        name = ""

        i = 0
        for each in temp:
            if i == 0:
                name += each
            else:
                name += " "+each
            i+=1

        
        sql = "select emp_name from somanath.employs where emp_name = '"+ name +"'"
        
        if not self.new_state:
            sql += " and emp_id != "+ str(self.selected_emp)
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            if len(req.json())>0:
                msg.showinfo("Error" , "This Employee name exists")
                self.ent_emp_name.select_range(0 , con.END)
                self.ent_emp_name.focus_set()
                return


        self.ent_emp_name.delete(0,con.END)
        self.ent_emp_name.insert(0,name)

    def select_tree(self , e):
        
        self.btn_new.config(state=con.NORMAL)
        self.btn_edit.config(state=con.NORMAL)
        self.btn_save.config(state=con.DISABLED)


        
        try:
            cur_item = self.tree.focus()
            cur_item = self.tree.item(cur_item)
            cur_item = cur_item['values']

            req = get("http://"+self.ip+":6000/employs/getSelectedEmp" , params = {"emp_id" : cur_item[0]})
            
            if req.status_code == 200:
                
                resp = req.json()[0]
                
                self.enable_all()
                self.clear_all()
                
                self.ent_emp_name.insert(0,resp['emp_name'])
                self.ent_emp_mob.insert(0,resp['emp_phone'])
                self.ent_emp_acc.insert(0,resp['emp_accno'])
                self.ent_emp_ifsc.insert(0,resp['emp_ifsc'])
                self.ent_emp_add.insert(0.0,resp['emp_address'])
                

                
                
                self.disable_all()

                if resp['emp_img'] == 'True':
                    self.lbl_emp_img.config(text = "photo.png")
                    file = get("http://"+self.ip+":6000/images/employs/"+str(cur_item[0])+"/photo.png")
                    self.emp_img = ImageTk.PhotoImage(Image.open(io.BytesIO(file.content)))
                    #self.btn_emp_photo_vw.config(state = con.NORMAL)
                
                
                
                self.btn_edit.config(state = con.NORMAL)
                self.selected_emp = resp['emp_id']
               
                
        except IndexError:
            self.btn_new.config(state = con.NORMAL)
            pass





   
        

class acc(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations,others , acc_form):
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , acc_form)
        if base == None:
            return
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.acc_img = None
        self.acc_img_loc = ""
        self.selected_acc = -1
        self.new_state = False
        self.edit_state = False
        self.rad_acc_type = IntVar()
        self.rad_cus_type = IntVar()
        self.check_cus = StringVar()
        self.check_sup = StringVar()
        self.homeDir = others[0]
        self.ip = others[1]
        self.user = others[3]
        self.root_frame = frames[0]
        self.tax_check = others[2]


        self.lbl_acc_type = ttk.Label(self.main_frame , text = "A/C Holder Type   :" , style = "window_text_medium.TLabel")
        self.lbl_acc_name = ttk.Label(self.main_frame , text = "A/C Holder Name   :" , style = "window_text_medium.TLabel")
        self.lbl_acc_email = ttk.Label(self.main_frame , text = "A/C Holder Email  :" , style = "window_text_medium.TLabel")
        self.lbl_acc_mob1 = ttk.Label(self.main_frame , text = "A/C Holder Mob1   :" , style = "window_text_medium.TLabel")
        self.lbl_acc_mob2 = ttk.Label(self.main_frame , text = "A/C Holder Mob2   :" , style = "window_text_medium.TLabel")
        self.lbl_acc_gst = ttk.Label(self.main_frame , text = "A/C Holder GST    :" , style = "window_text_medium.TLabel")
        self.lbl_acc_acno = ttk.Label(self.main_frame , text = "A/C Holder A/C no :" , style = "window_text_medium.TLabel")
        self.lbl_acc_ifsc = ttk.Label(self.main_frame , text = "A/C Holder IFSC   :" , style = "window_text_medium.TLabel")
        self.lbl_acc_ctype = ttk.Label(self.main_frame , text = "Customer Type     :" , style = "window_text_medium.TLabel")
        self.lbl_acc_address = ttk.Label(self.main_frame , text = "A/C Holder Address:" , style = "window_text_medium.TLabel")
        self.lbl_acc_img_txt = ttk.Label(self.main_frame , text = "A/C Holder Image  :" , style = "window_text_medium.TLabel")

        self.rad_cust = ttk.Radiobutton(self.main_frame , state = con.DISABLED, value = 0 , variable = self.rad_acc_type , style = "window_radio.TRadiobutton" , text = "Customer")
        self.rad_supp = ttk.Radiobutton(self.main_frame , state = con.DISABLED, value = 1 , variable = self.rad_acc_type , style = "window_radio.TRadiobutton" , text = "Supplier")
        self.ent_acc_name = ttk.Entry(self.main_frame  , state = con.DISABLED, width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)), validate="key", validatecommand=(validations[1], '%P'))
        self.ent_acc_name.bind("<FocusOut>" , self.check_name)
        self.ent_acc_email = ttk.Entry(self.main_frame  , state = con.DISABLED, width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[3], '%P'))
        self.ent_acc_email.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_acc_mob1 = ttk.Entry(self.main_frame  , state = con.DISABLED, width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[2], '%P'))
        self.ent_acc_mob1.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_acc_mob2 = ttk.Entry(self.main_frame  , state = con.DISABLED, width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[2], '%P'))
        self.ent_acc_mob2.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_acc_gst = ttk.Entry(self.main_frame  , state = con.DISABLED, width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[4], '%P'))
        self.ent_acc_gst.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_acc_acno = ttk.Entry(self.main_frame  , state = con.DISABLED, width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_acc_acno.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_acc_ifsc = ttk.Entry(self.main_frame  , state = con.DISABLED, width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_acc_ifsc.bind("<FocusOut>" , self.combo_entry_out)
        self.frm_rad_cust = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.rad_cust_nrm = ttk.Radiobutton(self.frm_rad_cust , state = con.DISABLED, value = 0 , variable = self.rad_cus_type , style = "window_radio.TRadiobutton" , text = "NRM")
        self.rad_cust_htl = ttk.Radiobutton(self.frm_rad_cust , state = con.DISABLED, value = 1 , variable = self.rad_cus_type , style = "window_radio.TRadiobutton" , text = "HTL")
        self.rad_cust_spl = ttk.Radiobutton(self.frm_rad_cust , state = con.DISABLED, value = 2 , variable = self.rad_cus_type , style = "window_radio.TRadiobutton" , text = "SPL")
        self.rad_cust_ang = ttk.Radiobutton(self.frm_rad_cust , state = con.DISABLED, value = 3 , variable = self.rad_cus_type , style = "window_radio.TRadiobutton" , text = "ANG")
        
        self.lbl_acc_img = ttk.Label(self.main_frame  , width = 30 , style = "window_lbl_ent.TLabel")

        self.btn_acc_img_brw = ttk.Button(self.main_frame , state = con.DISABLED, text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_acc(None))
        self.btn_acc_img_brw.bind("<Return>" , self.file_dialog_acc)
        self.btn_acc_img_view = ttk.Button(self.main_frame , state = con.DISABLED, text = " View " , style = "window_btn_medium.TButton" ,command = lambda : self.view_acc(None))
        self.btn_acc_img_view.bind("<Return>" , self.view_acc)

        self.ent_acc_address = Text(self.main_frame  , state = con.DISABLED, width = 30 , height = 4 ,  font = ('Lucida Grande' , -int(self.main_hgt*0.03)))

        if root.winfo_screenheight()>1000:
            self.tree_frame = ttk.Frame(self.main_frame , height = int(self.main_hgt*0.853) , width = int(self.main_wdt*0.45) , style = "root_menu.TFrame")
        else:
            self.tree_frame = ttk.Frame(self.main_frame , height = int(self.main_hgt*0.863) , width = int(self.main_wdt*0.45) , style = "root_menu.TFrame")
        self.tree_frame.pack_propagate(False)
        self.tree_frame.grid_propagate(False)

        self.frm_rad_acc = ttk.Frame(self.tree_frame , style = "root_main.TFrame")
        self.ent_acc_search = ttk.Entry(self.frm_rad_acc  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[1], '%P'))
        self.ent_acc_search.bind("<FocusOut>" , self.check_name)
        self.ent_acc_search.bind("<Return>" , self.acc_list)
        self.chk_cust = ttk.Checkbutton(self.frm_rad_acc ,variable = self.check_cus, onvalue = "True" , offvalue = "False" , text = "Customers" , style = "window_check.TCheckbutton")
        self.chk_supp = ttk.Checkbutton(self.frm_rad_acc ,variable = self.check_sup , onvalue = "True" , offvalue = "False" , text = "Suppliers" , style = "window_check.TCheckbutton")

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

        self.tree.bind('<Double-Button-1>',self.select_tree)
        self.tree.bind('<Return>',self.select_tree)
        

        self.btn_frame = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.btn_new = ttk.Button(self.btn_frame , text = "New" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.new(None))
        self.btn_new.bind("<Return>" , self.new) 
        self.btn_edit = ttk.Button(self.btn_frame , text = "Edit" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.edit(None))
        self.btn_edit.bind("<Return>" , self.edit)
        self.btn_save = ttk.Button(self.btn_frame , text = "Save" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.save(None))
        self.btn_save.bind("<Return>" , self.save)
        self.btn_refresh = ttk.Button(self.btn_frame , text = "Refresh" , width = 7 , style = "window_btn_medium.TButton" ,command = lambda : self.refresh(None))
        self.btn_refresh.bind("<Return>" , self.refresh)

        self.lbl_acc_type.grid(row = 0 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_name.grid(row = 1 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_email.grid(row = 2 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_mob1.grid(row = 3 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_mob2.grid(row = 4 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_gst.grid(row = 5 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_acno.grid(row = 6 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_ifsc.grid(row = 7 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_ctype.grid(row = 8 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_img_txt.grid(row = 9 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))
        self.lbl_acc_address.grid(row = 11 , column = 0 , pady = int(self.main_hgt*0.005), padx = int(self.main_wdt*0.007))


        self.rad_cust.grid(row = 0 , column = 1)
        self.rad_supp.grid(row = 0 , column = 2)
        self.ent_acc_name.grid(row = 1 , column = 1 , columnspan = 2)
        self.ent_acc_email.grid(row = 2 , column = 1 , columnspan = 2)
        self.ent_acc_mob1.grid(row = 3 , column = 1 , columnspan = 2)
        self.ent_acc_mob2.grid(row = 4 , column = 1 , columnspan = 2)
        self.ent_acc_gst.grid(row = 5 , column = 1 , columnspan = 2)
        self.ent_acc_acno.grid(row = 6 , column = 1 , columnspan = 2)
        self.ent_acc_ifsc.grid(row = 7 , column = 1 , columnspan = 2)
        self.frm_rad_cust.grid(row = 8 , column = 1 , columnspan = 2)
        self.rad_cust_nrm.grid(row = 0 , column = 0, padx = int(self.main_wdt*0.01))
        self.rad_cust_htl.grid(row = 0 , column = 1, padx = int(self.main_wdt*0.01))
        self.rad_cust_spl.grid(row = 0 , column = 2, padx = int(self.main_wdt*0.01))
        self.rad_cust_ang.grid(row = 0 , column = 3, padx = int(self.main_wdt*0.01))
        self.lbl_acc_img.grid(row = 9 , column = 1 , columnspan = 2)
        self.btn_acc_img_brw.grid(row = 10 , column = 1)
        self.btn_acc_img_view.grid(row = 10 , column = 2)
        self.ent_acc_address.grid(row = 11 , column = 1 , columnspan = 2)
        
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
        self.btn_refresh.grid(row = 0 , column = 3 , padx = int(self.main_wdt*0.01))

        self.tree_wdt = self.tree_frame.winfo_reqwidth()-self.scroll_y.winfo_reqwidth()
        
        self.tree.column('id' , width = int(self.tree_wdt*0.15) ,minwidth = int(self.tree_wdt*0.15) , anchor = "w")
        self.tree.column('type' , width = int(self.tree_wdt*0.15) , minwidth = int(self.tree_wdt*0.15) , anchor = "w")
        self.tree.column('name' , width = int(self.tree_wdt*0.70) , minwidth = int(self.tree_wdt*0.70) , anchor = "w")

        self.check_cus.set("False")
        self.check_sup.set("False")

        self.acc_list(None)

    def combo_entry_out(self , e):
        e.widget.select_clear()

    def file_dialog_acc(self , e):
        file = filedialog.askopenfilename(initialdir = self.homeDir+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        if file!= "":
            ext = file.split(".")[-1]
            if ext != 'jpg' and ext != 'png' and ext != 'jpeg' and ext != 'bmp':
                msg.showerror("error","Select only images \n (eg :- *.png or *.jpg or *.bmp or *.jpeg)")
                return
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]
            self.lbl_acc_img.config(text = text)
            self.acc_img = ImageTk.PhotoImage(Image.open(file)) 
        else:
            self.lbl_acc_img.config(text = "")

        self.acc_img_loc = file

    def view_acc(self , e):

        if self.acc_img != None or self.lbl_acc_img.cget("text") != "":
            image_viewer(self.acc_img_loc,"A/C Image" , self.root_frame)

    def enable_all(self):
        self.rad_cust.config(state = con.NORMAL)
        self.rad_supp.config(state = con.NORMAL)
        self.ent_acc_name.config(state = con.NORMAL)
        self.ent_acc_email.config(state = con.NORMAL)
        self.ent_acc_mob1.config(state = con.NORMAL)
        self.ent_acc_mob2.config(state = con.NORMAL)
        self.ent_acc_gst.config(state = con.NORMAL)
        self.ent_acc_acno.config(state = con.NORMAL)
        self.ent_acc_ifsc.config(state = con.NORMAL)
        self.rad_cust_nrm.config(state = con.NORMAL)
        self.rad_cust_htl.config(state = con.NORMAL) 
        self.rad_cust_spl.config(state = con.NORMAL)
        self.rad_cust_ang.config(state = con.NORMAL)
        self.btn_acc_img_brw.config(state = con.NORMAL)
        self.btn_acc_img_view.config(state = con.NORMAL)
        self.ent_acc_address.config(state = con.NORMAL)

    def disable_all(self):
        self.rad_cust.config(state = con.DISABLED)
        self.rad_supp.config(state = con.DISABLED)
        self.ent_acc_name.config(state = con.DISABLED)
        self.ent_acc_email.config(state = con.DISABLED)
        self.ent_acc_mob1.config(state = con.DISABLED)
        self.ent_acc_mob2.config(state = con.DISABLED)
        self.ent_acc_gst.config(state = con.DISABLED)
        self.ent_acc_acno.config(state = con.DISABLED)
        self.ent_acc_ifsc.config(state = con.DISABLED)
        self.rad_cust_nrm.config(state = con.DISABLED)
        self.rad_cust_htl.config(state = con.DISABLED) 
        self.rad_cust_spl.config(state = con.DISABLED)
        self.rad_cust_ang.config(state = con.DISABLED)
        self.btn_acc_img_brw.config(state = con.DISABLED)
        self.btn_acc_img_view.config(state = con.DISABLED)
        self.ent_acc_address.config(state = con.DISABLED)

    def clear_all(self):
       
        self.ent_acc_name.delete(0,con.END)
        self.ent_acc_email.delete(0,con.END)
        self.ent_acc_mob1.delete(0,con.END)
        self.ent_acc_mob2.delete(0,con.END)
        self.ent_acc_gst.delete(0,con.END)
        self.ent_acc_acno.delete(0,con.END)
        self.ent_acc_ifsc.delete(0,con.END)
        
        self.ent_acc_address.delete(0.0 , con.END)

        self.lbl_acc_img.config(text = "")
        self.rad_acc_type.set(-1)
        self.rad_cus_type.set(-1)

        self.selected_acc = -1
        self.acc_img_loc = ""
        self.acc_img = None

    def new(self , e):
        self.btn_new.config(state = con.DISABLED)
        self.btn_edit.config(state = con.DISABLED)
        self.btn_save.config(state = con.NORMAL)
        

        self.new_state = True
        self.edit_state = False

        self.enable_all()
        self.clear_all()

        self.ent_acc_name.focus_set()

    def edit(self , e):
        self.btn_new.config(state = con.DISABLED)
        self.btn_edit.config(state = con.DISABLED)
        self.btn_save.config(state = con.NORMAL)
        #self.btn_cancel.config(state = con.NORMAL)

        self.new_state = False
        self.edit_state = True

        acc_photo = self.lbl_acc_img.cget("text")
        acc_dir = os.path.join(self.homeDir,"Images" , "accounts")                                                     #delete all older firm images in the folder

        for f in os.listdir(acc_dir):
            os.remove(os.path.join(acc_dir, f))
    

        if acc_photo != "":
            self.acc_img_loc = os.path.join(acc_dir , "accounts." + acc_photo.split(".")[-1])
            imgpil = ImageTk.getimage(self.acc_img)
            imgpil.save( self.acc_img_loc , acc_photo.split(".")[-1])

        self.enable_all()
        self.ent_acc_name.focus_set()
        self.rad_cust.config(state = con.DISABLED)
        self.rad_supp.config(state = con.DISABLED)

    def save(self , e):
        type = self.rad_acc_type.get()
        name = self.ent_acc_name.get().upper()
        email = self.ent_acc_email.get().upper()
        mob1 = self.ent_acc_mob1.get().upper()
        mob2 = self.ent_acc_mob2.get().upper()
        gst = self.ent_acc_gst.get().upper()
        ifsc = self.ent_acc_ifsc.get().upper()
        accno = self.ent_acc_acno.get().upper()
        cus_type = self.rad_cus_type.get()
        add = self.ent_acc_address.get(0.0 , 10.0).upper()

    
        if type!=0 and type!=1:
            msg.showinfo("Info" , "select Customer/Supplier")
            self.lbl_acc_type.focus_set()
            return
        
        if name == "":
            msg.showinfo("Info" , "Enter Name")
            self.ent_acc_name.focus_set()
            return
  

        if type == 0:
            if not (cus_type>=0 and cus_type<=3):
                msg.showinfo("Info" , "select Customer type")
                self.lbl_acc_type.focus_set()
                return
        #acc_type, acc_name, acc_email, acc_add, ,acc_mob1, acc_mob2, acc_gstin, acc_accno, acc_ifsc, acc_cus_type, acc_img
        if gst !='':
            if len(gst) != 15:
                msg.showinfo("Info" , "GSTIN must be 15 charecters")
                return

        if cus_type == 0:
            cus_type = 'NRM'
        elif cus_type == 1:
            cus_type = 'HTL'
        elif cus_type == 2:
            cus_type = 'SPL'
        else :
            cus_type = 'ANG'

        if type == 0:
            type = 'CUST'
        else:
            type = 'SUPP'
            cus_type = ''


        parameters = {
                "acc_id" : "" ,
                "user_name" : self.user ,
                "acc_type" : type ,
                "acc_name" : name , 
                "acc_email":email , 
                "acc_add" : add ,
                "acc_mob1" : mob1 ,
                "acc_mob2" : mob2 ,
                "acc_gstin" : gst ,
                "acc_accno" : accno ,
                "acc_ifsc" :  ifsc,
                "acc_cus_type" :  cus_type,
                "acc_img" : False , 
                }

        files = []


        if self.acc_img_loc != "" and self.acc_img_loc != None:
            original = Image.open(self.acc_img_loc)
            temp = self.acc_img_loc.split(".")
            type = temp[-1]

            if type != "png":
                temp.pop(len(temp)-1)
                
                self.acc_img_loc = os.path.join(self.homeDir , "Images" , "tempImages" , "photo.png")
                original.save(self.acc_img_loc , format = "png")

            files.append(('images', (self.acc_img_loc, open(self.acc_img_loc, 'rb'), 'images/png')))
            parameters['acc_img'] = True

        

        if self.edit_state:
            parameters['acc_id'] = self.selected_acc

        req = post("http://"+self.ip+":6000/accounts/save" , params = parameters , files = files)
        
        if req.status_code == 201:
            msg.showerror("Error" , "Account with same Name / GSTIN exists")
            return
        
        self.clear_all()
        self.disable_all()
        self.acc_list(None)
        #self.btn_cancel.config(state = con.DISABLED)
        self.btn_new.config(state = con.NORMAL)
        self.btn_save.config(state = con.DISABLED)
        self.btn_edit.config(state = con.DISABLED)

    def acc_list(self , e):
        text = self.ent_acc_search.get().upper()
        sql =  "SELECT acc_id,acc_name,acc_type FROM somanath.accounts"

        sup = self.check_sup.get()
        cus = self.check_cus.get()
        
        

        if text != "":
            if cus == "True" and sup =="False":
                sql += " where acc_type = 'CUST' and acc_name regexp '"+text+"' order by acc_name"

            elif cus == "False" and sup =="True":
                sql += " where acc_type = 'SUPP' and acc_name regexp '"+text+"' order by acc_name"
            else:
                sql += " where acc_name regexp '"+text+"' order by acc_type , acc_name  "
        else:
            if cus == "True" and sup =="False":
                sql += " where acc_type = 'CUST' order by acc_name"

            elif cus == "False" and sup =="True":
                sql += " where acc_type = 'SUPP' order by acc_name"
            else:
                sql += " order by acc_type , acc_name  "
                


        self.tax_check == False

        req = get("http://"+self.ip+":6000/accounts/getAccList" , params = {'sql': sql , "tax_check" : self.tax_check})
        
        for each in self.tree.get_children():
            self.tree.delete(each)

        if req.status_code == 200:
            resp = req.json()
            tag_index = 0
            for each in resp:
                if tag_index%2:
                    tag = 'a'
                else:
                    tag = 'b'
                tag_index += 1
                self.tree.insert('','end' ,tags=(tag,), values = (each['acc_id'] , each['acc_type'] , each['acc_name']))

    def select_tree(self , e):
        self.btn_acc_img_view.config(state = con.DISABLED)
        self.btn_new.config(state = con.NORMAL)
        
       
        try:
            cur_item = self.tree.focus()
            cur_item = self.tree.item(cur_item)
            cur_item = cur_item['values']

            req = get("http://"+self.ip+":6000/accounts/getSelectedAcc" , params = {"acc_id" : cur_item[0]})
            
            if req.status_code == 200:
                
                resp = req.json()[0]
                
                self.enable_all()
                self.clear_all()
                
                if resp['acc_type'] == 'SUPP':
                    self.rad_acc_type.set(1)
                else:
                    self.rad_acc_type.set(0)
                    if resp['acc_cus_type'] == 'NRM':
                        self.rad_cus_type.set(0)
                    elif resp['acc_cus_type'] == 'HTL':
                        self.rad_cus_type.set(1)
                    elif resp['acc_cus_type'] == 'SPL':
                        self.rad_cus_type.set(2)
                    else:
                        self.rad_cus_type.set(3)

                self.ent_acc_name.insert(0 , resp['acc_name'])
                self.ent_acc_email.insert(0 , resp['acc_email'])
                self.ent_acc_mob1.insert(0 , resp['acc_mob1'])
                self.ent_acc_mob2.insert(0 , resp['acc_mob2'])
                self.ent_acc_gst.insert(0 , resp['acc_gstin'])
                self.ent_acc_acno.insert(0 , resp['acc_accno'])
                self.ent_acc_ifsc.insert(0 , resp['acc_ifsc'])
        
                self.ent_acc_address.insert(0.0 , resp['acc_add'])
                
                self.disable_all()

                if resp['acc_img'] == 'True':
                    self.lbl_acc_img.config(text = "photo.png")
                    file = get("http://"+self.ip+":6000/images/accounts/"+str(cur_item[0])+"/photo.png")
                    self.acc_img = ImageTk.PhotoImage(Image.open(io.BytesIO(file.content)))
                    #self.btn_acc_img_view.config(state = con.NORMAL)
                
                

                self.btn_edit.config(state = con.NORMAL)
                self.selected_acc = resp['acc_id']
                
        except IndexError:
            
            pass

    def check_name(self, e):
        self.ent_acc_name.select_clear()
        name = self.ent_acc_name.get().upper()
        temp = name.split()
        name = ""

        i = 0
        for each in temp:
            if i == 0:
                name += each
            else:
                name += " "+each
            i+=1

        
        sql = "select acc_name from somanath.accounts where acc_name = '"+ name +"'"
        
        if not self.new_state:
            sql += " and acc_id != "+ str(self.selected_acc)
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            if len(req.json())>0:
                msg.showinfo("Error" , "This account name exists")
                self.ent_acc_name.select_range(0 , con.END)
                self.ent_acc_name.focus_set()
                return


        self.ent_acc_name.delete(0,con.END)
        self.ent_acc_name.insert(0,name)

    def refresh(self , e):
        self.acc_list(None)








class prods(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations,others , prod_form):
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , prod_form)
        if base == None:
            return
        self.main_frame.grid_propagate(False)
        self.root_frame = frames[0] 
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.img_kan = None                                                                             #kannada image
        self.img_high = None                                                                       #high quality image
        self.img_low = None                                                                        #low quality image
        self.img_kan_loc = ""                                                                             
        self.img_high_loc = ""
        self.img_low_loc = ""
        self.selected_prod = -1                                                               
        self.homeDir = others[0]                                                       
        self.ip = others[1]
        self.user = others[2] 
        self.new_state = False
        self.edit_state = False
        self.units_values = ['N' , 'KG' , 'G' , 'M']
        self.gst_values = []
        self.cess_values = []
        self.check_state = StringVar()
        self.cat_state = StringVar()
        self.sup_state = StringVar()
        self.generated_bar = None   
        self.check_all = StringVar()

        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : 'select tax_per from somanath.taxes where tax_type = 0'})
        for each in req.json():
            self.gst_values.append(each['tax_per'])
        
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : 'select tax_per from somanath.taxes where tax_type = 1'})
        for each in req.json():
            self.cess_values.append(each['tax_per'])

        
                                                                                 
        
        self.lbl_bar = ttk.Label(self.main_frame , text = "Barcode    :" , style = "window_text_medium.TLabel")
        self.lbl_cat = ttk.Label(self.main_frame , text = "  Category :" , style = "window_text_medium.TLabel")
        self.lbl_name = ttk.Label(self.main_frame , text = "Name       :" , style = "window_text_medium.TLabel")
        self.lbl_hsn = ttk.Label(self.main_frame , text = "HSN        :" , style = "window_text_medium.TLabel")
        self.lbl_shelf = ttk.Label(self.main_frame , text = "  Shelf No :" , style = "window_text_medium.TLabel")
        self.lbl_kan_txt = ttk.Label(self.main_frame , text = "Kannada    :" , style = "window_text_medium.TLabel")
        self.lbl_eng = ttk.Label(self.main_frame , text = "English    :" , style = "window_text_medium.TLabel")
        self.lbl_min_qty = ttk.Label(self.main_frame , text = "Min Qty    :" , style = "window_text_medium.TLabel")
        self.lbl_exp = ttk.Label(self.main_frame , text = "Expiry   :" , style = "window_text_medium.TLabel")
        self.lbl_desc = ttk.Label(self.main_frame , text = "Description:" , style = "window_text_medium.TLabel")
        self.lbl_img1_txt = ttk.Label(self.main_frame , text = "Image 1    :" , style = "window_text_medium.TLabel")
        self.lbl_img2_txt = ttk.Label(self.main_frame , text = "Image 2    :" , style = "window_text_medium.TLabel")
        self.lbl_sup = ttk.Label(self.main_frame , text = "Supplier   :" , style = "window_text_medium.TLabel")
        self.lbl_tax1 = ttk.Label(self.main_frame , text = "GST        :" , style = "window_text_medium.TLabel")
        self.lbl_tax2 = ttk.Label(self.main_frame , text = "CESS     :" , style = "window_text_medium.TLabel")
        self.lbl_mrp1 = ttk.Label(self.main_frame , text = "MRP 1      :" , style = "window_text_medium.TLabel")
        self.lbl_mrp2 = ttk.Label(self.main_frame , text = "MRP 2    :" , style = "window_text_medium.TLabel")
        self.lbl_unit = ttk.Label(self.main_frame , text = "Unit     :" , style = "window_text_medium.TLabel")
        self.lbl_nrm = ttk.Label(self.main_frame , text = "Units NRM  :" , style = "window_text_medium.TLabel")
        self.lbl_htl = ttk.Label(self.main_frame , text = "Units HTL  :" , style = "window_text_medium.TLabel")
        self.lbl_spl = ttk.Label(self.main_frame , text = "Units SPL  :" , style = "window_text_medium.TLabel")
        self.lbl_ang = ttk.Label(self.main_frame , text = "Units ANG  :" , style = "window_text_medium.TLabel")



        self.btn_add_bar = ttk.Button(self.main_frame, state = con.DISABLED ,text = " Add "  , style = "window_btn_medium.TButton" , command = lambda : self.show_top_bar(None))
        self.btn_add_bar.bind("<Return>" , self.show_top_bar)

        self.btn_add_cat = ttk.Button(self.main_frame , state = con.DISABLED ,text = " Add "  , style = "window_btn_medium.TButton" , command = lambda : self.show_top_cat(None))
        self.btn_add_cat.bind("<Return>" , self.show_top_cat)

        self.ent_name = ttk.Entry(self.main_frame , state = con.DISABLED , width = 30 ,  font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[4], '%P'))
        self.ent_name.bind("<FocusOut>" , self.check_name)

        
        self.ent_hsn = ttk.Entry(self.main_frame , state = con.DISABLED , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[4], '%P'))
        self.ent_hsn.bind("<FocusOut>" , self.combo_entry_out)

        self.ent_shelf = ttk.Entry(self.main_frame  , state = con.DISABLED, width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[4], '%P'))
        self.ent_shelf.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_kan = ttk.Label(self.main_frame  , width = 30 , style = "window_lbl_ent.TLabel")
        #self.btn_kan_add = ttk.Button(self.main_frame, state = con.DISABLED , text = "Add Img" , style = "window_btn_medium.TButton" ,command = lambda : self.add_image(None))
        #self.btn_kan_add.bind("<Return>" , self.add_image)
        self.btn_kan_brw = ttk.Button(self.main_frame , state = con.DISABLED, text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_kan(None))
        self.btn_kan_brw.bind("<Return>" , self.file_dialog_kan)
        self.btn_kan_vw = ttk.Button(self.main_frame, state = con.DISABLED , text = "View" , style = "window_btn_medium.TButton" ,command = lambda : self.view_kan(None))
        self.btn_kan_vw.bind("<Return>" , self.view_kan)

        self.ent_name_eng = ttk.Entry(self.main_frame , state = con.DISABLED , width = 30 ,  font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[4], '%P'))
        self.ent_name_eng.bind("<FocusOut>" , self.combo_entry_out)

        self.ent_min_qty = ttk.Entry(self.main_frame , state = con.DISABLED , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_min_qty.bind("<FocusOut>" , self.combo_entry_out)

        self.ent_exp = ttk.Entry(self.main_frame , state = con.DISABLED , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[6], '%P'))
        self.ent_exp.bind("<FocusOut>" , self.combo_entry_out)

        
        self.lbl_img1 = ttk.Label(self.main_frame  , width = 30 , style = "window_lbl_ent.TLabel")
        self.btn_img1_brw = ttk.Button(self.main_frame , state = con.DISABLED, text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_img1(None))
        self.btn_img1_brw.bind("<Return>" , self.file_dialog_img1)
        self.btn_img1_vw = ttk.Button(self.main_frame , state = con.DISABLED, text = "View" , style = "window_btn_medium.TButton" ,command = lambda : self.view_img1(None))
        self.btn_img1_vw.bind("<Return>" , self.view_img1)

        self.lbl_img2 = ttk.Label(self.main_frame  , width = 30 , style = "window_lbl_ent.TLabel")
        self.btn_img2_brw = ttk.Button(self.main_frame, state = con.DISABLED , text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_img2(None))
        self.btn_img2_brw.bind("<Return>" , self.file_dialog_img2)
        self.btn_img2_vw = ttk.Button(self.main_frame , state = con.DISABLED, text = "View" , style = "window_btn_medium.TButton" ,command = lambda : self.view_img2(None))
        self.btn_img2_vw.bind("<Return>" , self.view_img2)

        self.btn_add_sup = ttk.Button(self.main_frame , state = con.DISABLED ,text = " Add "  , style = "window_btn_medium.TButton" , command = lambda : self.show_top_sup(None))
        self.btn_add_sup.bind("<Return>" , self.show_top_sup)

        self.combo_unit = ttk.Combobox(self.main_frame , state = con.DISABLED , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 6 , values = ['N' , 'KG' , 'G' , 'M']) 
        self.combo_unit.bind("<FocusOut>" , self.combo_entry_out)

        self.combo_tax1 = ttk.Combobox(self.main_frame  , values = self.gst_values ,state = con.DISABLED, font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 6 ) 
        self.combo_tax1.bind("<FocusOut>" , self.combo_entry_out)

        self.combo_tax2 = ttk.Combobox(self.main_frame  ,values = self.cess_values, state = con.DISABLED, font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 6) 
        self.combo_tax2.bind("<FocusOut>" , self.combo_entry_out)


        self.ent_mrp1 = ttk.Entry(self.main_frame , state = con.DISABLED , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_mrp1.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_mrp2 = ttk.Entry(self.main_frame , state = con.DISABLED , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_mrp2.bind("<FocusOut>" , self.combo_entry_out)

        self.frm_nrm = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.ent_nrm1 = ttk.Entry(self.frm_nrm  , state = con.DISABLED, width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_nrm1.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_nrm2 = ttk.Entry(self.frm_nrm  , state = con.DISABLED, width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_nrm2.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_nrm3 = ttk.Entry(self.frm_nrm , state = con.DISABLED , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_nrm3.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_nrm4 = ttk.Entry(self.frm_nrm  , state = con.DISABLED, width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_nrm4.bind("<FocusOut>" , self.combo_entry_out)

        self.frm_htl = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.chk_htl = ttk.Checkbutton(self.frm_htl  , state = con.DISABLED, style = "window_check.TCheckbutton")
        self.ent_htl1 = ttk.Entry(self.frm_htl  , state = con.DISABLED, width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_htl1.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_htl2 = ttk.Entry(self.frm_htl  , state = con.DISABLED, width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_htl2.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_htl3 = ttk.Entry(self.frm_htl , state = con.DISABLED , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_htl3.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_htl4 = ttk.Entry(self.frm_htl , state = con.DISABLED , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_htl4.bind("<FocusOut>" , self.combo_entry_out)


        self.frm_spl = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.chk_spl = ttk.Checkbutton(self.frm_spl , state = con.DISABLED , style = "window_check.TCheckbutton")
        self.ent_spl1 = ttk.Entry(self.frm_spl , state = con.DISABLED , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_spl1.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_spl2 = ttk.Entry(self.frm_spl , state = con.DISABLED , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_spl2.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_spl3 = ttk.Entry(self.frm_spl  , state = con.DISABLED, width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_spl3.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_spl4 = ttk.Entry(self.frm_spl , state = con.DISABLED , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_spl4.bind("<FocusOut>" , self.combo_entry_out)



        self.frm_ang = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.chk_ang = ttk.Checkbutton(self.frm_ang  , state = con.DISABLED, style = "window_check.TCheckbutton")
        self.ent_ang1 = ttk.Entry(self.frm_ang , state = con.DISABLED , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_ang1.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_ang2 = ttk.Entry(self.frm_ang , state = con.DISABLED , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_ang2.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_ang3 = ttk.Entry(self.frm_ang , state = con.DISABLED , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_ang3.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_ang4 = ttk.Entry(self.frm_ang , state = con.DISABLED , width = 7 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[5], '%P'))
        self.ent_ang4.bind("<FocusOut>" , self.combo_entry_out)

        self.ent_desc = Text(self.main_frame , state = con.DISABLED , width = 30 , height = 4 ,  font = ('Lucida Grande' , -int(self.main_hgt*0.03)) )
        self.chk_hide = ttk.Checkbutton(self.main_frame , state = con.DISABLED , style = "window_check.TCheckbutton" , text = "HIDE" , variable = self.check_state , onvalue = 'True' , offvalue = 'False')



        if root.winfo_screenheight()>1000:
            self.tree_frame = ttk.Frame(self.main_frame , height = int(self.main_hgt*0.844) , width = int(self.main_wdt*0.45) , style = "root_menu.TFrame")
        else:
            self.tree_frame = ttk.Frame(self.main_frame , height = int(self.main_hgt*0.858) , width = int(self.main_wdt*0.46) , style = "root_menu.TFrame")
        self.tree_frame.pack_propagate(False)
        self.tree_frame.grid_propagate(False)

        self.frm_chk_cat = ttk.Frame(self.tree_frame , style = "root_main.TFrame")
        self.chk_cat = ttk.Checkbutton(self.frm_chk_cat , text = "Category :" , style = "window_check.TCheckbutton" , variable = self.cat_state , onvalue = 'True' , offvalue = 'False')
        self.combo_cat1 = ttk.Combobox(self.frm_chk_cat  , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 22 , style = "window_combo.TCombobox") 
        self.combo_cat1.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_cat1.bind('<Down>', self.add_search_cats)
        self.combo_cat1.bind('<Button-1>', self.add_search_cats)
        self.combo_cat1.bind('<<ComboboxSelected>>', self.product_list)
        #self.combo_cat1.bind("<KeyRelease>" , self.restrict_entry)

        self.combo_cat2 = ttk.Combobox(self.frm_chk_cat  , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 22) 
        self.combo_cat2.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_cat2.bind('<Down>', self.add_search_cats)
        self.combo_cat2.bind('<Button-1>', self.add_search_cats)
        self.combo_cat2.bind('<<ComboboxSelected>>', self.product_list)

        self.frm_chk_sup = ttk.Frame(self.tree_frame , style = "root_main.TFrame")
        self.chk_sup = ttk.Checkbutton(self.frm_chk_sup , text = "Supplier :" , style = "window_check.TCheckbutton", variable = self.sup_state , onvalue = 'True' , offvalue = 'False')
        self.combo_sup1 = ttk.Combobox(self.frm_chk_sup  , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 22) 
        self.combo_sup1.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_sup1.bind('<Down>', self.add_search_sup)
        self.combo_sup1.bind('<Button-1>', self.add_search_sup)
        self.combo_sup1.bind('<<ComboboxSelected>>', self.product_list)

        self.combo_sup2 = ttk.Combobox(self.frm_chk_sup  , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 22) 
        self.combo_sup2.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_sup2.bind('<Down>', self.add_search_sup)
        self.combo_sup2.bind('<Button-1>', self.add_search_sup)
        self.combo_sup2.bind('<<ComboboxSelected>>', self.product_list)
        

        self.frm_prod_search = ttk.Frame(self.tree_frame , style = "root_main.TFrame")
        self.ent_prod_search = ttk.Entry(self.frm_prod_search  , width = 47 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[4], '%P'))
        self.ent_prod_search.bind('<FocusOut>', self.combo_entry_out)
        self.ent_prod_search.bind('<Return>', self.product_list)
        self.lbl_prod_search = ttk.Label(self.frm_prod_search , text = " Product  :" , style = "window_text_medium.TLabel")


        self.tree = ttk.Treeview(self.tree_frame ,selectmode = "browse", takefocus = True , show = "headings" , style = "window.Treeview")
        self.tree.tag_configure('a' , background = "#333333" , foreground = "#D9CC9C")
        self.tree.tag_configure('b' , background = "#282828" , foreground = "#D9CC9C")
        self.scroll_y = ttk.Scrollbar(self.tree_frame , orient = con.VERTICAL , command = self.tree.yview)
        self.scroll_x = ttk.Scrollbar(self.tree_frame , orient = con.HORIZONTAL , command = self.tree.xview)
        self.tree.config(yscrollcommand = self.scroll_y.set , xscrollcommand = self.scroll_x.set)

        

        self.tree['columns'] = ('hide','name')
        self.tree.heading('hide' , text = 'Hide')
        self.tree.heading('name' , text = 'Name')
        
        self.tree.bind('<Double-Button-1>',self.select_tree)
        self.tree.bind('<Return>',self.select_tree)

        self.chk_copy = ttk.Checkbutton(self.main_frame , variable = self.check_all , onvalue = 'True' , offvalue = 'False', text = "Copy all entries" , style = "window_check.TCheckbutton")
        self.check_all.set("False")

        self.btn_frame = ttk.Frame(self.main_frame , style = "root_main.TFrame")
        self.btn_new = ttk.Button(self.btn_frame , text = "New" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.new(None))
        self.btn_new.bind("<Return>" , self.new) 
        self.btn_edit = ttk.Button(self.btn_frame , text = "Edit" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.edit(None))
        self.btn_edit.bind("<Return>" , self.edit)
        self.btn_save = ttk.Button(self.btn_frame , text = "Save" , width = 6 , style = "window_btn_medium.TButton" ,command = lambda : self.save(None))
        self.btn_save.bind("<Return>" , self.save)
        self.btn_refresh = ttk.Button(self.btn_frame , text = "Refresh" , width = 7 , style = "window_btn_medium.TButton" ,command = lambda : self.refresh(None))
        self.btn_refresh.bind("<Return>" , self.refresh)


        self.lbl_bar.grid(row = 0 , column = 0  , pady = int(self.main_hgt*0.01))
        self.lbl_name.grid(row = 1 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_hsn.grid(row = 2 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_kan_txt.grid(row = 3 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_eng.grid(row = 5 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_min_qty.grid(row = 6 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_img1_txt.grid(row = 7 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_img2_txt.grid(row = 8 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_sup.grid(row = 9 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_tax1.grid(row = 10 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_mrp1.grid(row = 11 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_nrm.grid(row = 12 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_htl.grid(row = 13 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_spl.grid(row = 14 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_ang.grid(row = 15 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_desc.grid(row = 16 , column = 0 , rowspan = 2 , pady = int(self.main_hgt*0.01))


        self.btn_add_bar.grid(row = 0 , column = 1 , sticky= con.W)
        self.lbl_cat.grid(row = 0 , column = 2 , sticky = con.E)
        self.btn_add_cat.grid(row = 0 , column = 3)
        self.ent_name.grid(row = 1 , column = 1 , columnspan = 3)
        self.ent_hsn.grid(row = 2 , column = 1 , sticky = con.W)
        self.lbl_shelf.grid(row = 2 , column = 2 , sticky = con.E)
        self.ent_shelf.grid(row = 2 , column = 3 )
        self.lbl_kan.grid(row = 3 , column = 1 , columnspan = 3)
        #self.btn_kan_add.grid(row = 4 , column = 1 , sticky = con.W)
        self.btn_kan_brw.grid(row = 3 , column = 6 )
        self.btn_kan_vw .grid(row = 3 , column = 7 )
        self.ent_name_eng.grid(row = 5 , column = 1 , columnspan = 3)
        self.ent_min_qty.grid(row = 6 , column = 1 , sticky = con.W)
        self.lbl_exp.grid(row = 6 , column = 2 , sticky = con.E)
        self.ent_exp.grid(row = 6 , column = 3 , sticky = con.E)
        self.lbl_img1.grid(row = 7 , column = 1 , columnspan = 3)
        self.btn_img1_brw.grid(row = 7 , column = 6 , padx = int(self.main_wdt*0.01))
        self.btn_img1_vw.grid(row = 7 , column = 7 )
        self.lbl_img2.grid(row = 8 , column = 1 , columnspan = 3)
        self.btn_img2_brw.grid(row = 8 , column = 6 )
        self.btn_img2_vw.grid(row = 8 , column = 7 )
        self.btn_add_sup.grid(row = 9 , column = 1 , sticky = con.W)
        self.lbl_unit.grid(row = 9 , column = 2 , sticky = con.E)
        self.combo_unit.grid(row = 9 , column = 3 , sticky = con.E)
        self.chk_hide.grid(row = 9 , column = 5 , columnspan = 2 )
        self.combo_tax1.grid(row = 10 , column = 1 , sticky = con.W)
        self.lbl_tax2.grid(row = 10 , column = 2 , sticky = con.E)
        self.combo_tax2.grid(row = 10 , column = 3 , sticky = con.E)
        self.ent_mrp1.grid(row = 11 , column = 1 , sticky = con.W)
        self.lbl_mrp2.grid(row = 11 , column = 2 , sticky = con.E)
        self.ent_mrp2.grid(row = 11 , column = 3 , sticky = con.E)

        self.frm_nrm.grid(row = 12 , column = 1 , columnspan = 7 , sticky = con.W)
        self.ent_nrm1.grid(row = 0, column = 1)
        self.ent_nrm2.grid(row = 0, column = 2)
        self.ent_nrm3.grid(row = 0, column = 3)
        self.ent_nrm4.grid(row = 0, column = 4)
        
        self.frm_htl.grid(row = 13 , column = 1 , columnspan = 7, sticky = con.W)
        self.ent_htl1.grid(row = 0, column = 1)
        self.ent_htl2.grid(row = 0, column = 2)
        self.ent_htl3.grid(row = 0, column = 3)
        self.ent_htl4.grid(row = 0, column = 4)
        self.chk_htl.grid(row = 0, column = 5 , padx = int(self.main_wdt*0.01))

        self.frm_spl.grid(row = 14 , column = 1 , columnspan = 7, sticky = con.W)
        self.ent_spl1.grid(row = 0, column = 1)
        self.ent_spl2.grid(row = 0, column = 2)
        self.ent_spl3.grid(row = 0, column = 3)
        self.ent_spl4.grid(row = 0, column = 4)
        self.chk_spl.grid(row = 0, column = 5 , padx = int(self.main_wdt*0.01))

        self.frm_ang.grid(row = 15 , column = 1 , columnspan = 7, sticky = con.W)
        self.ent_ang1.grid(row = 0, column = 1)
        self.ent_ang2.grid(row = 0, column = 2)
        self.ent_ang3.grid(row = 0, column = 3)
        self.ent_ang4.grid(row = 0, column = 4)
        self.chk_ang.grid(row = 0, column = 5 , padx = int(self.main_wdt*0.01))

        self.ent_desc.grid(row = 16 , column = 1 , columnspan = 3 , rowspan = 2)

        self.tree_frame.grid(row = 0 , column = 8 , rowspan = 17 , columnspan = 2, padx = int(self.main_wdt*0.01) , pady = int(self.main_hgt*0.01))
        self.frm_chk_cat.pack()
        self.chk_cat.grid(row = 0, column = 1)
        self.combo_cat1.grid(row = 0, column = 2, padx = int(self.main_wdt*0.002))
        self.combo_cat2.grid(row = 0, column = 3)
        self.frm_chk_sup.pack()
        self.chk_sup.grid(row = 0, column = 1)
        self.combo_sup1.grid(row = 0, column = 2, padx = int(self.main_wdt*0.002) , pady = int(self.main_hgt*0.005))
        self.combo_sup2.grid(row = 0, column = 3)
        self.frm_prod_search.pack()
        self.lbl_prod_search.grid(row = 0, column = 0 , sticky = con.W)
        self.ent_prod_search.grid(row = 0 , column = 1)

        self.scroll_y.pack(anchor = con.E , side = con.RIGHT , fill = con.Y)
        self.scroll_x.pack(anchor = con.S , side = con.BOTTOM , fill = con.X)
        self.tree.pack(anchor = con.N , side = con.LEFT , fill = con.BOTH)

        self.chk_copy.grid(row = 17 , column = 8 , padx = int(self.main_wdt*0.01), sticky = con.W)
        self.btn_frame.grid(row = 17 ,column = 9 , sticky = con.E)
        self.btn_new.grid(row = 0 , column = 0 , padx = int(self.main_wdt*0.01))
        self.btn_edit.grid(row = 0 , column = 1 , padx = int(self.main_wdt*0.01))
        self.btn_save.grid(row = 0 , column = 2 , padx = int(self.main_wdt*0.01))
        self.btn_refresh.grid(row = 0 , column = 3 , padx = int(self.main_wdt*0.01))
       

        self.tree_wdt = self.tree_frame.winfo_reqwidth()-self.scroll_y.winfo_reqwidth()
        
        self.tree.column('hide' , width = int(self.tree_wdt*0.2) ,minwidth = int(self.tree_wdt*0.2) , anchor = "w")
        self.tree.column('name' , width = int(self.tree_wdt*0.80) , minwidth = int(self.tree_wdt*0.80) , anchor = "w")


        """===================pop up window to get set barcodes================================="""
        self.frm_barcode = ttk.Frame( self.root_frame , height = self.main_hgt*0.3 , width = self.main_wdt*0.3  , style = "root_menu.TFrame")
        self.frm_barcode.pack_propagate(False)
        self.btn_gen_bar = ttk.Button(self.frm_barcode , text = "Genarate Barcode" , state = con.DISABLED , style = "window_btn_medium.TButton" ,command = lambda : self.generate(None))
        self.btn_gen_bar.bind("<Escape>" , self.destroy_top_bar)
        self.btn_gen_bar.bind("<Return>" , self.generate)

        self.ent_bar1 = ttk.Entry(self.frm_barcode  , state = con.DISABLED,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[3], '%P'))
        self.ent_bar1.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_bar1.bind("<Escape>" , self.destroy_top_bar)
        self.ent_bar2 = ttk.Entry(self.frm_barcode   , state = con.DISABLED,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[3], '%P'))
        self.ent_bar2.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_bar2.bind("<Escape>" , self.destroy_top_bar)
        self.ent_bar3 = ttk.Entry(self.frm_barcode   , state = con.DISABLED,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[3], '%P'))
        self.ent_bar3.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_bar3.bind("<Escape>" , self.destroy_top_bar)
        self.ent_bar4 = ttk.Entry(self.frm_barcode   , state = con.DISABLED,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[3], '%P'))
        self.ent_bar4.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_bar4.bind("<Escape>" , self.destroy_top_bar)


        self.btn_gen_bar.pack()
        self.ent_bar1.pack( fill = con.BOTH , padx = self.main_wdt*0.01 , pady = self.main_hgt*0.01)
        self.ent_bar2.pack( fill = con.BOTH , padx = self.main_wdt*0.01 , pady = self.main_hgt*0.01)
        self.ent_bar3.pack( fill = con.BOTH , padx = self.main_wdt*0.01 , pady = self.main_hgt*0.01)
        self.ent_bar4.pack( fill = con.BOTH , padx = self.main_wdt*0.01 , pady = self.main_hgt*0.01)
        """===================pop up window to get set barcodes ends================================="""



        """===================pop up window to get set categories================================="""
        self.frm_category = ttk.Frame( self.root_frame , height = self.main_hgt*0.3 , width = self.main_wdt*0.3  , style = "root_menu.TFrame")
        self.frm_category.pack_propagate(False)

        self.lbl_top_cat = ttk.Label(self.frm_category , text = "Add Category from drop down" , style = "window_text_large.TLabel")
        self.combo_category = ttk.Combobox(self.frm_category , validate="key", validatecommand=(validations[4], '%P') , state = con.DISABLED, font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 22 , style = "window_combo.TCombobox") 
        self.combo_category.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_category.bind('<<ComboboxSelected>>', self.add_categories)
        self.combo_category.bind("<Down>" , self.get_categories)
        self.combo_category.bind("<Button-1>" , self.get_categories)
        self.combo_category.bind("<Escape>" , self.destroy_top_cat)
        
        self.ent_cat1 = ttk.Entry(self.frm_category , state = con.DISABLED  ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) )
        self.ent_cat1.bind("<KeyRelease>" , self.restrict_entry)
        self.ent_cat1.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_cat1.bind("<Escape>" , self.destroy_top_cat)
        self.ent_cat2 = ttk.Entry(self.frm_category , state = con.DISABLED ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)))
        self.ent_cat2.bind("<KeyRelease>" , self.restrict_entry)
        self.ent_cat2.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_cat2.bind("<Escape>" , self.destroy_top_cat)
        self.ent_cat3 = ttk.Entry(self.frm_category , state = con.DISABLED,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)))
        self.ent_cat3.bind("<KeyRelease>" , self.restrict_entry)
        self.ent_cat3.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_cat3.bind("<Escape>" , self.destroy_top_cat)
        
        self.lbl_top_cat.pack()
        self.combo_category.pack( fill = con.BOTH , padx = self.main_wdt*0.01 , pady = self.main_hgt*0.01)
        self.ent_cat1.pack( fill = con.BOTH , padx = self.main_wdt*0.01 , pady = self.main_hgt*0.01)
        self.ent_cat2.pack( fill = con.BOTH , padx = self.main_wdt*0.01 , pady = self.main_hgt*0.01)
        self.ent_cat3.pack( fill = con.BOTH , padx = self.main_wdt*0.01 , pady = self.main_hgt*0.01)
        """===================pop up window to get set categories ends================================="""



        """===================pop up window to get set categories================================="""
        self.frm_supplier = ttk.Frame( self.root_frame , height = self.main_hgt*0.3 , width = self.main_wdt*0.3  , style = "root_menu.TFrame")
        self.frm_supplier.pack_propagate(False)

        self.lbl_top_supp = ttk.Label(self.frm_supplier , text = "Add Supplier from drop down" , style = "window_text_large.TLabel")
        self.combo_supplier = ttk.Combobox(self.frm_supplier , validate="key", validatecommand=(validations[4], '%P') , state = con.DISABLED , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , width = 22 , style = "window_combo.TCombobox") 
        self.combo_supplier.bind("<FocusOut>" , self.combo_entry_out)
        self.combo_supplier.bind('<<ComboboxSelected>>', self.add_suppliers)
        self.combo_supplier.bind("<Down>" , self.get_suppliers)
        self.combo_supplier.bind("<Button-1>" , self.get_suppliers)
        self.combo_supplier.bind("<Escape>" , self.destroy_top_sup)
        

        self.ent_sup1 = ttk.Entry(self.frm_supplier , state = con.DISABLED  ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_sup1.bind("<KeyRelease>" , self.restrict_entry)
        self.ent_sup1.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_sup1.bind("<Escape>" , self.destroy_top_sup)
        self.ent_sup2 = ttk.Entry(self.frm_supplier, state = con.DISABLED  ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_sup2.bind("<KeyRelease>" , self.restrict_entry)
        self.ent_sup2.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_sup2.bind("<Escape>" , self.destroy_top_sup)
        self.ent_sup3 = ttk.Entry(self.frm_supplier , state = con.DISABLED,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_sup3.bind("<KeyRelease>" , self.restrict_entry)
        self.ent_sup3.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_sup3.bind("<Escape>" , self.destroy_top_sup)
        
        self.lbl_top_supp.pack()
        self.combo_supplier.pack( fill = con.BOTH , padx = self.main_wdt*0.01 , pady = self.main_hgt*0.01)
        self.ent_sup1.pack( fill = con.BOTH , padx = self.main_wdt*0.01 , pady = self.main_hgt*0.01)
        self.ent_sup2.pack( fill = con.BOTH , padx = self.main_wdt*0.01 , pady = self.main_hgt*0.01)
        self.ent_sup3.pack( fill = con.BOTH , padx = self.main_wdt*0.01 , pady = self.main_hgt*0.01)
        """===================pop up window to get set categories ends================================="""

        self.product_list(None)
        self.btn_new.focus_set()

    def combo_entry_out(self , e):
        e.widget.select_clear()
    
    def restrict_entry(self , e):
        e.widget.delete(0,con.END)



    """Barcode entry functions"""
    def show_top_bar(self,e):
        self.frm_barcode.place( x = self.main_wdt*0.4 , y = self.main_hgt*0.4)
        #moveTo(self.main_wdt*0.4 + self.main_wdt*0.15 , self.main_hgt*0.4 + self.main_hgt*0.2)
        #self.ent_bar1.focus_set()
        self.btn_gen_bar.focus_set()
        self.frm_barcode.lift()

        generated_bar = False

        bar1 = self.ent_bar1.get().upper()
        

        #to check if barcode is already generated 
        #if generated disable gen_barcode btn 
        if bar1 != "":
            if bar1[0] == 'S':
                try:
                    int(bar1[1:])
                    generated_bar = True
                except ValueError:
                    generated_bar = False

        if generated_bar:
            self.btn_gen_bar.config(state = con.DISABLED)
        else:
            self.btn_gen_bar.config(state = con.NORMAL)

    def destroy_top_bar(self , e):

        bar1 = self.ent_bar1.get().upper()
        bar2 = self.ent_bar2.get().upper()
        bar3 = self.ent_bar3.get().upper()
        bar4 = self.ent_bar4.get().upper()


        #removes " "
        temp = ""
        bar1 = bar1.split()
        for each in bar1:
            temp += each
        bar1 = temp

        temp = ""
        bar2 = bar2.split()
        for each in bar2:
            temp += each
        bar2 = temp
        
        temp = ""
        bar3 = bar3.split()
        for each in bar3:
            temp += each
        bar3 = temp

        temp = ""
        bar4 = bar4.split()
        for each in bar4:
            temp += each
        bar4 = temp
        #removal "" ends here

        #checks for s[0-9]
        if bar1 != "":
            if bar1[0] == 'S':
                try:
                    int(bar1[1:])
                    barGenerated = True
                except ValueError:
                    msg.showerror("Error","Barcode Contains Letter 'S'\nGenerate Barcode")
                    self.ent_bar1.select_range(0,con.END)
                    self.ent_bar1.focus_set()
                    return
            
        if bar2 != "":
            if bar2[0] == 'S':
                try:
                    int(bar2[1:])
                except ValueError:
                    msg.showerror("Error","Barcode Contains Letter 'S'\nGenerate Barcode")
                    self.ent_bar2.select_range(0,con.END)
                    self.ent_bar2.focus_set()
                    return

        if bar3 != "":
            if bar3[0] == 'S':
                try:
                    int(bar3[1:])
                except ValueError:
                    msg.showerror("Error","Barcode Contains Letter 'S'\nGenerate Barcode")
                    self.ent_bar3.select_range(0,con.END)
                    self.ent_bar3.focus_set()
                    return

        if bar4 != "":
            if bar4[0] == 'S':
                try:
                    int(bar4[1:])
                except ValueError:
                    msg.showerror("Error","Barcode Contains Letter 'S'\nGenerate Barcode")
                    self.ent_bar4.select_range(0,con.END)
                    self.ent_bar4.focus_set()
                    return
        #pattern check ends here

        #check if barcodes exists
        
        sql = "select prod_id,prod_name from somanath.products where prod_bar regexp ':"+ bar1 + ":'"
        if not self.new_state:                                                                                                              #when prod selected or edited
            sql += " and prod_id != "+str(self.selected_prod)
        
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            resp = req.json()
            if len(resp)>0:
                self.ent_bar1.focus_set()
                self.ent_bar1.select_range(0,con.END)
                msg.showinfo("Existing barcode" , "Barcode '" + bar1 + "' exists @:"+resp[0]['prod_name'])        
                return

        sql = "select prod_id,prod_name from somanath.products where prod_bar regexp ':"+ bar2 + ":'"
        if not self.new_state:
            sql += " and prod_id != "+str(self.selected_prod)
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            resp = req.json()
            if len(resp)>0:
                self.ent_bar2.focus_set()
                self.ent_bar2.select_range(0,con.END)
                msg.showinfo("Existing barcode" , "Barcode '" + bar2 + "' exists @:"+resp[0]['prod_name'])        
                return

        sql = "select prod_id,prod_name from somanath.products where prod_bar regexp ':"+ bar3 + ":'"
        if not self.new_state:
            sql += " and prod_id != "+str(self.selected_prod)
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            resp = req.json()
            if len(resp)>0:
                self.ent_bar3.focus_set()
                self.ent_bar3.select_range(0,con.END)
                msg.showinfo("Existing barcode" , "Barcode '" + bar3 + "' exists @:"+resp[0]['prod_name'])        
                return

        sql = "select prod_id,prod_name from somanath.products where prod_bar regexp ':"+ bar4 + ":'"
        if not self.new_state:
            sql += " and prod_id != "+str(self.selected_prod)
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            resp = req.json()
            if len(resp)>0:
                self.ent_bar4.focus_set()
                self.ent_bar4.select_range(0,con.END)
                msg.showinfo("Existing barcode" , "Barcode '" + bar4 + "' exists @:"+resp[0]['prod_name'])        
                return



        barcodes = []
        temp = [bar1 , bar2 , bar3 , bar4]
        for each in temp:
            if each not in barcodes:
                barcodes.append(each)    
            
        

        """if barGenerated:
            req = post("http://"+self.ip+":6000/barcodes" , params = {'type' : 'update' , 'barcode' : self.generated_bar})"""

        

        self.frm_barcode.place_forget()
        self.btn_add_cat.focus_set()

    def generate(self,e):
        
        req = post("http://"+self.ip+":6000/barcodes" , params = {'type' : 'get'})
        max_bar = req.json()
        self.generated_bar = int(max_bar)
        barcode = "S"+str("{:05d}".format(int(max_bar)))
            
        
        if self.ent_bar1.get() == "":
            self.ent_bar1.insert(0 , barcode)
        else:
            msg.showinfo("Error" , "Clear Barcode 1 to generate")
            self.ent_bar1.select_range(0,con.END)
            self.ent_bar1.focus_set()
            return



        self.btn_gen_bar.config(state = con.DISABLED)
    """Barcode entry ends here"""




    """Category entry functions"""
    def show_top_cat(self,e):
        self.frm_category.place( x = self.main_wdt*0.4 , y = self.main_hgt*0.4)
        #moveTo(self.main_wdt*0.4 + self.main_wdt*0.15 , self.main_hgt*0.4 + self.main_hgt*0.2)
        self.combo_category.focus_set()
        self.combo_category.delete(0,con.END)
        self.frm_category.lift()

    def destroy_top_cat(self , e):
        self.frm_category.place_forget()
        self.ent_name.focus_set()

    def get_categories(self,e):
        text = self.combo_category.get()
        if text == "":
            sql = "select cat_name from somanath.categories order by cat_name"
        else:
            sql = "select cat_name from somanath.categories where cat_name regexp '"+text+"' order by cat_name"
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            resp = req.json()
            values = []
            for each in resp:
                values.append(each['cat_name'])

            self.combo_category.config(values = values)

    def add_categories(self,e):
        category = self.combo_category.get()
        self.combo_category.delete(0,con.END)

        cat1 = self.ent_cat1.get()
        cat2 = self.ent_cat2.get()
        cat3 = self.ent_cat3.get()

        selected_categories = [cat1 , cat2 , cat3]

        if category in selected_categories:
            return

        if cat1 == "":
            self.ent_cat1.insert(0,category)
        elif cat2 == "":
            self.ent_cat2.insert(0,category)
        elif cat3 == "":
            self.ent_cat3.insert(0,category)
        else:
            msg.showinfo("Error" , "Empty any of the categories")
            return
    """category entry functions ends here"""






    """supplier entry functions"""
    def show_top_sup(self,e):
        self.frm_supplier.place( x = self.main_wdt*0.4 , y = self.main_hgt*0.4)
        #moveTo(self.main_wdt*0.4 + self.main_wdt*0.15 , self.main_hgt*0.4 + self.main_hgt*0.2)
        self.combo_supplier.focus_set()
        self.combo_supplier.delete(0,con.END)
        self.frm_supplier.lift()

    def destroy_top_sup(self , e):
        self.frm_supplier.place_forget()
        self.combo_unit.focus_set()

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

    def add_suppliers(self,e):
        supplier = self.combo_supplier.get()
        self.combo_supplier.delete(0,con.END)
        


        sup1 = self.ent_sup1.get()
        sup2 = self.ent_sup2.get()
        sup3 = self.ent_sup3.get()

        selected_suppliers = [sup1 , sup2 , sup3]

        if supplier in selected_suppliers:
            return

        if sup1 == "":
            self.ent_sup1.insert(0,supplier)
        elif sup2 == "":
            self.ent_sup2.insert(0,supplier)
        elif sup3 == "":
            self.ent_sup3.insert(0,supplier)
        else:
            msg.showinfo("Error" , "Empty any of the categories")
            return
    """supplier entry functions ends here"""
    


    """image editing functions"""
    def file_dialog_kan(self , e):
        file = filedialog.askopenfilename(initialdir = self.homeDir+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        if file!= "":
            ext = file.split(".")[-1]
            if ext != 'jpg' and ext != 'png' and ext != 'jpeg' and ext != 'bmp':
                msg.showerror("error","Select only images \n (eg :- *.png or *.jpg or *.bmp or *.jpeg)")
                return
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]

            self.lbl_kan.config(text = text)
            self.img_kan = ImageTk.PhotoImage(Image.open(file))
            
        else:
            
            self.lbl_kan.config(text = "")
        self.img_kan_loc = file

    def view_kan(self , e):
        if self.img_kan_loc != None or self.lbl_kan.cget("text") != "":
            image_viewer(self.img_kan,"Kannada Image" ,  self.root_frame)
   
    def file_dialog_img1(self , e):
        file = filedialog.askopenfilename(initialdir = self.homeDir+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        if file!= "":
            ext = file.split(".")[-1]
            if ext != 'jpg' and ext != 'png' and ext != 'jpeg' and ext != 'bmp':
                msg.showerror("error","Select only images \n (eg :- *.png or *.jpg or *.bmp or *.jpeg)")
                return
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]

            self.lbl_img1.config(text = text)
            self.img_high = ImageTk.PhotoImage(Image.open(file))
        else:
            self.lbl_img1.config(text = "")
        self.img_high_loc = file

    def view_img1(self , e):
        if self.img_high != None or self.lbl_img1.cget("text") != "":
            image_viewer(self.img_high_loc,"High Quality Image" , self.root_frame)

    def file_dialog_img2(self , e):
        file = filedialog.askopenfilename(initialdir = self.homeDir+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        if file!= "":
            ext = file.split(".")[-1]
            if ext != 'jpg' and ext != 'png' and ext != 'jpeg' and ext != 'bmp':
                msg.showerror("error","Select only images \n (eg :- *.png or *.jpg or *.bmp or *.jpeg)")
                return
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]

            self.lbl_img2.config(text = text)
            self.img_low = ImageTk.PhotoImage(Image.open(file))
        else:
            self.lbl_img2.config(text = "")
        self.img_low_loc = file

    def view_img2(self , e):
        if self.img_low != None or self.lbl_img2.cget("text") != "":
            image_viewer(self.img_low,"Low Quality Image" , self.root_frame)
    """image editing ends here"""

    def check_name(self, e):
        self.ent_name.select_clear()
        name = self.ent_name.get().upper()
        temp = name.split()
        name = ""

        i = 0
        for each in temp:
            if i == 0:
                name += each
            else:
                name += " "+each
            i+=1

        
        sql = "select prod_name from somanath.products where prod_name = '"+ name +"'"
        
        if not self.new_state:
            sql += " and prod_id != "+ str(self.selected_prod)
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            if len(req.json())>0:
                msg.showinfo("Error" , "This product name exists")
                self.ent_name.select_range(0 , con.END)
                self.ent_name.focus_set()
                return


        self.ent_name.delete(0,con.END)
        self.ent_name.insert(0,name)

    def enable_all(self):

        
        self.btn_add_bar.config(state = con.NORMAL)
        self.btn_add_cat.config(state = con.NORMAL)
        self.ent_name.config(state = con.NORMAL)
        self.ent_hsn.config(state = con.NORMAL)
        self.ent_shelf.config(state = con.NORMAL)
        #self.btn_kan_add.config(state = con.NORMAL)
        self.btn_kan_brw.config(state = con.NORMAL)
        self.btn_kan_vw .config(state = con.NORMAL)
        self.ent_name_eng.config(state = con.NORMAL)
        self.ent_min_qty.config(state = con.NORMAL)
        self.ent_exp.config(state = con.NORMAL)
        self.btn_img1_brw.config(state = con.NORMAL)
        self.btn_img1_vw.config(state = con.NORMAL)
        self.btn_img2_brw.config(state = con.NORMAL)
        self.btn_img2_vw.config(state = con.NORMAL)
        self.btn_add_sup.config(state = con.NORMAL)
        self.combo_unit.config(state = "readonly")
        self.chk_hide.config(state = con.NORMAL)
        self.combo_tax1.config(state = "readonly")
        self.combo_tax2.config(state = "readonly")
        self.ent_mrp1.config(state = con.NORMAL)
        self.ent_mrp2.config(state = con.NORMAL)

        self.ent_nrm1.config(state = con.NORMAL)
        self.ent_nrm2.config(state = con.NORMAL)
        self.ent_nrm3.config(state = con.NORMAL)
        self.ent_nrm4.config(state = con.NORMAL)
        
        self.ent_htl1.config(state = con.NORMAL)
        self.ent_htl2.config(state = con.NORMAL)
        self.ent_htl3.config(state = con.NORMAL)
        self.ent_htl4.config(state = con.NORMAL)
        self.chk_htl.config(state = con.NORMAL)

        self.ent_ang1.config(state = con.NORMAL)
        self.ent_ang2.config(state = con.NORMAL)
        self.ent_ang3.config(state = con.NORMAL)
        self.ent_ang4.config(state = con.NORMAL)
        self.chk_ang.config(state = con.NORMAL)

        self.ent_spl1.config(state = con.NORMAL)
        self.ent_spl2.config(state = con.NORMAL)
        self.ent_spl3.config(state = con.NORMAL)
        self.ent_spl4.config(state = con.NORMAL)
        self.chk_spl.config(state = con.NORMAL)
        self.ent_desc.config(state = con.NORMAL)



        
        self.ent_bar1.config(state = con.NORMAL)
        self.ent_bar2.config(state = con.NORMAL)
        self.ent_bar3.config(state = con.NORMAL)
        self.ent_bar4.config(state = con.NORMAL)

        self.combo_category.config(state = con.NORMAL)
        self.ent_cat1.config(state = con.NORMAL)
        self.ent_cat2.config(state = con.NORMAL)
        self.ent_cat3.config(state = con.NORMAL)

        self.combo_supplier.config(state = con.NORMAL)
        self.ent_sup1.config(state = con.NORMAL)
        self.ent_sup2.config(state = con.NORMAL)
        self.ent_sup3.config(state = con.NORMAL)
        
    def clear_all(self):
        self.img_kan = None                                                                             
        self.img_high = None                                                                       
        self.img_low = None
        self.img_kan_loc = ""                                                                          
        self.img_high_loc = ""
        self.img_low_loc = ""
        self.selected_prod = -1
        self.generated_bar = None

        self.lbl_img1.config(text = "")
        self.lbl_img2.config(text = "")
        self.lbl_kan.config(text = "")

        self.ent_name.delete(0,con.END)
        self.ent_hsn.delete(0,con.END)
        self.ent_shelf.delete(0,con.END)
        self.ent_name_eng.delete(0,con.END)
        self.ent_min_qty.delete(0,con.END)
        self.ent_exp.delete(0,con.END)
        self.combo_unit.config(state = con.NORMAL)
        self.combo_unit.delete(0,con.END)
        self.combo_unit.config(state = "readonly")

        if self.chk_hide.instate(['selected']) == True:
            self.chk_hide.invoke()
        
        self.combo_tax1.config(state = con.NORMAL)
        self.combo_tax1.delete(0,con.END)
        self.combo_tax1.config(state = "readonly")
        self.combo_tax2.config(state = con.NORMAL)
        self.combo_tax2.delete(0,con.END)
        self.combo_tax2.config(state = "readonly")
        self.ent_mrp1.delete(0,con.END)
        self.ent_mrp2.delete(0,con.END)

        self.ent_nrm1.delete(0,con.END)
        self.ent_nrm2.delete(0,con.END)
        self.ent_nrm3.delete(0,con.END)
        self.ent_nrm4.delete(0,con.END)
        
        self.ent_htl1.delete(0,con.END)
        self.ent_htl2.delete(0,con.END)
        self.ent_htl3.delete(0,con.END)
        self.ent_htl4.delete(0,con.END)
        if self.chk_htl.instate(['selected']) == True:
            self.chk_htl.invoke()

        self.ent_ang1.delete(0,con.END)
        self.ent_ang2.delete(0,con.END)
        self.ent_ang3.delete(0,con.END)
        self.ent_ang4.delete(0,con.END)
        if self.chk_ang.instate(['selected']) == True:
            self.chk_ang.invoke()

        self.ent_spl1.delete(0,con.END)
        self.ent_spl2.delete(0,con.END)
        self.ent_spl3.delete(0,con.END)
        self.ent_spl4.delete(0,con.END)
        if self.chk_spl.instate(['selected']) == True:
            self.chk_spl.invoke()

        self.ent_desc.delete(0.0,con.END)



        
        self.ent_bar1.delete(0,con.END)
        self.ent_bar2.delete(0,con.END)
        self.ent_bar3.delete(0,con.END)
        self.ent_bar4.delete(0,con.END)

        self.combo_category.delete(0,con.END)
        self.ent_cat1.delete(0,con.END)
        self.ent_cat2.delete(0,con.END)
        self.ent_cat3.delete(0,con.END)

        self.combo_supplier.delete(0,con.END)
        self.ent_sup1.delete(0,con.END)
        self.ent_sup2.delete(0,con.END)
        self.ent_sup3.delete(0,con.END)

    def disable_all(self):
        self.btn_add_bar.config(state = con.DISABLED)
        self.btn_add_cat.config(state = con.DISABLED)
        self.ent_name.config(state = con.DISABLED)
        self.ent_hsn.config(state = con.DISABLED)
        #self.btn_kan_add.config(state = con.DISABLED)
        self.ent_shelf.config(state = con.DISABLED)
        self.btn_kan_brw.config(state = con.DISABLED)
        self.btn_kan_vw .config(state = con.DISABLED)
        self.ent_name_eng.config(state = con.DISABLED)
        self.ent_min_qty.config(state = con.DISABLED)
        self.ent_exp.config(state = con.DISABLED)
        self.btn_img1_brw.config(state = con.DISABLED)
        self.btn_img1_vw.config(state = con.DISABLED)
        self.btn_img2_brw.config(state = con.DISABLED)
        self.btn_img2_vw.config(state = con.DISABLED)
        self.btn_add_sup.config(state = con.DISABLED)
        self.combo_unit.config(state = con.DISABLED)
        self.chk_hide.config(state = con.DISABLED)
        self.combo_tax1.config(state = con.DISABLED)
        self.combo_tax2.config(state = con.DISABLED)
        self.ent_mrp1.config(state = con.DISABLED)
        self.ent_mrp2.config(state = con.DISABLED)

        self.ent_nrm1.config(state = con.DISABLED)
        self.ent_nrm2.config(state = con.DISABLED)
        self.ent_nrm3.config(state = con.DISABLED)
        self.ent_nrm4.config(state = con.DISABLED)
        
        self.ent_htl1.config(state = con.DISABLED)
        self.ent_htl2.config(state = con.DISABLED)
        self.ent_htl3.config(state = con.DISABLED)
        self.ent_htl4.config(state = con.DISABLED)
        self.chk_htl.config(state = con.DISABLED)

        self.ent_ang1.config(state = con.DISABLED)
        self.ent_ang2.config(state = con.DISABLED)
        self.ent_ang3.config(state = con.DISABLED)
        self.ent_ang4.config(state = con.DISABLED)
        self.chk_ang.config(state = con.DISABLED)

        self.ent_spl1.config(state = con.DISABLED)
        self.ent_spl2.config(state = con.DISABLED)
        self.ent_spl3.config(state = con.DISABLED)
        self.ent_spl4.config(state = con.DISABLED)
        self.chk_spl.config(state = con.DISABLED)
        self.ent_desc.config(state = con.DISABLED)



        
        self.ent_bar1.config(state = con.DISABLED)
        self.ent_bar2.config(state = con.DISABLED)
        self.ent_bar3.config(state = con.DISABLED)
        self.ent_bar4.config(state = con.DISABLED)

        self.combo_category.config(state = con.DISABLED)
        self.ent_cat1.config(state = con.DISABLED)
        self.ent_cat2.config(state = con.DISABLED)
        self.ent_cat3.config(state = con.DISABLED)

        self.combo_supplier.config(state = con.DISABLED)
        self.ent_sup1.config(state = con.DISABLED)
        self.ent_sup2.config(state = con.DISABLED)
        self.ent_sup3.config(state = con.DISABLED)

    def new(self , e):
        self.new_state = True
        self.edit_state = False
        self.btn_new.config(state = con.DISABLED)
        self.btn_edit.config(state = con.DISABLED)
        self.btn_save.config(state = con.NORMAL)

        self.enable_all()
        if self.check_all == "False":
            self.clear_all()

        else:
            self.img_kan = None                                                                             
            self.img_high = None                                                                       
            self.img_low = None
            self.img_kan_loc = ""                                                                          
            self.img_high_loc = ""
            self.img_low_loc = ""
            self.selected_prod = -1
            self.generated_bar = None
            self.ent_bar1.delete(0,con.END)
            self.ent_bar2.delete(0,con.END)
            self.ent_bar3.delete(0,con.END)
            self.ent_bar4.delete(0,con.END)

        self.chk_hide.config(state = con.DISABLED)

        self.frm_barcode.place_forget()
        self.frm_category.place_forget()
        self.frm_supplier.place_forget()

        self.btn_add_bar.focus_set()

    def edit(self , e):
        self.btn_new.config(state = con.DISABLED)
        self.btn_edit.config(state = con.DISABLED)
        self.btn_save.config(state = con.NORMAL)

        self.new_state = False
        self.edit_state = True
    
        self.frm_barcode.place_forget()
        self.frm_category.place_forget()
        self.frm_supplier.place_forget()

        img_kan = self.lbl_kan.cget("text")
        img_high = self.lbl_img1.cget("text")
        img_low = self.lbl_img2.cget("text")

        prod_dir = os.path.join(self.homeDir,"Images" , "products")                                                     #delete all older firm images in the folder

        for f in os.listdir(prod_dir):
            os.remove(os.path.join(prod_dir, f))
    

        if img_kan != "":
            self.img_kan_loc = os.path.join(prod_dir , "kan." + img_kan.split(".")[-1])
            imgpil = ImageTk.getimage(self.img_kan)
            imgpil.save( self.img_kan_loc , img_kan.split(".")[-1])

        if img_high != "":
            self.img_high_loc = os.path.join(prod_dir , "high." + img_high.split(".")[-1])
            imgpil = ImageTk.getimage(self.img_high)
            imgpil.save( self.img_high_loc , img_high.split(".")[-1])
        
        if img_low != "":
            self.img_low_loc = os.path.join(prod_dir , "low." + img_low.split(".")[-1])
            imgpil = ImageTk.getimage(self.img_low)
            imgpil.save( self.img_low_loc , img_low.split(".")[-1])

        self.chk_hide.config(state = con.NORMAL)
        self.enable_all()

    def save(self , e):
        self.frm_barcode.place_forget()
        self.frm_category.place_forget()
        self.frm_supplier.place_forget()
        bar1 = self.ent_bar1.get().upper()
        bar2 = self.ent_bar2.get().upper()
        bar3 = self.ent_bar3.get().upper()
        bar4 = self.ent_bar4.get().upper()


        cat1 = self.ent_cat1.get().upper()
        cat2 = self.ent_cat2.get().upper()
        cat3 = self.ent_cat3.get().upper()

        sup1 = self.ent_sup1.get().upper()
        sup2 = self.ent_sup2.get().upper()
        sup3 = self.ent_sup3.get().upper()

        prod_name = self.ent_name.get().upper()
        hsn = self.ent_hsn.get().upper()
        shelf = self.ent_shelf.get().upper()
        name_eng = self.ent_name_eng.get().upper()
        min_qty  = self.ent_min_qty.get().upper()
        expiry = self.ent_exp.get().upper()
        unit = self.combo_unit.get().upper()
        gst = self.combo_tax1.get().upper()
        cess = self.combo_tax2.get().upper()
        mrp1 = self.ent_mrp1.get().upper()
        mrp2 = self.ent_mrp2.get().upper()

        if min_qty == "" : min_qty = "0"
        if expiry == "" : expiry = "0"


        if mrp1 == "" : mrp1 = "0.00"
        else : mrp1 = "{:.2f}".format(float(mrp1))
        
        if mrp2 == "" : mrp2 = "0.00"
        else : mrp2 = "{:.2f}".format(float(mrp2))

        nrm1 = self.ent_nrm1.get()
        nrm2 = self.ent_nrm2.get()
        nrm3 = self.ent_nrm3.get()
        nrm4 = self.ent_nrm4.get()

        desc = self.ent_desc.get(0.0 , con.END)
    
        if bar1 == "" and bar2 == "" and bar3 =="" and bar4 == "":
            msg.showerror("Error" , "Enter barcode")
            self.show_top_bar(None)
            return

        if cat1 == "" and cat2 == "" and cat3 =="":
            msg.showerror("Error" , "Enter category")
            self.show_top_cat(None)
            return

        if prod_name == "":
            msg.showinfo("Error" , "Add Name")
            self.ent_name.select_range(0,con.END)
            self.ent_name.focus_set()
            return


        if sup1 == "" and sup2 == "" and sup3 =="":
            msg.showerror("Error" , "Enter supplier")
            self.show_top_sup(None)
            return
        
        if unit == "":
            unit = 'N'

        if unit not in self.combo_unit['values']:
            msg.showinfo("Error" , "select unit from drop down")
            self.combo_unit.select_range(0,con.END)
            self.combo_unit.focus_set()
            return


        if gst == "":
            gst = 0
    
        if int(gst) not in self.gst_values:
            msg.showinfo("Error" , "select GST from drop down")
            self.combo_tax1.select_range(0,con.END)
            self.combo_tax1.focus_set()
            return

        

        if cess == "":
            cess = 0
        
        if int(cess) not in self.cess_values:
            msg.showinfo("Error" , "select CESS from drop down")
            self.combo_tax2.select_range(0,con.END)
            self.combo_tax2.focus_set()
            return

        if nrm1 =="":
            nrm1 = '1'

        # arranging units
        if nrm1 == "":
            msg.showinfo("Error" , "Enter NRM unit value")
            self.ent_nrm1.focus_set()
            return        

        if nrm2 == "":
            nrm2 = nrm1
            
        if nrm3 == "":
            nrm3 = nrm2
        
        if nrm4 == "":
            nrm4 = nrm3

        units_nrm = [round(float(nrm1) , 3) , round(float(nrm2) , 3) , round(float(nrm3) , 3) , round(float(nrm4) , 3)]
        if not units_nrm == sorted(units_nrm , key = float):
            msg.showerror("error" , "Enter NRM units in increasing order")
            return

        if self.chk_htl.instate(['selected']) == False:
            htl1 = self.ent_htl1.get()
            htl2 = self.ent_htl2.get()
            htl3 = self.ent_htl3.get()
            htl4 = self.ent_htl4.get()

            if htl1 == "":
                msg.showinfo("Error" , "Enter HTL unit value")
                self.ent_htl1.focus_set()
                return 
            if htl2 == "":
                htl2 = htl1
            
            if htl3 == "":
                htl3 = htl2
        
            if htl4 == "":
                htl4 = htl3

            units_htl = [round(float(htl1) , 3) , round(float(htl2) , 3) , round(float(htl3) , 3) , round(float(htl4) , 3)]
            if not units_htl == sorted(units_htl , key = float):
                msg.showerror("error" , "Enter HTL units in increasing order")
                return            
        else:
            htl1 = nrm1
            htl2 = nrm2
            htl3 = nrm3
            htl4 = nrm4
            units_htl = [round(float(htl1) , 3) , round(float(htl2) , 3) , round(float(htl3) , 3) , round(float(htl4) , 3)]
        
        if self.chk_spl.instate(['selected']) == False:
            spl1 = self.ent_spl1.get()
            spl2 = self.ent_spl2.get()
            spl3 = self.ent_spl3.get()
            spl4 = self.ent_spl4.get() 

            if spl1 == "":
                msg.showinfo("Error" , "Enter SPL unit value")
                self.ent_spl1.focus_set()
                return 
            if spl2 == "":
                spl2 = spl1
            
            if spl3 == "":
                spl3 = spl2
        
            if spl4 == "":
                spl4 = spl3
            units_spl = [round(float(spl1) , 3) , round(float(spl2) , 3) , round(float(spl3) , 3) , round(float(spl4) , 3)]
            if not units_spl == sorted(units_spl , key = float):
                msg.showerror("error" , "Enter SPL units in increasing order")
                return
        else:
            spl1 = nrm1
            spl2 = nrm2
            spl3 = nrm3
            spl4 = nrm4
            units_spl = [round(float(spl1) , 3) , round(float(spl2) , 3) , round(float(spl3) , 3) , round(float(spl4) , 3)]

        if self.chk_ang.instate(['selected']) == False:
            ang1 = self.ent_ang1.get()
            ang2 = self.ent_ang2.get()
            ang3 = self.ent_ang3.get()
            ang4 = self.ent_ang4.get() 

            if ang1 == "":
                msg.showinfo("Error" , "Enter ANG unit value")
                self.ent_ang1.focus_set()
                return 
            if ang2 == "":
                ang2 = ang1
            
            if ang3 == "":
                ang3 = ang2
        
            if ang4 == "":
                ang4 = ang3

            units_ang = [round(float(ang1) , 3) , round(float(ang2) , 3) , round(float(ang3) , 3) , round(float(ang4) , 3)]
            if not units_ang == sorted(units_ang , key = float):
                msg.showerror("error" , "Enter ANG units in increasing order")
                return       
        else:
            ang1 = nrm1
            ang2 = nrm2
            ang3 = nrm3
            ang4 = nrm4
            units_ang = [round(float(ang1) , 3) , round(float(ang2) , 3) , round(float(ang3) , 3) , round(float(ang4) , 3)]
        #arramging units ends here
        




        categories = []
        if cat1 != "" : categories.append(cat1) 
        if cat2 != "" : categories.append(cat2)
        if cat3 != "" : categories.append(cat3)
       
        suppliers = []
        if sup1 != "" : suppliers.append(sup1) 
        if sup2 != "" : suppliers.append(sup2)
        if sup3 != "" : suppliers.append(sup3)

        prod_bar = ":"
        if bar1 != "": prod_bar += bar1 +":"
        if bar2 != "": prod_bar += bar2 +":"
        if bar3 != "": prod_bar += bar3 +":"
        if bar4 != "": prod_bar += bar4 +":"
        
        
        temp = categories
        categories = ":"
        for each in temp:
            sql = "select cat_id from somanath.categories where cat_name = '"+ each + "'"
            req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
            categories += str(req.json()[0]['cat_id'])+":"
        
        temp = suppliers
        suppliers = ":"
        for each in temp:
            sql = "select acc_id from somanath.accounts where acc_name = '"+ each + "' and acc_type = 'SUPP'"
            req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
            suppliers += str(req.json()[0]['acc_id'])+":"
            
        temp = units_nrm
        units_nrm = ":"
        for each in temp:
            units_nrm += str(each) + ":"

        temp = units_htl
        units_htl = ":"
        for each in temp:
            units_htl += str(each) + ":"

        temp = units_spl
        units_spl = ":"
        for each in temp:
            units_spl += str(each) + ":"

        temp = units_ang
        units_ang = ":"
        for each in temp:
            units_ang += str(each) + ":"



        #prod_id, prod_bar, prod_name, prod_cat, prod_hsn, kan_img, prod_name_eng, prod_min_qty, prod_expiry, prod_mrp, prod_mrp_old, prod_sup, prod_gst, prod_cess, prod_unit_type, nml_unit, htl_unit, spl_unit, ang_unit, high_img, low_img, insert_time, insert_id, update_time, update_id
        parameters = {
            "prod_id"   : "",
            "user_name" :  self.user ,
            "prod_bar"  :  prod_bar , 
            "prod_name" : prod_name , 
            "prod_cat"  : categories ,
            "prod_hsn"  : hsn , 
            "prod_shelf": shelf,
            "prod_name_eng" : name_eng , 
            "prod_min_qty" : min_qty ,
            "prod_expiry" : expiry ,
            "prod_mrp"  : mrp1 , 
            "prod_mrp_old" : mrp2 , 
            "prod_sup"  : suppliers ,
            "prod_gst"  : gst ,
            "prod_cess" : cess,
            "prod_unit_type": unit,
            "nml_unit"  : units_nrm,
            "htl_unit"  : units_htl,
            "ang_unit"  : units_ang,
            "spl_unit"  : units_spl,
            "prod_desc" : desc ,
            "img_kan"   : False , 
            "img_high" : False , 
            "img_low" : False

        }

        files = []




        if self.img_kan_loc != "" and self.img_kan_loc != None:
            original = Image.open(self.img_kan_loc)

            temp = self.img_kan_loc.split(".")
            typeLow = temp[-1]

            if typeLow != "png":
                temp.pop(len(temp)-1)
                
                self.img_kan_loc = os.path.join(self.homeDir , "Images" , "tempImages" , "low.png")
                original.save(self.img_kan_loc , format = "png")

            files.append(('images', (self.img_kan_loc, open(self.img_kan_loc, 'rb'), 'images/png')))
            
            parameters['img_kan'] = True
            
        if self.img_high_loc != "" and self.img_high_loc != None:

            original = Image.open(self.img_high_loc)

            temp = self.img_high_loc.split(".")
            typeLow = temp[-1]

            if typeLow != "png":
                temp.pop(len(temp)-1)
                
                self.img_high_loc = os.path.join(self.homeDir , "Images" , "tempImages" , "low.png")
                original.save(self.img_high_loc , format = "png")

            files.append(('images', (self.img_high_loc, open(self.img_high_loc, 'rb'), 'images/png')))
            
            parameters['img_high'] = True

        if self.img_low_loc != "" and  self.img_low_loc != None:

            original = Image.open(self.img_low_loc)

            temp = self.img_low_loc.split(".")
            typeLow = temp[-1]

            if typeLow != "png":
                temp.pop(len(temp)-1)
                
                self.img_low_loc = os.path.join(self.homeDir , "Images" , "tempImages" , "low.png")
                original.save(self.img_low_loc , format = "png")

            files.append(('images', (self.img_low_loc, open(self.img_low_loc, 'rb'), 'images/png')))
            
            parameters['img_low'] = True
        
        self.img_kan = None                                                                             
        self.img_high = None                                                                       
        self.img_low = None

        
        

        if self.edit_state == True:
            parameters['prod_id'] = self.selected_prod
            parameters['prod_hide'] = self.chk_hide.instate(['selected'])


        req = post("http://"+self.ip+":6000/products/save" , params = parameters , files = files)

        if req.status_code == 201:
            msg.showerror("This products has been added")
            return

        if self.generated_bar != None:
            req = post("http://"+self.ip+":6000/barcodes" , params = {'type' : 'save' , 'barcode' : self.generated_bar})

        

        self.new_state = False
        self.edit_state = False

        if self.check_all.get() == 'True':
            self.img_kan = None                                                                             
            self.img_high = None                                                                       
            self.img_low = None
            self.img_kan_loc = ""                                                                          
            self.img_high_loc = ""
            self.img_low_loc = ""
            self.selected_prod = -1
            self.generated_bar = None
            self.ent_bar1.delete(0,con.END)
            self.ent_bar2.delete(0,con.END)
            self.ent_bar3.delete(0,con.END)
            self.ent_bar4.delete(0,con.END)

        else:
            self.clear_all()

        
        self.disable_all()
        self.product_list(None)
        self.btn_new.config(state = con.NORMAL)
        self.btn_save.config(state = con.DISABLED)
        self.btn_edit.config(state = con.DISABLED)

    def product_list(self , e): 

        cat1 = self.combo_cat1.get()
        cat2 = self.combo_cat2.get()
        sup1 = self.combo_sup1.get()
        sup2 = self.combo_sup2.get()
        prod = self.ent_prod_search.get().upper()
        

        firstSql = True
        sql = "select prod_hide , prod_name , prod_id from somanath.products"

        if self.cat_state.get() == 'True':
            if cat1 != "":
                req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select cat_id from somanath.categories where cat_name = '" + cat1 + "'"})
                resp = req.json()
                if resp == "":
                    self.combo_cat1.delete(0,con.END)
                else:
                    sql += " where prod_cat regexp ':"+str(resp[0]['cat_id'])+":'"
                    firstSql = False
            
            if cat2 != "":
                req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select cat_id from somanath.categories where cat_name = '" + cat2 + "'"})
                resp = req.json()
                if resp == "":
                    self.combo_cat2.delete(0,con.END)
                else:
                    if firstSql:
                        sql += " where prod_cat regexp ':"+str(resp[0]['cat_id'])+":'"
                        firstSql = False
                    else:
                        sql += " and prod_cat regexp ':"+str(resp[0]['cat_id'])+":'"


        if self.sup_state.get() == 'True':
            if sup1 != "":
                req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select acc_id from somanath.accounts where acc_name = '" + sup1 + "' and acc_type = 'SUPP'"})
                resp = req.json()
                if resp == "":
                    self.combo_sup1.delete(0,con.END)
                else:
                    if firstSql:
                        sql += " where prod_sup regexp ':"+str(resp[0]['acc_id'])+":'"
                        firstSql = False
                    else:
                        sql += " and prod_sup regexp ':"+str(resp[0]['acc_id'])+":'"

            if sup2 != "":
                req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select acc_id from somanath.accounts where acc_name = '" + sup2 + "' and acc_type = 'SUPP'"})
                resp = req.json()
                if resp == "":
                    self.combo_sup2.delete(0,con.END)
                else:
                    if firstSql:
                        sql += " where prod_sup regexp ':"+str(resp[0]['acc_id'])+":'"
                    else:
                        sql += " and prod_sup regexp ':"+str(resp[0]['acc_id'])+":'"

        if prod != "":
            if firstSql:
                sql += " where prod_name regexp '"+prod+"'"
            else:
                sql += " and prod_name regexp '"+prod+"'"

        sql += ' order by prod_name'

        print(sql)

        req = get("http://"+self.ip+":6000/Products/getProductList" , params = {'sql' : sql})
        
        for each in self.tree.get_children():
            self.tree.delete(each)

        if req.status_code == 200:
            resp = req.json()
            tag_index = 0
            for each in resp:
                if tag_index%2:
                    tag = 'a'
                else:
                    tag = 'b'
                tag_index += 1
                self.tree.insert('','end' ,tags=(tag,), values = (each['prod_hide'] , each['prod_name'] , each['prod_id']))

    def select_tree(self , e):
        self.btn_kan_vw.config(state = con.DISABLED)
        self.btn_img1_vw.config(state = con.DISABLED)
        self.btn_img2_vw.config(state = con.DISABLED)

        self.btn_new.config(state = con.NORMAL)

        try:
            cur_item = self.tree.focus()
            cur_item = self.tree.item(cur_item)
            cur_item = cur_item['values']
            req = get("http://"+self.ip+":6000/products/getSelectedProduct" , params = {"prod_id" : cur_item[2]})

            if req.status_code == 200:
                resp = req.json()[0]
                
                self.enable_all()
                self.clear_all()
                self.combo_unit.config(state = con.NORMAL)
                self.combo_tax1.config(state = con.NORMAL)
                self.combo_tax2.config(state = con.NORMAL)

                barcodes = resp['prod_bar'].split(":")  
                for each in barcodes:
                    if each == "":
                        barcodes.remove(each)
                if len(barcodes) >= 1 : self.ent_bar1.insert(0 , barcodes[0])               
                if len(barcodes) >= 2 : self.ent_bar2.insert(0 , barcodes[1])
                if len(barcodes) >= 3 : self.ent_bar3.insert(0 , barcodes[2])
                if len(barcodes) >= 4 : self.ent_bar4.insert(0 , barcodes[3])
                    

                categories = resp['prod_cat'].split(":")
                for each in categories:
                    if each == "":
                        categories.remove(each)
                temp = categories
                categories = []
                for each in temp:
                    req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select cat_name from somanath.categories where cat_id = "+str(each)})
                    categories.append(req.json()[0]['cat_name'])
                if len(categories) >= 1 : self.ent_cat1.insert(0 , categories[0])
                if len(categories) >= 2 : self.ent_cat2.insert(0 , categories[1])
                if len(categories) >= 3 : self.ent_cat3.insert(0 , categories[2])



                suppliers = resp['prod_sup'].split(":")
                for each in suppliers:
                    if each == "":
                        suppliers.remove(each)
                temp = suppliers
                suppliers = []
                for each in temp:
                    req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select acc_name from somanath.accounts where acc_id = "+str(each) + " and acc_type = 'SUPP'"})
                    suppliers.append(req.json()[0]['acc_name'])
                if len(suppliers) >= 1 : self.ent_sup1.insert(0 , suppliers[0])
                if len(suppliers) >= 2 : self.ent_sup2.insert(0 , suppliers[1])
                if len(suppliers) >= 3 : self.ent_sup3.insert(0 , suppliers[2])

                
                gst = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select tax_per from somanath.taxes where tax_id = " + str(resp['prod_gst']) + " and tax_type = 0"}).json()[0]['tax_per']
                cess = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : "select tax_per from somanath.taxes where tax_id = " + str(resp['prod_cess']) + " and tax_type = 1"}).json()[0]['tax_per']

                    
                self.ent_name.insert(0 , resp['prod_name'])
                self.ent_hsn.insert(0 , resp['prod_hsn'])
                self.ent_shelf.insert(0 , resp['prod_shelf'])
                self.ent_name_eng.insert(0 , resp['prod_name_eng'])
                self.ent_min_qty.insert(0 , resp['prod_min_qty'])
                self.ent_exp.insert(0 , resp['prod_expiry'])
                self.combo_unit.insert(0 , resp['prod_unit_type'])
                self.combo_tax1.insert(0 , gst)
                self.combo_tax2.insert(0 , cess)
                self.ent_mrp1.insert(0 , resp['prod_mrp'])
                self.ent_mrp2.insert(0 , resp['prod_mrp_old'])


                nrm_units = resp['nml_unit'].split(":")
                for each in nrm_units:
                    if each == "":
                        nrm_units.remove(each)
                self.ent_nrm1.insert(0,nrm_units[0])
                self.ent_nrm2.insert(0,nrm_units[1])
                self.ent_nrm3.insert(0,nrm_units[2])
                self.ent_nrm4.insert(0,nrm_units[3])
                
                htl_units = resp['htl_unit'].split(":")
                for each in htl_units:
                    if each == "":
                        htl_units.remove(each)
                self.ent_htl1.insert(0,htl_units[0])
                self.ent_htl2.insert(0,htl_units[1])
                self.ent_htl3.insert(0,htl_units[2])
                self.ent_htl4.insert(0,htl_units[3])
                
                spl_units = resp['spl_unit'].split(":")
                for each in spl_units:
                    if each == "":
                        spl_units.remove(each)
                self.ent_spl1.insert(0,spl_units[0])
                self.ent_spl2.insert(0,spl_units[1])
                self.ent_spl3.insert(0,spl_units[2])
                self.ent_spl4.insert(0,spl_units[3])
                
                ang_units = resp['ang_unit'].split(":")
                for each in ang_units:
                    if each == "":
                        ang_units.remove(each)
                self.ent_ang1.insert(0,ang_units[0])
                self.ent_ang2.insert(0,ang_units[1])
                self.ent_ang3.insert(0,ang_units[2])
                self.ent_ang4.insert(0,ang_units[3])
                
                
                self.ent_desc.insert(0.0 , resp['prod_desc'])
                #if resp['prod_hide'] == 'True':
                self.check_state.set(resp['prod_hide'])

                

                self.disable_all()

                if resp['kan_img'] == 'True':
                    self.lbl_kan.config(text = "Kan.png")
                    file = get("http://"+self.ip+":6000/images/products/"+str(cur_item[2])+"/kan.png")
                    self.img_kan = ImageTk.PhotoImage(Image.open(io.BytesIO(file.content)))
                    self.btn_kan_vw.config(state = con.NORMAL)
                
                if resp['high_img'] == 'True':
                    self.lbl_img1.config(text = "high.png")
                    file = get("http://"+self.ip+":6000/images/products/"+str(cur_item[2])+"/high.png")
                    self.img_high = ImageTk.PhotoImage(Image.open(io.BytesIO(file.content)))
                    self.btn_img1_vw.config(state = con.NORMAL)
                
                if resp['low_img'] == 'True':
                    self.lbl_img2.config(text = "low.png")
                    file = get("http://"+self.ip+":6000/images/products/"+str(cur_item[2])+"/low.png")
                    self.img_low = ImageTk.PhotoImage(Image.open(io.BytesIO(file.content)))
                    self.btn_img2_vw.config(state = con.NORMAL)
                
                self.btn_add_bar.config(state = con.NORMAL)
                self.btn_add_cat.config(state = con.NORMAL)
                self.btn_add_sup.config(state = con.NORMAL)
                self.btn_edit.config(state = con.NORMAL)
                self.selected_prod = resp['prod_id']


        except IndexError:
            pass

    def add_search_cats(self , e):
        cat = e.widget.get()
        if cat != "":
            sql = "select cat_name from somanath.categories where cat_name regexp '"+ cat +"' order by cat_name"
        else:
            sql = "select cat_name from somanath.categories order by cat_name"
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            resp = req.json()
            values = []
            for each in resp:
                values.append(each['cat_name'])

            e.widget['values'] = values

    def add_search_sup(self , e):
        sup = e.widget.get()
        if sup != "":
            sql = "select acc_name from somanath.accounts where acc_name regexp '"+ sup +"' and acc_type = 'SUPP' order by acc_name"
        else:
            sql = "select acc_name from somanath.accounts where acc_type = 'SUPP' order by acc_name"
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : sql})
        if req.status_code == 200:
            resp = req.json()
            values = []
            for each in resp:
                values.append(each['acc_name'])

            e.widget['values'] = values
   
    def close(self , e):
        self.frm_barcode.place_forget()
        self.frm_category.place_forget()
        self.frm_supplier.place_forget()
        base_window.close(self,e)
    
    def minimize(self, e):
        self.frm_barcode.place_forget()
        self.frm_category.place_forget()
        self.frm_supplier.place_forget()
        base_window.minimize(self,e)       
 
    def refresh(self , e):
        self.product_list(None)
        self.gst_values.clear()
        self.cess_values.clear()
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : 'select tax_per from somanath.taxes where tax_type = 0'})
        for each in req.json():
            self.gst_values.append(each['tax_per'])
        
        req = get("http://"+self.ip+":6000/onlySql" , params = {'sql' : 'select tax_per from somanath.taxes where tax_type = 1'})
        for each in req.json():
            self.cess_values.append(each['tax_per'])

        






class users(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations,others):
        base_window.__init__(self , root ,frames , dmsn , lbls ,title)
        self.main_frame.grid_propagate(False)
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()
        self.rad_user = None
        self.image_user = None
        self.others = others

        self.lbl_user_name = ttk.Label(self.main_frame , text = "User Name        :" , style = "window_text_medium.TLabel")
        self.lbl_user_pass = ttk.Label(self.main_frame , text = "User Password    :" , style = "window_text_medium.TLabel")
        self.lbl_user_img_txt = ttk.Label(self.main_frame , text = "User Image       :" , style = "window_text_medium.TLabel")
        self.lbl_user_type = ttk.Label(self.main_frame , text = "User Type        :" , style = "window_text_medium.TLabel")

        self.ent_user_name = ttk.Entry(self.main_frame  , width = 30 ,   font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_user_name.bind("<FocusOut>" , self.combo_entry_out)
        self.ent_user_pass = ttk.Entry(self.main_frame  , width = 30 , show = "*" , font = ('Lucida Grande' , -int(self.main_hgt*0.03)) , validate="key", validatecommand=(validations[0], '%P'))
        self.ent_user_pass.bind("<FocusOut>" , self.combo_entry_out)

        self.lbl_user_img = ttk.Label(self.main_frame  , width = 30, style = "window_lbl_ent.TLabel")
        self.btn_user_img_brw = ttk.Button(self.main_frame , text = "Browse" , style = "window_btn_medium.TButton" ,command = lambda : self.file_dialog_img(None))
        self.btn_user_img_brw.bind("<Return>" , self.file_dialog_img)
        self.btn_user_img_vw = ttk.Button(self.main_frame , text = "View" , style = "window_btn_medium.TButton" ,command = lambda : self.view_img(None))
        self.btn_user_img_vw.bind("<Return>" , self.view_img)

        self.rad_usr_adm = ttk.Radiobutton(self.main_frame , value = 0 , variable = self.rad_user , style = "window_radio.TRadiobutton" , text = "ADMIN")
        self.rad_usr_own = ttk.Radiobutton(self.main_frame , value = 1 , variable = self.rad_user , style = "window_radio.TRadiobutton" , text = "OWNER")
        self.rad_usr_emp = ttk.Radiobutton(self.main_frame , value = 2 , variable = self.rad_user , style = "window_radio.TRadiobutton" , text = "EMPLOY")

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




        self.lbl_user_name.grid(row = 0 , column = 0 , pady = int(self.main_hgt*0.01), padx = int(self.main_wdt*0.01))
        self.lbl_user_pass.grid(row = 1 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_user_img_txt.grid(row = 2 , column = 0 , pady = int(self.main_hgt*0.01))
        self.lbl_user_type.grid(row = 3 , column = 0 , pady = int(self.main_hgt*0.01))

        self.ent_user_name.grid(row = 0 , column = 1 , columnspan = 3)
        self.ent_user_pass.grid(row = 1 , column = 1 , columnspan = 3)
        self.lbl_user_img.grid(row = 2 , column = 1 , columnspan = 3)
        self.btn_user_img_brw.grid(row = 2 , column = 4, padx = int(self.main_wdt*0.002))
        self.btn_user_img_vw.grid(row = 2 , column = 5, padx = int(self.main_wdt*0.002))
        self.rad_usr_adm.grid(row = 3 , column = 1)
        self.rad_usr_own.grid(row = 3 , column = 2)
        self.rad_usr_emp.grid(row = 3 , column = 3)

        self.tree_frame.grid(row = 0 , column = 6 , rowspan = 15 , padx = int(self.main_wdt*0.01) , pady = int(self.main_hgt*0.035))
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



    def file_dialog_img(self , e):
        file = filedialog.askopenfilename(initialdir = self.others[0]+"\Pictures",title = "Select a File",filetypes = [["Image ","*.*"]])
        file_lbl = file.split("/")
        if file!= "":
            text = "/"+file_lbl[-3]+"/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-2]+"/"+file_lbl[-1]
            if len(text)>30:
                text = "/"+file_lbl[-1]
            self.lbl_user_img.config(text = text)
            self.image_user = ImageTk.PhotoImage(Image.open(file))
        else:
            self.lbl_user_img.config(text = "")

    def view_img(self , e):
        if self.image_user != None or self.lbl_user_img.cget("text") != "":
            image_viewer(self.image_user,"QR Code Image")

    def new(self , e):
        pass

    def edit(self , e):
        pass

    def save(self , e):
        pass
    
    def combo_entry_out(self , e):
        e.widget.select_clear()



