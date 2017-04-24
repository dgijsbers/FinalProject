#THINGS I GOTTA DO HERE
#Upload stuff to databases 
#methods to get the stuff
#methods to find fun stuff about it 
#methods to match that ish with twitter info
#JOIN INNER to match like users with rating info
#documentation 

import json
import unittest
import random
import requests
import tweepy
import twitter_info
import sqlite3

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# I set up library to grab stuff from twitter with my authentication, and set it up so I can return it in a JSON format to keep it clean
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

## Now I want to actually gather the data and chache it so that we can access all the data that is gathered throughout the process. I will first set up the cache file, and then begin the process of caching the data I need from twitter 

CACHE_FNAME = "SI206_final_project_cache.json"
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

# I want to set up a function that will cache data from twitter into my cache file. I will define this as get_tweets because I want it to save tweets

#I want to set up a request to get information from the OMDb and save the information I get from that into a dictionary which will then also be cached into the cache file 


#Now that I have all that information cached, I want to upload some info into the database. 

conn = sqlite3.connect('final_project.db')
cur = conn.cursor()

#In addition to the Class Movie, I will also be creating the recommended Class Tweet to handle the Twitter data.
class Movie(object):
	def __init__(self, title, director, rating, actor, languages):
		self.title = title
		self.director = director
		self.rating = rating
		self.actor = actor
		self.languages = languages

	def __str__(self):
		return "{} got a {} rating and the top actor is {}".format(self.title, self.rating, self.actor)

	def get_movie_info(self, title, director, actor):
		base_url = "http://www.omdbapi.com/?"
		params_diction = {}
		params_diction["s"] = "Title"
		r = requests.get(base_url, params = params_diction)
		r_dict =r.text

		if movie_title in CACHE_DICTION:
			movie_results = CACHE_DICTION[r_dict]
		else:
			movie_results = requests.get(r_dict)
			CACHE_DICTION[r_dict] = movie_results.text
			movie_results = movie_results.text

			cache_file = open(CACHE_DICTION, 'w')
			cache_file.write(json.dumps(CACHE_DICTION))
			cache_file.close()
		print(movie_results)

	def best_actor(self):
		return self.actor()[0]

	

class Tweet(object):
#The class Tweet will take the tweet text, the tweet ID, the username of the person who posted the tweet, the name of the movie that was searched, the number of favorites the tweet received, and lastly, the number of retweets the tweet received as well. All of these things will ultimately be uploaded to the database into the Tweets table as well. 
	def __init__(self, tweet_info):
		for tweet in tweet_info:
		self.text = tweet["text"]
		self.id = tweet["id"]
		self.username["user"]["screen_name"]
		#self.movie = tweet
		self.num_faves = tweet["statuses"][0]["favorite_count"]
		self.retweet_count = tweet["status"][0]["retweet_count"]


#What will 1 instance of this class represent?
#1 instance of this class will represent one tweet containing the information searched for. 

#What are 3 instance variables this class will have? What will they be called, and what information will they hold? Why are they important?

#3 instance variables this class will have are:
		#self.tweet #which will be a list that will hold all the information of the tweet, which is important as it is holding information that is vital to organizing our information. 
	 	#self.movie_name #which will be a list that holds the information about the movie including movie name and actors. This will be important to keep this as its own list apart from the tweet information so we can cross it with the information from the Class Movie. 
		#self.popularity #which will be an accumulation method, and will accumulate a point of popularity with every positive word (out of a list of 10 or so) about the movie in the tweet


#Explain 2 methods the class will have that are not the class constructor (__init__ method) by answering the following questions for each. 
#ONE METHOD:
	tweet_texts = []
	public_tweets = api.home_timeline()
	results = api.search(q = search)
	tweet_texts = results["statuses"][:3]
	print(tweet_texts)
	print("***************")

	def tweet_deet(searched):
		search_term = "twitter_"+str(searched)
		list_tweets = []

		if search_term in CACHE_DICTION:
			print('using cached data for info about', searched)
			twitter_results = CACHE_DICTION[searched] 
		else:
			print('getting data from internet about', searched)
			twitter_results = api.home_timeline(searched) 
#
			CACHE_DICTION[searched] = twitter_results 
			f = open(CACHE_FNAME,'w') 
			f.write(json.dumps(CACHE_DICTION)) 
			f.close()

		#tweet_texts = [] # collect 'em all!
		#for tweet in twitter_results:
		#	results = api.search(q="movie")

		#	tweet_texts.append(results["text"])
		#return tweet_texts[:3]
	#print(tweet_texts[:3])


