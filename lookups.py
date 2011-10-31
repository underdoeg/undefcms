from undefcms.models import Image
from django.db.models import Q
from django.conf import settings
'''
class ImageLookup(object):

    def get_query(self,q,request):
        """ return a query set.  you also have access to request.user if needed """
        return Image.objects.filter(Q(name__icontains=q))

    def format_result(self,image):
        """ the search results display in the dropdown menu.  may contain html and multiple-lines. will remove any |  """
        return u"%s" % ("<img src='"+settings.MEDIA_URL+"images/"+str(image.file)+"' alt=''>&nbsp;&nbsp;"+image.name)

    def format_item(self,image):
        """ the display of a currently selected object in the area below the search box. html is OK """
        return u"%s" % ("<img src='"+settings.MEDIA_URL+"images/"+str(image.file)+"' alt=''>&nbsp;&nbsp;"+image.name)

    def get_objects(self,ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        return Image.objects.filter(pk__in=ids).order_by('name')
'''