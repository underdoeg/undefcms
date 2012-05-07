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
