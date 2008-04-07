from rewinder.util.syncr.tweet import TwitterSyncr

def run():
	t = TwitterSyncr('gmacgregor', 'faerie')
	t.syncTwitterUserTweets('gmacgregor')
