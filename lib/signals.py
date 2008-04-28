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
    
    In the case of a blog post, if the article's status is PUBLISHED_STATUS, attempt to create a new TumblelogItem.
    If it's not (ie. it is DRAFT_STATUS), try to remove it from the Tumblelog
    '''
    ctype = get_ctype(instance)
    if ctype.name == "article":
        pub_date = instance.pub_date
        from rewinder.apps.blog.models import PUBLISHED_STATUS
        if int(instance.status) is not PUBLISHED_STATUS:
            try:
                item = TumblelogItem.objects.get(object_id=instance.id, content_type=ctype)
                item.delete()
            except ObjectDoesNotExist:
                pass
        else:
            try:
                item = TumblelogItem.objects.get(object_id=instance.id, content_type=ctype)
            except ObjectDoesNotExist:
                item = TumblelogItem(object_id=instance.id, content_type=ctype, pub_date=pub_date)
                item.save()
    elif ctype.name == "tweet":
        pub_date = instance.pub_time
    elif ctype.name == "bookmark":
        pub_date = instance.saved_date
    elif ctype.name == "photo":
        pub_date = instance.taken_date
    elif ctype.name == "video":
        pub_date = instance.pub_date
    try:
        item = TumblelogItem.objects.get(object_id=instance.id, content_type=ctype)
    except ObjectDoesNotExist:
        item = TumblelogItem(object_id=instance.id, content_type=ctype, pub_date=pub_date)
        item.save()

def kill_tumblelog_item(sender, instance):
    ctype = get_ctype(instance)
    try:
        item = TumblelogItem.objects.get(object_id=instance.id, content_type=ctype)
        item.delete()
    except ObjectDoesNotExist:
        pass
