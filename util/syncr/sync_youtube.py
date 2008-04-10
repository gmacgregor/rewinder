from rewinder.util.syncr.youtube import YoutubeSyncr

def run():
    yt = YoutubeSyncr()
    videos = yt.syncUserFavorites('gregor003')
    for video in videos:
        print video
        print '*'*40
