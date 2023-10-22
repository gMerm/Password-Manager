import tkinter as tk
from tkinter import messagebox, Label, Text
import mysql.connector
import bcrypt

#connect with mysql
cnx = mysql.connector.connect(user="root", password="20028218", host="localhost", database="PASSMANAGER")
username_credential="admin"
password_credential="admin"


#insert sto db
def insert():
    cursor=cnx.cursor() 
    if website_text.index("end") == 0 or password_text.index("end")==0:
        messagebox.showinfo("Message", "You need to fill the entries")
    else:
        try:
            cursor.execute("INSERT INTO tag (website, password) VALUES (%s, %s)", (website_text.get(), password_text.get()))
            messagebox.showinfo("Message", "Success")
            website_text.delete(first=0, last=1000)
            password_text.delete(first=0, last=1000)

        except:
            messagebox.showinfo("Message", "Something went wrong")

    cnx.commit()
    cursor.close()


#gia na vlepw poia passwords exw saved
def checkpasses():

    messagebox.showinfo("Message", "Proceed Carefully")
    for item in root.winfo_children():
        item.destroy()



#evala password kai username kai mpika sto gui ayto
def connected():
    
    if username_text.get()==username_credential and loginpassword_text.get()==password_credential:

        messagebox.showinfo("Message", "Successful Sign In")

        #gia na diwxnei ta parathira afou erthw se ayto to page
        for item in root.winfo_children():
            item.destroy()

        main_frame = tk.Frame(root, bg="lightblue")
        main_frame.pack(fill="both", expand=False)

        #website gui
        website = Label(root, text = "Website", width="10", height="3")
        website.config(font =("Courier", 18))
        website.pack()

        global website_text
        website_text = tk.Entry(root)
        website_text.config(font =("Courier", 18))
        website_text.pack()

        #password gui
        password = Label(root, text = "Password", width="10", height="3")
        password.config(font =("Courier", 18))
        password.pack()

        global password_text
        password_text = tk.Entry(root,show="*")
        password_text.config(font =("Courier", 18))
        password_text.pack()

        #button for insert
        insert_button = tk.Button(text="Insert", command=insert)
        insert_button.config(font =("Courier", 18))
        insert_button.pack(anchor="center", pady=10)

        #gia ta password pou yparxoyn idi
        check_button = tk.Button(text="History", command=checkpasses)
        check_button.config(font =("Courier", 18))
        check_button.pack(anchor="center", pady=10)
        

    else:
        messagebox.showinfo("Message", "Wrong Credentials")
        username_text.delete(first=0, last=1000)
        loginpassword_text.delete(first=0, last=1000)



#mainloop gia authorization
root = tk.Tk()
root.title("Password Manager")
root.resizable(False, False)

login_frame = tk.Frame(root, bg="lightblue")
login_frame.pack(fill="both", expand=False)

#username gui
username = Label(root, text = "Username", width="10", height="3")
username.config(font =("Courier", 18))
username.pack()

username_text = tk.Entry(root)
username_text.config(font =("Courier", 18))
username_text.pack()

#password gui
loginpassword = Label(root, text = "Password", width="10", height="3")
loginpassword.config(font =("Courier", 18))
loginpassword.pack()

loginpassword_text = tk.Entry(root,show="*")
loginpassword_text.config(font =("Courier", 18))
loginpassword_text.pack()

#button gia elegxo credentials
login_button = tk.Button(text="Connect", command=connected)
login_button.config(font =("Courier", 18))
login_button.pack(side=tk.BOTTOM, pady=10)

root.mainloop()




