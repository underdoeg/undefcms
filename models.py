from django.db import models
from taggit.managers import TaggableManager
from filebrowser.fields import FileBrowseField
import mimetypes
from undefcms.types import filetypes
import commands
import fields
from django.conf import settings
import re

#CATEGORY
class Category(models.Model):
    name = models.CharField(max_length = 512)
    slug = models.SlugField(max_length = 128)
    description = models.TextField(blank=True)
    parent = models.ForeignKey("self", blank=True, null=True)
    visible = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("name",)

#DEFINITIONS FOR COMMON PAGE AND POST FIELDS
class Content(models.Model):
    title = models.CharField(max_length = 512)
    slug = models.SlugField(max_length = 128)
    tags = TaggableManager(blank=True)
    creation = models.DateTimeField(blank=True)
    last_edit = models.DateTimeField(blank=True, auto_now_add=True)
    visible = models.BooleanField(default=True)
    #content = tinymce_models.HTMLField(blank=True)
    content = models.TextField(blank=True)
    description = models.TextField(blank=True)
    
    #category
    category = models.ManyToManyField(Category, blank=True, null=True)
    
    #image
    preview = FileBrowseField("Preview", max_length=200, directory="", extensions=[".jpg",".jpeg", ".gif", ".png"], blank=True, null=True)
    
    #header stuff
    header = models.TextField(blank=True)
    javascript = models.TextField(blank=True)
    css = models.TextField(blank=True)
    
    class Meta:
        abstract = True
    
#POST AND PAGE MODELS
class Post(Content):
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ('-creation',)
        
    def getFiles(self):
        return self.postfile_set.all()

class Page(Content):
    parent = models.ForeignKey("self", blank=True, null=True)
    index = models.PositiveIntegerField(default = 0)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ("index", )
        
    def getFiles(self):
        return self.pagefile_set.all()


FILE_TYPE_CHOICES = (
    ('auto', 'auto'),
    ('img', filetypes['image']),
    ('html', filetypes['html']),
    ('video', filetypes['video']),
    ('audio', filetypes['audio'])
)

#FILE
class File(models.Model):
    name = models.CharField(max_length = 512, blank=True)
    description = models.TextField(blank = True, verbose_name="content")
    file = FileBrowseField("File", max_length=200, directory="", blank=True, null=True)
    index = models.PositiveIntegerField()
    type = models.CharField(max_length = 128, blank = False, null = True, editable = True, choices = FILE_TYPE_CHOICES, default = "auto")
    extra = fields.JSONField(null=True, blank=True, editable = False)
    
    def save(self, *args, **kwargs):
        if self.file:
            mime = mimetypes.guess_type(self.file.path)[0]
            if self.extra is None:
                self.extra = {}
            self.extra["mime"] = mime
            
            if self.type == "auto": #We don't know the mime type yet. try to guess it
                if mime == "image/jpeg" or mime == "image/png" or mime == "image/gif":
                    self.type = filetypes["image"]
                elif mime == "video/mp4":
                    self.type = filetypes["video"]
                    if self.extra.has_key("lastFile") is False or self.extra["lastFile"] != self.file.filename or settings.DEBUG:
                        res = commands.getoutput("ffmpeg -i "+self.file.path)
                        dimFind = re.findall(r'(\d+x\d+)', res)
                        if len(dimFind) is not 0:
                            dim = dimFind[0].split("x")
                            width = dim[0]
                            height = dim[1]
                            self.extra["width"] = width
                            self.extra["height"] = height
                        '''
                        #time to encode
                        videoPath = settings.MEDIA_ROOT+"encodedVideos/"
                        comOGG = "ffmpeg -i "+self.file.path+" -acodec libvorbis -ac 2 -ab 96k -ar 44100 -b 345k -s "+dimFind[0]+" "+videoPath+self.file.filename+".ogv"
                        res = commands.getoutput(comOGG)
                        self.extra["encodeMsg"] = res
                        '''
                elif mime == 'audio/mpeg':
                    self.type = filetypes["audio"]
                else:
                    self.type = mime
            self.extra["lastFile"] = self.file.filename
        super(File, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('index',)
        abstract = True
    
class PageFile(File):
    page = models.ForeignKey(Page)

class PostFile(File):
    post = models.ForeignKey(Post)
    
    
