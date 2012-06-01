from models import *
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Q
import os.path

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