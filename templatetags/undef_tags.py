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
#register.tag(thumb_width)