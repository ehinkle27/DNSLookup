import MySQLdb
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
db = MySQLdb.connect("localhost","pythonuser","Password2","dnslookup" )


try:
	myAnswers = myResolver.query("google.com", "A") #Lookup the 'A' record(s) for google.com
	for rdata in myAnswers: #for each response
		print rdata #print the data
except DNSException as enx:
	print DNSException