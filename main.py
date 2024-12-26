# initalizations
import tkinter
import os
import smtplib
from cryptography.fernet import Fernet
import random
loginwin = tkinter.Tk()

smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "bunny.rnd@gmail.com"
smtp_password = "aebx xjjx rnpm ynxl"

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

# user functions
def checkuserexist(name):
    if os.path.isfile(f"./{name}.txt"):
        return True
    else:
        return False

def infochecker(name, password):
    with open(name + ".txt", "rb") as fil:
        q = fil.read()
    if decryptor(q) == password:
        return True
    else:
        return False
    
def newuser(name, passward, email):
    with open(name + ".txt", "wb") as fil:
        fil.writelines([encryptor(passward), encryptor(email)])

def getinfo(name, line): # line is the line number of the info you want (passwords are on the first line, emails on the seconds)
    with open(name + ".txt", "rb") as fil:
        q = fil.read()
        print(type(q))
    return decryptor(q).split("\n")[(line-1)]

def passvalidity(password, name = "password"):
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
    else:
        return True, "Password is valid"

def passsuggest():
    x = True
    while x == True:
        n = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_+[];:,.<>?", k=(random.randint(8, 12))))
        if passvalidity(n):
            x = False
    return n

def deleteuser(name):
    os.remove(name + ".txt")
    # add a message box to confirm deletion
    # send an email to user to confirm deletion

'''def changepassword(name, password):
    with open(name + ".txt", "wb") as fil:
        fil.write(encryptor(password))ure
        # a later feature'''

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

# encryptor and decryptor functions

def encryptor(password):
    epassword = password.encode('utf-8')
    ecpass = genkey().encrypt(epassword)
    return ecpass

def decryptor(password):
    dpassword = genkey().decrypt(password)
    dcpass = dpassword.decode('utf-8')
    return dcpass

# testing (no input yet so manually)
if not checkuserexist("mward"):
    newuser("mward", "quacquack", "all4music4us@gmail.com")
    print("new user detected")
else:
    print("User already exists")
    getinfo("mward", 1)

# login window
while True:
    loginwin.title("Login Window")
    loginwin.geometry("400x400")
    loginwin.resizable(True, False)
    loginwin.configure(bg="black")
    # background image
    # bg = tkinter.PhotoImage(file="bg.png")
    loginwin.iconbitmap("omward_corral.ico")
    loginwin.mainloop()