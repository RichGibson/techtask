import sys
from django.test import TestCase
from datetime import datetime, timedelta


from techtask.models import *




class test_readable_date(TestCase):
    def test_1(self): 
        self.assertEqual(1,1) 

        mydate = datetime.now() 

        st = readable_date(datetime.now() - timedelta(seconds=10))
        self.assertEqual(st,'Just now')

        st = readable_date(datetime.now() - timedelta(minutes=10))
        self.assertEqual(st,'[10] minute(s) ago')

        st = readable_date(datetime.now() - timedelta(minutes=61))
        self.assertEqual(st,'[1] hour(s) ago')

        st = readable_date(datetime.now() - timedelta(minutes=120))
        self.assertEqual(st,'[2] hour(s) ago')

        st = readable_date(datetime.now() - timedelta(days=6))
        self.assertEqual(st,'[6] day(s) ago')

        st = readable_date(datetime.now() - timedelta(days=7))
        self.assertEqual(st,'[1] week(s) ago')

        st = readable_date(datetime.now() - timedelta(days=29))
        self.assertEqual(st,'[4] week(s) ago')

        st = readable_date(datetime.now() - timedelta(days=30))
        self.assertEqual(st,'[1] month(s) ago')

        st = readable_date(datetime.now() - timedelta(days=364))
        self.assertEqual(st,'[12] month(s) ago')

        st = readable_date(datetime.now() - timedelta(days=365))
        self.assertEqual(st,'[1] year(s) ago')

        st = readable_date(datetime.now() - timedelta(days=3650))
        self.assertEqual(st,'[10] year(s) ago')

class test_list_of_objects(TestCase):
    def test_1(self): 
        self.assertEqual(1,1) 

        d= [ {'id':40, 'name':"Joe Bloggs", 'posts': 4} ,
            {'id':567, 'name':"Jenny Smith", 'posts': 3} ,
            {'id':3, 'name':"Frank Jones", 'posts': 54} ,
            {'id':46, 'name':"Samantha Wills", 'posts': 0} ,
            {'id':6789, 'name':"Ahmed Joseph Naran", 'posts': 15} 
        ]


        rslt =  sort_by_posts(d)
        for u in rslt:
            print >>sys.stderr,  u

        self.assertEqual(len(rslt),4)
        self.assertEqual(rslt[0]['posts'],54)

        rslt  = stats(d)
        print >>sys.stderr, "average: %f median: %f max: %f min: %f stdev: %f" % (rslt['average'], rslt['median'], rslt['max'], rslt[
'min'], rslt['std']) 
        self.assertAlmostEqual(rslt['average'],15.19999999)
        self.assertAlmostEqual(rslt['median'],4)
        self.assertEqual(rslt['max'],54)
        self.assertEqual(rslt['min'],0)
        self.assertAlmostEqual(rslt['std'],20.05392729)




