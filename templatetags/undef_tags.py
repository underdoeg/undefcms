from django import template
from undefcms.utils import getThumbWidth, getThumbHeight, getImageWidth, getImageHeight

register = template.Library()

@register.simple_tag
def image_width(path):
    return getImageWidth(path)
    
@register.simple_tag
def image_height(path, height):
    return getImageHeight(path)

@register.simple_tag
def thumb_height(path, height):
    return getThumbHeight(path, height)
#register.tag(thumb_height)

@register.simple_tag 
def thumb_width(path, width):
    return getThumbWidth(path, width)
    
@register.filter
def thumbUrl(obj, widthHeight):
    split = widthHeight.split(",")
    return obj.thumbUrl(int(split[0]), int(split[1]))
    
@register.filter
def thumbUrlWidth(obj, w):
    return obj.thumbUrl(width=w)
    
@register.filter
def thumbUrlHeight(obj, h):
    return obj.thumbUrl(height=h)
    
@register.filter
def thumbHeight(obj, w):
    return obj.thumbHeight(w)

@register.filter
def thumbWidth(obj, h):
    return obj.thumbWidth(h)
#register.tag(thumb_width)