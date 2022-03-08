
from tkinter import Listbox , constants as con  , messagebox as msg , ttk , Listbox 
from requests import get 
from other_classes import base_window
import datetime

class sales_bill(base_window):

    def __init__(self , root ,frames , dmsn , lbls ,title,validations, others , pur_form , sio):
        base = base_window.__init__(self , root ,frames , dmsn , lbls ,title , pur_form)
        if base == None:
            return

        base.acc_title.bind("<Button-1>" , self.pack_top)

        
