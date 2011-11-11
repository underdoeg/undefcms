from models import *
from django.shortcuts import get_object_or_404
from django.conf import settings

def getCategoriesRecursiveHelper(parent, activeId):
    if parent == None:
        set = Category.objects.filter(parent__isnull=True)
    else:
        set = Category.objects.filter(parent=parent.id)
    
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

def getPostsByCategory(catId):
    return getPosts().filter(category=catId)
    
def getPostsByCategorySlug(slug):
    return getPostsByCategory(getCategoryIdBySlug(slug))
    
def getPostIdBySlug(slug):
    return get_object_or_404(Post, slug__iexact=slug).id
    
def getPost(postId):
    return Post.objects.get(id=postId)

##pages stuff
def getPages():
    return Page.objects.all().filter(visible = True)

def getPagesByCategory(catId):
    return getPages().filter(category=catId)    

def getPagesByCategorySlug(slug):
    return getPagesByCategory(getCategoryIdBySlug(slug))

def getPageIdBySlug(slug):
    return get_object_or_404(Page, slug__iexact=slug).id
    
def getPage(postId):
    return Page.objects.get(id=postId)

def getPageBySlug(slug):
    return getPage(getPageIdBySlug(slug))

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