import pretty_midi as pm
import os
import shutil
from sys import argv

script, arg_path, arg_orig_data  = argv

path = arg_path # '/Users/reinierdevalk/Dropbox/SAAM-2018/MelodyShape/data/'
orig = arg_orig_data #'midi/' # contains the original MIDI files, divided over subdirectories
orig_single = 'midi-all/' # contains all files from orig, copied into a single directory
prep = 'midi-preprocessed/' # contains all non-corrupt files from orig_single, preprocessed 
q_threshold = 2

# make empty orig_single directory and copy all original MIDI files into it
if not os.path.exists(path + orig_single):
	os.makedirs(path + orig_single)
else:
	shutil.rmtree(path + orig_single)
	os.makedirs(path + orig_single)
root = path + orig
for root, dirs, files in os.walk(root):
	for filename in files:
		filename = os.path.join(root, filename)
		if os.path.isfile(filename) or os.path.isdir(filename):
			# ignore hidden files
			if not filename.startswith('.'):
				shutil.copy2(filename, path + orig_single)

# list files to preprocess
all_files = os.listdir(path + orig_single)
corrupt_files = [] # add files found to be corrupt here
for item in corrupt_files:
    all_files.remove(item)
all_files.sort()

# make empty prep directory and store the preprocessed files in it. files with 
# significant note overlap in all tracks will be removed completely
if not os.path.exists(path + prep):
	os.makedirs(path + prep)
else:
	shutil.rmtree(path + prep)
	os.makedirs(path + prep)
non_monophonic = []
for s in all_files:
#	name_only = s[:s.casefold().index('.mid')]
	midi_old = pm.PrettyMIDI(path + orig_single + s)
	midi_new = pm.PrettyMIDI()

	# search all tracks for multiple simultaneous notes
	# see https://github.com/craffel/pretty-midi/issues/119
	for instr in midi_old.instruments:
		instr_is_mono = True
		for note1 in instr.notes:
			dur1 = note1.end - note1.start
			# if the instrument is still monophonic: keep searching
			if instr_is_mono == True:
				for note2 in instr.notes:
					# skip any notes that have already been note1
					if not note2.start < note1.start:
						# if there is overlap
						if (note1 != note2) and (note2.start < note1.end):
							overlap = note1.end - note2.start
							# if the overlap is larger than threshold: consider non-monophonic and break
							if overlap > dur1/q_threshold:
								instr_is_mono = False
								break
							# if the overlap is smaller than the threshold: quantise
							else:
								note1.end = note2.start
			# if the instrument is no longer monophonic: proceed to the next instrument
			else:
				break
		# if the instrument is monophonic: add to new MIDI file
		if instr_is_mono:
			midi_new.instruments.append(instr)
	# if the new MIDI file contains tracks: save; else add to list
	if len(midi_new.instruments) != 0:
		midi_new.write(path + prep + s)
	else:
		non_monophonic.append(s)

# save a list of all the MIDI files containing only non-monophonic tracks
removed_files = ''
for item in non_monophonic:
	removed_files = removed_files + item + '\n'

with open(path + 'files_removed.txt', 'w') as text_file:
	text_file.write(removed_files)
