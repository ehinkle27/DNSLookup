from threading import Thread
import urllib
import re
import pypyodbc

gmap ={}


def th(ur):
    base = "http://finance.yahoo.com/q?s="+ur
    regex = '<span id="yfs_l84_'+ur.lower()+'">(.+?)</span>'
    pattern = re.compile(regex)
    htmltext = urllib.urlopen(base).read()
    results = re.findall(pattern,htmltext)
    try:
       gmap[ur] = results[0]
    except:
        print "got an error"

symbolslist = open("symbols.txt").read()
symbolslist = symbolslist.split(",")
print symbolslist

threadlist = []

for u in symbolslist:
    t = Thread(target=th,args=(u,))
    t.start()
    threadlist.append(t)


for b in threadlist:
    b.join()
#connect to MSSQL Database
conn = pypyodbc.connect("DRIVER={SQL Server};SERVER=10.29.5.115;UID=python;PWD=Password1;DATABASE=stockdata")

for key in gmap.keys():
    print key,gmap[key]
    query = "INSERT INTO tutorial (symbol,last) VALUES ("
    query = query+"'"+key+"',"+gmap[key]+")"
    x = conn.cursor()
    x.execute(query)
x.commit()
x.close()



