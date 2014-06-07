import re, os, glob, csv

tweets = []
ignored = 0

# for each csv file
for filename in glob.glob('*.csv'):

    # open the file and parse it as csv
    with open(filename, 'rb') as csvfile:
        tweetreader = csv.DictReader(csvfile)
        for tweet in tweetreader:
            text = tweet["text"]
            print text
            
            # add it to the tweetlist if it isn't a reply or retweet
            if not text.startswith('@') and not text.startswith('RT'):
                tweets.append(text)
            else:
                ignored += 1

# we have all the tweets now! throw em in a file, one per line
open('./tweets.txt', 'w').write('\n'.join(tweets))
print "Processed %d tweets (ignored %d)" % (len(tweets), ignored)
