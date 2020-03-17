# MIDI_preprocessing

Script for preprocessing MIDI files by removing or quantising non-monophonic tracks. The script, which takes two arguments, is called as follows: 

    $ python3 midi_preprocessing.py <data_path> <data_dir>

where `<data_path>` is the path on which the directory `<data_dir>`, which contains the MIDI files to be preprocessed, resides. On the same path, the script creates two additional directories with fixed names:

* `midi-all`, in which all files from `<data_dir>` are copied, ignoring any subdirectory structure;
* `midi-preprocessed`, in which the preprocessed files are stored.

Using the [`pretty_midi`](https://github.com/craffel/pretty-midi) library, the script checks, for each MIDI file in `<data_dir>`,  whether the file's individual tracks contain note overlap. If overlap is found and it is significant (more than 1/2 the duration of the left note), the track is removed; if it is insignificant, quantisation is applied by setting the left note's offset to the right note's onset.

Some files are removed in their entirety, as they contain significant note overlap in _all_ of their individual tracks; a list of these files is saved as a text file in `<data_path>`.  
    

