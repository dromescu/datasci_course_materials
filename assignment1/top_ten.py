# import json
# import sys
#
# def find_top_ten(tweet_file):
#
#     hashtag_counts = {}
#
#     with open(tweet_file, 'r') as tweets:
#
#         for tweet in tweets:
#
#             tweet = json.loads(tweet)
#
#             for hashtags in tweet['entities']['hashtags']:
#                 hashtag =  hashtags['text']
#                 hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
#
#     sorted_hashtags = sorted(hashtag_counts,
#                              key=hashtag_counts.get,
#                              reverse=True)
#     for key in sorted_hashtags[:10]:
#         print key, hashtag_counts[key]
#
# def main():
#
#     tweet_file = sys.argv[1]
#
#     # tweet_file = 'output_big.txt'
#     # tweet_file = 'problem_1_submission.txt'
#
#     find_top_ten(tweet_file)
#
# if __name__ == '__main__':
#     main()

import sys
import json
import re

instances = {}

def getHashTags():
	tweet_file = open(sys.argv[1])
	for line in tweet_file:
		result = json.loads(line)
		e = result.get('entities', None)
		if e!=None:
			h = e.get('hashtags',None)
			if h!=None:
				for i in range(0, len(h)):
					term = h[i].get('text').encode('ascii','ignore')
					instances[term] = int(instances.get(term,0))-1

def frequencies():
	count = 0
	for key, value in sorted(instances.iteritems(), key=lambda (k,v): (v,k)):
		if key!='' and count<10:
			print "%s %f" % (key, -instances[key])
			count = count+1

def main():
	getHashTags()
	frequencies()

if __name__ == '__main__':
	main()
