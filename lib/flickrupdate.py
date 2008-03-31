"""
flickrupdate.py

via: http://www.djangosnippets.org/snippets/299/

Requires flickrlib.py (http://monotonous.org/2005/11/26/flickrlib-05/)

Syncs Django flickr model with flickr.
Sync is one way (flickr->django), as I didn't see any need to edit photos in Django.

Copyright (c) 2007, Bret Walker

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of the Bret Walker nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from math import ceil
from datetime import datetime
import sys

from flickrlib import FlickrAgent

from rewinder.apps.photos.models import Photo
from rewinder.apps.photos.models import Set
from rewinder.apps.photos.models import Pool

api_key = "c5b82d5a4ae7101366113790d947da9e"
api_secret = "072822dd97710515"
flickr_uid = 'gregor002'
#flickr_username = 'gregor002'
#flickr_password = 'faerie'

agent = FlickrAgent(api_key, api_secret)

def update_sets():
    
    """Get sets from Flickr"""
    photo_sets = agent.flickr.photosets.getList()['photosets'][0]
    
    """Create a list of all set ids (flickr ids).  Items will be removed from the list if they're found to be in the local database"""
    sets_to_prune = []
    current_sets = Set.objects.values('set_id')
    for current_set in current_sets:
        sets_to_prune.append(int(current_set['set_id']))    
    
    """Iterate through photo sets returned by flickr"""
    for photo_set in photo_sets['photoset']:
        
        """Create a new set from the info given to us by flickr and save it to the database"""
        s = Set(set_id=int(photo_set['id']),
        primary=photo_set['primary'],
        secret=photo_set['secret'],
        server=int(photo_set['server']),
        farm=int(photo_set['farm']),
        title=photo_set['title'][0]['text'],
        description=photo_set['description'][0]['text'],
        photos=int(photo_set['photos']),
        )
        
        """Try to find a set in the database which has the same set id as given to us by flickr"""
        try:
            matching_set = Set.objects.get(set_id=photo_set['id'])
            """Found matching set, remove it from the list of sets to be removed from local database"""
            sets_to_prune.remove(int(photo_set['id']))
            
            """Iterate through each of the fields, looking for differences.  Skip the first (auto id) field, since it will always differ"""
            for k in s._meta.fields[1:]:
                """If a difference is found, go ahead and commit the s Set to the database and break out of this loop"""
                if getattr(s, k.name) != getattr(matching_set, k.name):
                    s.id = matching_set.id
                    s.save()
                    #print 'Updated set ' + s.title + ' k: ' + k.name
                    break
                                
        except Set.DoesNotExist:
            """Exception thrown by above try meaning there is no record of an object with the set id give by flickr"""
            s.save()
            #print 'Created set: ' + s.title
        
    
    """Iterate through the sets_to_prune list, deleting any remaining sets from the local database"""            
    for photo_set in sets_to_prune:
        s = Set.objects.get(set_id=photo_set)
        #print 'Deleted set: ' + s.title
        s.delete()
    
