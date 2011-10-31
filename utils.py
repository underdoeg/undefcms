from models import *
from django.shortcuts import get_object_or_404
from django.conf import settings

def getCategories(slug = "", id = -1):
    ret =  Category.objects.all()
    for c in ret:
        if id != -1 and c.id == active:
            c.active = True
        if slug != "" and c.slug == slug:
            c.active = True
        else:
            c.active = False
    return ret
    
def getCategoryIdBySlug(catSlug):
    return get_object_or_404(Category, slug__iexact=catSlug).id

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

def getPostsByCategory(catId):
    return getPosts().filter(category=catId)
    
def getPostsByCategorySlug(slug):
    return getPostsByCategory(getCategoryIdBySlug(slug))
    
def getPostIdBySlug(slug):
    return get_object_or_404(Post, slug__iexact=slug).id
    
def getPost(postId):
    return Post.objects.get(id=postId)
    
##image stuff
try:
    from PIL import Image, ImageOps
except ImportError:
    import Image
    import ImageOps

def getThumbWidth(path, height):
    image = Image.open(path)
    ratio = float(height)/float(image.size[1])
    return int(ratio*int(image.size[0]))
    
def getThumbHeight(path, width):
    image = Image.open(path)
    ratio = float(width)/float(image.size[0])
    return int(ratio*int(image.size[1]))