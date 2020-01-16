# coding=utf-8
import tweepy
import os


# TwitterアカウントのTwitterAPIを用意
def prepare_twitter_api():
    """
    TwitterのAPIアクセスキーを取得
    """
    auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
    auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])
    return tweepy.API(auth)


def search_user_tweets_by_id(api, id, include_rts):
    """
    user_screen_name(@taroのtaroの部分)のTwitterユーザーのつぶやきを200件取得します。
    :param: include_rts リツイートを含むかどうか (True = リツイート含む, False = リツイート含まず)
    """
    return api.user_timeline(user_id=id, count=200, include_rts=include_rts)