def update_photos():
    
    """Empty dict to hold photo ids and update times"""
    photo_ids = {}
    """Set number to fetch, and whether to get additional photos if there are more than the number you're fetching.
    Max number to fetch is 500.  Depending on how often you run this script, you may or may not need to get all, or
    even 500.  Think carefully about how many photos you need to """
    num_to_fetch = 50
    get_all = True
    
    photos_to_prune = []
    for p in Photo.objects.all():
        photos_to_prune.append(int(p.photo_id))
    
    """Search photos, getting all belonging to you"""
    photos = agent.flickr.photos.recentlyUpdated(user_id=flickr_uid, per_page=num_to_fetch, extras="last_update", min_date='18000')['photos'][0]
    
    """Store photo ids returned by search"""
    for photo in photos['photo']:
        photo_ids[photo['id']] = photo['lastupdate']
    
    """If get more is true, then loop through all photos"""
    if get_all:
        """Get the total number of photos that flickr reports"""
        total_photos = int(photos['total'])
        
        """Make sure there are more photos than the number we've already fetched"""
        if total_photos > num_to_fetch:
            """Loop, searching flickr for remaining photos"""
            while total_photos > len(photo_ids):
                photos = agent.flickr.photos.search(user_id=flickr_uid, per_page=num_to_fetch, page=(len(photo_ids)+num_to_fetch)/num_to_fetch)['photos'][0]

                """Store photo ids returned by search"""
                for photo in photos['photo']:
                    photo_ids[photo['id']] = photo['lastupdate']
                
    for photo_id in photo_ids.keys():
        try:
            matching_photo = Photo.objects.get(photo_id=photo_id)
            """Match found, so remove it from list of bad photos"""
            photos_to_prune.remove(int(photo_id))
            if datetime.fromtimestamp(float(photo_ids[photo_id])) > matching_photo.last_updated:
                p = Photo(**get_photo_info(photo_id))
                p.id = matching_photo.id
                p.save()
                #print 'Updated photo: ' + p.title
                update_pools(photo_id)
                
        except Photo.DoesNotExist:
            p = Photo(**get_photo_info(photo_id))
            p.save()
            #print 'Created photo: ' + p.title
            update_pools(photo_id) 
    
    """Iterate through the sets_to_prune list, deleting any remaining sets from the local database"""            
    for photo_id in photos_to_prune:
        p = Photo.objects.get(photo_id=photo_id)
        #print "Deleted photo: " + p.title
        p.delete()    
    
def get_photo_info(photo_id):
    photo_info = agent.flickr.photos.getInfo(photo_id=photo_id)['photo'][0]
    
    
    return_data = {}
    return_data['photo_id'] = photo_id
    return_data['secret'] = photo_info['secret']
    return_data['server'] = photo_info['server']
    return_data['is_favorite'] = photo_info['isfavorite']
    return_data['farm'] = photo_info['farm']
    return_data['original_secret'] = photo_info['originalsecret']
    return_data['views'] = photo_info['views']
    return_data['original_format'] = photo_info['originalformat']
    return_data['license'] = photo_info['license']
    return_data['title'] = photo_info['title'][0]['text']
    return_data['description'] = photo_info['description'][0]['text']
    return_data['is_public'] = photo_info['visibility'][0]['ispublic']
    return_data['is_family'] = photo_info['visibility'][0]['isfamily']
    return_data['is_friend'] = photo_info['visibility'][0]['isfriend']
    return_data['date_taken'] = photo_info['dates'][0]['taken']
    return_data['date_uploaded'] = datetime.fromtimestamp(float(photo_info['dateuploaded']))
    return_data['last_updated'] = datetime.fromtimestamp(float(photo_info['dates'][0]['lastupdate']))
    return_data['comments'] = photo_info['comments'][0]['text']
    return_data['photo_page'] = photo_info['urls'][0]['url'][0]['text']

    try:
        return_data['tags'] = ",".join(["%s" % (d['text']) for d in photo_info['tags'][0]['tag'][0]])
    except:
        """No tags"""
        pass
        
    try:
        return_data['latitude'] = photo_info['location'][0]['latitude']
        return_data['longitude'] = photo_info['location'][0]['longitude']
        return_data['accuracy'] = photo_info['location'][0]['accuracy']
        return_data['locality'] = photo_info['location'][0]['locality'][0]['text']
        return_data['county'] = photo_info['location'][0]['county'][0]['text']
        return_data['region'] = photo_info['location'][0]['region'][0]['text']
        return_data['country'] = photo_info['location'][0]['country'][0]['text']
        return_data['geo_is_public'] = photo_info['geoperms'][0]['ispublic']
        return_data['geo_is_contact'] = photo_info['geoperms'][0]['iscontact']
        return_data['geo_is_friend'] = photo_info['geoperms'][0]['isfriend']
        return_data['geo_is_family'] = photo_info['geoperms'][0]['isfamily']
    except:
        pass
    
    try:
        """Try to get the EXIF data"""
        """EXIF comes back a little funky, so it needs to be reformatted"""
    
        """Get EXIF data"""
        exif_info = agent.flickr.photos.getExif(photo_id=photo_id)['photo'][0]
    
        """Define a sortkey, in this cast tag number"""
        def sortkey(item):
            return item.get("tag")
        
        """Sort the list"""
        exif_info['exif'].sort(key=sortkey)
        exif_info['exif'].reverse() # often two apertures, the second one normally includes only raw.  reverse so the second one contains clean too
        
        """Create a dict to be used to hold sorted, relevant data"""
        exif_info_sorted = {}
    
        """Pull out raw and clean tags.  Every attribute has raw, some have clean"""
        for d in exif_info['exif']:
            try:
                exif_info_sorted[d['label']] = {'raw': d['raw'], 'clean': d['clean']}
            except:
                try:
                    exif_info_sorted[d['label']] = {'clean': d['clean']}
                except:
                    exif_info_sorted[d['label']] = {'raw': d['raw']}
        
        def get_exif(attribute):
            """Return the selected attribute.
            This function will always try to return the clean attribute, but if it can't, it will return the raw version"""
        
            try:
                return exif_info_sorted[attribute]['clean'][0]['text']
            except:
                return exif_info_sorted[attribute]['raw'][0]['text']
        
        return_data['exif_make'] = get_exif('Make')
        return_data['exif_model'] = get_exif('Model')
        return_data['exif_orientation'] = get_exif('Orientation')
        return_data['exif_exposure'] = get_exif('Exposure')
        return_data['exif_software'] = get_exif('Software')
        return_data['exif_aperture'] = get_exif('Aperture')
        return_data['exif_exposure_program'] = get_exif('Exposure Program')
        return_data['exif_iso'] = get_exif('ISO Speed')
        return_data['exif_metering_mode'] = get_exif('Metering Mode')
        return_data['exif_flash'] = get_exif('Flash')
        return_data['exif_focal_length'] = get_exif('Focal Length')
        return_data['exif_color_space'] = get_exif('Color Space')
    
    except:
        """No EXIF data, so just move along"""
        pass   
    
    return return_data

