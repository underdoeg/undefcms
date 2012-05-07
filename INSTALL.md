# INSTALL INSTRUCTIONS
+ create a new django project

		django-admin startproject projectname
+ create a new application in your project. 

		cd to project & python manage.py startapp sitename
+ download undefcms into your project folder

		git clone git@github.com:underdoeg/undef-cms.git
+ add undefcms to your installed apps

+ enable django-admin

+ download and add the following libraries to installed apps:

	+ django-taggit https://github.com/sehmaschine/django-grappelli
	+ django-filebrowser https://github.com/sehmaschine/django-filebrowser
	+ django-taggit-autocomplete-modified https://bitbucket.org/gnotaras/django-taggit-autocomplete-modified/overview

+ add the undefcms url patterns to urls.py (this will also add the url patterns for the above apps)

		from django.conf.urls.defaults import patterns, include, url
		import undefcms.urls
		import settings
		from django.contrib import admin
		from django.contrib.staticfiles.urls import staticfiles_urlpatterns
		
		admin.autodiscover()
		
		urlpatterns = patterns('',
		    url(r'^admin/', include(admin.site.urls)),
		    url(r'^cms/', include(undefcms.urls))
		)
		
		
		urlpatterns += staticfiles_urlpatterns()
		
		if settings.DEBUG:
		    from django.views.static import serve
		    _media_url = settings.MEDIA_URL
		    if _media_url.startswith('/'):
		        _media_url = _media_url[1:]
		        urlpatterns += patterns('',
		            (r'^%s(?P<path>.*)$' % _media_url,
		            serve,
		            {'document_root': settings.MEDIA_ROOT}))
		    del(_media_url, serve)

+ fill in your DB and path setting then python manage.py syncdb && manage.py collectstatic
+ create a folder uploads/, thumbs/ and uploads/images in your MEDIA folder
+ run the server and insert your content in the admin page