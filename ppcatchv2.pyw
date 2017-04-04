
# pp!catch second prototype
import tkinter
import requests
import math
import configparser
# import os.path

# window stuff
window = tkinter.Tk()
window.title("pp!catch")
window.wm_iconbitmap('pp!catch.ico')

windowh = 400
windoww = 300

window.minsize(width=windoww, height=windowh)
window.maxsize(width=windoww, height=windowh)
window.resizable(False, False)
window.grid()
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

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

def configuration():
	configfile = configparser.ConfigParser()
	configfile["Default"] = {'APIKey': 0, 'username': ""}
	confwin = tkinter.Toplevel(window)
	confwin.title("Settings")
	confwin.wm_iconbitmap('pp!catch.ico')
	confwin.geometry("200x300")
	confwin.resizable(False, False)
	tester = tkinter.Label(confwin, text="angery")
	tester.pack(fill="both", expand=1)


def get_api_data(api_key):
	# request for data
	beatmap_id = btmp_idI.get()
	if beatmap_id == "":
		ppdisplay.configure(text="Invalid beatmap ID.\n Click the difficulty name and try again")
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

# icon
icon = tkinter.PhotoImage(file="pp!catch.png")
iconlabel = tkinter.Label(window, image=icon)
iconlabel.grid(columnspan=3)

# config button
configurate = tkinter.Button(window, text="Configuration", command=configuration)
configurate.grid(columnspan=3)

# beatmap stuff
titleinfo = tkinter.Label(window, text="Beatmap ID:")
titleinfo.grid(columnspan=3)

btmp_idI = tkinter.StringVar()
btmp_id = tkinter.Entry(window, textvariable=btmp_idI)
btmp_id.grid(columnspan=3)

# max combo, acc, miss
combo_info = tkinter.Label(window, text="Combo (Default: Max):")
combo_info.grid(columnspan=3)

max_player_comboI = tkinter.StringVar()
combo = tkinter.Entry(window, textvariable=max_player_comboI)
combo.grid(columnspan=3)

miss_info = tkinter.Label(window, text="Misses (Default: 0):")
miss_info.grid(columnspan=3)

missI = tkinter.StringVar()
miss = tkinter.Entry(window, textvariable=missI)
miss.grid(columnspan=3)

acc_info = tkinter.Label(window, text="Accuracy (Default: Perfect):")
acc_info.grid(columnspan=3)

accI = tkinter.StringVar()
acc = tkinter.Entry(window, textvariable=accI)
acc.grid(columnspan=3)

# mods
HD = tkinter.IntVar()
tkinter.Checkbutton(window, text="HD", variable=HD).grid(column=0, sticky='w')

FL = tkinter.IntVar()
tkinter.Checkbutton(window, text="FL", variable=FL).grid(column=1, sticky='w')

NF = tkinter.IntVar()
tkinter.Checkbutton(window, text="NF", variable=NF).grid(column=2, sticky='w')

DT = tkinter.IntVar()
tkinter.Checkbutton(window, text="DT (WIP)", variable=DT).grid(column=0, sticky='w')

HR = tkinter.IntVar()
tkinter.Checkbutton(window, text="HR (WIP)", variable=HR).grid(column=1, sticky='w')

# buttotanical!
calc = tkinter.Button(window, text="Calculate pp!", command=calculatepp)
calc.grid(columnspan=3)

ppdisplay = tkinter.Label(window, text="")
ppdisplay.grid(columnspan=3, rowspan=3)

# END OF MAIN CODE

window.mainloop()
