#!/usr/bin/env python
# -*- coding= UTF-8 -*-

"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from django.test.client import Client
from django.contrib.auth import (authenticate, login as django_login,
                                 logout as django_logout)

from django.test import TestCase
from django.core.urlresolvers import reverse


class SimpleTest(TestCase):
    """
    Tests of ``blog`` application.
    """
    fixtures = ['test_data']

    def test_login(self):
        self.logged_admin = Client()
        logged_admin = self.logged_admin.login(username='admin',\
                                               password='admin')
        self.assertTrue(logged_admin)

    def test_dashboard(self):
        """ Je teste la view dashboard"""
        response = self.client.get(reverse(v-dashboard)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'vente/dashboard.html')

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)


#~ __test__ = {"doctest": """
#~ Another way to test that 1 + 1 is equal to 2.
#~
#~ >>> 1 + 1 == 2
#~ True
#~ """}
