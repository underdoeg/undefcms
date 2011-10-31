from django import template
from undefcms.utils import getThumbWidth, getThumbHeight

register = template.Library()

@register.simple_tag
def thumb_height(path, height):
    return getThumbHeight(path, height)
#register.tag(thumb_height)

@register.simple_tag 
def thumb_width(path, width):
    return getThumbWidth(path, width)
#register.tag(thumb_width)