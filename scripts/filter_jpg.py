# -*- coding: utf-8 -*-
import argparse
import datetime
from datetime import date
from datetime import datetime
import re
import sys


def intersection(lst1, lst2):
    # Use of hybrid method
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def end_prog(code=0):
    code_str = ''
    if code!=0:
        code_str = f' (met code {code})'
    einde = datetime.today().strftime(f"einde: %H:%M:%S{code_str}")
    stderr(einde)
    print(einde)
    sys.exit(code)


def stderr(text,nl='\n'):
    sys.stderr.write(f'{text}{nl}')


def arguments():
    ap = argparse.ArgumentParser(description='Read inventaris1.txt')
    ap.add_argument('-i', '--inputfile',
                    help="inputfile",
                    default= "inventaris1.txt")
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":
    start = datetime.today().strftime("start: %H:%M:%S")
    stderr(start)

    args = arguments()
    inputfile = args['inputfile']
#    output = args['outputfile']
#    uitvoer_f = open(failed, 'w', encoding='utf-8')

    prog = re.compile('^(.+)\\.(.+)$')
    teller = 0
    count_matched = 0
    count_not_matched = 0
    count_db = 0
    count_thumbs_db = 0
    all_jpg = []
    all_tif = []
    with open('results.txt' , 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            filename = line.split('/')[-1]
            md = prog.match(filename)
            name = md.group(1)
            extension = md.group(2).lower()
            if extension=='jpg':
                all_jpg.append(f'{name}')
            elif extension=='tif':
                all_tif.append(f'{name}')

    stderr(f'all_jpg: {len(all_jpg)}')
    stderr(f'all_tif: {len(all_tif)}')

    stderr(datetime.today().strftime("%H:%M:%S"))
    del_jpg = []
    teller = 0

    del_jpg = intersection(all_tif, all_jpg)
    stderr(f'del_jpg: {len(del_jpg)}')

#    stderr(del_jpg[0:10])

    end_prog(0)

