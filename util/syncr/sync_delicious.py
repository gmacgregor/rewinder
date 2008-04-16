from rewinder.util.syncr.delicious import DeliciousSyncr

def run():
    d = DeliciousSyncr('sixminutes', 'faerie')
    # sync today's bookmarks
    d.syncBookmarks()
