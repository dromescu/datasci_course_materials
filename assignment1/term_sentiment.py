import sys
import string
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



def strip_punct(text):
    ''' Strips punctuation from a utf-8 string.
    Args:
        text (string): utf-8 string to strip punctuation from
    Returns:
        (string): String in original decoded format with punctuation removed
    '''
    encoded_string = text.encode('utf-8').translate(None, string.punctuation)
    return encoded_string.decode('utf-8')


def report_UNK_avg_sentiment(sentiments_file_name, tweet_file_name):
    '''Keeps a running dictionary of the average sentiment score for any words
        not found in the AFINN sentiment word score text file.
        Calculates based on average sentiment of tweet found in.
        Then averaged with all other occurrences found in the twitter text file
        provided.
        Could return dictionary to keep running affect dictionary between
        sessions.
    Args:
        sentiments_file_name (string): Filename of a text file containing
         Space delimited AFINN dictionary of word:sentiment-value pairs
        tweet_file_name (string): Filename of a text file containing a string
         representation of a json object from the Twitter API on each line.
    Returns:
        (None) prints output to stdout
    '''
    AFINN_dict = build_dict(sentiments_file_name)

    # Build a new dictionary of words not in AFINN
    # Update as we go along to update sentiment as we see more tweets
    # Useful if we want to save the dict in the end for later use
    # Keep separate from AFINN since those words are already scaled
    # This will have to be in the format:
    #  key: word
    #  value: [times seen, score]
    # This is to keep a running average of the word sentiment as we see more
    new_word_AFINN = {}

    with open(tweet_file_name, 'r') as tweets:
        for tweet in tweets:
            # Extract the text of tweet from json object/string
            tweet = extract_txt_from_json_string(tweet)

            tweet = strip_punct(tweet)

            # print 'SANITY CHECK'
            # print 'Original Tweet: {0}'.format(tweet.encode('utf-8'))
            tweet_words = [word.lower() for word in tweet.split()]
            # print 'Words list: {0}'.format(tweet_words)

            total_tweet_sentiment = score_tweet(tweet, AFINN_dict)

            for word in tweet_words:

                try:
                    # If word is in AFINN, print word:value
                    assert(AFINN_dict[word])
                    print word, AFINN_dict[word]
                except KeyError as e:
                    # Try to get current tuple value of word not in AFINN, or 0
                    #  if not found
                    new_value_list = new_word_AFINN.get(word, [0, 0])

                    # update times seen
                    new_value_list[0] += 1

                    # Set as average sentiment of words in tweet for unseen words
                    word_sent = total_tweet_sentiment / float(len(tweet_words))


                    # update running average value
                    new_score = (new_value_list[1] + word_sent) / new_value_list[0]
                    new_value_list[1] = new_score

                    new_word_AFINN[word] = new_value_list

                    print word, new_score




def main():
    sentiments_file_name = sys.argv[1]
    tweet_file_name = sys.argv[2]
    report_UNK_avg_sentiment(sentiments_file_name, tweet_file_name)
    # report_UNK_avg_sentiment('AFINN-111.txt', 'problem_1_submission.txt')


if __name__ == '__main__':
    main()
