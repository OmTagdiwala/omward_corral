# initalizations
import tkinter
from tkinter import messagebox
from tkinter import PhotoImage
import os
import smtplib
import hashlib
from cryptography.fernet import Fernet
import random

### general functions

def emailuser(email, purpose, body):    
    message = f'Subject: {purpose}\n\n{body}'
    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.sendmail("bunny.rnd@gmail.com", email, message)

def infowriter(desc, passname="", password="", pemail="", note=""):
    with open(hasher(xerror) + ".txt", "ab") as fil:
        fil.write(encryptor(passname) + b"," + encryptor(password) + b"," + encryptor(pemail) + b"," + encryptor(note) + b"," + encryptor(desc) + b"\n")

def passsuggest():
    x = True
    while x == True:
        n = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_+[];:.<>?", k=(random.randint(8, 12))))
        if passvalidity(n):
            x = False
    return n

def infofinder(name, passname):
    with open(hasher(name) + ".txt", "rb") as fil:
        q = fil.readlines()
        for i in q[1:]:
            l = i.split(b",")
            if l[0] == encryptor(passname):
                w = l[1]
                break
            else:
                continue
        return decryptor(w)

# encryptor and decryptor functions
def encryptor(password):
    epassword = password.encode('utf-8')
    ecpass = genkey().encrypt(epassword)
    return ecpass

def decryptor(password):
    dpassword = genkey().decrypt(password)
    dcpass = dpassword.decode('utf-8')
    return dcpass

### login functions

loginwin = tkinter.Tk()

smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "bunny.rnd@gmail.com"
smtp_password = "aebx xjjx rnpm ynxl"
eye = (PhotoImage(file="eye.png")).subsample(15, 15)
closeye = (PhotoImage(file="closeye.png")).subsample(15, 15)
success = False
path = __file__
path = path.replace("main.py", "userpasswords")
# change the directory to the userpasswords folder
os.chdir(path)

# key generator function
def genkey():
    if not os.path.exists("xxx.txt"):
        key = Fernet.generate_key()
        with open("xxx.txt", "wb") as key_file:
            key_file.write(key)
    else:
        with open("xxx.txt", "rb") as key_file:
            key = key_file.read()
    cs = Fernet(key)
    return cs

# changing user info functions

def newuser(name, passward, confpass, email):
    if os.path.exists(hasher(name) + ".txt"):
        messagebox.showerror("Error", "User already exists\nTry a different username")
    elif passvalidity(passward, confpass, name)[0] == False:
        messagebox.showerror("Error", passvalidity(passward, confpass, name)[1])
    elif verifyemail(email) == False:
        messagebox.showerror("Error", "Email is invalid")
    elif passvalidity(passward, confpass, name)[0] == True and verifyemail(email) == True and not os.path.exists(hasher(name) + ".txt"):
        confirmuser(name, passward, email)
    else:
        messagebox.showerror("Error", "Unknown error, try something else")

def confirmuser(name, passward, email):
    global confcode
    confcode = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", k=5))
    emailuser(email, "Omward Corral Confirmation Code", f"Your confirmation code is {confcode}")
    messagebox.showinfo("Confirm Account", "Confirmation code has been sent to your email (check spam too)")
    global newbutton
    newbutton.config(text="Resend Code", command=lambda: [confirmuser(name, passward, email)]) 
    checkcode(name, passward, email)

def checkcode(name, password, email):
    confirmlab = tkinter.Label(loginwin, text="Enter Your Confirmation Code", font=("Segoe UI", 12), fg="white", bg="black")
    confirmlab.pack(side="top", anchor="w")
    confirmentry = tkinter.Entry(loginwin, font=("Segoe UI", 12), fg="black", bg="white")
    confirmentry.pack(side="top", anchor="w")
    print(confcode)
    loginwin.bind("<Return>", lambda event: createuser(name, password, email) if confcode == confirmentry.get() else messagebox.showerror("Error", "Confirmation code is incorrect"))
    confirmbtn = tkinter.Button(loginwin, text="Confirm", font=("Segoe UI", 12), fg="black", bg="white", command=lambda: createuser(name, password, email) if confcode == confirmentry.get() else messagebox.showerror("Error", "Confirmation code is incorrect"))    
    confirmbtn.pack(side="top", anchor="w")

