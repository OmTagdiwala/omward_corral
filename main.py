# initalizations
import tkinter
import os
from cryptography.fernet import Fernet
import random
loginwin = tkinter.Tk()

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
        fil.write((encryptor(passward + "\n" + email + "\n")))

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
'''if not checkuserexist("mward"):
    newuser("mward", "quacquack")
    print("new user detected")
else:
    print("User already exists")
'''

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