from django.db import models
from taggit_autocomplete_modified.managers import TaggableManagerAutocomplete as TaggableManager
from imagekit.models import ImageModel
import undefcms.imagespecs

class Image(ImageModel):
    title = models.CharField(max_length=100)
    original_image = models.ImageField(upload_to='images')
    
    num_views = models.PositiveIntegerField(editable=False, default=0)
    
    class IKOptions:
        # This inner class is where we define the ImageKit options for the model
        spec_module = 'undefcms.imagespecs'
        cache_dir = 'thumbs'
        image_field = 'original_image'
        save_count_as = 'nunm_views'
        admin_thumbnail_spec = 'thumbnail_image'

#MAIN MODEL
class Post(models.Model):
    title = models.CharField(max_length = 512)
    slug = models.SlugField(max_length = 128)
    tags = TaggableManager(blank=True)
    creation = models.DateTimeField(blank=True)
    last_edit = models.DateTimeField(blank=True, auto_now_add=True)
    visible = models.BooleanField()
    content = models.TextField()
    
    #header stuff
    header = models.TextField(blank=True)
    javascript = models.TextField(blank=True)
    css = models.TextField(blank=True)
    
    #image
    preview = models.ForeignKey(Image, related_name="+", blank=True, null=True)
    
    images = models.ManyToManyField(Image, blank=True)
    
    
    
