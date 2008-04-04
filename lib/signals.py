from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import signals
from django.db.models import get_model
from django.dispatch import dispatcher
from django.contrib.contenttypes.models import ContentType

from rewinder.apps.tumblelog.models import TumblelogItem


def get_ctype(instance):
    return ContentType.objects.get_for_model(instance)

def create_tumblelog_item(sender, instance):
    '''
    If the instance exists, just "pass". Otherwise, create a new TumblelogItem
    '''
    ctype = get_ctype(instance)
    pub_date = instance.pub_date
    try:
        item = TumblelogItem.objects.get(object_id=instance.id, content_type=ctype)
    except ObjectDoesNotExist:
        item = TumblelogItem(pub_date=pub_date, object_id=instance.id, content_type=ctype)
        item.save()

def create_article_tumblelog_item(sender, instance):
    '''
    If the article's status is PUBLISHED_STATUS, attempt to create a new TumblelogItem
    If it's not (ie. it is DRAFT_STATUS), try to remove it from the Tumblelog
    '''
    from rewinder.apps.blog.models import PUBLISHED_STATUS, Article
    ctype = get_ctype(Article)
    if int(instance.status) is PUBLISHED_STATUS:
        try:
            item = TumblelogItem.objects.get(object_id=instance.id, content_type=ctype)
        except ObjectDoesNotExist:
            item = TumblelogItem(pub_date=instance.pub_date, object_id=instance.id, content_type=ctype)
            item.save()
    else:
        try:
            item = TumblelogItem.objects.get(object_id=instance.id, content_type=ctype)
            item.delete()
        except ObjectDoesNotExist:
            pass

def create_twitter_tumblelog_item(sender, instance):
    from syncr.twitter.models import Tweet
    ctype = get_ctype(Tweet)
    try:
        item = TumblelogItem.objects.get(object_id=instance.id, content_type=ctype)
    except ObjectDoesNotExist:
        item = TumblelogItem(pub_date=instance.pub_time, object_id=instance.id, content_type=ctype)
        item.save()   

def create_link_tumblelog_item(sender, instance):
    from syncr.delicious.models import Bookmark
    ctype = get_ctype(Bookmark)
    try: 
        item = TumblelogItem.objects.get(object_id=instance.id, content_type=ctype)
    except ObjectDoesNotExist:
        item = TumblelogItem(pub_date=instance.saved_date, object_id=instance.id, content_type=ctype)
        item.save()

#for model in settings.TUMBLELOG_MODELS:
#    dispatcher.connect(create_tumblelog_item, sender=get_model(*model.split('.')), signal=signals.post_save)