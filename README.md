# Scripts to move files from the NIOD Archive

`read_inventaris.py` read the list of files and write them to `result.txt` if matched of `failed.txt` if not.

`filter_jpg.py` Take a list of all `jpg` and `tif` files in `result.txt` and make a list of all that occur in both.

`test.py` tests several filenames to see if they can be matched.

## The Move Script

`move_files.py` moves or copies the files from the old to the new depot. It also makes a list like `read_inventaris.py` does.

Parameters:

`-v` inventory list: all the files and their locations to be moved

`-i` the inputdir (old depot)

`-o` the outputdir (new depot)

`-m` switch: if added set `do_move` to `True`

`-c` switch: if added set `do_copy` to `True`; if both `-m` and `-c` are used `-c` overwrites `-m`, i.e. files are copied but not moved!

`-r` resultsfile

`-f` list of failed filename conversions

If both `-m` and `-c` are `False` you perform a 'dry run', i.e. a series of `mv source target` are printed on the prompt.
