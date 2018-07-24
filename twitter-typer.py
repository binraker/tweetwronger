# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 20:37:06 2018

@author: Peter
"""
testing = False

from birdy.twitter import UserClient
import urllib
import emoji
import textwrap
import datetime
import os
import sys
import twittersettings as settings


client = UserClient(settings.CONSUMER_KEY,
                    settings.CONSUMER_SECRET,
                    settings.ACCESS_TOKEN,
                    settings.ACCESS_TOKEN_SECRET)

os.chdir(os.path.dirname(sys.argv[0]))
if not os.path.isfile('tweetlock'):
    
    f = open('tweetlock','w+')
    f.close()
    
    printHist = 'tweets.txt'

    idfile = open(printHist, 'r')
    ids = idfile.readlines()
    idfile.close()
     
    
    print('\n')
    print(str(datetime.datetime.now()))
    ret = client.api.search.tweets.get(q=settings.mentionee,f='tweets', count = settings.gather)
    data = ret.data.statuses
    print ('number of tweets found: ', len(data))
    idfile = open(printHist, 'a')
    for entry in data:
        
        tweetid = entry.id_str + '\n'
        user = entry.user.screen_name
        
        if tweetid in ids:
            continue
        if settings.hashtags != []:
            found = False
            for hashtag in entry.entities.hashtags:   
                if (hashtag.text).lower() in settings.hashtags:
                    found = True
            if not found:
                continue
        if user in settings.blacklist:
            continue
        if user == settings.mentionee and settings.exclude:
            continue
        
        text = emoji.demojize(entry.text)
        print(user, text, '\n')           
        text = textwrap.wrap(text,55)
        if not testing:
            try:
                f = urllib.request.urlopen(settings.TWURL + urllib.parse.urlencode({'text': '@' + user + ' : ', 'bold' : 1, 'underline' : 1}))               
                multiline = False
                for line in text:
                    if multiline:
                        f = urllib.request.urlopen(settings.TWURL + urllib.parse.urlencode({'text': (' ' * (len(user) + 3))}))
                    multiline = True
                    f = urllib.request.urlopen(settings.TWURL + urllib.parse.urlencode({'text': line + '\n'}))
                f = urllib.request.urlopen(settings.TWURL + urllib.prse.urlencode({'text': '\n'}))
                ids.append(tweetid)
                idfile.write(tweetid)
            except:
                print('error sending tweet to typewriter')       
    idfile.close()
    os.remove('tweetlock')