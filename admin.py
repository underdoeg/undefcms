from undefcms.models import *
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django import forms
from django.db import models
from forms import ContentForm, FileForm
#from ajax_select.admin import AjaxSelectAdmin
from datetime import datetime
from django.conf import settings
from types import filetypes

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'visible', 'index')
    list_filter = ('visible', 'parent')
    search_fields = ('name','description')
    prepopulated_fields = {"slug": ("name",)}
    
    list_editable = ('index',)  # 'position' is the name of the model field which holds the position of an element


class ContentAdmin(admin.ModelAdmin):
    form = ContentForm
    list_display = ('the_preview', 'title', 'the_categories', 'the_tags', 'creation', 'visible')
    list_filter = ('category', 'creation', 'last_edit', 'visible')
    search_fields = ('title','content', 'tags', 'category')
    list_display_links = ('the_preview', 'title')
    
    prepopulated_fields = {"slug": ("title",)}
    #fields = ('title', 'slug')
    
    fieldsets = (
        ('title & infos',{
            #'classes': ('collapse open',),
            'fields': (('title', 'slug','visible'), ('preview', 'creation'), ('category', 'tags'))
        }),
        ('content', {
            'classes': ('collapse closed',),
            'fields':  ('content', 'description'),
        }),
        ('header', {
            'classes': ('collapse closed',),
            'fields' : ('header','javascript','css',),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if obj.creation == None:
            obj.creation = datetime.now()
        obj.save()
        
    def the_tags(self, obj):
        ret = ""
        for t in obj.tags.all():
            ret += t.name+", "
            
        return ret
    
    def the_categories(self, obj):
        ret = ""
        for t in obj.category.all():
            ret += t.name+", "
            
        return ret
        
    def the_preview(self, obj):
        if obj.preview:
            return  '<img src="/cms/thumb/60/60/'+str(obj.preview.path)+'" />'
        else:
            return '<img src="/cms/thumb/60/60/hh" />'
        
    class Media:
        js = [
            settings.STATIC_URL+'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            settings.STATIC_URL+'js/tinymce_setup.js',
        ]
    
    the_preview.allow_tags = True
    the_preview.short_description = "Preview"


class StackedFileInline(InlineModelAdmin):
    template = 'admin/edit_inline/tabular.html'
    
    sortable_field_name = 'index'
    extra = 0
    ordering = ['index']
    classes = ('collapse open',)
    form = FileForm
    fields = ('name','description', 'file', 'type', 'index')
    
class FilePostInline(StackedFileInline):
    model = PostFile   

class PostAdmin(ContentAdmin):
    inlines = (FilePostInline, )

class FilePageInline(StackedFileInline):
    model = PageFile

class PageAdmin(ContentAdmin):
    '''
    def __init__(self, model, admin_site):
        ContentAdmin.fieldsets[0][1]["fields"] = ContentAdmin.fieldsets[0][1]["fields"][0:3]+ ("parent",) + ContentAdmin.fieldsets[0][1]["fields"][3:]
        ContentAdmin.__init__(self, model, admin_site)    
        logger.error(str(self.fieldsets[0][1]["fields"]))
    '''
    fieldsets = (
        ('title & infos',{
            #'classes': ('collapse open',),
            'fields': (('title', 'slug','visible'), ('preview', 'creation', 'index'), ('parent', 'category', 'tags'))
        }),
        ('content', {
            'classes': ('collapse closed',),
            'fields':  ('content', 'description'),
        }),
        ('header', {
            'classes': ('collapse closed',),
            'fields' : ('header','javascript','css',),
        }),
    )
    sortable_field_name = 'index'
    ordering = ['index']
    inlines = (FilePageInline, )

    
    list_display = ('the_preview', 'title', 'the_categories', 'the_tags', 'creation', 'visible', 'index')
    list_display_links = ('the_preview', 'title',)
    
    list_editable = ('index',)  # 'position' is the name of the model field which holds the position of an element
    
    class Media:
        js = (
            #'js/admin_list_reorder.js',
        )
    
    

class FileAdmin(admin.ModelAdmin):
    list_display = ('the_preview', 'name', 'type')
    list_filter = ('type',)
    
    form = FileForm

    
    def the_preview(self, obj):
        if obj.type == filetypes["image"]:
           return  '<img src="/cms/thumb/60/60/'+str(obj.file.path_relative)+'" />'#'<img src="%s" />' % obj.preview.version_generate("admin_thumbnail").url
        else:
            return '<img src="/cms/thumb/60/60/hh" />'
    
    the_preview.allow_tags = True


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PageFile, FileAdmin)
admin.site.register(PostFile, FileAdmin)
admin.site.register(Page, PageAdmin)