import sys
import httplib
import os
import re
import threading
import urllib2
import time

def download(url):
        file_name = url.split('/')[-1]
        u = urllib2.urlopen(url)
        f = open('lib/books/'+file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
                buffer = u.read(block_sz)
                if not buffer:
                        break

                file_size_dl += len(buffer)
                f.write(buffer)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8)*(len(status)+1)
                print status,

        f.close()





def process():
	n=0
	while True:
		try:
			moon = httplib.HTTPSConnection('www.google.com')
			query = "/search?q=filetype:pdf+intext:IT+intext:computer+intext:software+information+technology+intext:ISBN"
			getRequest =getQuery(n,query)
			print('www.google.com'+getRequest)
			moon.request("GET",getRequest)
			res=moon.getresponse()
			data = res.read()
			n+=10
			####################################
			listedUrl = re.findall('((http://|https://)+(www\.)?[-a-zA-Z0-9_%/.:]+\.(pdf|PDF))',data)
			if not listedUrl:
				print('NOT LINKS FOUND:: %s \n'%data)
			dlinks = set(listedUrl)
			for link in dlinks:
        			if 'webcache.googleusercontent.com' not in link[0]:
					threading.Thread(target=download,args=(link[0],)).start()				
                			time.sleep(60)
		except Exception, err:
			print("Error occured fetching "+getRequest+" ERROR-->"+str(err))

def getQuery(n,query):
	if n==0:
		return query
	res =query+"&start="+str(n)
	return res

def heading():
    BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'
    sys.stdout.write(GREEN + """
                                
                                ,--. ,--.,--.               ,------.         ,--.                  
                                |  .'   /`--',--,--,  ,---. |  .-.  \  ,---. |  |,-. ,---. ,--.--. 
                                |  .   ' ,--.|      \| .-. ||  |  \  :| .-. ||     /| .-. :|  .--' 
                                |  |\   \|  ||  ||  |' '-' '|  '--'  /' '-' '|  \  \\   --.|  |    
                                `--' '--'`--'`--''--'.`-  / `-------'  `---' `--'`--'`----'`--'    
                                                      `---'                                         
    """ + END + BLUE +
    '\n' + '                        {0}By Kaburu{1}'.format(RED,END).center(80) +
    '\n' + '                           Version: {0}0.1{1}\n\n\n'.format(YELLOW, END).center(86))
    
heading()
process()
