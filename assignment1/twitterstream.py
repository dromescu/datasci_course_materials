import oauth2 as oauth
import json
import urllib2 as urllib

# See assignment1.html instructions or README for how to get these credentials

#api_key = "8RcVJ90o80FAQe1UR1ipQBvLe"
#api_secret = "9Bg8RJBUYEMMn8P4nIjNSpicc7QrY2ZAbh0QvU9zC8GpW0xhtW"
#access_token_key = "731638093984497664-RFAjBgA5JjEmm8ZOYqXejDAw1bfI1bE"
#access_token_secret = "DY4c8ZQyAUca1O6sqvKzvh8Z1b77OCGrfn4UbLG31RaKU"


# See assignment1.html instructions or README for how to get these credentials

api_key = "xWfLbCbnoLLzdVAGnjYVJAcoA"
api_secret = "fKxxuBfZBShvoi8gRGe1IUC0jVy8ldwGw5pSOKHeUCQ0fLu57F"
access_token_key = "737346366-DVHUXU6Af5fLUxKhkK6QY4OgCFGxQSk8zZ0ei8Zy"
access_token_secret = "4K9p5vqf1yq6ktEaoMk5dfWII8oHtWL9O976RG1r1uZPk"

_debug = 0

oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"

http_handler = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''


def twitterreq(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                token=oauth_token,
                                                http_method=http_method,
                                                http_url=url,
                                                parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response


def fetchsamples():

    url = "https://stream.twitter.com/1.1/statuses/sample.json"
    parameters = []
    response = twitterreq(url, "GET", parameters)

    n_tweets = 10000

    with open('output.txt', 'w') as text_file:

        for i, line in enumerate(response):

            # print line.strip()
            string_to_json_dict = json.loads(line)
            if 'created_at' in string_to_json_dict:
                # print string_to_json_dict['text']
                # print string_to_json_dict['text']
                # print line
                text_file.write(line)
            elif 'delete' in string_to_json_dict:
                # Do something with string_to_json_dict['delete]
                pass
            else:
                # Handle unexpected error here
                pass
            if i % 500 == 0:
                print ('{0} of {1} tweets processed.'.format(i, n_tweets))
            if i == n_tweets:
                print('Done!')
                break


if __name__ == '__main__':
    fetchsamples()
