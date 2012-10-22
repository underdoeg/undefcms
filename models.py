from django.db import models
from taggit.managers import TaggableManager
from filebrowser.fields import FileBrowseField
from filebrowser.base import FileListing, FileObject
import mimetypes
from undefcms.types import filetypes
import commands
import fields
from django.conf import settings
import re
from filebrowser.settings import MEDIA_ROOT
import os
import md5

# import the logging library
import logging

#CATEGORY
class Category(models.Model):
    name = models.CharField(max_length = 512)
    slug = models.SlugField(max_length = 128)
    description = models.TextField(blank=True)
    parent = models.ForeignKey("self", blank=True, null=True)
    visible = models.BooleanField(default=True)
    index = models.PositiveIntegerField(default = 0)

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("index", "name",)

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
        ordering = ("index", "title")
        
    def getFiles(self):
        return self.pagefile_set.all()


FILE_TYPE_CHOICES = (
    ('auto', 'auto'),
    ('img', filetypes['image']),
    ('html', filetypes['html']),
    ('video', filetypes['video']),
    ('audio', filetypes['audio']),
    ('text', filetypes['text']),
    ('listfolder', 'listfolder')
)

#FILE
def getHash(file):
    output = commands.getoutput("md5sum "+file)
    split = output.split(" ")
    return split[0]

