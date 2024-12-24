import tkinter
import os
loginwin = tkinter.Tk()

path = __file__
print(path)

'''def does_user_exist():
    if os.path.exists(path):
        print("exisiting user")
    else:
        print("new user detected")'''

def newuser(name, passward):
    
    with open(str(path+"userpasswords\\" + name), "a") as newuser:
        newuser.write(f"prim pass: {passward}")



while True:
    newuser("quacky", "amongus")

    loginwin.mainloop()
