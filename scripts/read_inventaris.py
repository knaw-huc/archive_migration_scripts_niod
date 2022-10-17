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

prog_f3 = re.compile('([0-9]+[a-z]?)(?:_|-)([A-Z]?[0-9]+)(?:_|-)([0-9]+)\\.(.+)$')

prog_f9 = re.compile('(?:NL-AsdNIOD|NIOD)?(?:_|-)([0-9a-zA-Z]+?)(?:PRIVACY)?(?:_|-)([0-9a-zA-Z.-]+)(?:_|-)([0-9]+)(?:_[a-zA-Z]+)?\\.(.+)$')

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
    res = prog_f9.search(filename)
    if res:
        return ['a',res.group(1), res.group(2), res.group(3), res.group(4)]
    res = prog_p1.search(tekst)
    if res:
        return ['a',res.group(1), res.group(2), res.group(3), res.group(4)]
    res = prog_p2.search(tekst)
    if res:
        return ['b',res.group(1), res.group(2), res.group(3), res.group(4)]
    return ['','','','','']




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
    uitvoer_s = open(output, 'w', encoding='utf-8')
    failed = args['failed']
    uitvoer_f = open(failed, 'w', encoding='utf-8')

    teller = 0
    count_matched = 0
    count_not_matched = 0
    count_db = 0
    count_thumbs_db = 0
    with open(inputfile , 'r', encoding='utf-8') as f:
        for line in f:
            res = do_search(line.strip())
            if '' not in res:
                [soort,collectie, inventaris, sequentie, extensie] = res
                if extensie=='db':
                    count_db += 1
                if extensie in ['jpg','tif']:
                    p_t = 'preservation'
                else:
                    p_t = 'transcription'
                uitvoer_s.write(f"{line.strip()}\t")
                if soort=='a':
                    uitvoer_s.write(f"NL-AsdNIOD_{collectie}_{inventaris}/{p_t}/NL-AsdNIOD_")
                    uitvoer_s.write(f"{collectie}_{inventaris}_{sequentie}.{extensie}\n")
                else: # soort = 'b
                    uitvoer_s.write(f"NL-AsdNIOD_{collectie}_{inventaris}/")
                    uitvoer_s.write(f"{sequentie}.{extensie}\n")
                count_matched += 1
            else:
                if line.strip().endswith('.db'):
                    count_db += 1
                uitvoer_f.write(f"{line.strip()}\n")
                count_not_matched += 1
                if (count_not_matched % 500)==0:
                    stderr(line.strip())
            if line.strip().endswith('Thumbs.db'):
                count_thumbs_db += 1
            teller += 1

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
