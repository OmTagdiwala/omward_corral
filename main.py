# initalizations
import tkinter
from tkinter import messagebox
from tkinter import PhotoImage
import os
import smtplib
import hashlib
from cryptography.fernet import Fernet
import random
loginwin = tkinter.Tk()

smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "bunny.rnd@gmail.com"
smtp_password = "aebx xjjx rnpm ynxl"
eye = (PhotoImage(file="eye.png")).subsample(15, 15)
closeye = (PhotoImage(file="closeye.png")).subsample(15, 15)

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
    confcode = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", k=5))
    emailuser(email, "Omward Corral Confirmation Code", f"Your confirmation code is {confcode}")
    messagebox.showinfo("Confirm Account", "Confirmation code has been sent to your email (check spam too)")
    checkcode(name, passward, email, confcode)

def checkcode(name, password, email, ogcode):
    confirmlab = tkinter.Label(loginwin, text="Enter Your Confirmation Code", font=("Segoe UI", 12), fg="white", bg="black")
    confirmlab.pack(side="top", anchor="w")
    confirmentry = tkinter.Entry(loginwin, font=("Segoe UI", 12), fg="black", bg="white")
    confirmentry.pack(side="top", anchor="w")
    confirmentry.bind("<Return>", lambda event: mainwin())
    confirmbtn = tkinter.Button(loginwin, text="Confirm", font=("Segoe UI", 12), fg="black", bg="white", command=lambda: createuser(name, password, email) if ogcode == confirmentry.get() else messagebox.showerror("Error", "Confirmation code is incorrect"))    
    confirmbtn.pack(side="top", anchor="w")

def createuser(name, passward, email):
    global xerror
    xerror = name
    messagebox.showinfo("Success!", "User has been successfully created\nNow try logging in")
    with open(hasher(xerror) + ".txt", "wb") as fil:
        fil.write((hasher(name)).encode() + b"," + encryptor(passward) + b"," + encryptor(email) + b"\n")
    loginwin.bind("<Return>", lambda event: infochecker(userentry.get(), passentry.get()))
    loginwin.geometry("400x250")


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
def passwordvalresp():
    pass
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

def emailuser(email, purpose, body):    
    message = f'Subject: {purpose}\n\n{body}'
    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.sendmail("bunny.rnd@gmail.com", email, message)

# logging in

def infochecker(name, password):
    try: # if the file cant be found, it'll error and so return False
        with open(hasher(name) + ".txt", "rb") as fil:
            q = fil.readline()
        if decryptor((q.split(b","))[1]) == password: # if file is found, it'll check for username
            global xerror
            xerror = name
            right()
        else:
            wrong()
    except:
        return wrong()

# basic functions

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

def hasher(name):
    return hashlib.sha256(name.encode('utf-8')).hexdigest()

# correct or incorrect password functions
def right():
    pass
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
newuserbut = tkinter.Button(loginwin, text="New User", font=("Segoe UI", 12), fg="black", bg="white", command=newuserinfo)
newuserbut.pack(side="top", anchor="w")
# forgot password button
# forgotbutton = tkinter.Button(loginframe, text="Forgot Password", font=("Segoe UI", 12), fg="black", bg="white", command=forgotpassword)
# forgotbutton.pack(side="top", anchor="w")
# exit button
# background image
# bg = tkinter.PhotoImage(file="bg.png")
loginwin.iconbitmap("omward_corral.ico")
loginwin.mainloop()

def mainwin():
    pass
# main window