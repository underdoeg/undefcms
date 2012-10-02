# coding: utf-8

# DJANGO IMPORTS
from django.conf.urls.defaults import *
from django.conf import settings
from filebrowser.sites import site


urlpatterns = patterns('',
    
    #thumbs
    url(r'^thumb/(?P<w>\d+)/(?P<h>\d+)/(?P<path>.*)', 'undefcms.views.thumb'),
    url(r'^thumb/(?P<w>\d+)/(?P<path>.*)', 'undefcms.views.thumb'),
    url(r'^thumb/h/(?P<h>\d+)/(?P<path>.*)', 'undefcms.views.thumb'),
    
    #post
    url(r'^$', 'undefcms.views.posts', name='index'),
    url(r'^posts/$', 'undefcms.views.posts', name='posts'),
    url(r'^posts/(?P<category>.*)$', 'undefcms.views.posts', name='postCategory'),   
    url(r'^post/(?P<slug>.*)$', 'undefcms.views.post', name='post'),
    
    #page
    url(r'^pages/$', 'undefcms.views.pages', name='pages'),
    url(r'^pages/(?P<category>.*)$', 'undefcms.views.pages', name='pageCategory'),   
    url(r'^page/(?P<slug>.*)$', 'undefcms.views.page', name='page'),
    
    #backup
    url(r'^backup/(?P<email>.*)', 'undefcms.views.backup', name='backup')
)

urlpatterns += patterns('',
   url(r'^admin/filebrowser/', include(site.urls)),
)

urlpatterns += patterns('',
    (r'^grappelli/', include('grappelli.urls')),
)
