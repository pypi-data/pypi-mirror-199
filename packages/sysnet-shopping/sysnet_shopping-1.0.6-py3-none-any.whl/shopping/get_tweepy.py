import tweepy

from shopping.config import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, \
    TWITTER_ACCESS_TOKEN_SECRET, TWITTER_BEARER_TOKEN

twitter_auth_key = {
    "consumer_key": TWITTER_CONSUMER_KEY,
    "consumer_secret": TWITTER_CONSUMER_SECRET,
    "access_token": TWITTER_ACCESS_TOKEN,
    "access_token_secret": TWITTER_ACCESS_TOKEN_SECRET,
    "bearer_token": TWITTER_BEARER_TOKEN
}


def get_tweets(word, lang, count, retweet):
    auth = tweepy.OAuthHandler(
        twitter_auth_key["consumer_key"],
        twitter_auth_key["consumer_secret"]
    )
    auth.set_access_token(
        twitter_auth_key["access_token"],
        twitter_auth_key["access_token_secret"]
    )
    API = tweepy.API(auth)
    results = [status._json for status in
               tweepy.Cursor(API.search_tweets, q=word, lang=lang, tweet_mode='extended').items(count)]
    my_tweets = []
    cols = []
    count_results = len(results)
    for result in results:
        keys = ("created_at", "full_text", "id", "user")
        res = {k: result[k] for k in keys}
        res["name_user"] = res["user"]["name"]
        res["user"] = res["user"]["location"]
        res["location"] = res.pop("user")
        # twid = res["id"]
        if retweet:
            if 'retweeted_status' in result.keys():
                retweet = result["retweeted_status"]
                retweet = {k: retweet[k] for k in keys}
                retweet["created_at_orig"] = retweet.pop("created_at")
                retweet["full_text_orig"] = retweet.pop("full_text")
                retweet["id_orig"] = retweet.pop("id")
            else:
                retweet = {
                    "created_at_orig": "",
                    "full_text_orig": "",
                    "id_orig": ""
                }
            res = {**res, **retweet}
        my_tweets.append(res)
        cols = list(res.keys())
    return my_tweets, cols, count_results


# https://www.programcreek.com/python/example/76301/tweepy.Cursor


def get_tweets_client(word, count):
    auth = twitter_auth_key["bearer_token"]
    api = tweepy.Client(auth)

    response = api.search_recent_tweets(
        query=word,
        max_results=count,
        tweet_fields=['text'],
        # tweet_fields=['author_id', 'created_at', 'text', 'source', 'lang', 'geo'],
        # user_fields=['name', 'username', 'location', 'verified'],
        # expansions=['geo.place_id', 'author_id'],
        place_fields=['country', 'country_code'])
    search_results = response.data
    return search_results
