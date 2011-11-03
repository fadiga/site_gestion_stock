#!/usr/bin/env python
# -*- coding= UTF-8 -*-

from django import forms
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify


class NavigationForm(forms.Form):

    to_display = forms.ChoiceField()

    def __init__(self, label, choices, obj, url_name,
                    year, duration, duration_number):

        forms.Form.__init__(self)

        all_fields = self.fields.items()
        field_name, field_object = all_fields[0]
        field_object.label = label
        field_object.choices = choices
        field_object.initial = obj.id

        if duration:
            self.action_url = reverse(url_name,
                                     args=(obj.id,
                                           slugify(obj.name),
                                           year,
                                           duration,
                                           duration_number))
        else:
            self.action_url = reverse(url_name,
                                      args=(obj.id,
                                            slugify(obj.name),
                                            year))