class File(models.Model):
    name = models.CharField(max_length = 512, blank=True)
    description = models.TextField(blank = True, verbose_name="content")
    file = FileBrowseField("File", max_length=200, directory="", blank=True, null=True)
    index = models.PositiveIntegerField()
    type = models.CharField(max_length = 128, blank = False, null = True, editable = True, choices = FILE_TYPE_CHOICES, default = "auto")
    extra = fields.JSONField(null=True, blank=True, editable = False)
    
    def content(self):
        return self.description
    
    def save(self, *args, **kwargs):
        logger = logging.getLogger("undefcms")
        
        isFileNew = False
        
        if self.file:
            #get the mime
            mime = mimetypes.guess_type(self.file.path)[0]
            if self.extra is None:
                self.extra = {}
            self.extra["mime"] = mime
            if not "md5" in self.extra:
                self.extra["md5"] = ""
            
            #get the md5 hash
            oldMd5 = self.extra["md5"]
            self.extra["md5"] = getHash(settings.MEDIA_ROOT+self.file.path)
            
            if oldMd5 != self.extra["md5"]:
                isFileNew = True
            
            #isFileNew = True
            
            if self.type == "auto": #We don't know the mime type yet. try to guess it
                if mime == "image/jpeg" or mime == "image/png" or mime == "image/gif":
                    self.type = filetypes["image"]
                elif mime == "video/mp4":
                    self.type = filetypes["video"]
                elif mime == "video/ogg":
                    self.type = filetypes["video"]
                elif mime == "video/avi":
                    self.type = filetypes["video"]
                elif mime == 'audio/mpeg':
                    self.type = filetypes["audio"]
                else:
                    self.type = mime
            
            if self.type == "img":
                if isFileNew:
                    self.extra["width"] = self.file.width
                    self.extra["height"] = self.file.height
            
            if self.type == "listfolder":
                logger.debug("LOOKING THRU "+MEDIA_ROOT+self.file.path)
                
                def filter(item):
                    return item.is_version != True
                
                filelisting = FileListing(MEDIA_ROOT+self.file.path,  sorting_by='name', sorting_order='desc', filter_func=filter)
                for item in filelisting.files_walk_filtered():
                    #logger.debug(type(self) == type(PostFile))
                    #logger.debug(isinstance(self, PageFile))
                    newFile = None
                    if isinstance(self, PageFile):
                        newFile = PageFile(page=self.page)
                    if isinstance(self, PostFile):
                        newFile = PostFile(post = self.post)
                    if newFile is not None:
                        newFile.index = self.index
                        newFile.file = FileObject(os.path.join(self.file.path, item.filename))
                        newFile.save()
                if self.id > 0:
                    self.delete()
                return
            
            if self.type == "video":
                if isFileNew:
                    #get width and height of video
                    res = commands.getoutput("ffmpeg -i \""+settings.MEDIA_ROOT+self.file.path+"\"")
                    dimFind = re.findall(r'( \d+x\d+ )', res)
                    if len(dimFind) is 0:
                        dimFind = re.findall(r'(\d+x\d+)', res)
                    width = 0
                    height = 0
                    self.extra["width"] = 0
                    self.extra["height"] = 0
                    if len(dimFind) is not 0:
                        dim = dimFind[0].split("x")
                        width = dim[0]
                        height = dim[1]
                        self.extra["width"] = width
                        self.extra["height"] = height
                    #and now convert it to use for web
                    from utils import convertVideo
                    if width != 0 and height != 0:
                        self.extra["msg"] = convertVideo(self.file.path, width, height)
            
            self.extra["lastFile"] = self.file.filename
        super(File, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name
    
    def dimensions(self):
        if self.type != "img":
            return 0, 0
        
         #get width and height
        imgWidth = 0
        imgHeight = 0
        
        if self.extra is None:
            self.extra =  {}
            saveIt = True
            
        if "width" in self.extra:
            imgWidth = self.extra["width"]
        if "height" in self.extra:
            imgHeight = self.extra["height"]
            
        saveIt = False
        if imgWidth == 0 or imgWidth == None:
            imgWidth = self.file.width
            self.extra["width"] = imgWidth
            saveIt = True
            
        if imgHeight == 0 or imgHeight == None:
            imgHeight = self.file.height
            self.extra["height"] = imgHeight
            saveIt = True
        
        if saveIt:
            self.save()
        
        return imgWidth, imgHeight
    
    def thumbUrl(self, width = None, height = None):
        if self.type != "img":
            return "no image"
        
        if width == None and height == None:
            width = 10
        
        imgWidth, imgHeight = self.dimensions()
        
        from utils import getThumbUrl
        
        if width>imgWidth:
            width = imgWidth
        
        if height>imgHeight:
            height = imgHeight
        
        return getThumbUrl(self.file.path, imgWidth, imgHeight, width, height)
    
    def videoOggUrl(self):
        return settings.MEDIA_URL+"encodedVideos/"+self.file.path+".ogv"

    def videoMp4Url(self):
        return settings.MEDIA_URL+"encodedVideos/"+self.file.path+".mp4"
    
    def videoWebmUrl(self):
        return settings.MEDIA_URL+"encodedVideos/"+self.file.path+".webm"
    
    class Meta:
        ordering = ('index',)
        abstract = True
    
    def thumbWidth(self, height):
        imgWidth, imgHeight = self.dimensions()
        if height>imgHeight:
            height = imgHeight
        return int(height/float(imgHeight)*imgWidth)

    def thumbHeight(self, width):
        imgWidth, imgHeight = self.dimensions()
        if width>imgWidth:
            width = imgWidth
        return int(width/float(imgWidth)*imgHeight)
    
class PageFile(File):
    page = models.ForeignKey(Page)
    
    def getNext(self):
        next_queryset = PageFile.objects.filter(page=self.page, index__gt=self.index)
        if next_queryset.count() > 0:
            return next_queryset.order_by('index')[0]
        return None
    
    def getPrev(self):
        next_queryset = PageFile.objects.filter(page=self.page, index__lt=self.index)
        if next_queryset.count() > 0:
            return next_queryset.order_by('-index')[0]
        return None

class PostFile(File):
    post = models.ForeignKey(Post)
    
    def getNext(self):
        next_queryset = PostFile.objects.filter(post=self.post, index__gt=self.index)
        if next_queryset.count() > 0:
            return next_queryset.order_by('index')[0]
        return None
    
    def getPrev(self):
        next_queryset = PostFile.objects.filter(post=self.post, index__lt=self.index)
        if next_queryset.count() > 0:
            return next_queryset.order_by('-index')[0]
        return None
