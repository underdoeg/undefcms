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

	+ django-grappelli https://github.com/sehmaschine/django-grappelli
	+ django-filebrowser https://github.com/sehmaschine/django-filebrowser
	+ django-taggit-autocomplete-modified https://bitbucket.org/gnotaras/django-taggit-autocomplete-modified/overview

+ add the undefcms url patterns to urls.py

		from django.conf.urls.defaults import patterns, include, url
		import undefcms.urls
		from django.contrib import admin
		admin.autodiscover()

		urlpatterns = patterns('',
			url(r'^admin/', include(admin.site.urls)),
			#your urls
		)
		urlpatterns += undefcms.urls.urlpatterns

+ fill in your DB and path setting then python manage.py syncdb && manage.py collectstatic
+ run the server and insert your content in the admin page