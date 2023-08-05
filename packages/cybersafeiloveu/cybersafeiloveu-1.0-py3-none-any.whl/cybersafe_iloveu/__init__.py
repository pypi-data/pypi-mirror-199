from tkinter import messagebox
import rotatescreen


global result

def show_Message(string2):
    global result
    result = messagebox.askyesno(title="Coded by CyberSafe", message=string2)

def check():
    if (result == True):
        messagebox.showinfo(title="I love U", message="Thanks I Love U too")

    else:
        messagebox.showwarning(title="I hate U", message="I'm going to destroy your PC!!")
        destroy()
def destroy():
    screen = rotatescreen.get_primary_display()

    for i in range(9999):
        #left
        #time.sleep(1)
        screen.set_portrait_flipped()

        #flip
        #time.sleep(1)
        screen.set_landscape_flipped()

        #right
        #time.sleep(1)
        screen.set_portrait()

        #normal
        #time.sleep(1)
        screen.set_landscape()