def update_photos_sets():
    sets = Set.objects.all()
    for s in sets:
        set_photos = agent.flickr.photosets.getPhotos(photoset_id=str(s.set_id))['photoset'][0]
        
        photos_to_prune = []
        current_photos = s.photo_set.all()
        for current_photo in current_photos:
            photos_to_prune.append(current_photo.photo_id)
                
        for p_id in set_photos['photo']:
            try:
                photos_to_prune.remove(int(p_id['id']))
            except:
                # not in set
                pass
                
            p = Photo.objects.get(photo_id=p_id['id'])
            if not (p.sets.filter(set_id=s.set_id)):
                p.save()
                p.sets.add(Set.objects.get(set_id=s.set_id))   
                #print 'Added ' + p.title + ' to Set ' + s.title
        
        """Iterate through the sets_to_prune list, deleting any remaining sets from the local database"""            
        for photo in photos_to_prune:
            p = Photo.objects.get(photo_id=photo)
            p.sets.remove(Set.objects.get(set_id=s.set_id))
            #print "Removed photo: " + p.title + " from Set " + s.title

def update_pools(photo_id):
    photo_context = agent.flickr.photos.getAllContexts(photo_id=photo_id)
    
    try:
        for pool in photo_context['pool']:
            """Try to find a pool in the database which has the same set id as given to us by flickr"""
            try:
                matching_pool = Pool.objects.get(pool_id=pool['id'])
            
                """Found matching pool, associate it with this photo"""
                p = Photo.objects.get(photo_id=photo_id)
                p.save()
                p.pools.add(matching_pool)
                #print "Added " + p.title + " to Pool " + matching_pool.title
                                
            except Pool.DoesNotExist:
                """Exception thrown by above try meaning there is no record of an object with the set id give by flickr"""
                """Create a new set from the info given to us by flickr and save it to the database"""
                pool = Pool(pool_id=pool['id'],
                title=pool['title'],
                )
                pool.save()
                #print 'Created pool: ' + p.title
                """Add photo to pool"""
                p = Photo.objects.get(photo_id=photo_id)
                p.save()
                p.pools.add(matching_pool)
                #print "Added " + p.title + " to Pool " + matching_pool.title
    except:
        """No pool"""
        pass
    
if __name__ == '__main__':
    update_sets()
    update_photos()
    update_photos_sets()

"""
END OF FLICKRUPDATE
"""