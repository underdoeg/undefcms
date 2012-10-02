from models import *
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Q
import os.path
from undefcms.types import filetypes

def getCategoriesRecursiveHelper(parent, activeId):
    if parent == None:
        set = Category.objects.filter(parent__isnull=True, visible=True)
    else:
        set = Category.objects.filter(parent=parent.id, visible=True)
    
    for c in set:
        c.parent = parent;
        if c.id == activeId:
            p = parent
            while p is not None:
                p.active = True
                p = p.parent
            c.active = True
        else:
            c.active = False
        c.children = getCategoriesRecursiveHelper(c, activeId)
    return set
    
def getCategories(slug = "", id = -1):
    activeId = id
    if slug != "":
        activeId = getCategoryIdBySlug(slug)
    ret = getCategoriesRecursiveHelper(None, activeId)
    return ret
    
def getCategoryIdBySlug(catSlug):
    return get_object_or_404(Category, slug__iexact=catSlug).id

def getCategory(id=-1, slug=""):
    if slug != "":
        return get_object_or_404(Category, slug__iexact=slug)
    else:
        return get_object_or_404(Category, pk=id)

def getPosts(showHidden = False, excludeCategories = []):
    ret = Post.objects.all()
    for exclude in excludeCategories:
        if type(exclude) is int:
            ret = ret.exclude(category__id=exclude)
        else:
            ret = ret.exclude(category__slug=exclude)
    if showHidden == False:
        ret = ret.filter(visible = True)
    return ret

def getPostsByCategory(catId, showHidden=False):
    ret = getPosts(showHidden=showHidden)
    if isinstance(catId, int) or isinstance(catId, long):
        return ret.filter(category=catId)
    else:
        if len(catId) is 0:
            return getPosts(showHidden=showHidden)
        for c in catId:
            ret = ret.filter(category=c)
        return ret

def getPostsByCategorySlug(slug, showHidden=False):
    return getPostsByCategory(getCategoryIdBySlug(slug), showHidden=showHidden)
    
def getPostsGroupedByCategory():
    ret = []
    categories = getCategories()
    for cat in categories:
        ret.append({'category':cat, 'posts':getPostsByCategory(cat.id)})
    return ret

def getPostsByTags(tags):
    if isinstance(tags, basestring):
        tags = [tags,]
    return getPosts().filter(tags_name_in=tags)

def getPostIdBySlug(slug):
    return get_object_or_404(Post, slug__iexact=slug).id
    
def getPost(postId):
    if isinstance(postId, basestring):
        return Post.objects.get(id=getPostIdBySlug(postId))
    return Post.objects.get(id=postId)

def getPostBySlug(slug):
    return getPost(getPostIdBySlug(slug))

def searchPosts(query):
    return getPosts().filter(
        Q(title__icontains = query) |
        Q(content__icontains = query),
    )

def getPostFile(id):
    return get_object_or_404(PostFile, pk=id)

##pages stuff
def getPages(showHidden=False):
    if showHidden is False:
        return Page.objects.all().filter(visible = True)
    else:
        return Page.objects.all()

def getPagesByCategory(catId, showHidden = False):
    return getPages().filter(category=catId)    

def getPagesByCategorySlug(slug, showHidden=False):
    return getPagesByCategory(getCategoryIdBySlug(slug), showHidden=showHidden)

def getPageIdBySlug(slug):
    return get_object_or_404(Page, slug__iexact=slug).id
    
def getPage(postId):
    if isinstance(postId, basestring):
        return Page.objects.get(id=getPageIdBySlug(postId))
    return Page.objects.get(id=postId)

def getPageBySlug(slug):
    return getPage(getPageIdBySlug(slug))

def getPagesByParentSlug(slug):
    return getPages().filter(parent__slug=slug)

##image stuff
try:
    from PIL import Image, ImageOps
except ImportError:
    import Image
    import ImageOps

def getImageHeight(path):
    image = Image.open(path)
    return image.size[1]
    
def getImageWidth(path):
    image = Image.open(path)
    return image.size[0]
    
def getThumbWidth(path, height):
    path = str(path)
    if not path.startswith(settings.MEDIA_ROOT) and not path.startswith(settings.STATIC_ROOT):
        path = settings.MEDIA_ROOT+path
    if not os.path.isfile(path):
        return 0
    image = Image.open(path)
    if image.size[1] < height:
        height = image.size[1]
    ratio = float(height)/float(image.size[1])
    return int(ratio*int(image.size[0]))
    
def getThumbHeight(path, width):
    path = str(path)
    if not path.startswith(settings.MEDIA_ROOT) and not path.startswith(settings.STATIC_ROOT):
        path = settings.MEDIA_ROOT+path
    if not os.path.isfile(path):
        return 0
    image = Image.open(path)
    if image.size[0] < width:
        width = image.size[0]
    ratio = float(width)/float(image.size[0])
    return int(ratio*int(image.size[1]))

