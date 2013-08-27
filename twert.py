import argparse, sys, os
from botconfig import config
import twert_helper
from twitter import *

parser = argparse.ArgumentParser(description="Post ebooks tweets to twitter.")
parser.add_argument('-o', '--stdout', action='store_true', help="Output to stdout instead of posting to twitter.")
parser.add_argument('-b', '--both', action='store_true', help="Output to stdout instead of posting to twitter.")
parser.add_argument('-t', '--tweet', help="Tweet arbitrary text instead of using the brain.")

args = parser.parse_args()

t = Twitter(auth = OAuth(**config['api']))

if args.tweet:
    t.statuses.update(args.tweet)
else:
    tweet = twert_helper.create_tweet()
    if args.stdout:
        print tweet
    elif args.both:
        print tweet
        status = t.statuses.update(status=tweet)
    else:
        status = t.statuses.update(status=tweet)
