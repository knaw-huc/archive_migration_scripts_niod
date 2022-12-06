# -*- coding: utf-8 -*-
import argparse
import datetime
from datetime import datetime
import os
from os.path import dirname
from pathlib import Path
import re
import shutil
import sys

prog_f1 = re.compile('([0-9]+)(?:_|-)([0-9]+)(?:_|-)([0-9]+)\\.(.+)$')

prog_f2 = re.compile('([0-9]+[a-z]?)(?:_|-)([0-9]+)(?:_|-)([0-9]+)\\.(.+)$')

prog_f3 = re.compile('([0-9]+[a-z]?)(?:_|-)([A-Z]?[0-9]+)(?:_|-)([0-9]+)\\.(.+)$')

prog_f9 = re.compile('(?:NL-AsdNIOD|NIOD)?(?:_|-)([0-9a-zA-Z]+?)(?:PRIVACY)?(?:_|-)([0-9a-zA-Z.-]+)(?:_|-)([0-9]+)(?:_[a-zA-Z]+)?\\.(.+)$')

prog_p1 = re.compile('/([0-9]+)/(?:JPG|TIFF)/([0-9]+[a-z]?)/([a-zA-Z0-9-_]+)\\.(.+)')

prog_p2 = re.compile('/([0-9]+)[-_]([0-9]+)/([a-zA-Z0-9-_ ]+)\\.(.+)')

prog_p3 = re.compile('/([0-9]+)-([A-Z][0-9]+)-([0-9]+)/(?:[a-zA-Z0-9-_ ]+)\\.(.+)')


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
    res = prog_p3.search(tekst)
    if res:
        return ['a',res.group(1), res.group(2), res.group(3), res.group(4)]
    return ['','','','','']


def make_target(res):
    preservation =['jpg','tif'] 
    [soort, collectie, inventaris, sequentie, extensie] = res
    extensie = extensie.lower()
    result = ''
    directory = f"NL-AsdNIOD_{collectie}_{inventaris}/"
    result = directory
    if soort=='a':
        if extensie.lower() in preservation:
            p_t = 'preservation'
        else:
            p_t = 'transcription'
        result += f"{p_t}/NL-AsdNIOD_{collectie}_{inventaris}_{sequentie}.{extensie}"
    else: # soort = 'b'
        result += f"{sequentie}.{extensie}"
    return directory,result


def move_file(dir_in,file_in, dir_out, target, do_move=False, do_copy=False):
    source = os.path.join(dir_in,file_in)
    target = os.path.join(dir_out,target)
    if (do_move or do_copy) and not os.path.exists(dirname(target)):
        Path(dirname(target)).mkdir(parents=True)
    if do_move:
        shutil.move(source,target)
    elif do_copy:
        shutil.copy2(source,target)
    else:
        print(f'mv {source} {target}')


def end_prog(code=0):
    code_str = ''
    if code!=0:
        code_str = f' (met code {code})'
    einde = datetime.today().strftime(f"einde: %H:%M:%S{code_str}")
    stderr(einde)
    sys.exit(code)


def stderr(text,nl='\n'):
    sys.stderr.write(f'{text}{nl}')


def arguments():
    ap = argparse.ArgumentParser(description='Read inventaris1.txt')
    ap.add_argument('-v', '--inventaris',
                    help="inventaris",
                    default= "inventaris1.txt")
    ap.add_argument('-c', '--copy',
                    help="copy - default = False (overwrites move)",
                    action='store_true')
    ap.add_argument('-i', '--inputdir',
                    help="inputdir",
                    default="old_niod_depot")
    ap.add_argument('-o', '--outputdir',
                    help="outputdir",
                    default="new_niod_depot")
    ap.add_argument('-m', '--move',
                    help='move immediately (default = False)',
                    action='store_true')
    ap.add_argument('-r', '--resultsfile',
                    help="resultsfile",
                    default="results.txt")
    ap.add_argument('-f', '--failed',
                    help="list of failed conversions",
                    default="failed.txt")
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":
    start = datetime.today().strftime("start: %H:%M:%S")
    stderr(start)
    print(start)

    args = arguments()
    inventaris = args['inventaris']
    dir_in = args['inputdir']
    dir_out = args['outputdir']
    do_move = args['move']
    do_copy = args['copy']
    if do_copy:
        do_move = False
    results = args['resultsfile']
    uitvoer_s = open(results, 'w', encoding='utf-8')
    failed = args['failed']
    uitvoer_f = open(failed, 'w', encoding='utf-8')

    all_dirs = []
    teller = 0
    count_matched = 0
    count_not_matched = 0
    count_db = 0
    count_thumbs_db = 0
    with open(inventaris , 'r', encoding='utf-8') as f:
        for line in f:
            res = do_search(line.strip())
            if '' not in res:
                directory,target = make_target(res)
                move_file(dir_in, line.strip(), dir_out, target, do_move, do_copy)
                uitvoer_s.write(f"{line.strip(target)}\t{target}\n")
                count_matched += 1
            else:
                uitvoer_f.write(f"{line.strip()}\n")
                count_not_matched += 1
            teller += 1

    stderr(f'counted {teller:>7} files')
    stderr(f'counted {count_matched:>7} matched')
    stderr(f'counted {count_not_matched:>7} not matched')
    stderr(f'matched: {(100 * count_matched / teller):>6.2f}%')

    print(f'counted {teller:>7} files')
    print(f'counted {count_matched:>7} matched')
    print(f'counted {count_not_matched:>7} not matched')
    print(f'matched: {(100 * count_matched / teller):>6.2f}%')

    end_prog(0)
