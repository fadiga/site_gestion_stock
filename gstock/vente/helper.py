#!/usr/bin/env python
# -*- coding: utf-8 -*-
#maintainer: FAd

from models import *


def produit_signaler():
    # Verification des valeurs d"alerte"
    liste_alert = []
    magasins = Magasin.objects.all()
    produits = Produit.objects.all()
    for prod in produits:
        for mag in magasins:
            try:
                rapp = Rapport.objects.\
                filter(produit__name=prod.name,\
                        magasins__name=mag.name).order_by("-date")[0]
                if rapp.carton_remaining < 100:
                    liste_alert.append(rapp)
            except:
                pass
    return liste_alert
