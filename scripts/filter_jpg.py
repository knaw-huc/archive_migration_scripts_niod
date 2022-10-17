# -*- coding: utf-8 -*-
import argparse
import datetime
from datetime import date
from datetime import datetime
import glob
import json
import re
import sys


prog_f1 = re.compile('([0-9]+)(?:_|-)([0-9]+)(?:_|-)([0-9]+)\\.(.+)$')

prog_f2 = re.compile('([0-9]+[a-z]?)(?:_|-)([0-9]+)(?:_|-)([0-9]+)\\.(.+)$')

prog_f3 = re.compile('(?:NL-AsdNIOD|NIOD)?(?:_|-)([0-9a-zA-Z]+?)(?:PRIVACY)?(?:_|-)([0-9a-zA-Z.-]+)(?:_|-)([0-9]+)(?:_[a-zA-Z]+)?\\.(.+)$')

prog_p1 = re.compile('/([0-9]+)/(?:JPG|TIFF)/([0-9]+[a-z]?)/([a-zA-Z0-9-_]+)\\.(.+)')

prog_p2 = re.compile('/([0-9]+)-([0-9]+)/([a-zA-Z0-9-_ ]+)\\.(.+)')

#saved_ext = []

def read_catalogue(catalogue):
    with open('names.csv', newline='') as csvfile:
        reader = csv.DictReader(catalogue)
        for row in reader:
            print(row['TOEGANG'],row['INVNR'])

def do_search(tekst):
    collectie = ''
    inventaris = ''
    sequentie = ''
    extensie = ''
    filename = tekst.split('/')[-1]
    res = prog_f1.search(filename)
    if res:
        return ['a',res.group(1), res.group(2), res.group(3), res.group(4)]
    res = prog_f2.search(filename)
    if res:
        return ['a',res.group(1), res.group(2), res.group(3), res.group(4)]
    res = prog_f3.search(filename)
    if res:
        return ['a',res.group(1), res.group(2), res.group(3), res.group(4)]
    res = prog_p1.search(tekst)
    if res:
        return ['a',res.group(1), res.group(2), res.group(3), res.group(4)]
    res = prog_p2.search(tekst)
    if res:
        return ['b',res.group(1), res.group(2), res.group(3), res.group(4)]
    return ['','','','','']


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
    ap.add_argument('-c', '--catalogue',
                    help="catalogue",
                    default= "catalogus_collectienummers_inventarisnummers.csv")
    ap.add_argument('-o', '--outputfile',
                    help="outputfile",
                    default="results.txt")
    ap.add_argument('-f', '--failed',
                    help="failed conversion",
                    default="failed.txt")
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":
    start = datetime.today().strftime("start: %H:%M:%S")
    stderr(start)
    print(start)

    args = arguments()
    inputfile = args['inputfile']
    catalogue = args['catalogue']
    #catalogus = read_catalogue(catalogue)
    output = args['outputfile']
 #   uitvoer_s = open(output, 'w', encoding='utf-8')
    failed = args['failed']
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
    '''
    for tif in all_tif:
        if tif in all_jpg:
            del_jpg.append(f'{tif}.jpg')
        teller += 1
        if(teller % 1000)==0:
            stderr('.','')
        if(teller % 25000)==0:
            stderr('')
    for jpg in all_jpg:
        if jpg in all_tif:
            del_jpg.append(f'{jpg}.jpg')
        teller += 1
        if(teller % 1000)==0:
            stderr('.','')
        if(teller % 25000)==0:
            stderr('')
'''

    del_jpg = intersection(all_tif, all_jpg)
    stderr(f'del_jpg: {len(del_jpg)}')

    stderr(del_jpg[0:10])


    end_prog(1)
    stderr(f'')

    stderr(f'counted {teller:>7} files')
    stderr(f'counted {count_matched:>7} matched')
    stderr(f'counted {count_not_matched:>7} not matched')
    stderr(f'matched: {(100 * count_matched / teller):>6.2f}%')

    print(f'counted {teller:>7} files')
    print(f'counted {count_matched:>7} matched')
    print(f'counted {count_not_matched:>7} not matched')
    print(f'matched: {(100 * count_matched / teller):>6.2f}%')
    print(f'db: {count_db:>7}')
    print(f'db: {count_thumbs_db:>7} thumbs')

    #stderr(f'\ngevonden extensies: {saved_ext}')

    end_prog(0)
