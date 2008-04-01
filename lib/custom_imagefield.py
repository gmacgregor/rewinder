from django.db.models import ImageField, signals
from django.dispatch import dispatcher

# via: http://scottbarnham.com/blog/2007/07/31/uploading-images-to-a-dynamic-path-with-django/
# also: http://scottbarnham.com/blog/2008/02/24/imagefield-and-edit_inline-revisited/
class CustomImageField(ImageField):
    """
    Allows model instance to specify upload_to dynamically.
    Model class should have a method like:
    
        def get_upload_to(self, attname):
            return 'path/to/%d' % self.id
    
    Based on: http://code.djangoproject.com/wiki/CustomUploadAndFilters
    """
    def contribute_to_class(self, cls, name):
        """Hook up events so we can access the instance."""
        super(CustomImageField, self).contribute_to_class(cls, name)
        dispatcher.connect(self._post_init, signals.post_init, sender=cls)
    
    def _post_init(self, instance=None):
        """Get dynamic upload_to value from the model instance."""
        if hasattr(instance, 'get_upload_to'):
            self.upload_to = instance.get_upload_to(self.attname)
            
    def db_type(self):
        """Required by Django for ORM."""
        return 'varchar(100)'

