from undefcms.models import *
from django.contrib import admin
from django import forms
from django.db import models
from forms import ContentForm
from ajax_select.admin import AjaxSelectAdmin
from datetime import datetime
from django.conf import settings

    
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class ContentAdmin(AjaxSelectAdmin):
    form = ContentForm
    list_display = ('the_preview', 'title', 'the_categories', 'the_tags', 'creation', 'visible')
    list_filter = ('category', 'creation', 'last_edit', 'visible')
    search_fields = ('title','content', 'tags', 'category')
    
    prepopulated_fields = {"slug": ("title",)}
    #fields = ('title', 'slug')
    
    
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
    inlines = (FilePageInline, )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PageFile)
admin.site.register(PostFile)
admin.site.register(Page, PageAdmin)