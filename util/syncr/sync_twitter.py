from rewinder.syncr.app.tweet import TwitterSyncr

def run():
	t = TwitterSyncr('gmacgregor', 'faerie')
	t.syncTwitterUserTweets('gmacgregor')