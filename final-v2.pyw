
# pp!catch second prototype
import tkinter
import requests
import math
import osuapikey

# window stuff
window = tkinter.Tk()
window.title("pp!catch")
window.wm_iconbitmap('pp!catch.ico')
window.geometry("300x400")
window.resizable(False, False)
window.grid()
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)


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

def get_api_data():
	# request for star rating
	beatmap_id = btmp_idI.get()
	if beatmap_id == "":
		ppdisplay.configure(text="Invalid beatmap ID.\n Click the difficulty name and try again")
	api_key = osuapikey.api_key
	parameters = {
		"k": api_key,
		"b": beatmap_id,
		"m": 2,
		"a": 1
	}

	osuresponse = requests.get("https://osu.ppy.sh/api/get_beatmaps", params=parameters)
	return osuresponse.json()

def calculatepp():
	global modnames, btmp_id, stars, max_player_comboI, missI, accI
	modnames = {}

	# var setting
	osudata = get_api_data()
	stars = float(osudata[0]["difficultyrating"])
	max_combo = int(osudata[0]["max_combo"])
	try:
		miss = int(missI.get()) if int(missI.get()) < max_combo else 0
	except:
		miss = 0
	try:
		max_player_combo = int(max_player_comboI.get()) if int(max_player_comboI.get()) <= max_combo else max_combo - miss
	except:
		max_player_combo = max_combo - miss
	try:
		acc = float(accI.get()) if float(accI.get()) >= 0 and float(accI.get()) <= 100 else 100
	except:
		acc = float(100)
	ar = float(osudata[0]["diff_approach"])

	# DT must be applied first since it is not a multiplier
	if DT.get() == 1:
		if ar > 5:
			ms = 200 + (11 - ar) * 100
		else:
			ms = 800 + (5 - ar) * 80
		if (ms < 300):
			ar = 11
		elif (ms < 1200):
			ar = round((11 - (ms - 300) / 150) * 100, 0) / 100
		else:
			ar = round((5 - (ms - 1200) / 120) * 100, 0) / 100
		print(ar)
	print(ar)
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
	if HD.get() == 1:
		finalpp *= 1.05 + 0.075 * (10.0 - min(10.0, ar))
	if FL.get() == 1:
		finalpp *= 1.35 * (0.95 + 0.4 * min(1.0, max_combo / 3000.0) + (math.log(max_combo / 3000.0, 10) * 0.5 if max_combo > 3000 else 0.0))
	if NF.get() == 1:
		finalpp *= 0.90
	# end
	ppdisplaying(round(finalpp, 2))

# end


icon = tkinter.PhotoImage(file="pp!catch.png")
iconlabel = tkinter.Label(window, image=icon)
iconlabel.grid(column=0, row=0, columnspan=2)

# beatmap stuff
titleinfo = tkinter.Label(window, text="Beatmap ID:")
titleinfo.grid(column=0, row=1, columnspan=2)

btmp_idI = tkinter.StringVar()
btmp_id = tkinter.Entry(window, textvariable=btmp_idI)
btmp_id.grid(column=0, row=2, columnspan=2)

# max combo, acc, miss
combo_info = tkinter.Label(window, text="Combo (Default: Max):")
combo_info.grid(column=0, row=3, columnspan=2)

max_player_comboI = tkinter.StringVar()
combo = tkinter.Entry(window, textvariable=max_player_comboI)
combo.grid(column=0, row=4, columnspan=2)

miss_info = tkinter.Label(window, text="Misses (Default: 0):")
miss_info.grid(column=0, row=5, columnspan=2)

missI = tkinter.StringVar()
miss = tkinter.Entry(window, textvariable=missI)
miss.grid(column=0, row=6, columnspan=2)

acc_info = tkinter.Label(window, text="Accuracy (Default: Perfect):")
acc_info.grid(column=0, row=7, columnspan=2)

accI = tkinter.StringVar()
acc = tkinter.Entry(window, textvariable=accI)
acc.grid(column=0, row=8, columnspan=2)

# mods
HD = tkinter.IntVar()
tkinter.Checkbutton(window, text="HD", variable=HD).grid(column=0, row=9)

FL = tkinter.IntVar()
tkinter.Checkbutton(window, text="FL", variable=FL).grid(column=1, row=9)

NF = tkinter.IntVar()
tkinter.Checkbutton(window, text="NF", variable=NF).grid(column=0, row=10)

DT = tkinter.IntVar()
tkinter.Checkbutton(window, text="DT (WIP)", variable=DT).grid(column=1, row=10)

HR = tkinter.IntVar()
tkinter.Checkbutton(window, text="HR (WIP)", variable=HR).grid(column=0, row=11)

# buttotanical!
calc = tkinter.Button(window, text="Calculate pp!", command=calculatepp)
calc.grid(column=0, row=12, columnspan=2)

ppdisplay = tkinter.Label(window, text="")
ppdisplay.grid(column=0, row=13, columnspan=2, rowspan=3)

# END OF MAIN CODE

window.mainloop()
