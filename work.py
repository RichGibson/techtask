import operator
from numpy import mean,  std, array

def sort_by_posts(d):
    # gratuitious use of a list comprehension
    rslt = [ {'first_name':u['name'].split()[0], 'last_name':u['name'].split()[-1], 'posts':u['posts']} for u in d if u['posts'] > 0 ]
    rslt.sort(key=operator.itemgetter('posts'))
    rslt.reverse()
    return rslt

def stats(d):
    lst  = array([u['posts'] for u in d] )
    rslt = {'average':mean(lst),'max': max(lst), 'min':min(lst), 'std':std(lst)}
    return rslt

d= [ {'id':40, 'name':"Joe Bloggs", 'posts': 4} ,
     {'id':567, 'name':"Jenny Smith", 'posts': 3} ,
     {'id':3, 'name':"Frank Jones", 'posts': 54} ,
     {'id':46, 'name':"Samantha Wills", 'posts': 0} ,
     {'id':6789, 'name':"Ahmed Joseph Naran", 'posts': 15} 
]
print "posts:"
print sort_by_posts(d)
print "stats:"
print stats(d)




