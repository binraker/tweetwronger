# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 20:37:06 2018

@author: Peter
"""


from birdy.twitter import UserClient
import urllib
import emoji
import textwrap
import datetime
import os
import sys


client = UserClient(CONSUMER_KEY,
                    CONSUMER_SECRET,
                    ACCESS_TOKEN,
                    ACCESS_TOKEN_SECRET)

os.chdir(os.path.dirname(sys.argv[0]))

printHist = 'tweets.txt'
mentionee = 'twitertypetest'
idfile = open(printHist, 'r')
ids = idfile.readlines()
idfile.close()

TWURL = 'http://127.0.0.1/type?'


print('\n')
print(str(datetime.datetime.time()))
ret = client.api.search.tweets.get(q=mentionee,f='tweets', count = 100)
data = ret.data.statuses
print ('number of tweets found: ', len(data))
idfile = open(printHist, 'a')
for entry in data:
    tweetid = entry['id_str'] + '\n'
    if( not entry['user']['name'] == mentionee) and (not tweetid in ids):
        user = entry['user']['screen_name']
        text = emoji.demojize(entry['text'])
        print(user, text)
        
        text = textwrap.wrap(text,60)
        try:
            f = urllib.request.urlopen(TWURL + urllib.parse.urlencode({'text': '@' + user + ' : ', 'bold' : 1, 'underline' : 1}))
            
            multiline = False
            for line in text:
                if multiline:
                    f = urllib.request.urlopen(TWURL + urllib.parse.urlencode({'text': (' ' * (len(user) + 3))}))
                multiline = True
                f = urllib.request.urlopen(TWURL + urllib.parse.urlencode({'text': line + '\n'}))
            f = urllib.request.urlopen(TWURL + urllib.parse.urlencode({'text': '\n'}))
            ids.append(tweetid)
            idfile.write(tweetid)
        except:
            print('error sending tweet to typewriter')       
idfile.close()
        

