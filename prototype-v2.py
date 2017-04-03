
# pp!catch second prototype
import tkinter
import os
from tkinter import filedialog

# window stuff
window = tkinter.Tk()
window.title("pp!catch")
window.wm_iconbitmap('pp!catch.ico')
window.geometry("250x300")
window.resizable(False, False)
window.grid()


# GUI functions
filenm = None


def ppdisplaying(pp):
	if(False):
		ppdisplay.configure(text=str(pp) + "pp with mods " + modnames)
	else:
		ppdisplay.configure(text=str(pp) + "pp with no mods")


def filechoosing():
	global filenm
	filenm = filedialog.askopenfilename(title="Choose a beatmap difficulty", defaultextension="osu", filetypes=[("osu! beatmaps", "osu")], initialdir=os.getenv('LOCALAPPDATA') + "/osu!/Songs")

# end


# logic function
finalpp = 0
modnames = ""
stars = 0


def calculatepp():
	global finalpp, modnames, stars
	if filenm is not None:
		file = open(filenm)
		data = file.read()
		file.close()
		print("I got %d bytes from this file." % len(data))
	ppdisplaying(finalpp)

# end


icon = tkinter.PhotoImage(file="pp!catch.png")
iconlabel = tkinter.Label(window, image=icon)
iconlabel.pack()

filenm = tkinter.Button(window, text="Choose an .osu file", command=filechoosing)
filenm.pack()

calc = tkinter.Button(window, text="Calculate pp!", command=calculatepp)
calc.pack()

ppdisplay = tkinter.Label(window, text="")
ppdisplay.pack()

# END OF MAIN CODE

window.mainloop()
