import tkinter as tk
from tkinter import messagebox, Label, Text
import mysql.connector
import base64
from PIL import Image, ImageTk

#connect with mysql
cnx = mysql.connector.connect(user="root", password="", host="localhost", database="PASSMANAGER")
username_credential="admin"
password_credential="admin"

#insert sto db
def insert():
    cursor=cnx.cursor() 
    if website_text.index("end") == 0 or password_text.index("end")==0:
        messagebox.showinfo("Message", "You need to fill the entries")
    else:
        try:
            #encoded password
            encoded_pass=encode_pass(password_text.get())


            #gia to insert dinw to hashed password
            cursor.execute("INSERT INTO tag (website, password) VALUES (%s, %s)", (website_text.get(), encoded_pass))
            cnx.commit()
            messagebox.showinfo("Message", "Success")
            website_text.delete(first=0, last=1000)
            password_text.delete(first=0, last=1000)
            resetpage()

        except:
            messagebox.showinfo("Message", "Something went wrong")


#toggle password
def toggle_password():
    if password_text.cget('show') == '':
        password_text.config(show='*')
        toggle_btn.config(image=img)
    else:
        password_text.config(show='')
        toggle_btn.config(image=img)


#kanei delete to website
def delete_selected_item():
    for i in listbox.curselection():
        selected_item = listbox.get(i)
        index = selected_item.split(':')[0]

        cursor1 = cnx.cursor()
        cursor1.execute("DELETE FROM tag WHERE id = %s", (index,))
        cnx.commit()
        resetpage()



#emfanizei messagebox me to password
def selected_item():
    for i in listbox.curselection():
        
        selected_item = listbox.get(i)
        index = selected_item.split(':')[0]

        cursor1 = cnx.cursor()
        cursor1.execute("SELECT password FROM tag WHERE id = %s", (index,))
        myresult = cursor1.fetchall()

        for x in myresult:
            decoded_pass=decode_pass(x[0])
            messagebox.showinfo("Message", f"Password: {decoded_pass}")
        


#reset page when insertion is done so the listbox refreshes
def resetpage():
    
    root.title("Password Manager")

    website = tk.Label(main_frame, text="Website", width="10", height="2")
    website.config(font=("Courier", 18))
    website.grid(row=0, column=0, pady=10)

    global website_text
    website_text = tk.Entry(main_frame)
    website_text.config(font=("Courier", 18))
    website_text.grid(row=1, column=0, padx="10", pady="10")

    password = tk.Label(main_frame, text="Password", width="10", height="2")
    password.config(font=("Courier", 18))
    password.grid(row=2, column=0)

    global password_text
    password_text = tk.Entry(main_frame, show="*")
    password_text.config(font=("Courier", 18))
    password_text.grid(row=3, column=0, padx="10", pady="15")

    insert_button = tk.Button(main_frame, text="Insert", command=insert)
    insert_button.config(font=("Courier", 18))
    insert_button.grid(row=4, column=0, pady=10)

    # Create and configure the Listbox
    global listbox
    listbox = tk.Listbox(main_frame, selectmode=tk.SINGLE)
    listbox.config(font=("Courier", 18), width=25)
    listbox.grid(row=0, column=2, rowspan=500, padx=10, pady=10, sticky='ns')

    password_text = tk.Entry(main_frame, show="*")
    password_text.config(font=("Courier", 18))
    password_text.grid(row=3, column=0, padx="10", pady="15")

    toggle_btn = tk.Button(main_frame, command=toggle_password)
    toggle_btn.config(image=img, bg="white")

    #gia na topothetisw ta password_text kai toggle button konta
    password_text.grid(row=3, column=0, padx="10", pady="15", sticky="w")
    toggle_btn.grid(row=3, column=1, sticky="e")

    c=cnx.cursor()
    c.execute("select * from tag")
    tag = c.fetchall()

    for t in tag:
        index=t[0]
        website_id=t[1]
        listbox.insert(tk.END, f"{index}: {website_id}")
        
    showpass_button = tk.Button(main_frame, text="Show", command=selected_item, width="6", height="1")
    showpass_button.config(font=("Courier", 18))
    showpass_button.grid(row=1, column=3, pady=10, padx=10)

    deletepass_button = tk.Button(main_frame, text="Delete", command=delete_selected_item, width="6", height="1")
    deletepass_button.config(font=("Courier", 18))
    deletepass_button.grid(row=2, column=3, pady=10, padx=10)


