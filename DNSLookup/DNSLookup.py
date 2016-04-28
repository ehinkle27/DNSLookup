import pymysql.cursors
import pymysql
import pypyodbc
import dns.resolver #import the module
from dns.exception import DNSException


myResolver = dns.resolver.Resolver() #create a new instance named 'myResolver'
myResolver.lifetime = 1
myResolver.lifetime = .5
#myResolver.nameservers = ['8.8.8.8', '8.8.4.4']
#myAnswers = myResolver.query("google.com", "A") #Lookup the 'A' record(s) for google.com
#for rdata in myAnswers: #for each response
#	print rdata #print the data

# Open database connection
#db = pymysql.connect("localhost","pythonuser","Password2","dnslookup" )
# Connect to the database
#connection = pymysql.connect(host='10.29.5.38',
#                            user='pythonuser',
#                            password='Password1',
#                            db='Test',
#                            charset='utf8mb4',
#                            cursorclass=pymysql.cursors.DictCursor)

#connect to MSSQL Database
conn = pypyodbc.connect("DRIVER={SQL Server};SERVER=10.29.5.115;UID=python;PWD=Password1;DATABASE=stockdata")

try:
	myAnswers = myResolver.query("google.com", "A") #Lookup the 'A' record(s) for google.com
	for rdata in myAnswers: #for each response
		print rdata #print the data
except DNSException as enx:
	print DNSException