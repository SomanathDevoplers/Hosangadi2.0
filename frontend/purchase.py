from tkinter import Listbox, StringVar, Text , constants as con , filedialog , messagebox as msg , ttk , Listbox
import requests
from base_window import base_window

class purchase(base_window):
    def __init__(self , root ,frames , dmsn , lbls ,title,validations, others , pur_form):
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , pur_form)
        if base == None:
            print(1)
            return
        self.main_frame.grid_propagate(False)
        self.root_frame = frames[0] 
        self.main_hgt = self.main_frame.winfo_reqheight()
        self.main_wdt = self.main_frame.winfo_reqwidth()

        self.btn_add_dets = ttk.Button(self.main_frame, state = con.DISABLED ,text = " Add Details "  , style = "window_btn_medium.TButton" , command = lambda : self.show_pur_details(None))
        self.btn_add_dets.bind("<Return>" , self.show_pur_details)

        #----------------------------------------purchase_detail_toplevel------------------------------------------------#
        self.frm_pur_details = ttk.Frame( self.root_frame , height = self.main_hgt*0.5 , width = self.main_wdt*0.4  , style = "root_menu.TFrame")
        self.frm_pur_details.grid_propagate(False)
        
        
        
        #----------------------------------------purchase_detail_toplevel Ends here------------------------------------------------#

        #----------------------------------------supplier name adding top level-------------------------------------------#
        
        #----------------------------------------supplier name adding top level-------------------------------------------#


        self.btn_add_dets.grid(row = 0 , column = 0)


        self.btn_add_dets.config(state = con.NORMAL)



    def show_pur_details(self , e):
        self.frm_pur_details.place( x = self.main_wdt*0.25 , y = self.main_hgt*0.3)
        self.frm_pur_details.lift()
        try:
            self.btn_gen_bar.focus_set()

        except:
            pass
        #self.frm_pur_details.place_forget()

    



    def close(self , e):
        
        self.frm_pur_details.place_forget()
        base_window.close(self,e)