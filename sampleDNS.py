resolver = dns.resolver.Resolver()
resolver.lifetime= 1
resolver.timeout= 0.5

def getAAAArecord(domain):
    try:
        answers = resolver.query(domain,'AAAA')
        return answers[0]
    except:
        return "N/A"


         print "*** Getting AAAA NS records for", domain
        writeLog("*** Getting AAAA NS records for "+domain)
        try:
            answers = resolver.query(domain, 'NS')
            for ns in answers:
                ip_ns = getAAAArecord(str(ns))
                print ip_ns,' :: ', ns
                writeLog(str(ip_ns)+' :: '+str(ns))
                       
                sql = "INSERT INTO ns (id_domain,ns,ip_ns) VALUES ("+str(id_domain)+",'"+str(ns)+"','"+str(ip_ns)+"')"
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    db.rollback()
                       
            print
            writeLog("\n")
        except NXDOMAIN as enx:
            print "Error: NXDOMAIN - domain does not exist"
            writeLog("Error: NXDOMAIN - domain does not exist")
        except Timeout as etime:
            print "Error: dns.exception.Timeout"
            writeLog("Error: dns.exception.Timeout")