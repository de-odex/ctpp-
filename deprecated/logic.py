
file = CtPP.entryVariable.get()

with open(file, 'r') as f:
	for line in f:
		if '[HitObjects]' in line:
			for line in f:  # now you are at the lines you want
				# do work
