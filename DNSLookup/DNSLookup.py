import pymysql.cursors
import pymysql
import pypyodbc
import dns.resolver #import the module
from dns.exception import DNSException
from datetime import datetime
import time

#time.sleep(60)  # Delay for 1 minute (60 seconds)

gmap ={}
domain = "google.com"
myResolver = dns.resolver.Resolver() #create a new instance named 'myResolver'
myResolver.lifetime = 1
myResolver.lifetime = .5
#myResolver.nameservers = ['8.8.8.8', '8.8.4.4']
#myAnswers = myResolver.query(domain, "A") #Lookup the 'A' record(s) for google.com
#for rdata in myAnswers: #for each response
#	print rdata.address #print the data

#gmap['IPAddr'] = rdata.address
gmap['domain'] = domain
gmap['IP_seen'] = ""



# Open MYSQL database connection
conn = pymysql.connect("10.29.5.38","pythonuser","Password2","Test" )
# Connect to the database
#connection = pymysql.connect(host='10.29.5.38',
#                            user='pythonuser',
#                            password='Password1',
#                            db='Test',
#                            charset='utf8mb4',
#                            cursorclass=pymysql.cursors.DictCursor)

#connect to MSSQL Database
#conn = pypyodbc.connect("DRIVER={SQL Server};SERVER=10.29.5.115;UID=python;PWD=Password1;DATABASE=stockdata")
#nowtd =datetime.now()
#nowstamp = nowtd.strftime('%Y-%m-%d %H:%M:%S')
#gmap['First_Seen'] = nowstamp
#print gmap['First_Seen']
print gmap['domain']
#print gmap['IPAddr']
i = 1
while i < 420:
   nowtd =datetime.now()
   nowstamp = nowtd.strftime('%Y-%m-%d %H:%M:%S')
   gmap['First_Seen'] = nowstamp
   gmap['Last_Seen'] = nowstamp
# Look up IP address from DNS name
   try:
       myAnswers = myResolver.query(domain, "A") #Lookup the 'A' record(s) for google.com
       for rdata in myAnswers: #for each response
           print rdata.address #print the data
           gmap['IPAddr'] = rdata.address
   except: #If any error set IP Address to below value and insert in database.
           gmap['IPAddr'] = '0.0.0.0'

   if gmap['IPAddr'] == gmap['IP_seen']:
      print "IP Didn't change"
      #break
   elif gmap['IPAddr'] == '0.0.0.0':
      gmap['First_Seen'] = '2001-01-01 00:00:00'
      gmap['Last_Seen'] = '2001-01-01 00:00:00'
      print "Error"
   elif (gmap['IPAddr'] <> gmap['IP_seen'] and gmap['IP_seen'] == ""):
      print "IP address not seen and Seen is empty"
      print "IP Seen (should be blank): " + gmap['IP_seen']
      print "IP Address: " + gmap['IPAddr']
      print " First Seen: " + gmap['First_Seen']

      query = "INSERT INTO DNSLookup (First_Seen,DomainName,IP_ADDR) VALUES ("
      query = query+"'"+gmap['First_Seen']+"','"+gmap['domain']+"','"+gmap['IPAddr']+"')"
      x = conn.cursor()
      x.execute(query)
      #x.commit() #Needed for MSSQL
      conn.commit() #needed for MYSQL
      gmap['IP_seen'] = gmap['IPAddr']
      print "IP Seen: " + gmap['IP_seen']
      i=i+1

   else: 
      print "Entered else statement IP "
      print "Seen IP when starting: " + gmap['IP_seen']
      query = "INSERT INTO DNSLookup (First_Seen,DomainName,IP_ADDR) VALUES ("
      query = query+"'"+gmap['First_Seen']+"','"+gmap['domain']+"','"+gmap['IPAddr']+"')"
      query2 = "INSERT INTO DNSLookup (Last_Seen,DomainName,IP_ADDR) VALUES ("
      query2 = query2+"'"+gmap['Last_Seen']+"','"+gmap['domain']+"','"+gmap['IP_seen']+"')"
      x = conn.cursor()
      x.execute(query)
      x.execute(query2)
      conn.commit() #Needed for MYSQL
      #x.commit() #Needed for MSSQL
      gmap['IP_seen'] = gmap['IPAddr']
      
      print "Seen IP after updating database" + gmap['IP_seen']
      print gmap['IPAddr']
      print gmap['First_Seen']
      print gmap['Last_Seen']
      i=i+1
   i=i+1
   time.sleep(60)  # Delay for 1 minute (60 seconds)

      #query = "INSERT INTO DNSLookup (First_Seen,DomainName,IP_ADDR) VALUES ("
      #query = query+"'"+gmap['First_Seen']+"','"+gmap['domain']+"','"+gmap['IPAddr']+"')"
      
      #x = conn.cursor()
      #x.execute(query)
      #x.commit()
      

#query = "INSERT INTO DNSLookup (First_Seen,DomainName,IP_ADDR) VALUES ("
#query = query+"'"+gmap['First_Seen']+"','"+gmap['domain']+"','"+gmap['IPAddr']+"')"
#x = conn.cursor()
#x.execute(query)
#x.commit()
#x.close()


#try:
#	myAnswers = myResolver.query("google.com", "A") #Lookup the 'A' record(s) for google.com
#	for rdata in myAnswers: #for each response
#		print rdata.address + " " + nowstamp #print the data
#except DNSException as enx:
#	print DNSException