#gia encoded password prin mpei sto db
def encode_pass(password):
    encoded_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    return encoded_password

#when the password gets selected from the db gets decoded so the user can see it 
def decode_pass(encoded_password):
    decoded_password = base64.b64decode(encoded_password.encode('utf-8')).decode('utf-8')
    return decoded_password



#evala password kai username kai mpika sto gui ayto
def connected():
    
    if username_text.get()==username_credential and loginpassword_text.get()==password_credential:

        messagebox.showinfo("Message", "Successful Sign In")
        root.title("Password Manager")

        #gia na diwxnei ta parathira afou erthw se ayto to page
        for item in root.winfo_children():
            item.destroy()

        global main_frame
        main_frame = tk.Frame(root, bg="black")
        main_frame.pack(fill="both", expand=False)

        website = tk.Label(main_frame, text="Website", width="10", height="2")
        website.config(font=("Courier", 18))
        website.grid(row=0, column=0, pady=10)

        global website_text
        website_text = tk.Entry(main_frame)
        website_text.config(font=("Courier", 18))
        website_text.grid(row=1, column=0, padx="10", pady="10")

        password = tk.Label(main_frame, text="Password", width="10", height="2")
        password.config(font=("Courier", 18))
        password.grid(row=2, column=0)

        global password_text
        password_text = tk.Entry(main_frame, show="*")
        password_text.config(font=("Courier", 18))
        password_text.grid(row=3, column=0, padx="10", pady="15")

        global toggle_btn
        toggle_btn = tk.Button(main_frame, command=toggle_password)
        toggle_btn.config(image=img, bg="white")

        #gia na topothetisw ta password_text kai toggle button konta
        password_text.grid(row=3, column=0, padx="10", pady="15", sticky="w")
        toggle_btn.grid(row=3, column=1, sticky="e")

        insert_button = tk.Button(main_frame, text="Insert", command=insert)
        insert_button.config(font=("Courier", 18))
        insert_button.grid(row=4, column=0, pady=10)

        # Create and configure the Listbox
        global listbox
        listbox = tk.Listbox(main_frame, selectmode=tk.SINGLE)
        listbox.config(font=("Courier", 18), width=25)
        listbox.grid(row=0, column=2, rowspan=500, padx=10, pady=10, sticky='ns')

        c=cnx.cursor()
        c.execute("select * from tag")
        tag = c.fetchall()

        for t in tag:
            index=t[0]
            website_id=t[1]
            listbox.insert(tk.END, f"{index}: {website_id}")
        
        showpass_button = tk.Button(main_frame, text="Show", command=selected_item, width="6", height="1")
        showpass_button.config(font=("Courier", 18))
        showpass_button.grid(row=1, column=3, pady=10, padx=10)


        deletepass_button = tk.Button(main_frame, text="Delete", command=delete_selected_item, width="6", height="1")
        deletepass_button.config(font=("Courier", 18))
        deletepass_button.grid(row=2, column=3, pady=10, padx=10)


    else:
        messagebox.showinfo("Message", "Wrong Credentials")
        username_text.delete(first=0, last=1000)
        loginpassword_text.delete(first=0, last=1000)



#mainloop gia authorization
root = tk.Tk()
root.title("Login")
root.resizable(False, False)

#gia to icon tou button password gia na anoigei o kwdikos visible
img=Image.open("/Users/georgemermigkis/Desktop/coding/PassManager/visible.png")
img=img.resize((20,20))
img=ImageTk.PhotoImage(img)

#gia na allaksw to icon tou ektelesimou
imgIcon=tk.PhotoImage(file="/Users/georgemermigkis/Desktop/coding/PassManager/siren.png")
root.iconphoto(True, imgIcon)

login_frame = tk.Frame(root, bg="black")
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




