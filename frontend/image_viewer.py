from tkinter import PhotoImage, Toplevel , Label
from PIL import Image , ImageTk

class image_viewer:
    def __init__(self , image , image_name):
        self.root = Toplevel()
        self.root.geometry("+10+30")
        self.root.title(image_name)
        self.root.focus_set()
        self.root.bind("<FocusOut>" , self.close)
        self.root.bind("<Escape>" , self.close)
        self.root.overrideredirect(True)
        
        self.label = Label(self.root , image = image)

        self.label.pack()

        self.root.mainloop()
        
    def close(self , e):
        self.root.destroy()