def getThumbPath(path, imgWidth, imgHeight, width=None, height=None):
    #calculate image size
    offsetX = 0
    offsetY = 0
    widthNonCrop = 0
    heightNonCrop = 0
    
    if imgWidth < width:
        width = imgWidth
    
    if imgHeight < height:
        height = imgHeight
    
    if width is None or height is None:
        if width is None:
            width = int(height/float(imgHeight)*imgWidth)
            
        if height is None:
            height = int(width/float(imgWidth)*imgHeight)
    else:
        if imgWidth < imgHeight:
            heightNonCrop = int(width/float(imgWidth)*imgHeight)
            widthNonCrop = width
            offsetY = int((heightNonCrop-height)/2)
        else:
            widthNonCrop = int(height/float(imgHeight)*imgWidth)
            heightNonCrop = height
            offsetX = int((widthNonCrop-width)/2)
    
    #get correct file paths
    path = path.replace(settings.MEDIA_ROOT, "")
    thumbPath = settings.MEDIA_ROOT+"thumbs/"+path
    basename, extension = os.path.splitext(thumbPath)
    thumbPath = basename+"_"+str(width)+"x"+str(height)+".jpg"
    
    if hasattr(settings, "NO_THUMB_CACHING") and settings.NO_THUMB_CACHING == True:
        if os.path.exists(thumbPath):
            os.remove(thumbPath)
    
    #now check if the path exists and if not, create the image
    if not os.path.exists(thumbPath):
        folder = os.path.dirname(thumbPath)
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        if not path.startswith(settings.MEDIA_ROOT) and not path.startswith(settings.STATIC_ROOT):
            path = settings.MEDIA_ROOT+path
        
        quality = 83
        if hasattr(settings, "THUMB_QUALITY"):
            quality = int(settings.THUMB_QUALITY)
        
        if hasattr(settings, "USE_IMAGEMAGICK") and settings.USE_IMAGEMAGICK == True:
            #return "convert "+path+" -resize "+str(width)+"x"+str(height)+" "+thumbPath
            if offsetX != 0 or offsetY != 0:
                os.system("convert "+path+" -resize "+str(widthNonCrop)+"x"+str(heightNonCrop)+"! -crop "+str(width)+"x"+str(height)+"+"+str(offsetX)+"+"+str(offsetY)+" -quality "+str(quality)+" "+thumbPath)
            else:
                os.system("convert "+path+" -resize "+str(width)+"x"+str(height)+"! -quality "+str(quality)+" "+thumbPath)
        else:
            try:
                from PIL import Image, ImageOps
            except ImportError:
                import Image
                import ImageOps
            image = Image.open(path)
            if offsetX != 0 or offsetY != 0:
                image = image.resize((widthNonCrop, heightNonCrop), Image.ANTIALIAS)
                image = image.crop((offsetX, offsetY, offsetX+width, offsetY+height))
            else:
                image = image.resize((width, height), Image.ANTIALIAS)
            image.save(thumbPath, "JPEG", quality=quality)
    return thumbPath

    #return str(offsetY)
def getThumbUrl(path, imgWidth, imgHeight, width=None, height=None):
    return getThumbPath(path, imgWidth, imgHeight, width, height).replace(settings.MEDIA_ROOT, settings.MEDIA_URL)
    
    
################################################################################################################################
## BACKUP
## based on https://github.com/stbarnabas/django-backup/

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from tempfile import mkdtemp
import db
import tarfile
from datetime import datetime
from contextlib import closing

def sendBackup(email="philip@undef.ch"):
    ok = True
        
    #get db settings    
    if hasattr(settings, 'DATABASES'):
        database_list = settings.DATABASES
    else:
        # database details are in the old format, so convert to the new one
        database_list = {
            'default': {
                'ENGINE': settings.DATABASE_ENGINE,
                'NAME': settings.DATABASE_NAME,
                'USER': settings.DATABASE_USER,
                'PASSWORD': settings.DATABASE_PASSWORD,
                'HOST': settings.DATABASE_HOST,
                'PORT': settings.DATABASE_PORT,
            }
        }
    
    mediaRoot = settings.MEDIA_ROOT
    
    backupPath = mediaRoot+"backups/"
    if not os.path.exists(backupPath):
        os.makedirs(backupPath)
    
    archiveFile = backupPath+"backup-"+datetime.now().strftime("%m-%d-%Y")+".tgz"
    
    backup_root = mkdtemp()
    database_root = os.path.join(backup_root, 'databases')
    os.mkdir(database_root)
    
    for name, database in database_list.iteritems():
        db.backup(database, os.path.join(database_root, name))
    
    tf = tarfile.open(archiveFile, 'w:gz')
    tf.add(database_root, arcname="backup/databases")
    
    for post in Post.objects.all():
        for file in post.getFiles():
            if file.file:
                if file.type != filetypes["video"]:
                    tf.add(mediaRoot+file.file.path, arcname="backup/media/"+file.file.path)
        if post.preview:
            tf.add(mediaRoot+post.preview.path, arcname="backup/media/"+post.preview.path)
    
    for post in Page.objects.all():
        for file in post.getFiles():
            if file.file:
                if file.type != filetypes["video"]:
                    tf.add(mediaRoot+file.file.path, arcname="backup/media/"+file.file.path)
        if post.preview:
            tf.add(mediaRoot+post.preview.path, arcname="backup/media/"+post.preview.path)
    
    email = EmailMessage('Backup', 'Your backup is in the attachment. Only images that are attached to a post or page are included in the archive. Videos are not backuped.', 'undefcms@undef.ch', [email,])
    email.attach_file(archiveFile)
    if email.send() == False:
        ok = False
    
    return ok