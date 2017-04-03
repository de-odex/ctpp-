
# pp!catch second prototype
import tkinter
import requests
import math

# window stuff
window = tkinter.Tk()
window.title("pp!catch")
window.wm_iconbitmap('pp!catch.ico')
window.geometry("250x300")
window.resizable(False, False)
window.grid()

modnames = None
stars = None
# GUI functions
filenm = None


def ppdisplaying(pp):
	if(False):
		ppdisplay.configure(text=str(pp) + "pp with mods " + modnames)
	else:
		ppdisplay.configure(text=str(pp) + "pp with no mods")

# end


# logic function


def calculatepp():
	global modnames, btmp_id, stars, max_player_comboI, missI, accI
	modnames = {}

	# request for star rating
	print(btmp_idI)
	beatmap_id = btmp_idI.get()
	print(beatmap_id)
	parameters = {
		"k": "7ec7168b3a0b7bec07fe66e7bbe259a15bafc287",
		"b": beatmap_id,
		"m": 2,
		"a": 1
	}
	osuresponse = requests.get("https://osu.ppy.sh/api/get_beatmaps", params=parameters)
	osudata = osuresponse.json()
	print(osudata)
	stars = float(osudata[0]["difficultyrating"])
	max_combo = int(osudata[0]["max_combo"])
	max_player_combo = int(max_player_comboI.get()) if max_player_comboI is not None else 0
	miss = int(missI.get()) if missI is not None else 0
	acc = float(accI.get()) if accI is not None else 100
	ar = float(osudata[0]["diff_approach"])

	finalpp = pow(((5 * max(1, stars / 0.0049)) - 4), 2) / 100000
	finalpp *= 0.95 + 0.4 * min(1.0, max_combo / 3000.0) + (math.log(max_combo / 3000.0, 10) * 0.5 if max_combo > 3000 else 0.0)
	finalpp *= pow(0.97, miss)
	finalpp *= pow(max_player_combo / max_combo, 0.8)
	if (ar > 9):
		finalpp *= 1 + 0.1 * (ar - 9.0)
	if (ar < 8):
		finalpp *= 1 + 0.025 * (8.0 - ar)
	else:
		finalpp *= 1
	finalpp *= pow(acc / 100, 5.5)

	# mods
	# if HD do: finalpp *= 1.05 + 0.075 * (10.0 - min(10.0, approachRate))

	# end
	ppdisplaying(round(finalpp, 2))

# end


icon = tkinter.PhotoImage(file="pp!catch.png")
iconlabel = tkinter.Label(window, image=icon)
iconlabel.pack()

# beatmap stuff
titleinfo = tkinter.Label(window, text="")
titleinfo.pack()

btmp_idI = tkinter.StringVar()
btmp_id = tkinter.Entry(window, textvariable=btmp_idI)
btmp_id.pack()

# max combo, acc, mods stuff
combo_info = tkinter.Label(window, text="Combo (Default: Max):")
combo_info.pack()

max_player_comboI = tkinter.StringVar()
combo = tkinter.Entry(window, textvariable=max_player_comboI)
combo.pack()

miss_info = tkinter.Label(window, text="Misses (Default: 0):")
miss_info.pack()

missI = tkinter.StringVar()
miss = tkinter.Entry(window, textvariable=missI)
miss.pack()

acc_info = tkinter.Label(window, text="Accuracy (Default: Perfect):")
acc_info.pack()

accI = tkinter.StringVar()
acc = tkinter.Entry(window, textvariable=accI)
acc.pack()

# buttotanical!
calc = tkinter.Button(window, text="Calculate pp!", command=calculatepp)
calc.pack()

ppdisplay = tkinter.Label(window, text="")
ppdisplay.pack()

# END OF MAIN CODE

window.mainloop()
