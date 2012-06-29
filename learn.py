import twitter, os
import config
from simplejson import loads, dumps
from cobe.brain import Brain

b = Brain(os.path.join(os.path.dirname(__file__), 'cobe.brain'))

try:
	state = loads(open(os.path.join(os.path.dirname(__file__), '.state'), 'r').read())
except:
	state = {'accounts': {}}

api = twitter.Api(**config.api)

b.start_batch_learning()
tweets = 0
for account in config.dump_accounts:
	print "Grabbing tweets for %s" % account
	if account in state['accounts']:
		last_tweet = state['accounts'][account]
	else:
		last_tweet = 0
	latest_tweet = 0
	timeline = api.GetUserTimeline(account, count=200, since_id=latest_tweet)
	for tweet in timeline:
		if tweet.id > last_tweet:
			if config.skip_mentions and tweet.text[0] == '@':
				continue

			b.learn(tweet.text)
			if tweet.id > latest_tweet:
				latest_tweet = tweet.id
			tweets += 1

	state['accounts'][account] = latest_tweet

print "Learning %d tweets" % tweets
b.stop_batch_learning()
print "Saving data"

open(os.path.join(os.path.dirname(__file__), '.state'), 'w').write(dumps(state))