def createuser(name, passward, email):
    global xerror
    xerror = name
    messagebox.showinfo("Success!", "User has been successfully created\nNow try logging in")
    with open(hasher(xerror) + ".txt", "wb") as fil:
        fil.write((hasher(name)).encode() + b"," + encryptor(passward) + b"," + encryptor(email) + b"\n")
    loginwin.bind("<Return>", lambda event: infochecker(userentry.get(), passentry.get()))
    loginwin.geometry("400x250")
    print(name, passward, email)

def passvalidity(password, confpassword=",", name = "password"):
    if password != confpassword and confpassword != ",":
        return False, "Passwords do not match"
    if len(password) < 8:
        return False, "Length of password is less than 8 characters"
    if password == name:
        return False, "Password is the same as username"
    if password.islower():
        return False, "Password is all lowercase"
    if password.isupper():
        return False, "Password is all uppercase"
    if password.isnumeric():
        return False, "Password is all numbers"
    if password.isalpha():
        return False, "Password is all letters"
    if password.isalnum():
        return False, "Password is only alphanumeric"
    if password.isspace():
        return False, "Password is all spaces"
    if "," in password:
        return False, "Password contains a comma (invalid for program purposes)"
    else:
        return True, "Password is valid"

'''def forgotpassword():
    pass
    # a later feature'''

'''def changepassword(name, password):
    with open(name + ".txt", "wb") as fil:
        fil.write(encryptor(password))ure
        # a later feature'''

def deleteuser():
    os.remove(hasher(xerror) + ".txt")
    # add a message box to confirm deletion
    # send an email to user to confirm deletion

# email functions

def verifyemail(email):
    if "@" in email and "." in email:
        return True
    else:
        return False


# logging in

def infochecker(name, password):
    try: # if the file cant be found, it'll error and so return False
        with open(hasher(name) + ".txt", "rb") as fil:
            q = fil.readline()
        if decryptor((q.split(b","))[1]) == password: # if file is found, it'll check for username
            global xerror
            xerror = name
            global success
            success = True
            loginwin.destroy()
        else:
            wrong()
    except:
        return wrong()

# basic functions

def hasher(name):
    return hashlib.sha256(name.encode('utf-8')).hexdigest()

# correct or incorrect password functions
def wrong():
    messagebox.showerror("Error", "Incorrect Username or Password")
def showpassword(event):
    passentry.config(show="")
    showbutton.config(image=eye)  
def hidepassword(event):
    passentry.config(show="*")
    showbutton.config(image=closeye)

# new user info maker
def newuserinfo():
    newuserbut.config(state="disabled")
    loginwin.bind("<Return>", lambda event: [newuser(userentry.get(), passentry.get(), confirmpassentry.get(), emailentry.get())])
    loginwin.geometry("400x600")
    title = tkinter.Label(loginwin, text="New User?", font=("Segoe UI Black", 17), justify="center", fg="white", bg="black")
    title.pack(side="top", anchor="center")
    userlabel = tkinter.Label(loginwin, text="Username", font=("Segoe UI", 12), fg="white", bg="black")
    userlabel.pack(side="top", anchor="w")
    userentry = tkinter.Entry(loginwin, font=("Segoe UI", 12), fg="black", bg="white")
    userentry.pack(side="top", anchor="w")
    # password
    passlabel = tkinter.Label(loginwin, text="Password", font=("Segoe UI", 12), fg="white", bg="black")
    passlabel.pack(side="top", anchor="w")
    # password entry should be in dots
    # allow password to be shown while a button is pressed
    passentry = tkinter.Entry(loginwin, font=("Segoe UI", 12), fg="black", bg="white", show="*")
    passentry.pack(side="top", anchor="w")
    # confirm password
    confirmpasslabel = tkinter.Label(loginwin, text="Confirm Password", font=("Segoe UI", 12), fg="white", bg="black")
    confirmpasslabel.pack(side="top", anchor="w")
    confirmpassentry = tkinter.Entry(loginwin, font=("Segoe UI", 12), fg="black", bg="white", show="*")
    confirmpassentry.pack(side="top", anchor="w")

    # email
    emaillabel = tkinter.Label(loginwin, text="Email", font=("Segoe UI", 12), fg="white", bg="black")
    emaillabel.pack(side="top", anchor="w")
    emailentry = tkinter.Entry(loginwin, font=("Segoe UI", 12), fg="black", bg="white")
    emailentry.pack(side="top", anchor="w")
    # newuser button
    global newbutton
    newbutton = tkinter.Button(loginwin, text="Create User", font=("Segoe UI", 12), fg="black", bg="white", command=lambda: [newuser(userentry.get(), passentry.get(), confirmpassentry.get(), emailentry.get())])
    newbutton.pack(side="top", anchor="w")

