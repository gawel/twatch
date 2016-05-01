# -*- coding: utf-8 -*-


def format_tweet(tweet):
    return (
        '@{user[screen_name]}: {text} - '
        'https://twitter.com/{user[screen_name]}/status/{id_str}'
    ).format(**tweet)


def print_tweet(tweet):
    print(format_tweet(tweet))


def print_real_tweet(tweet):
    if tweet['retweeted'] or tweet['in_reply_to_user_id']:
        return
    if 'RT ' in tweet['text']:
        return
    print(format_tweet(tweet))
