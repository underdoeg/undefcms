# Create your views here.
from django.template import RequestContext, loader, Context
from django.http import HttpResponse
from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import redirect

from models import *
from utils import *

templatePath = "undefcms/"
'''
if hasattr(settings, 'CMS_TEMPLATE_PATH'):
    templatePath = settings.CMS_TEMPLATE_PATH
'''

def posts(request, category=None):
    t = loader.get_template(templatePath+'posts.html')
    c = {}
    if category is None:
        c["posts"] = getPosts()
    else:
        c["posts"] = getPostsByCategorySlug(category)

    c["pages"] = getPages()
    c["categories"] = getCategories()
    c["activeCategory"] = category;
    c["area"] = "posts"
    return HttpResponse(t.render(RequestContext(request, c)))
    
def post(request, slug):
    t = loader.get_template(templatePath+'post.html')
    c = {}
    c["post"] = getPostBySlug(slug)
    c["pages"] = getPages()
    c["categories"] = getCategories()
    c["area"] = "posts"
    
    filesTemplate = loader.get_template(templatePath+"files.html")
    c["files"] = filesTemplate.render(RequestContext(request, {'files':c['post'].postfile_set.all()}))
    
    return HttpResponse(t.render(RequestContext(request, c)))
    
def pages(request, category=None):
    t = loader.get_template(templatePath+'pages.html')
    c = {}
    c["pages"] = getPages()
    c["categories"] = getCategories()
    c["area"] = "pages"
    return HttpResponse(t.render(RequestContext(request, c)))

def page(request, slug):
    t = loader.get_template(templatePath+'page.html')
    c = {}
    c["page"] = getPageBySlug(slug)
    c["categories"] = getCategories()
    c["area"] = "pages"
    c["pages"] = getPages()
    
    filesTemplate = loader.get_template(templatePath+"files.html")
    c["files"] = filesTemplate.render(RequestContext(request, {'files':c['page'].pagefile_set.all()}))
    
    return HttpResponse(t.render(RequestContext(request, c)))

def backup(request, email):
    if sendBackup(email, request.META['HTTP_HOST']) == True:
        return HttpResponse("backup sent to "+email)
    else:
        return HttpResponse("could not send backup to "+email)

################################################################################################################################

import os

try:
    from PIL import Image, ImageOps
except ImportError:
    import Image
    import ImageOps

def thumb(request, w=None, h=None, path=""):
    if path == "":
        path = settings.STATIC_ROOT+"img/image_not_found.jpg"
    if not path.startswith(settings.MEDIA_ROOT) and not path.startswith(settings.STATIC_ROOT):
        path = settings.MEDIA_ROOT+path
    image = Image.open(path)
    if h != None:
        h = int(h)
    if w != None:
        w = int(w)
    return redirect(getThumbUrl(path, image.size[0], image.size[1], w, h))
    

    