
# pp!catch second prototype
import tkinter
import requests
import math
import configparser
import os.path

# window stuff
window = tkinter.Tk()
window.title("pp!catch")
window.wm_iconbitmap('pp!catch.ico')

windowh = 500
windoww = 400

window.minsize(width=windoww, height=windowh)
window.maxsize(width=int(windoww * 1.5), height=windowh)
window.resizable(True, False)
window.grid()
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1, minsize=windoww / 2)
window.grid_columnconfigure(1, weight=1, minsize=windoww / 2)

modnames = None
stars = None
filenm = None

config = configparser.ConfigParser()

# start up checking
if not os.path.isfile("config.ini") or os.path.getsize("config.ini") == 0:
	open("config.ini", 'a')
	config.read("config.ini")
	config.set('DEFAULT', 'APIKey', '0')
	config.set('DEFAULT', 'username', '0')
	config.write(open("config.ini", "a"))


# GUI functions


def ppdisplaying(pp):
	if(False):
		ppdisplay.configure(text=str(pp) + "pp with mods " + modnames)
	else:
		ppdisplay.configure(text=str(pp) + "pp with no mods")

# END


# logic function

def configuration():
	# configfile = configparser.ConfigParser()

	confwin = tkinter.Toplevel(window)
	confwin.title("Settings")
	confwin.wm_iconbitmap('pp!catch.ico')
	confwin.geometry("200x300")
	confwin.resizable(False, False)
	confwin.grid()

	config_frame = tkinter.Frame(confwin, bd=1, relief="sunken")
	config_frame.grid_columnconfigure(0, weight=1, minsize=100)
	config_frame.grid_columnconfigure(1, weight=1, minsize=100)

	tester = tkinter.Label(config_frame, text="WIP")
	tester.pack()
	config_frame.grid(row=0, column=0, columnspan=2, sticky="NEWS")


def get_b_data(api_key):
	# request for data
	beatmap_id = btmp_idI.get()
	if beatmap_id == "":
		errors.configure(text="Invalid beatmap ID.\n Click the difficulty name and try again")
	parameters = {
		"k": api_key,
		"b": beatmap_id,
		"m": 2,  # pick ctb game mode
		"a": 1  # allow converts
	}
	osubresponse = requests.get("https://osu.ppy.sh/api/get_beatmaps", params=parameters)
	return osubresponse.json()


def calculatepp():
	global modnames, btmp_id, stars, max_player_comboI, missI, accI
	modnames = {}

	config.read('config.ini')
	api_key = config.get("DEFAULT", "APIKey")
	# var setting
	if api_key is not "":
		osubdata = get_b_data(api_key)
	else:
		errors.configure(text="No API Key! Please indicate one in the config.ini.\n API Key can be found at \"https://osu.ppy.sh/p/api\".")
		pass
	stars = float(osubdata[0]["difficultyrating"])
	max_combo = int(osubdata[0]["max_combo"])
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
	ar = float(osubdata[0]["diff_approach"])

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
	# END

	ppdisplaying(round(finalpp, 2))


def getuserdata():
	pass

# END


# GUI
# # Frames

title_frame = tkinter.Frame(window, bd=1, relief="flat")
input_frame = tkinter.Frame(window, bd=1, relief="flat")
output_frame = tkinter.Frame(window, bd=1, relief="flat")

# # END

# # Elements
# # # icon
icon = tkinter.PhotoImage(file="pp!catch.png")
iconlabel = tkinter.Label(title_frame, image=icon)
iconlabel.pack()

# # # config button
configurate = tkinter.Button(title_frame, text="Configuration", command=configuration)
configurate.pack()
# # # beatmap stuff
titleinfo = tkinter.Label(input_frame, text="Beatmap ID:")
titleinfo.pack()

btmp_idI = tkinter.StringVar()
btmp_id = tkinter.Entry(input_frame, textvariable=btmp_idI)
btmp_id.pack()

# # # max combo, acc, miss
combo_info = tkinter.Label(input_frame, text="Combo (Default: Max):")
combo_info.pack()

max_player_comboI = tkinter.StringVar()
combo = tkinter.Entry(input_frame, textvariable=max_player_comboI)
combo.pack()

miss_info = tkinter.Label(input_frame, text="Misses (Default: 0):")
miss_info.pack()

missI = tkinter.StringVar()
miss = tkinter.Entry(input_frame, textvariable=missI)
miss.pack()

acc_info = tkinter.Label(input_frame, text="Accuracy (Default: Perfect):")
acc_info.pack()

accI = tkinter.StringVar()
acc = tkinter.Entry(input_frame, textvariable=accI)
acc.pack()

# # # mods
HD = tkinter.IntVar()
tkinter.Checkbutton(input_frame, text="HD", variable=HD).pack()

FL = tkinter.IntVar()
tkinter.Checkbutton(input_frame, text="FL", variable=FL).pack()

NF = tkinter.IntVar()
tkinter.Checkbutton(input_frame, text="NF", variable=NF).pack()

DT = tkinter.IntVar()
tkinter.Checkbutton(input_frame, text="DT (WIP)", variable=DT).pack()

HR = tkinter.IntVar()
tkinter.Checkbutton(input_frame, text="HR (WIP)", variable=HR).pack()

# # # buttotanical!
calc = tkinter.Button(input_frame, text="Calculate pp!", command=calculatepp)
calc.pack()

undisplay = tkinter.Label(output_frame, text="Username: ")
undisplay.pack()

ppdisplay = tkinter.Label(output_frame, text="")
ppdisplay.pack()

errors = tkinter.Label(output_frame, text="Errors will be displayed here")
errors.pack()

# # # END

# # END

# # Frame packing
title_frame.grid(row=0, columnspan=2, sticky="NEWS")
input_frame.grid(column=0, row=1, sticky="NEWS", pady=15)
output_frame.grid(column=1, row=1, sticky="NEWS", pady=15)

# # END

# END

# END OF MAIN CODE

window.mainloop()
