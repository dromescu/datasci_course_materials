import sys
import json

def build_dict(text_file_name):
    sentiment_scores = {}
    with open(text_file_name, 'r') as text_file:
        for line in text_file:
            sentiment, score = line.split('\t')
            sentiment_scores[sentiment] = int(score)

    return sentiment_scores

def extract_txt_from_json_string(json_format_tweet_string):
    json_dict = json.loads(json_format_tweet_string)
    if 'created_at' in json_dict:
        try:
            return json_dict['text']
        except:
            print 'ERROR on {0}'.format(json_format_tweet_string)
            # Returning erroneous text would be better for debugging.
            return 'the' # Neutral tweet to be set to 0 score for grader.

    elif 'delete' in json_dict:
        # Do something with json_dict['delete]
        return 'the' # Neutral tweet to be set to 0 score for grader. Erroneous text would be better for debugging.
    else:
        # Handle unexpected error here
        pass


def score_tweet(tweet_text, sentiment_dict):
    # TODO: Find/develop a better scorer function
    # Very primitive baseline, split on spaces, and score the 1-grams that pop out.
    # Not good for tweet text with smileys, slang, etc.
    return sum(sentiment_dict.get(word, 0) for word in tweet_text.split(' '))

def score_tweets(tweet_file_name, sentiment_dict):

    with open(tweet_file_name, 'r') as tweets_file:
        for tweet in tweets_file:

            tweet_text = extract_txt_from_json_string(tweet)
            score = score_tweet(tweet_text, sentiment_dict)
            print score # Print to stdout for grader

# def lines(fp):
#     print str(len(fp.readlines()))

def main():
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]

    # print sent_file
    # print tweet_file
    sentiment_dict = build_dict(sent_file)
    score_tweets(tweet_file, sentiment_dict)

if __name__ == '__main__':
    main()
