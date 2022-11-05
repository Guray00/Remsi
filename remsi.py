import sys, re
import os

selectionsList = []
timeSelection = "between(t,0,"
filename = inputFile = end = start = None

# read standard input once, line by line
for line in sys.stdin:
	# detect a start of silence, which is an end of our selection
	end = re.search(r"silence_start: (\d+\.?\d+)", line)
	# detect an end of silence, which is a start of our selection
	start = re.search(r"silence_end: (\d+\.?\d+)", line)

	if filename is None:
		# find the input filename
		filename = re.search(r"Input .+ from '(.+)':", line)
	else:
		if inputFile is None:
			inputFile = filename.group(1)

	if start is not None:
		timeSelection = "between(t," + start.group(1) + ","
	if end is not None:
		timeSelection += end.group(1) + ")"
		selectionsList.append(timeSelection)

# Note: silencedetect apparently handles properly files that start and/or end in silence
# so we don't need to check for that and complete filters with no start or no end
selectionFilter = "'" + "+".join(selectionsList) + "'"

#open text file
text_file = open("./afilter.txt", "w") 
text_file.write("aselect=" + selectionFilter + ",asetpts=N/SR/TB" ) 
text_file.close()

# file di audio
text_file = open("./vfilter.txt", "w") 
text_file.write("select=" + selectionFilter + ",setpts=N/FRAME_RATE/TB") 
text_file.close()

"""
vfilter = "-vf \"select=" + selectionFilter + ",setpts=N/FRAME_RATE/TB\""
afilter = "-af \"aselect=" + selectionFilter + ",asetpts=N/SR/TB\""


# recupero il nome in uscita
filename, file_extension = os.path.splitext(inputFile)		# recupero il nome del file senza estensione
name = os.path.basename(filename)							# recupero il nome del file con estensione
output = f"{filename}[JUNK]{file_extension}"				# creo il nome del file di output

disable_chapter = "-map_chapters -1"


# ffmpeg -i "input" -filter_script:v "./vfilter.txt" -filter_script:a "./afilter.txt" "output"

# output ffmpeg command
# changed the output filename
print("ffmpeg -i", '"' + inputFile + '"', vfilter, afilter, disable_chapter, '"' + output + '"')
"""