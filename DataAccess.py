###### INSTRUCTIONS ###### 


#Demery Gijsbers 

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
def get_tweets(username):


	unique_identifier = "twitter_{}".format(username) 
	if unique_identifier in CACHE_DICTION:
		print('using cached data for info about', username)
		twitter_results = CACHE_DICTION[unique_identifier] 
	else:
		print('getting data from internet about', username)
		twitter_results = api.user_timeline(username) 
#
		CACHE_DICTION[unique_identifier] = twitter_results 
		f = open(CACHE_FNAME,'w') 
		f.write(json.dumps(CACHE_DICTION)) 
		f.close()

		tweet_texts = [] # collect 'em all!
		for tweet in twitter_results:
			tweet_texts.append(tweet["text"])
		return tweet_texts[:3]


#new_tweets = get_tweets("demerygijsbers")
#for t in new_tweets:
#	print("TWEET TEXT:", t)

	public_tweets = api.home_timeline()
	results = api.search(q = "username")
	list_tweets = results["statuses"][:20]
	print(list_tweets)
	print("***************")

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
print(movie_results)
#Now that I have all that information cached, I want to upload some info into the database. 

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
for tweet in list_tweets:
	new_list.append(tweet['id_str'], tweet['user']['id'], tweet['favorite_count'], tweet['retweet_count'])
	for tup in info_list:
		cur.execute(statement, tup)
	cur.execute('INSERT INTO Users VALUES (?, ?, ?)', tweet['user']['id'], tweet['user']['screen_name'], tweet['user']['favourites_count'])	
for info in movie_results:
	cur.execute('INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?', info['imdbID'], info['Title'], info['Director'], info['language'], info['imdbRating'], info['actors'][0])


conn.commit()



# Put your tests here, with any edits you now need from when you turned them 
#in with your project plan.


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





































# Remember to invoke your tests so they will run! (Recommend using the 
	#verbosity=2 argument.)

