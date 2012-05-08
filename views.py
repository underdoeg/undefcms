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

################################################################################################################################

import os

try:
    from PIL import Image, ImageOps
except ImportError:
    import Image
    import ImageOps

def thumb(request, w=-1, h=-1, path=""):
    
    if path == "":
        path = settings.STATIC_ROOT+"img/image_not_found.jpg"
    else:
        if not path.startswith(settings.MEDIA_ROOT) and not path.startswith(settings.STATIC_ROOT):
            path = settings.MEDIA_ROOT+path
    
    if os.path.exists(path) == False:
        path = settings.STATIC_ROOT+"img/image_not_found.jpg"
    
    thumbPath = settings.MEDIA_ROOT+"thumbs/"
    
    #load the image and resize
    image = Image.open(path)
    
    if int(w) > image.size[0]:
        w = image.size[0]
    
    if int(h) > image.size[1]:
        h = image.size[1] 
    
    if h == -1:
        ratio = float(w)/float(image.size[0])
        h = int(ratio*int(image.size[1]))
    if w == -1:
        ratio = float(h)/float(image.size[1])
        w = int(ratio*int(image.size[0]))

    if int(w) == image.size[0] and int(h) == image.size[1]:
        path = path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL, 1)
        path = path.replace(settings.STATIC_ROOT, settings.STATIC_URL, 1)
        return redirect(path)
    
    basename, extension = os.path.splitext(os.path.basename(path))
    filename = thumbPath+basename+"_"+str(w)+"x"+str(h)+".jpg"
    
    if os.path.exists(filename) == False:
        imagefit = ImageOps.fit(image, (int(w), int(h)), Image.ANTIALIAS)
        imagefit.save(filename, 'JPEG', quality=88)
    
    return redirect(settings.MEDIA_URL+"thumbs/"+basename+"_"+str(w)+"x"+str(h)+".jpg")