import config
import textwrap
import webbrowser
import tweepy

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)

print('BIRDBATH: Clean your twitter history!')


try:
    redirect_url = auth.get_authorization_url()
    print('1. Go to: ' + redirect_url )
    webbrowser.open(redirect_url)
    pin = input('2. Enter your verification pin: ').strip()
    token = auth.get_access_token(verifier=pin)
except tweepy.TweepError:
    print('Invalid pin. Enter again!')

auth.set_access_token(*token)
api = tweepy.API(auth)
print('Logged in as: ' + api.me().screen_name)

for tweet in tweepy.Cursor(api.user_timeline).items():
    print(textwrap.fill(tweet.text))
    print('({},{})'.format(tweet.favorite_count, tweet.retweet_count))
    s = input('Delete? y/n  ')
    if (s == 'y'):
        try:
            api.destroy_status(tweet.id)
            print('DELETED: ', tweet.id)
        except Exception as err:
            print('Failed to delete: ', tweet.id)
            print(err)
    print(' -' * 30)
