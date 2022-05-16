from os import chdir,system,remove
from shutil import copyfile
from tkinter import Tk,Label,Button,Entry,ttk,DISABLED,NORMAL,PhotoImage,messagebox,FALSE
import tkinter.font as tkFont
import datetime.date
import os.path
homedir = os.path.expanduser("~").split('\\')[-1]

#chdir("C:\\program files\\mysql\\mysql server 8.0\\bin")

#system('mysqldump -uroot -p******* somnathstores>"file location"')


usb = False

date = str(datetime.date.today())
date = date.split("-")

db_file = "somanathstores_"+str(int(date[0]))+"_"+str(int(date[1]))+"_"+str(int(date[2]))+".sql"
src = "C:\\Users\\"+homedir+"\\angadiImages\\"+db_file
main = Tk()
main.geometry("200x150+305+40")
photo = PhotoImage(file = "C:\\Program Files\\Hosangadi\\icon\\PNG\\db.png")
main.iconphoto(FALSE,photo)
main.title("Data Backup")
main.config(bg = "#d8f4cd")
main.resizable(FALSE,FALSE)
fontStyle = tkFont.Font(family = "Lucida Grande" , size = 13)

def chck_usb():
    global usb
    if len(chck_usb.state())>3:
        usb = True
        entry_drive.config(state = NORMAL)
    else:
        usb = False
        entry_drive.config(state = DISABLED)

def backup():
    global usb,db_file,src
    
    drive = entry_drive.get().upper()


    if usb == True and drive == "":
        messagebox.showerror("ERROR" , "Enter Drive Letter ")
        return  
    
    chdir("C:\\program files\\mysql\\mysql server 8.0\\bin")
    sys = 'mysqldump -uadmin -pmysqlpassword5 -h192.168.0.100 --databases somanath somanath2021>"'+src+'"'

    system(sys)
    
    dir_folder = "C:\\backup\\"+db_file
    copyfile(src,dir_folder)

    #dir_folder = "A:\\G-drive\\backup\\"+db_file
    #copyfile(src,dir_folder)

    if usb == True:
        try:
            dir_folder = drive+":\\Hosangadi\\"+db_file
    
            #copyfile(src,dir_folder)
        except FileNotFoundError:
            messagebox.showerror("ERROR" , "Enter Correct Usb Drive Letter \n Goto This Pc and find usb drive letter")         
    remove(src)
    messagebox.showinfo("Success!","Backup Complete")
    main.quit()

#label_copy1 = Label(main , text = "Backup in C      " , font = fontStyle , bg = "#d8f4cd")
#label_copy2 = Label(main , text = "Backup in D     " , font = fontStyle , bg = "#d8f4cd")
label_usb = Label(main , text = "Backup in USB " , font = fontStyle , bg = "#d8f4cd")

#chck_copy_1 = ttk.Checkbutton(main,command = chck_copies_1)
#chck_copy_2 = ttk.Checkbutton(main,command = chck_copies_2)
chck_usb = ttk.Checkbutton(main,command = chck_usb )

label_drive = Label(main , text = "Ent USB Letter:" , font = fontStyle , bg = "#d8f4cd")
entry_drive = Entry(main , width = 2 , font = fontStyle ,state = DISABLED)

btn_db = Button(main  , text = "Backup" , font = fontStyle , command = backup)

#label_copy1.place(x = 10, y = 10)
#label_copy2.place(x = 10, y = 40)
label_usb.place(x = 10, y = 10)
#chck_copy_1.place(x = 130, y = 10)
#chck_copy_2.place(x = 130, y = 40)
chck_usb.place(x = 130, y = 10)
label_drive.place(x = 10 , y = 40)
entry_drive.place(x = 130 , y = 40)
btn_db.place(x = 50 , y = 100)


main.mainloop()