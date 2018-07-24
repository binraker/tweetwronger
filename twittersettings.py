# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 18:34:33 2018

@author: Peter
"""

#keys for twitter
 
#name of account to type tweets mentioning 
mentionee = 'tweetwronger'

#should this account also be type (True or False)
exclude = True

#number of tweets back to collect 
gather = 100

#number of tweetes to print in one cycle
cycle = 10

#hastages tweets must include. make [] if none (use lowercase only)  
#e.g. ['typethis', 'tweetwronger']
hashtags = []

#blacklist of accounts not to type
#e.g. ['twitter', 'realDonaldTrump']
blacklist = []

#URL of typewriter
TWURL = 'http://127.0.0.1/type?'  
