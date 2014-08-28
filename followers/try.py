import urllib2

url = 'http://www.quora.com/Stock-Market/How-exactly-does-the-stock-market-work'

reply = urllib2.urlopen(url).read()
print reply