# testing (no input yet so manually)
'''if not infochecker("mward", "quacquack"):
    newuser("mward", "quacquack", "all4music4us@gmail.com")
    print("new user detected")
else:
    print("User already exists")
    getinfo("mward", 1)'''

# login window

loginwin.title("Login Window")
loginwin.geometry("400x250")
loginwin.resizable(True, False)
loginwin.configure(bg="black")
title = tkinter.Label(loginwin, text="Welcome to Omward Corral!", font=("Segoe UI Black", 17), justify="center", fg="white", bg="black")
title.pack(side="top", anchor="center")
userlabel = tkinter.Label(loginwin, text="Username", font=("Segoe UI", 12), fg="white", bg="black")
userlabel.pack(side="top", anchor="w")
userentry = tkinter.Entry(loginwin, font=("Segoe UI", 12), fg="black", bg="white")
userentry.pack(side="top", anchor="w")
# password
passlabel = tkinter.Label(loginwin, text="Password", font=("Segoe UI", 12), fg="white", bg="black")
passlabel.pack(side="top", anchor="w")
# password entry should be in dots
# allow password to be shown while a button is pressed
passentry = tkinter.Entry(loginwin, font=("Segoe UI", 12), fg="black", bg="white", show="*")
passentry.pack(side="top", anchor="w")
# show password button
showbutton = tkinter.Button(loginwin, image=closeye, font=("Segoe UI", 12), fg="black", bg="white")
showbutton.pack(side="top", anchor="w")
showbutton.bind("<ButtonPress-1>", showpassword)
showbutton.bind("<ButtonRelease-1>", hidepassword)
# if enter is pressed it will try the infochecker function
loginwin.bind("<Return>", lambda event: infochecker(userentry.get(), passentry.get()))
# login button
loginbutton = tkinter.Button(loginwin, text="Login", font=("Segoe UI", 12), fg="black", bg="white", command=lambda: [infochecker(userentry.get(), passentry.get())])
loginbutton.pack(side="top", anchor="w")
newuserbut = tkinter.Button(loginwin, text="New User?", font=("Segoe UI", 12), fg="black", bg="white", command=newuserinfo)
newuserbut.pack(side="top", anchor="w")
# forgot password button
# forgotbutton = tkinter.Button(loginframe, text="Forgot Password", font=("Segoe UI", 12), fg="black", bg="white", command=forgotpassword)
# forgotbutton.pack(side="top", anchor="w")
# exit button
# background image
# bg = tkinter.PhotoImage(file="bg.png")
loginwin.iconbitmap("omward_corral.ico")
loginwin.mainloop()

### main functions

