import argparse, os
import twert_helper
from botconfig import config
from twitter import *
from simplejson import loads, dumps
import string

parser = argparse.ArgumentParser(description="Checks for recent unanswered @mentions and replies to them individually")
parser.add_argument('-o', '--stdout', action='store_true', help="Shows replies without actually sending to twitter")
args = parser.parse_args()

try:
    state = loads(open(os.path.join(os.path.dirname(__file__), '.state'), 'r').read())
except:
    state = {}

if 'last_reply' not in state:
    state['last_reply'] = 0

api = Twitter(auth=OAuth(**config['api']))

def check_names(rp):
    print rp
    for name in config['screen_name']:
        if rp["user"]["screen_name"].lower() == name.lower():
            return True
    return False

if config['replies']:
    if not args.stdout:
        print "Performing replies"
    else:
        print "Printing test replies (dry-run)"
    
    last_tweet = long(state['last_reply'])
    
    replies = None
    if last_tweet:
        replies = api.statuses.mentions_timeline(since_id=last_tweet)
    else:
        replies = api.statuses.mentions_timeline()
    
    for reply in replies:
        if check_names(reply):
            continue
        
        tweet_text = reply["text"].encode('utf-8', 'replace')
        tweet_text = string.lstrip(tweet_text, "@" + config["screen_name"])
        
        reply_tweet = twert_helper.create_tweet().encode('utf-8', 'replace')
        reply_tweet = twert_helper.smart_truncate('@%s %s' % (reply["user"]["screen_name"].encode('utf-8', 'replace'), reply_tweet))
        if not args.stdout:
            api.statuses.update(status=reply_tweet, in_reply_to_status_id=reply["id"])
        else: 
            print(reply_tweet)
        # except:
        #   print 'Error posting reply.'

        last_tweet = max(reply["id"], last_tweet)
        break

    if not args.stdout:
        state['last_reply'] = str(last_tweet)
        print "Saving state"

open(os.path.join(os.path.dirname(__file__), '.state'), 'w').write(dumps(state))
