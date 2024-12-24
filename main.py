# initalizations
import tkinter
import os
from cryptography.fernet import Fernet
loginwin = tkinter.Tk()

path = __file__
path = path.replace("main.py", "userpasswords")
# change the directory to the userpasswords folder
os.chdir(path)

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

# when called this function will work (tested)
def newuser(name, passward):
    with open(name + ".txt", "wb") as fil:
        fil.write((encryptor(passward)))

def checkuserexist(name):
    if os.path.isfile(f"./{name}.txt"):
        # only for testing
        with open(name + ".txt", "rb") as fil:
            q = fil.read()
        print(decryptor(q))
        return True
    else:
        return False
    
def encryptor(password):
    epassword = password.encode('utf-8')
    ecpass = genkey().encrypt(epassword)
    return ecpass

def decryptor(password):
    dpassword = genkey().decrypt(password)
    dcpass = dpassword.decode('utf-8')
    return dcpass

if not checkuserexist("omward"):
    newuser("omward", "quackquack")
else:
    print("User already exists")
# main login window loop
'''while True:
    loginwin.title("Login Window")
    loginwin.geometry("400x400")
    loginwin.resizable(True, False)
    loginwin.configure(bg="black")
    # background image
    # bg = tkinter.PhotoImage(file="bg.png")
    loginwin.iconbitmap("omward_corral.ico")
    loginwin.mainloop()'''