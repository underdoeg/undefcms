# Create your views here.
from django.http import HttpResponse
from django.conf import settings
from django.core.servers.basehttp import FileWrapper

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
        path = settings.MEDIA_ROOT+path
    
    if os.path.exists(path) == False:
        path = settings.STATIC_ROOT+"img/image_not_found.jpg"
    
    thumbPath = settings.MEDIA_ROOT+"thumbs/"
    
    #load the image and resize
    image = Image.open(path)
    if h == -1:
        ratio = float(w)/float(image.size[0])
        h = int(ratio*int(image.size[1]))
    if w == -1:
        ratio = float(h)/float(image.size[1])
        w = int(ratio*int(image.size[0]))

    if int(w) == image.size[0] and int(h) == image.size[1]:
        return HttpResponse(open(path), mimetype="image/png")
    
    basename, extension = os.path.splitext(os.path.basename(path))
    filename = thumbPath+basename+"_"+str(w)+"x"+str(h)+".png"
    
    if os.path.exists(filename) == False:
        imagefit = ImageOps.fit(image, (int(w), int(h)), Image.ANTIALIAS)
        imagefit.save(filename, 'PNG', quality=80)
    data = open(filename, "rb").read()
    return HttpResponse(data, mimetype="image/png")
    '''
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='image/png')
    response['Content-Length'] = os.path.getsize(filename)
    return response
    '''