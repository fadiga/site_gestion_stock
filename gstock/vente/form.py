#! usr/bin/env python
# -*- coding= UTF-8 -*-
#maintenaire : Fadiga

from datetime import date, datetime

from django.db import models
from django import forms
from django.contrib.auth.models import User

from models import *


class MagasinForm(forms.ModelForm):

    class Meta:
        model = Magasin


class ProduitForm(forms.ModelForm):

    class Meta:
        model = Produit


class RapportForm(forms.ModelForm):

    class Meta:
        model = Rapport
        exclude = ['carton_remaining', 'piece_remaining', \
                    'auteur', 'date_saisie']

    def __init__(self, request, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.auteur = User.objects.get(pk=request.user.pk)

    def save(self, *args, **kwargs):
        self.instance.auteur = self.auteur
        return forms.ModelForm.save(self, *args, **kwargs)

    def clean_date(self):

        d = self.cleaned_data["date"]
        dt = datetime.now()
        date_ = datetime(d.year, d.month, d.day, dt.hour, \
                                dt.minute, dt.second, dt.microsecond)
        if date_ > datetime.now():
            error = u"la date de ce rapport est > à la date d'aujourd'hui"
            raise forms.ValidationError(error)
        try:
            last_rapport = Rapport.objects \
                                  .filter(magasins=self \
                                  .cleaned_data["magasins"], produit=self \
                                  .cleaned_data["produit"])\
                                  .order_by("-id")[0]
            if last_rapport.date > date_:
                error = u"la date de ce rapport est < à la date du \
                                                        denier rapport"
                raise forms.ValidationError(error)
        except IndexError:
            pass
        except KeyError:
            pass
        return date_

    def clean_type_r(self):
        type_r = self.cleaned_data["type_r"]
        return type_r

    def clean_nbr_carton(self):
        """
        """
        nbr_c = self.cleaned_data["nbr_carton"]
        if nbr_c < 0:
            error = u"le nombre de carton doit être supérieur à Zéro (0)"
            raise forms.ValidationError(error)
        return nbr_c


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label="Nom d'utilisateur")
    password = forms.CharField(max_length=30, label="Mot de passe",\
                               widget=forms.PasswordInput)


class rapport_periodiqueForm(forms.Form):
    date_debut = forms.DateField(label="Date debut")
    date_fin = forms.DateField(label="Date fin")


class AddOwner(forms.Form):

    def __init__(self, request, *args, **kwargs):
        super(AddOwner, self).__init__(*args, **kwargs)

    username = forms.CharField(max_length=100,\
                               label=("Nom d’utilisateur"))
    password = forms.CharField(max_length=100,\
                               label=("Mot de passe"),\
                               widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=100,\
                                            label=("Retapez le mot de \
                                                   passe"),\
                                            widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=100, label=("Nom"))
    last_name = forms.CharField(max_length=100, label=("Prénom"))
    email = forms.EmailField(label=("Email"), required=False)


class Owner_editForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(Owner_editForm, self).__init__(*args, **kwargs)

    username = forms.CharField(max_length=100,\
                               label=("Nom d’utilisateur"))
    password = forms.CharField(max_length=100,\
                               label=("Mot de passe"),\
                               widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=100,\
                                           label=("Retapez le \
                                           mot de passe"),\
                                           widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=100, label=("Nom"))
    last_name = forms.CharField(max_length=100, label=("Prénom"))
    email = forms.EmailField(label=("Email"), required=False)
    actif = forms.BooleanField(label=("Actif"), required=False)
