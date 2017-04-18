###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what 
#you should do for each step of your project. You should specify variable names 
#and processes to use. For example, "Use dictionary accumulation with the list 
#you just created to create a dictionary called tag_counts, where the keys 
#represent tags on flickr photos and the values represent frequency of times
# those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") 
#or whatever is comfortable for you, as long as you are clear about what should 
#be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, 
#and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test
# that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, 
#such that your program can be run over and over again without error and without 
#duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should 
	#accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.
import json
import unittest
import random
import requests
import tweepy
import twitter_info
import sqlite3

# Begin filling in instructions....
#I will need to set up my twitter keys, so I have imported twitter_info into my final project folder and have updated the keys, set them equal to variables that will be easier to use later in the code. 
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# I set up library to grab stuff from twitter with my authentication, and set it up so I can return it in a JSON format to keep it clean
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

## Now I want to actually gather the data and chache it so that we can access all the data that is gathered throughout the process. I will first set up the cache file, and then begin the process of caching the data I need from twitter 

CACHE_FNAME = "SI206_finalproject_cache.json"
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

# I want to set up a function that will cache data from twitter into my cache file. I will define this as get_tweets because I want it to save tweets
def get_tweets(keyword):


	unique_identifier = "twitter_{}".format(keyword) 
	if unique_identifier in CACHE_DICTION:
		print('using cached data for info about', keyword)
		twitter_results = CACHE_DICTION[unique_identifier] 
	else:
		print('getting data from internet about', keyword)
		twitter_results = api.user_timeline(keyword) 
#
		CACHE_DICTION[unique_identifier] = twitter_results 
		f = open(CACHE_FNAME,'w') 
		f.write(json.dumps(CACHE_DICTION)) 
		f.close()
#I want to set up a request to get information from the OMDb and save the information I get from that into a dictionary which will then also be cached into the cache file 

	base_url = "http://www.omdbapi.com/?"
	params_diction = {}
	params_diction["s"] = "Title"
	r = requests.get(base_url, params = params_diction)
	r_dict = json.loads(r.text)

	if r_dict in CACHE_DICTION:
		movie_results = CACHE_DICTION[r_dict]
	else:
		movie_results = requests.get(r_dict)
		CACHE_DICTION[r_dict] = movie_results.text
		movie_results = movie_results.text

		cache_file = open(CACHE_DICTION, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()





# Put your tests here, with any edits you now need from when you turned them 
#in with your project plan.


# Remember to invoke your tests so they will run! (Recommend using the 
	#verbosity=2 argument.)

