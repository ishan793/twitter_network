import json,os,time
from application_only_auth import Client
CONSUMER_KEY = 'dzxgD8JMD6wBqb8DiyAaP3y4i'
CONSUMER_SECRET = 'OVi5EzU3dUTSg2Fnd4oeWYWxSF15qJ3VRLsARGw5sU2EBA79pz'
client = Client(CONSUMER_KEY, CONSUMER_SECRET)
# status = client.rate_limit_status()
# print status['resources']['search']
# a=json.dumps(tweet, sort_keys=True, indent=4, separators=(',', ':'))
# print type(a)
def limitcheck(client):
	requestlimits = client.request('https://api.twitter.com/1.1/application/rate_limit_status.json?resources=statuses')
	remaining = int(requestlimits['resources']['statuses']['/statuses/user_timeline']['remaining'])
	resettime = int(requestlimits['resources']['statuses']['/statuses/user_timeline']['reset'])
	if(remaining <= 1):
		curtime = int(round(time.time()))+1
		time.sleep(resettime-curtime)



f=open('list.txt','r')
limitcheck(client)
last_tweet = 0
for line in f:
	querystr = (line.split('@'))[1]
	querystr = querystr[0:-1]
	print querystr
	if(querystr in os.listdir('listtweets')):
		pass
	else:
		os.mkdir(r'listtweets\\'+querystr)
	datadirlist=os.listdir(r'listtweets\\'+querystr)
	while(len(datadirlist) <= 17):
		datadirlist=os.listdir(r'listtweets\\'+querystr)
		if(len(datadirlist) == 0):
			limitcheck(client)
			tweet = client.request('https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name='+querystr+'&count=200')
			last_tweet = tweet[-1]['id_str']
			tweetdict = {}
			for t in tweet:
				tweetdict[t['id_str']] = t
			fp = open(r'listtweets\\'+querystr+'\\'+'1.json','w')
			json.dump(tweetdict,fp)
			fp.close()
			
		else:
			if(last_tweet):
				pass
			else:
				datadirlist = (os.listdir(r'listtweets\\'+querystr))
				datadirlist.sort()
				print datadirlist[-1]
				lastfile = datadirlist[-1]
				
				fr = open(r'listtweets\\'+querystr+'\\'+lastfile,'r')
				for line in fr:
					d = json.loads(line)
					tweetids = d.keys()
					tweetids.sort()
					last_tweet = tweetids[0]
				fr.close()
			limitcheck(client)
			tweet = client.request('https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name='+querystr+'&count=200&max_id='+last_tweet)
			last_tweet = tweet[-1]['id_str']
			tweetdict = {}
			for t in tweet:
				tweetdict[t['id_str']] = t
			fp = open(r'listtweets\\'+querystr+'\\'+str(len(datadirlist)+1)+'.json','w')
			json.dump(tweetdict,fp)
			fp.close()
		datadirlist = os.listdir(r'listtweets\\'+querystr)