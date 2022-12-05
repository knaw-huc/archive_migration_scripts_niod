# -*- coding: utf-8 -*-
import unittest
from read_inventaris import do_search
from read_inventaris import make_target

class TestRegEx(unittest.TestCase):

    def test_1(self):
        res = do_search('/400_01868_00001.jpg')
        exp = ['a','400','01868','00001','jpg']
        self.assertEqual(res,exp,'test1a failed')
        exp2 = 'NL-AsdNIOD_400_01868/preservation/NL-AsdNIOD_400_01868_00001.jpg'
        ignore,res2 = make_target(res)
        self.assertEqual(exp2,res2,'test1b failed')

    def test_2(self):
        res = do_search('NL-AsdNIOD_181cPRIVACY_00036_00003_alto.xml')
        exp = ['a','181c','00036','00003','xml']
        self.assertEqual(res,exp,'test2a failed')
        exp2 = 'NL-AsdNIOD_181c_00036/transcription/NL-AsdNIOD_181c_00036_00003.xml'
        ignore,res2 = make_target(res)
        self.assertEqual(exp2,res2,'test2b failed')

    def test_3(self):
        res = do_search('/data/m/A 2.2.4 Joodse instellingen/293/JPG/398/NIOD-293-398-093.jpg')
        exp = ['a','293','398','093','jpg']
        self.assertEqual(res,exp,'test3a failed')
        exp2 = 'NL-AsdNIOD_293_398/preservation/NL-AsdNIOD_293_398_093.jpg'
        ignore,res2 = make_target(res)
        self.assertEqual(exp2,res2,'test3b failed')

    def test_4(self):
        res = do_search('NL-AsdNIOD_250g_0456-73.pdf')
        exp = ['a','250g','0456','73','pdf']
        self.assertEqual(res,exp,'test4a failed')
        exp2 = 'NL-AsdNIOD_250g_0456/transcription/NL-AsdNIOD_250g_0456_73.pdf'
        ignore,res2 = make_target(res)
        self.assertEqual(exp2,res2,'test4b failed')

    def test_5(self):
        res = do_search('/data/m/Doc II/249-0215c/PDF/NIOD_249-0215C_01.pdf')
        exp = ['a','249','0215C','01','pdf']
        self.assertEqual(res,exp,'test5a failed')
        exp2 = 'NL-AsdNIOD_249_0215C/transcription/NL-AsdNIOD_249_0215C_01.pdf'
        ignore,res2 = make_target(res)
        self.assertEqual(exp2,res2,'test5b failed')

    def test_6(self):
        res = do_search('/data/m/D 1. Nederlands-Indië/400/1868/400_01868_00001.jpg')
        exp = ['a','400','01868','00001','jpg']
        self.assertEqual(res,exp,'test6a failed')
        exp2 = 'NL-AsdNIOD_400_01868/preservation/NL-AsdNIOD_400_01868_00001.jpg'
        ignore,res2 = make_target(res)
        self.assertEqual(exp2,res2,'test6b failed')

    def test_7(self):
        res = do_search('//data/m/D 2. Gevangenissen en Kampen/250d/250d_0053_01.jpg')
        exp = ['a','250d','0053','01','jpg']
        self.assertEqual(res,exp,'test7a failed')
        exp2 = 'NL-AsdNIOD_250d_0053/preservation/NL-AsdNIOD_250d_0053_01.jpg'
        ignore,res2 = make_target(res)
        self.assertEqual(exp2,res2,'test7b failed')

    def test_8(self):
        res = do_search('//data/m/D 6. TESTSAAS/400-3991/bladzij 51.jpg')
        exp = ['b','400','3991','bladzij 51','jpg']
        self.assertEqual(res,exp,'test8a failed')
        exp2 = 'NL-AsdNIOD_400_3991/bladzij 51.jpg'
        ignore,res2 = make_target(res)
        self.assertEqual(exp2,res2,'test8b failed')

    def test_9(self):
        res = do_search('/data/m/Doc II/249-A1180/249-A1180_16.jpg')
        exp = ['a','249','A1180','16','jpg']
        self.assertEqual(res,exp,'test9a failed')
        exp2 = 'NL-AsdNIOD_249_A1180/preservation/NL-AsdNIOD_249_A1180_16.jpg'
        ignore,res2 = make_target(res)
        self.assertEqual(exp2,res2,'test9b failed')

    def test_10(self):
        res = do_search('/data/m/Doc II/249-A1084/249-A1084-307/1943-02-12  aanwervingsbev b.JPG')
        exp = ['a','249','A1084','307','JPG']
        self.assertEqual(res,exp,'test10a failed')
        exp2 = 'NL-AsdNIOD_249_A1084/preservation/NL-AsdNIOD_249_A1084_307.JPG'
        ignore,res2 = make_target(res)
        self.assertEqual(exp2,res2,'test10b failed')

    def test_11(self):
        res = do_search('/data/m/D 5. CollectieCorrespondentie/247_1601/247_16010_herdenkingstekst.docx')
        exp = ['b','247','1601','247_16010_herdenkingstekst','docx']
        self.assertEqual(res,exp,'test11a failed')
        exp2 = 'NL-AsdNIOD_247_1601/247_16010_herdenkingstekst.docx'
        ignore,res2 = make_target(res)
        self.assertEqual(exp2,res2,'test11b failed')


#        test_regex('MMNIOD01_AF_000992_00000057_u.jpg')
        

if __name__ == '__main__':
    unittest.main()

