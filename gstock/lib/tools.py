
#!usr/bin/env python
# -*- coding: utf-8 -*-
#maintainer: Fad
from datetime import date, timedelta
from calendar import monthrange


def get_week_boundaries(year, week):
    """
        Retoure les date du premier et du dernier jour de la semaine dont
        on a le numéro.
    """
    d = date(year, 1, 1)
    if(d.weekday() > 3):
        d = d + timedelta(7 - d.weekday())
    else:
        d = d - timedelta(d.weekday())

    dlt = timedelta(days=(week - 1) * 7)
    return d + dlt, d + dlt + timedelta(days=6)


def get_time_pagination(year, duration, duration_number):
    """
    navigation entre les dates année, mois, week """

    todays_date_is_before = False
    todays_date_is_after = False

    # la date du jour
    todays_date = date.today()

    if duration == "week":
        # on recupere le premier jour
        current_date = get_week_boundaries(year, duration_number)[0]

        # la date de la semaine avant celle qu'on affiche
        delta = timedelta(7)
        previous_date = current_date - delta
        previous_week_number = previous_date.isocalendar()[1]

        # la date de la semaine après celle qu'on affiche
        next_date = current_date + delta
        next_week_number = next_date.isocalendar()[1]

        # la date de la semaine avant celle qu'on affiche
        two_dates_ago = current_date - (delta * 2)

        # la date de la semaine avant celle qu'on affiche
        in_two_dates = current_date + (delta * 2)

        # Vérification que la semaine d'aujourd'hui est à afficher ou non
        if todays_date <= two_dates_ago:
            todays_date_is_before = True

        if todays_date >= in_two_dates:
            todays_date_is_after = True

        # l'adresse pour afficher l'année d'aujourd'hui
        todays_date_url = reverse(url,
                                   args=additional_args + (todays_date.year,
                                        duration,
                                        todays_date.isocalendar()[1]))

        # l'adresse pour afficher le mois précédent
        previous_date_url = reverse(url,
                                     args=additional_args + \
                                     (previous_date.year, duration, \
                                                   previous_week_number))

        # l'adresse pour afficher le mois suivant
        next_date_url = reverse(url,
                                 args=additional_args + (next_date.year,
                                       duration,
                                       next_week_number))

        # formatage de l'affichage des mois
        current_date_ = current_date
        previous_date_ = previous_date
        next_date_ = next_date
        todays_date = u"Cette semaine"

    elif duration == "month":

        current_date = date(year, duration_number, 1)

         # la date du mois avant celui qu'on affiche
        delta = timedelta(1)
        previous_date = current_date - delta
        previous_date = date(previous_date.year, previous_date.month, 1)

        # la date du mois après celui qu'on affiche
        days_count = monthrange(current_date.year, current_date.month)[1]
        delta = timedelta(days_count + 1)
        next_date = current_date + delta

        # Vérification que la semaine d'aujourd'hui est à afficher ou non
        if todays_date < previous_date:
            todays_date_is_before = True

        if todays_date > next_date:
            todays_date_is_after = True

        # l'adresse pour afficher le mois d'ajourd'hui
        todays_date_url = reverse(url,
                                  args=additional_args + (todays_date.year,
                                        duration,
                                        todays_date.month))


        # l'adresse pour afficher le mois précédent
        previous_date_url = reverse(url,
                                     args=additional_args + \
                                     (previous_date.year, duration, \
                                                    previous_date.month))

        # l'adresse pour afficher le mois suivant
        next_date_url = reverse(url,
                                 args=additional_args + (next_date.year,
                                       duration,
                                       next_date.month))

        # formatage de l'affichage des mois en tenant compte de la
        #language code
        current_date_ = current_date
        previous_date_ = previous_date
        next_date_ = next_date
        todays_date = u"Ce mois ci"

    else:

        current_date = date(year, 1, 1)

         # la date de l'année avant celle qu'on affiche
        previous_date = date(current_date.year - 1,
                             current_date.month,
                             current_date.day)

        # la date de l'année après celle qu'on affiche
        next_date = date(current_date.year + 1,
                             current_date.month,
                             current_date.day)

        # Vérification que l'année d'aujourd'hui est à afficher ou non
        if todays_date.year < (current_date.year - 1):
            todays_date_is_before = True

        if todays_date.year > (current_date.year + 1):
            todays_date_is_after = True

        # l'adresse pour afficher l'année d'aujourd'hui
        todays_date_url = reverse(url,
                                  args=additional_args + \
                                            (todays_date.year,))

        # l'adresse pour afficher l'année précédent
        previous_date_url = reverse(url,
                                    args=additional_args + \
                                            (previous_date.year,))

        # l'adresse pour afficher l'année suivant
        next_date_url = reverse(url,
                                args=additional_args + (next_date.year,))

        # formatage de l'affichage des années
        current_date_ = current_date.strftime("%Y")
        previous_date_ = previous_date.strftime("%Y")
        next_date_ = next_date.strftime("%Y")
        todays_date = u"Cette année"

    return (previous_date_url,
            todays_date_url,
            next_date_url,
            previous_date_,
            current_date_,
            next_date_,
            todays_date,
            todays_date_is_before,
            todays_date_is_after)


# TODO : faire de ce bébé mamouth un middleware ou un context processor
def get_duration_pagination(year, duration,
                            duration_number, url,
                            additional_args=()):
    """
    navigation entre les dates: année, mois, week """
    # la date d'aujourd'hui
    week_date_url, month_date_url, year_date_url = "", "", ""

    if duration == "week":
        # l'adresse pour afficher le mois
        month = get_week_boundaries(year, duration_number)[0].month

        month_date_url = reverse(url, \
                            args=additional_args + (year, "month", month))

        # l'adresse pour afficher l'année
        year_date_url = reverse(url, args=additional_args + (year,))

    elif duration == "month":

        year, week, day = date(year, duration_number, 1).isocalendar()

        # l'adresse pour afficher la semaine
        week_date_url = reverse(url, args=additional_args + (year,
                                                            "week",
                                                             week))

        # l'adresse pour afficher l'année
        year_date_url = reverse(url, args=additional_args + (year,))

    else:
        # l'adresse pour afficher la semaine
        week_numbers = date.today().isocalendar()
        week_date_url = reverse(url, args=additional_args + \
                                        (year, "week", week_numbers[1]))
        # l'adresse pour afficher le mois
        month_date_url = reverse(url, args=additional_args + \
                                    (year, "month", date.today().month))
    return (week_date_url, month_date_url, year_date_url)
