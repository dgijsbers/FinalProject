
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
tweet_texts = []
public_tweets = api.home_timeline()
results = api.search(q = input("Enter the name of a movie please"))
tweet_texts = results['statuses'][:10]
for tweet in tweet_texts:
	text = tweet['text']
	print(text)
	print("***************")
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

	#def __str__(self, title, rating, actor):
	#	return "{} got a {} rating and the top actor is {}".format(self.title, self.rating, self.actor)
	#print("The string is", __str__(input("Type the movie name!!")))


def get_movie_info(self):
	base_url = "http://www.omdbapi.com/?"
	params_diction = {}
	params_diction["s"] = (input("Type the title of the movie one more time"))
	r = requests.get(base_url, params = params_diction)
	r_dict =r.text
	print(type(r_dict))
	return r_dict

	print("^&^&^&^&^&^&^&^&^&^&")


	if title in CACHE_DICTION:
		movie_results = CACHE_DICTION[r_dict]
	else:
		movie_results = requests.get(r_dict)
		CACHE_DICTION[r_dict] = movie_results.text
		movie_results = movie_results.text

		cache_file = open(CACHE_DICTION, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
	print("Printing movie results", movie_results)

	def best_actor(self):
		return self.actor()[0]

class Tweet(object):
	def __init__(self, tweet_info):
		for tweet in tweet_info:
			self.text = tweet["text"]
			self.id = tweet["id"]
			self.username["user"]["screen_name"]
			#self.movie = tweet
			self.num_faves = tweet["statuses"][0]["favorite_count"]
			self.retweet_count = tweet["status"][0]["retweet_count"]
#	def tweet_list(self):
#		tweet_texts = []
#		public_tweets = api.home_timeline()
#		results = api.search(q = "movie")
#		tweet_texts = results["statuses"][:20]
#		print(tweet_texts)
#		print("***************")
#3 instance variables this class will have are:
		#self.tweet #which will be a list that will hold all the information of the tweet, which is important as it is holding information that is vital to organizing our information. 
	 	#self.movie_name #which will be a list that holds the information about the movie including movie name and actors. This will be important to keep this as its own list apart from the tweet information so we can cross it with the information from the Class Movie. 
		#self.popularity #which will be an accumulation method, and will accumulate a point of popularity with every positive word (out of a list of 10 or so) about the movie in the tweet


	def tweet_deet(searched):
		search_term = "twitter_"+str(searched)
		#list_tweets = []

		if search_term in CACHE_DICTION:
			print('using cached data for info about', searched)
			twitter_results = CACHE_DICTION[searched] 
		else:
			print('getting data from internet about', searched)
			twitter_results = api.home_timeline("movie") 
#
			CACHE_DICTION[searched] = twitter_results 
			f = open(CACHE_FNAME,'w') 
			f.write(json.dumps(CACHE_DICTION)) 
			f.close()

movie_info = (get_movie_info(input("Type the name of the same movie"))

print("PRINTING MOVIE_INFO", movie_info)
print ("()()()()()()()())()()")

conn = sqlite3.connect('final_project.db')
cur = conn.cursor()

# List, in English, 2 queries you'll want to make from your database. At least one should be a JOIN. You can always change these later, but start with  ideas you're interested in and lessen the work on yourself later on! 
#(e.g. from class examples, maybe "I want to make a query that accesses the numbers of times each user has favorited tweets, and the number of times tweets that user posted have been favorited -- so I'll be joining the Tweets table and the Users table")
#I want to see how many favorites a user gets on a tweet mentioning one of the top actors, so I would join the Tweets table and the Movie table. 
#I also want to see what the screen name of a user is that mentions a movie where there is a specific director, thus using join to combine the User and Movie table, and using WHERE to find a tweet with a specific director. 
cur.execute("DROP TABLE IF EXISTS Tweets")
table_one = "CREATE TABLE IF NOT EXISTS "
table_one += 'Tweets (tweet_id TEXT PRIMARY KEY, '
table_one += 'user_id INTEGER, num_faves INTEGER, retweet_count INTEGER)' #Need to add one for the movie title searched 
cur.execute(table_one)

cur.execute("DROP TABLE IF EXISTS Users")
table_two = "CREATE TABLE IF NOT EXISTS "
table_two += 'Users (user_id INTEGER PRIMARY KEY, '
table_two += 'screen_name TEXT, total_faves INTEGER)'

cur.execute(table_two)

cur.execute("DROP TABLE IF EXISTS Movies")
table_three = "CREATE TABLE IF NOT EXISTS "
table_three += 'Movies (id INTEGER PRIMARY KEY, '
table_three += 'title TEXT, director TEXT, num_lang INTEGER, rating INTEGER, rich_actor TEXT)'

cur.execute(table_three)

#Below, I will add the information necessary to fill the columns in my table. I will access the tweet information from the tweets about the movies
# I will access the movie information from the OMDb
statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?)' #Need to add one for the searched movie title
new_list = []
for tweet in tweet_texts:
	new_list.append((tweet['id_str'], tweet['user']['id'], tweet['favorite_count'], tweet['retweet_count']))
for tup in new_list:
	cur.execute(statement, tup)
cur.execute('INSERT INTO Users VALUES (?, ?, ?)', (tweet['user']['id'], tweet['user']['screen_name'], tweet['user']['favourites_count']))	

#conn.commit()
for deets in movie_info[0]:

	for info in deets:
		cur.execute('INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?)', info['imdbID'], info['Title'], info['Director'], info['language'], info['imdbRating'], info["actors"][0])


conn.commit()
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



































