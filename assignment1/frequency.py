import string
import sys
import json

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



def strip_punct(text):
    ''' Strips punctuation from a utf-8 string.
    Args:
        text (string): utf-8 string to strip punctuation from
    Returns:
        (string): String in original decoded format with punctuation removed
    '''
    encoded_string = text.encode('utf-8').translate(None, string.punctuation)
    return encoded_string.decode('utf-8')

def term_freq_histogram(tweet_file_name):

    frequency_dict = {}

    with open(tweet_file_name, 'r') as tweets:

        word_count = 0

        for tweet in tweets:

            tweet = extract_txt_from_json_string(tweet)
            tweet = strip_punct(tweet)

            tweet_words = [word.lower() for word in tweet.split()]

            for word in tweet_words:
                word_count += 1
                frequency_dict[word] = frequency_dict.get(word, 0) + 1

        for each_word, each_count in frequency_dict.iteritems():
            print each_word, each_count/float(word_count)



def main():

    tweet_file = sys.argv[1]
    # tweet_file = 'problem_1_submission.txt'
    # tweet_file = 'test.txt'

    term_freq_histogram(tweet_file)

if __name__ == '__main__':
    main()
