from undefcms.models import *
from django.contrib import admin
from django import forms
from django.db import models
from forms import ContentForm
#from ajax_select.admin import AjaxSelectAdmin
from datetime import datetime
from django.conf import settings

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class ContentAdmin(admin.ModelAdmin):
    form = ContentForm
    list_display = ('the_preview', 'title', 'the_categories', 'the_tags', 'creation', 'visible')
    list_filter = ('category', 'creation', 'last_edit', 'visible')
    search_fields = ('title','content', 'tags', 'category')
    
    prepopulated_fields = {"slug": ("title",)}
    #fields = ('title', 'slug')
    
    fieldsets = (
        (None, {
            'fields': (('title', 'slug'), ('preview', 'visible'), 'category', 'creation', 'content', 'description'),
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
        if obj.preview and obj.preview.filetype == "Image":
           return  '<img src="/thumb/60/60/uploads/images/'+str(obj.preview)+'" />'#'<img src="%s" />' % obj.preview.version_generate("admin_thumbnail").url
        else:
            return '<img src="/thumb/60/60/hh" />'
        
    class Media:
        js = [
            settings.STATIC_URL+'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            settings.STATIC_URL+'js/tinymce_setup.js',
        ]
    
    the_preview.allow_tags = True
    the_preview.short_description = "Preview"

class FilePostInline(admin.TabularInline):
    model = PostFile
    sortable_field_name = 'index'
    extra = 0
    ordering = ['index']

class PostAdmin(ContentAdmin):
    inlines = (FilePostInline, )

class FilePageInline(admin.TabularInline):
    model = PageFile
    sortable_field_name = 'index'
    extra = 0
    ordering = ['index']

class PageAdmin(ContentAdmin):
    '''
    def __init__(self, model, admin_site):
        ContentAdmin.fieldsets[0][1]["fields"] = ContentAdmin.fieldsets[0][1]["fields"][0:3]+ ("parent",) + ContentAdmin.fieldsets[0][1]["fields"][3:]
        ContentAdmin.__init__(self, model, admin_site)    
        logger.error(str(self.fieldsets[0][1]["fields"]))
    '''
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'preview', 'parent', 'category', 'creation', 'visible', 'content', 'description'),
        }),
        ('header', {
            'classes': ('collapse closed',),
            'fields' : ('header','javascript','css',),
        }),
    )
    inlines = (FilePageInline, )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PageFile)
admin.site.register(PostFile)
admin.site.register(Page, PageAdmin)