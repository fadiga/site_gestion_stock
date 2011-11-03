# -*- coding: utf-8 -*-
#maintainer: FAd


from django.conf.urls.defaults import *


urlpatterns = patterns('',

    url(r"^add_owner/$", "vente.views.add_owner", name="add_owner"),
    url(r"^owner/$", "vente.views.owner", name="owner"),
    url(r"^owner_edit/(?P<id>\d+)$", "vente.views.owner_edit",\
                                    name="owner_edit"),
    url(r"^dashboard$", "vente.views.dashboard", name="v-dashboard"),
    url(r"^produit$", "vente.views.produit", name="produit"),
    url(r"^magsin$", "vente.views.magasin", name="magasin"),
    url(r"^gestion-rapport/(?P<num>\d+)*$", "vente.views.gestion_rapports", \
                                                        name="g-rapport"),
    # Tout les rapports
    url(r'^tous-rapports/(?:(?P<year>\d{4})/(?:(?P<duration>(?:month|week))/(?:(?P<duration_number>\d{1,2})/)*)*)*$',
          'vente.views.tous_rapports', name="stock-all"),
    # Produits
    url(r'^par-produits/(?P<id>\d+)/(?:(?P<magasin_name_slug>[a-z0-9\-]+)/(?:(?P<year>\d{4})/(?:(?P<duration>(?:month|week))/(?:(?P<duration_number>\d{1,2})/)*)*)*)*$',
         "vente.views.par_produits", name="par-produits"),
    # Magasins
    url(r'^par-magasins/(?P<id>\d+)/(?:(?P<product_name_slug>[a-z0-9\-]+)/(?:(?P<year>\d{4})/(?:(?P<duration>(?:month|week))/(?:(?P<duration_number>\d{1,2})/)*)*)*)*$',
           "vente.views.par_magasins", name="par-magasins"),
    # Suppression
    url(r"^delete/(?P<num>\d+)*$", 'vente.views.deleting', name="delete"),
    url(r"^delete_confirm/(?P<num>\d+)$", "vente.views.delete_confirm",
        name="delete-confirm"),
    # rapport_periodique
    url(r"^rapport-periodique/$", "vente.views.rapport_periodique", \
        name="rapport_periodique"),
    url(r"^inventaire/$", "vente.views.inventaire", name="invent"),
    url(r"^commande/$", "vente.views.commande", name="commande"),
    url(r'^export/excel/$', \
        "vente.views.export_excel", name='export_excel'),

)
