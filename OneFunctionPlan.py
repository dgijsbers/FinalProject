# One function I would use in my code would be a function under the class Tweet that would get the tweets necessary. 
#Similar to the function get_user_tweets, but one that would get one star actor in each of the 3 movies that I get from OMDB. 
# It will get the information that is stored in the cache dictionary
def get_top_actor(term):
	unique_identifier = "twitter_{}".format(actor__name)
	if unique_identifier in CACHE_DICTION:
		twitter_results = CACHE_DICTION[unique_identifier]
	else:
		twitter_results = api_user_timelines(actor_name)

		CACHE_DICTION[unique_identifier] = twitter_results
		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close

	tweet_texts = []
	for tweet in twitter_results:
		tweet_texts.append(tweet)
	return tweet_texts

	actor_list = get_top_actor((*insert actor name here*)


