# initalizations
import tkinter
import os
loginwin = tkinter.Tk()

path = __file__
path = path.replace("main.py", "userpasswords")
# change the directory to the userpasswords folder
os.chdir(path)

'''def does_user_exist():
    if os.path.exists(path):
        print("exisiting user")
    else:
        print("new user detected")'''

# when called this function will work (tested)
def newuser(name, passward):
    with open(name + ".txt", "a") as fil:
        fil.write(passward)
        fil.write("\n")

def checkuserexist(name):
    if os.path.isfile(f"./{name}.txt"):
        return True
    else:
        return False
    
# main login window loop
while True:
    loginwin.title("Login Window")
    loginwin.geometry("400x400")
    loginwin.resizable(True, False)
    loginwin.configure(bg="black")
    # background image
    # bg = tkinter.PhotoImage(file="bg.png")
    loginwin.iconbitmap("omward_corral.ico")
    loginwin.mainloop()