#new_tweets = get_tweets("demerygijsbers")
#for t in new_tweets:
#	print("TWEET TEXT:", t)

#- What will the method do?
#this method will compile a list of details about the tweet

#- Will it take any additional input? 
#self, text, id, username, num_faves and retweet_count

#- Will it return anything? Should it change anything about the instance/an instance variable? 
#this will return the list and will not change the instance variables. 

#- Why is it useful for this class definition, in this program?
#This is useful for the class definition because it is organizing all of the tweet information right away and will make it easily accessible


#ANOTHER METHOD:
#- What will the name of the method be?
	##def movie_info(self, movie):

#- What will the method do?
#compile a short list of the information about the movie that is in the tweet

#- Will it take any additional input? 
#self and movie

#- Will it return anything? Should it change anything about the instance/an instance variable? 
#This will return the list of keywords found in the tweet like an actor name and/or movie title and/or director.

#- Why is it useful for this class definition, in this program?
#In an attempt to gather all the information I can about the movies from a set of tweets, this list will help keep it all in order and make it easily accessible. 

#What will the tables in your database be?
#The tables in my database will be the required: Tweets, Users, and Movies. 


#What fields will each database table have? Which field of them is the primary key? You should list the fields for each database table here, e.g.
#Tweets:
#- text, tweet ID (primary key), user, movie name, number of favorites, and number of retweets
#Users:
#- User ID (primary key), screen name, number of favorites (ever)
#Movies:
#- ID (primary key), title, director, number of languages, IMDB rating, top-billed

# List, in English, 2 queries you'll want to make from your database. At least one should be a JOIN. You can always change these later, but start with  ideas you're interested in and lessen the work on yourself later on! 
#(e.g. from class examples, maybe "I want to make a query that accesses the numbers of times each user has favorited tweets, and the number of times tweets that user posted have been favorited -- so I'll be joining the Tweets table and the Users table")
#I want to see how many favorites a user gets on a tweet mentioning one of the top actors, so I would join the Tweets table and the Movie table. 
#I also want to see what the screen name of a user is that mentions a movie where there is a specific director, thus using join to combine the User and Movie table, and using WHERE to find a tweet with a specific director. 
#* What are at least 2 of the data processing mechanics you're planning to use? 
#I will use list comprehension and the zip function 


#* Why will each of those be useful to you? What data might you use it on? 
#(e.g. "Set comprehension: I think I'm going to be looking for unique names and proper nouns in this big set of text, so I'm going to use a set comprehension"). 
#>>>This is especially important if you are doing Option 3, but it's important for everyone!<<<

#I plan on using a list comprehension to compile the list of information I need from the tweets as this will be easily accessible when I just needs parts of the list. 
#I also plan on using a zip mechanic to maybe put together a list of tweet information with information from the movie search to compile an overall tuple of the information and keywords we were looking for in the tweet. 

#What will your output look like? Will it be a .txt file? a CSV file? something else? What information will it contain? >>>This is especially important if you are doing Option 3, but it's important for everyone!<<<
#My output will be a .txt file containing information about what kinds of tweets (positive or negative) are associated with a certain movie and a couple of the actors in that movie. 


class CodeTests(unittest.TestCase):
	def test_1(self):
		a = Movie()
		a.title
		self.assertEqual(type(a.title, str))
# testing that the title of the movie comes out as a string

	def test_2(self):
		b = Movie()
		b.rating
		self.assertEqual(type(b.rating), int)
# testing that the rating will come out as an integer

	def test_3(self):
		c = Movie()
		d = c.movie_info()
		self.assertTrue(len(d)>= 2, "Testing that there are at least 2 items in the movie info list")
# testing that there are at least 2 elements in the list of movie info

	def test_4(self):
		e = Tweet()
		f = e.tweet_deet
		self.assertEqual(type(f), list)
# Testing that the type of the tweet_deet method will be a list

	def test_5(self):
		g = Tweet()
		self.assertTrue(len(g)>= 4, "testing that there are at least 4 items in the tweet list")

	def test_6(self):
		conn = sqlite.connect('final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[0] == 6, "testing that there are 6 columns in the Tweets table"))
		conn.close()

	def test_7(self):
		conn = sqlite.connect('final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertTrue(len(result[0] == 6), "Testing that there are 6 columns in the Movies table")
		conn.close()

	def test_8(self):
		conn = sqlite.connect('final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies')
		result = cur.fetchall()
		self.assertEqual(type(result[0][0], int))
#Testing that the first element in the movies table, the ID, is an integer 



































