import json,os,time
from oauth2 import Client
from config import *

client = Client(CONSUMER_KEY, CONSUMER_SECRET)

def limitcheck(client):
    status = client.request(STATUS_URL)
    request_remaining = int(status['resources']['friends']['/friends/ids']['remaining'])
    reset_time = int(status['resources']['friends']['/friends/ids']['reset'])
    if(request_remaining <= 1):
            current_time = int(round(time.time()))+1
            time.sleep(abs(reset_time-current_time))

def getFollowingIds(user_name):
    request_url = FOLLOWING_URL+user_name
    friends_list = []
    cursor = '-1'
    while(cursor != 0):
        limitcheck(client)
        url = request_url+'&cursor='+str(cursor)
        try:
            reply = client.request(url)
        except:
            # TO DO: find possible exceptions and write appropriate handlers
            pass
        friends_list += reply['ids']
        cursor = int(reply['next_cursor_str'])

    result = []
    for i in friends_list:
        result.append(str(i))
            
    return  result               

def getUserName(file_name):
    result = []
    with open(file_name,'r') as f:
        for line in f:
            try:
                screen_name = line.split('@')[1]
                result.append(screen_name.split('\n')[0])
            except IndexError:
                pass
            
    return result

def startCrawling(user_name_file,target_directory):
    current_dir = os.getcwd();
    #create a new folder to store the results
    try:
        os.mkdir(target_directory)
    except OSError:
        # in case the folder is already made, we don't do anything
        pass
    
    storing_dir = current_dir+'\\'+target_directory+'\\'
    # find the user for which crawling has been done
    existing_files = os.listdir(storing_dir)
    # get the list of users for which crawling needs to be done
    user_list = getUserName(user_name_file)
    for user in user_list:
        modified_name = user+'.txt'
        # check if the user has already been crawled
        if modified_name in existing_files:
            print user,'already done'
            pass
        else:
            following_list = getFollowingIds(user)
            print user,'follows',str(len(following_list)),'people'
            with open(storing_dir+user+'.txt','w') as f:
                for i in following_list:
                    f.write(i+'\n')

startCrawling('list_a.txt','data_collection')
