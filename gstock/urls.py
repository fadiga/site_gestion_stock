# -*- coding: utf-8 -*-

import settings

from django.conf.urls.defaults import *
from django.contrib import admin

from settings import MEDIA_ROOT, DEBUG
admin.autodiscover()


urlpatterns = patterns('',

    url(r"^$", "vente.views.login", name="login"),
    url(r"^logout/$", 'vente.views.logout', name='logout'),
    url(r"^home$","vente.views.home", name="home"),
    url(r"^vente/", include("vente.urls")),
)
if DEBUG :
    urlpatterns += patterns('',

          # Permet de servir les fichiers statiques durant
          # le developpement. ex : css, js, images
          url(r'^static/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': MEDIA_ROOT, 'show_indexes': True}),

          # Permet l'export des données en fixture
          # 'smuggler' doit se trouver en premier
          url(r'^admin/', include('smuggler.urls')),
    )

# Inclusion de l'admin en dernier car on doit l'inclure après
# smuggler
urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
