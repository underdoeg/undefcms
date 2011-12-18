from django.template import loader
from django.http import HttpResponse
from django.template import RequestContext
from django.core.files import File
from django.conf import settings
from django.template.defaultfilters import slugify

from BeautifulSoup import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import os
import sys

from undefcms.models import *
from filebrowser.base import FileObject

import unicodedata

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetRecentPosts, NewPost
from wordpress_xmlrpc.methods.categories import GetCategories
from wordpress_xmlrpc.methods.users import GetUserInfo

def wpimport(request, url, user, password):
    
    #make dir for wp uploads
    uploadDirRel = "uploads/images/wp-import/"
    uploadDir = settings.MEDIA_ROOT+uploadDirRel
    if not os.path.exists(uploadDir):
        os.makedirs(uploadDir)
    
    t = loader.get_template('wp-import.html')
    c = {}
    
    ret = ""
    wp = Client(url, user, password)
    
    #get all categories
    categories = wp.call(GetCategories())
    for cat in categories:
        catName = cat.name
        category, created = Category.objects.get_or_create(name=catName, slug=slugify(catName))
        pass
    
    #get all the posts
    posts = wp.call(GetRecentPosts(1))
    c["posts"] = posts
    for p in posts:
        if not hasattr(p, 'slug'):
            p.slug = ""
        if not hasattr(p, 'description'):
            p.description = ""
        post, created = Post.objects.get_or_create(slug=p.slug, creation = p.date_created)
        post.visible = True
        post.title = p.title
        p.description = p.description.replace('\n','<br />')
        
        
        #extract the images
        soup = bs(p.description)
        parsed = list(urlparse.urlparse(url))
        out_folder = uploadDir
        curImg = 0
        for image in soup.findAll("img"):
            filename = image["src"].split("/")[-1]
            parsed[2] = image["src"]
            outpath = os.path.join(out_folder, filename)
            #return HttpResponse(outpath)
            if image["src"].lower().startswith("http"):
                urlretrieve(image["src"], outpath)
            else:
                urlretrieve(urlparse.urlunparse(parsed), outpath)
            
            image.extract()
            
            #add image to post
            fileObj = FileObject(uploadDirRel+filename)

            file, created = PostFile.objects.get_or_create(file = fileObj, post=post, index=curImg)
            #file = PostFile.objects.create(file = fileObj, post=post, index=curImg)
            file.save()
                
            #check if the image is the preview image
            if curImg is 0:
                post.preview = fileObj
            
            curImg+=1
        
        post.content = str(soup)
        
        #add the categories
        if not hasattr(p, 'categories'):
            p.categories = []
        for c in p.categories:
            #return HttpResponse(c)
            post.category.add(Category.objects.get_or_create(name=c)[0])
        
        #add the tags
        if not hasattr(p, 'tags'):
            p.tags = []
         
        for t in p.tags:
            post.tags.add(t)
        
        post.save()
                
    return HttpResponse(t.render(RequestContext(request, c)))
