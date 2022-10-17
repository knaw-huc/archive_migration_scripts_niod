# -*- coding: utf-8 -*-
import argparse
import csv
from datetime import datetime
import re
import sys
import xlrd 
import json
from pprint import pprint
from read_inventaris import do_search

def stderr(text=""):
    sys.stderr.write("{}\n".format(text))

import unittest

class TestRegEx(unittest.TestCase):

    def test_1(self):
        res = do_search('/400_01868_00001.jpg')
        exp = ['a','400','01868','00001','jpg']
        self.assertEqual(res,exp,'test1 failed')

    def test_2(self):
        res = do_search('NL-AsdNIOD_181cPRIVACY_00036_00003_alto.xml')
        exp = ['a','181c','00036','00003','xml']
        self.assertEqual(res,exp,'test2 failed')

    def test_3(self):
        res = do_search('/data/m/A 2.2.4 Joodse instellingen/293/JPG/398/NIOD-293-398-093.jpg')
        exp = ['a','293','398','093','jpg']
        self.assertEqual(res,exp,'test3 failed')

    def test_4(self):
        res = do_search('NL-AsdNIOD_250g_0456-73.pdf')
        exp = ['a','250g','0456','73','pdf']
        self.assertEqual(res,exp,'test4 failed')

    def test_5(self):
        res = do_search('/data/m/Doc II/249-0215c/PDF/NIOD_249-0215C_01.pdf')
        exp = ['a','249','0215C','01','pdf']
        self.assertEqual(res,exp,'test5 failed')

    def test_6(self):
        res = do_search('/data/m/D 1. Nederlands-Indië/400/1868/400_01868_00001.jpg')
        exp = ['a','400','01868','00001','jpg']
        self.assertEqual(res,exp,'test6 failed')

    def test_7(self):
        res = do_search('//data/m/D 2. Gevangenissen en Kampen/250d/250d_0053_01.jpg')
        exp = ['a','250d','0053','01','jpg']
        self.assertEqual(res,exp,'test7 failed')

    def test_8(self):
        res = do_search('//data/m/D 6. TESTSAAS/400-3991/bladzij 51.jpg')
        exp = ['b','400','3991','bladzij 51','jpg']
        self.assertEqual(res,exp,'test8 failed')

    def test_9(self):
        res = do_search('/data/m/Doc II/249-A1180/249-A1180_16.jpg')
        exp = ['a','249','A1180','16','jpg']
        self.assertEqual(res,exp,'test9 failed')




#        test_regex('MMNIOD01_AF_000992_00000057_u.jpg')
        

if __name__ == '__main__':
    unittest.main()

