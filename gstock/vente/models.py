#!/usr/bin/env python
# -*- coding= UTF-8 -*-
#maintainer: FAd

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from lib.tools import get_week_boundaries


class Produit(models.Model):
    """ """
    name = models.CharField(max_length=100,
                                    verbose_name=u"Produit", unique=True)
    qtte = models.IntegerField(verbose_name=u"Nbre de piece pour un carton")

    def __unicode__(self):
        return u"%s %s" % (self.name, self.qtte)


class Magasin(models.Model):
    """ """
    name = models.CharField(max_length=100,\
                            verbose_name=u"Nom du magasin", unique=True)
    adresse = models.CharField(max_length=100, verbose_name=u"Adresse",\
                                                            blank=True)

    def __unicode__(self):
        return u"%s %s" % (self.name, self.adresse)


class Rapport(models.Model):
    """ """
    N = ""
    E = "e"
    S = "s"
    Type_op = ((N, "----"), (E, "Entrer"), (S, "Sortie"))
    auteur = models.ForeignKey(User, related_name='auteur', \
                                verbose_name=("Utilisateur"))
    date_saisie = models.DateTimeField(verbose_name=u"Date creation", \
                                                 default=datetime.now())
    magasins = models.ForeignKey(Magasin, verbose_name=u"Magasin")
    produit = models.ForeignKey(Produit, verbose_name=u"Produit")
    nbr_carton = models.IntegerField(verbose_name=u"Nbre Carton")
    carton_remaining = models.\
                 IntegerField(verbose_name=u"Carton restant", default=0)
    piece_remaining = models.\
                  IntegerField(verbose_name=u"Piece Restant", default=0)
    date = models.DateTimeField(u"Date")
    type_r = models.CharField(max_length=30, verbose_name=(u"Type"),\
                                             choices=Type_op, default=N)

    @classmethod
    def get_reports_filtered_by_duration(cls, year, duration, \
                                                     duration_quantity):
        """
            Retourne un queryset de rapports filtre selon la date

            obtenue a travers l'url.
            Cela permet donc d'avoir tous les rapports pour une annee
            et optionnellement pour un mois ou une semaine de cette
            annee.
        """
        reports = Rapport.objects.filter(date__year=year)
        if duration == "month":
            reports = reports.filter(date__month=duration_quantity)
        if duration == "week":
            first_day, last_day = get_week_boundaries(year, \
                                                      duration_quantity)
            reports = reports.filter(date__gte=first_day, \
                                                     date__lte=last_day)
        return reports

    def save(self):
        """
        Calcul du restant en stock après un mouvement.
        """
        # Recupration de tous les reports filtrer par produit et
        # par magasin puis ordonée par date.
        last_reports = Rapport.objects.filter(produit__name=self \
                                      .produit.name, magasins__name=self \
                                      .magasins.name, date__lt=self.date) \
                                      .order_by('-date')
        # On permet le qui a été  le produit
        produit = Produit.objects.get(name=self.produit.name)
        # Condition qui determine si il ya ou pas un restant de stock et
        # sauvegarde dans la base le restant actuelle après l'avoir calculé.
        previous_remaining_c = 0
        self.carton_remaining = 0
        self.piece_remaining = 0
        if last_reports:
            previous_remaining_c = last_reports[0].carton_remaining
            if self.type_r == "e":
                self.carton_remaining = previous_remaining_c + self.nbr_carton
                self.piece_remaining = self.carton_remaining * produit.qtte
            if self.type_r == "s":
                self.carton_remaining = previous_remaining_c - self.nbr_carton
                self.piece_remaining = self.carton_remaining * produit.qtte
        else:
            self.carton_remaining = self.nbr_carton
            self.piece_remaining = self.carton_remaining * produit.qtte

        super(Rapport, self).save()
        # on recupere tous les enregistrements suivant
        next_reports = Rapport.objects \
                              .filter(produit__name=self.produit.name, \
                                      magasins__name=self.magasins.name, \
                                      date__gt=self.date).order_by('date')
        #~ import pdb; pdb.set_trace()
        # on met a jour le premier d'entre eux
        # comme il va faire de meme, cela va tous les mettre a jour
        if next_reports:
            next_reports[0].save()

    def __unicode__(self):
        return u"%s %s  %d %d %s %s %s" % (self.magasins.name, \
                                              self.produit.name, \
                                              self.produit.qtte, \
                                              self.nbr_carton, self.date, \
                                              self.type_r, self.auteur)
