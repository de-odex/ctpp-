
# pp!catch second prototype
import tkinter

window = tkinter.Tk()
window.title("pp!catch")
window.wm_iconbitmap('pp!catch.ico')
window.geometry("250x300")

# display functions


def ppdisplaying():
	if(False):
		ppdisplay.configure(text=str(finalpp) + "pp with mods " + modnames)
	else:
		ppdisplay.configure(text=str(finalpp) + "pp with no mods")
# end

icon = tkinter.PhotoImage(file="pp!catch.png")
iconlabel = tkinter.Label(window, image=icon)
iconlabel.pack()

btn = tkinter.Button(window, text="calculate pp!", command=ppdisplaying)
btn.pack()

ppdisplay = tkinter.Label(window, text="")
ppdisplay.pack()

# logic

finalpp = 0
modnames = ""
stars = 0

# end

window.mainloop()