# main window
def passwin(desc, passname, password, pemail, note):
    passwin = tkinter.Tk()
    passwin.title(desc)
    passwin.geometry("300x610")
    passwin.resizable(True, True)
    passwin.configure(bg="black")
    # copiolet, add entries for the description, username, password, email, and notes 
    desc_label = tkinter.Label(passwin, text="Description: ", font=('Bahnschrift SemiBold SemiConden', 12), bg="black", fg="white")
    desc_label.pack()
    desc_entry = tkinter.Entry(passwin, font=('Century Gothic', 12))
    desc_entry.insert(0, desc)
    desc_entry.pack()
    passname_label = tkinter.Label(passwin, font=('Bahnschrift SemiBold SemiConden', 12), text="Username: ", bg="black", fg="white")
    passname_label.pack()
    passname_entry = tkinter.Entry(passwin, font=('Century Gothic', 12))
    passname_entry.insert(0, passname)
    passname_entry.pack()
    password_label = tkinter.Label(passwin, font=('Bahnschrift SemiBold SemiConden', 12), text="Password: ", bg="black", fg="white")
    password_label.pack()
    password_entry = tkinter.Entry(passwin, font=('Century Gothic', 12))
    password_entry.insert(0, password)
    password_entry.pack()
    pemail_label = tkinter.Label(passwin, font=('Bahnschrift SemiBold SemiConden', 12), text="Email: ", bg="black", fg="white")
    pemail_label.pack()
    pemail_entry = tkinter.Entry(passwin, font=('Century Gothic', 12))
    pemail_entry.insert(0, pemail)
    pemail_entry.pack()
    note_label = tkinter.Label(passwin, font=('Bahnschrift SemiBold SemiConden', 12), text="Notes: ", bg="black", fg="white")
    note_label.pack()
    note_entry = tkinter.Text(passwin, font=('Century Gothic', 12), height=15, width=30)
    note_entry.insert(tkinter.END,note)
    note_entry.pack(pady=10)
    # add a save button
    passwin.bind("<Control-s>", lambda event: infowriter(desc=desc_entry.get(), passname=passname_entry.get(), password=password_entry.get(), pemail=pemail_entry.get(), note=note_entry.get(tkinter.END))) # infowriter function here
    save_button = tkinter.Button(passwin, text="Save", font=('Bahnschrift SemiBold SemiConden', 12), bg="black", fg="white", command=lambda: infowriter(desc=desc_entry.get(), passname=passname_entry.get(), password=password_entry.get(), pemail=pemail_entry.get(), note=note_entry.get(tkinter.END))) # info writer function here
    save_button.pack()
    # , lambda event: infowriter(desc=desc_entry.get(), passname=passname_entry.get(), password=password_entry.get(), pemail=pemail_entry.get(), note=note_entry.get())
    passwin.iconbitmap("omward_corral.ico")
    passwin.mainloop()


if success == True:
    mainwin = tkinter.Tk()
    mainwin.title("Omward Corral")
    mainwin.geometry("800x600")
    mainwin.resizable(True, True)
    mainwin.configure(bg="black")
    mainwin.iconbitmap("omward_corral.ico")
    nepass = tkinter.Button(mainwin, text="New", font=("Segoe UI", 12), fg="black", bg="white", command=lambda: [passwin("", "", "", "", "")])
    nepass.pack()
    '''# main menu
    mainmenu = tkinter.Menu(mainwin)
    mainwin.config(menu=mainmenu)
    # file menu
    filemenu = tkinter.Menu(mainmenu, tearoff=0)
    mainmenu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New", command=lambda: [infowriter("New")])
    filemenu.add_command(label="Open", command=lambda: [infowriter("Open")])
    filemenu.add_command(label="Save", command=lambda: [infowriter("Save")])
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=mainwin.quit)
    # edit menu
    editmenu = tkinter.Menu(mainmenu, tearoff=0)
    mainmenu.add_cascade(label="Edit", menu=editmenu)
    editmenu.add_command(label="Cut")
    editmenu.add_command(label="Copy")
    editmenu.add_command(label="Paste")
    # help menu
    helpmenu = tkinter.Menu(mainmenu, tearoff=0)
    mainmenu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About")'''
    # main window

    mainwin.mainloop()