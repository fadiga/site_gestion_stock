#!usr/bin/env python
# -*- coding= UTF-8 -*-
#maintainer: Fadiga


from datetime import datetime

from django.core.urlresolvers import reverse
from django.db.models import Avg, Sum, Q
from django.shortcuts import (render_to_response, HttpResponseRedirect,
                                                            redirect)
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (authenticate, login as django_login,
                                 logout as django_logout)
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404, HttpResponse
from django.contrib.auth.models import Group, User

from models import *
from vente.form import (rapport_periodiqueForm, RapportForm, LoginForm,
                    Owner_editForm, AddOwner, MagasinForm, ProduitForm)
from lib.tools import *
from lib.export_xls import (write_xls_commande, write_xls_inventaire,
                                                rapport_p_export_excel)
from vente.helper import produit_signaler


@login_required
def home(request):
    """ """
    c = {}
    c.update({"user": request.user})
    return render_to_response("home.html", c)


@login_required
def add_owner(request):
    """ add owner
    """
    group_users = ''
    try:
        # on recupere le groupe de l'utilisateur connecté
        group_users = request.user.groups.values_list()
    except IndexError:
        pass
    grp = group_users[0][1]
    if grp.__eq__("chef"):
        c = {}
        c.update(csrf(request))
        form = AddOwner(request=request)
        user = request.user
        c.update({'form': form, 'user': user,\
                                'erreur': "Ce champ est obligatoire."})
        if request.method == 'POST':
            #On charge le formulaire en lui passant comme
            #paramettre la requette POST.
            form = AddOwner(request, request.POST)
            c.update({'form': form})
            if request.POST.get('password') != request.POST.\
                                            get('password_confirmation'):
                c.update({'error': "Les mots de passe sont diffirents"})

            if request.POST.get('email') == "":
                e_mail = 'aucun@email.ml'
            else:
                e_mail = request.POST.get('email')
            if form.is_valid():
                if request.POST.get('password') == request.POST.\
                                            get('password_confirmation'):
                    username = request.POST.get('username')
                    password = request.POST.get('password')
                    email = e_mail

                    #On oblige l'utilisateur connecter a
                    #remplir tous les champs.
                    if username != ''and password != '' and email != '' \
                                     and request.POST.get('first_name') != ''\
                                     and request.POST.get('last_name') != '':
                        try:
                            user = User.objects.\
                                       create_user(username,\
                                                    email, password)
                        except IntegrityError:
                            c.update({'error': "le nom d'utilisateur\
                                       existe deja"})
                            return render_to_response('/vente/add_owner.html', c)
                        user.first_name = request.POST.get('first_name')
                        user.last_name = request.POST.get('last_name')
                        user.is_staff = True
                        user.is_active = True
                        user.groups.add(Group.objects.get(id=2))
                        user.save()
                        return redirect('/vente/owner')
        return render_to_response('vente/add_owner.html', c)
    else:
        return redirect('/vente/dashboard')


@login_required
def owner(request):
    """create an url by owner
    """
    group_users = ''
    try:
        # on recupere le groupe de l'utilisateur connecté
        group_users = request.user.groups.values_list()
    except IndexError:
        pass
    grp = group_users[0][1]
    if grp.__eq__("chef"):
        user = request.user
        owners = User.objects.all()
        l_utilisateur = []
        for i in range(len(owners)):
            if owners[i].groups.values_list()[0][1] == "utilisateur":
                l_utilisateur.append(owners[i])
                #On cree l'url de chaque utilisateur.
                owners[i].url = reverse('owner_edit', args=[owners[i].id])

        ctx = ({'owners': l_utilisateur, 'user': user})
        return render_to_response('vente/owner.html', ctx)
    else:
        return redirect('/vente/dashboard')


@login_required
def owner_edit(request, *args, **kwargs):
    """ edit an organization
    """
    c = {}
    c.update(csrf(request))
    owner_id = kwargs["id"]
    selected_owner = User.objects.get(id=owner_id)
    groupes = selected_owner.groups.add(Group.objects.get(id=2))

    dict_ = {"username": selected_owner.username, \
            "password": selected_owner.password, \
            "password_confirmation": selected_owner.password, \
            "last_name": selected_owner.last_name, \
            "first_name": selected_owner.first_name,\
            "email": selected_owner.email,\
            "actif": selected_owner.is_active,\
            "groupe": "utilisateur"
            }
    #~ import pdb; pdb.set_trace()
    form = Owner_editForm(dict_)
    user = request.user
    c.update({'form': form, 'user': user,\
                            'selected_owner': selected_owner,\
                            'erreur': "Ce champ est obligatoire."})

    if request.method == 'POST':
        #On charge le formulaire en lui passant comme paramettre
        #la requette POST.
        form = Owner_editForm(request.POST)
        c.update({'form': form})
        if request.POST.get('password') != request.\
                   POST.get('password_confirmation'):
            c.update({'error': "Les mots de passe sont diffirents"})

        if request.POST.get('email') == "":
            e_mail = 'aucun@email.ml'
        else:
            e_mail = request.POST.get('email')
        if request.POST.get('actif') == None:
            statu = False
        else:
            statu = True
        if form.is_valid():
            if request.POST.get('password') == request.\
                       POST.get('password_confirmation'):
                selected_owner.username = request.POST.get('username')
                selected_owner.password = request.POST.get('password')
                selected_owner.last_name = request.POST.get('last_name')
                selected_owner.first_name = request.POST.\
                                                    get('first_name')
                selected_owner.email = e_mail
                selected_owner.is_active = statu
                selected_owner.groups.add(Group.objects.get(id=2))
                selected_owner.save()
                return HttpResponseRedirect(reverse('owner'))
    return render_to_response('vente/owner_edit.html', c)


def login(request):
    """login est la views qui permet de se connecter
    """
    if request.user.is_authenticated():
        try:
            if request.user.groups.values_list()[0][1] in  ["admin"]:
                return redirect("/admin")

            if request.user.groups.values_list()[0][1] in \
                                                    ["utilisateur"]:
                return redirect("/vente/dashboard")
            if request.user.groups.values_list()[0][1] in \
                                                    ["chef"]:
                return redirect("/home")
        except IndexError:
            raise Http404
    else:
        ctx = {}
        ctx.update(csrf(request))
        state = ""

        #Initialise username et password à vide
        username = ""
        password = ""

        # On appel la fonction LoginForm() dans le formulaire
        form = LoginForm()
        ctx = ({"form": form})

        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            url = request.GET.get("next")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    if url:
                        return HttpResponseRedirect(request, url)
                    else:
                        try:
                            if request.user.\
                                       groups.values_list()[0][1] in \
                                                            ["admin"]:
                                return redirect("/admin")

                            if request.user.\
                                      groups.values_list()[0][1] in \
                                                        ["utilisateur"]:
                                return redirect("vente/dashboard")
                            if request.user.groups.values_list()[0][1] in \
                                                            ["chef"]:
                                return redirect("/home")
                        except IndexError:
                            raise Http404
            else:
                state = (u"Votre Identifiant et/ou Mot de passe est \
                                        incorrect. Veuillez réessayer.")
        ctx.update({"user": request.user, "state": state})

        ctx.update(csrf(request))
        return render_to_response("vente/login.html", ctx)


def logout(request):
    """
        logout est la views qui permet de se deconnecter
    """
    django_logout(request)
    return redirect("/")


@login_required
def dashboard(request):
    """ """
    ctx = {}
    rapports = Rapport.objects.order_by("-date")
    if len(rapports) < 20:
        d_operation = rapports
    else:
        d_operation = rapports[:20]
    # Verification des valeurs d"alerte"
    liste_alert = produit_signaler()

    ctx.update({"list_op": d_operation, "alert": liste_alert})
    ctx.update({"user": request.user})
    return render_to_response("vente/dashboard.html", ctx)


@login_required
def inventaire(request):
    """Presente tous les restants des produits """
    ctx = {"user": request.user}
    ctx.update(csrf(request))
    liste_last_report = []
    for mag in Magasin.objects.all():
        for prod in Produit.objects.all():
            rap =''
            dic ={}
            try:
                rap = Rapport.objects.filter(magasins__name=mag.name,produit__name=prod.name).order_by('-date')[0]
                dic["mag"] = rap.magasins
                dic["prod"] = rap.produit
                dic["carton_r"] = rap.carton_remaining
                dic["piece_r"] = rap.piece_remaining
                liste_last_report.append(dic)
            except:
                pass
    if "commande" in request.session:
        del request.session["commande"]
    if "rapport_periodique" in request.session:
        del request.session["rapport_periodique"]
    request.session["inventaire"] = liste_last_report

    #~ import pdb; pdb.set_trace()
    ctx.update({"l":liste_last_report})
    return render_to_response("vente/inventaire.html", ctx)


@login_required
def commande(request):
    """Presente tous les produit à signaler et

    et donne la possibilité de selectionner des produits"""
    ctx = {"user": request.user}
    ctx.update(csrf(request))
    if request.method == "POST":
        list_commande = []
        dict_commande = {}
        for r in request.POST:
            if request.POST[r] == "on":
                dict_commande[r] = request.POST[r + "2"]
        # export
        list_commande.append(dict_commande)
        try:
            list_commande.append(request.POST["num_com"])
        except:
            list_commande.append(" ")
        
        if "commande" in request.session:
            del request.session["commande"]
        if "rapport_periodique" in request.session:
            del request.session["rapport_periodique"]
        request.session["commande"] = list_commande
        return HttpResponseRedirect(reverse("export_excel"))

    propos_command = Produit.objects.all()
    ctx.update({"propos_command": propos_command})
    return render_to_response("vente/commande.html", ctx)


@login_required
def export_excel(request):
    if "commande" in request.session:
        rapport = request.session.get("commande")
        file_name = 'commande-du-%(date)s a bko.xls' \
                                            % {'date': datetime.now()}
        file_content = write_xls_commande(rapport).getvalue()

    if "inventaire" in request.session:
        file_name = 'inventaire-du-%(date)s a bko.xls' \
                                            % {'date': datetime.now()}
        rapport = request.session.get("inventaire")
        file_content = write_xls_inventaire(rapport).getvalue()
    
    if "rapport_periodique" in request.session:
        file_name = "Rapport-du-%(date)s a bko.xls" \
                                            % {'date': datetime.now()}
        rapport = request.session.get("rapport_periodique")
        file_content = rapport_p_export_excel(rapport).getvalue()

    response = HttpResponse(file_content, \
                            content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    response['Content-Length'] = len(file_content)
    return response


@login_required
def produit(request):
    """ """
    produits = Produit.objects.all().order_by("-id")
    form = ProduitForm()
    ctx = {}
    ctx.update(csrf(request))
    if request.method == "POST":
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("produit"))
    ctx.update({"produits": produits, "form": form, "user": request.user})
    return render_to_response("vente/produit.html", ctx)


@login_required
def magasin(request):
    """ """
    magasins = Magasin.objects.all().order_by("-id")
    form = MagasinForm()
    ctx = {}
    ctx.update(csrf(request))
    if request.method == "POST":
        form = MagasinForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("magasin"))
    ctx.update({"magasin": magasins, "form": form, "user": request.user})
    return render_to_response("vente/magasin.html", ctx)


@login_required
def gestion_rapports(request, *args, **kwargs):
    """ """
    ctx = ({"user": request.user})
    # On recupere le numero depuis l"url si le numero
    # est none on donne 1 par  defaut
    num = kwargs["num"] or 1

    # On ordonne par dates recentes les rapports
    rapports = Rapport.objects.order_by("-id")

    #pour mettre 20 rapport par page
    paginator = Paginator(rapports, 15)

    # s'execute si la base est vide
    if not rapports.count():
        ctx.update({"in_empty_case": "Pas de rapport "})
    # s'execute si il ya des données dans la base
    else:
        try:
            page = paginator.page(int(num))
        # affiche une erreur Http404 si l'on de passe la page est vide
        except EmptyPage:
            raise Http404
        # si le numero de la page est 2
        page.is_before_first = (page.number == 2)
        # si le numero de la page est egale au numero de l'avant derniere page
        page.is_before_last = (page.number == paginator.num_pages - 1)
        # On constitue l'url de la page suivante
        page.url_next = reverse("g-rapport", args=[int(num) + 1])
        # On constitue l'url de la page precedente
        page.url_previous = reverse("g-rapport", args=[int(num) - 1])
        # On constitue l'url de la 1ere page
        page.url_first = reverse("g-rapport")
        # On constitue l'url de la derniere page
        page.url_last = reverse("g-rapport", args=[paginator.num_pages])

        for report in page.object_list:
            # On recupere l'année, le nombre de semaines et le nombre de jours
            year, week_number, day_number = report.date.isocalendar()
            # On constitue l'url du lien pointant sur le nom du village
            report.url_magasin = reverse("par-produits",
                                       args=[report.magasins.id,
                                             slugify(report.magasins),
                                             year, "week", week_number])
            # On constitue l"url du lien pointant sur le nom du product
            report.url_produit = reverse("par-magasins",
                                          args=[report.produit.id,
                                                slugify(report.produit),
                                                year, "week", week_number])
            # On constitue l'url du lien pointant sur la vue
            # de la confirmation du rapport
            report.url_delete = reverse("delete-confirm", args=[report.id])
            ctx.update({"page": page, "paginator": paginator, \
                                "user": request.user, "lien": "before"})

    form = RapportForm(request=request)
    ctx.update(csrf(request))
    if request.method == "POST":
        form = RapportForm(request, request.POST)
        drapo = False
        last_rapport = ""
        m_error = ""
        try:
            last_rapport = Rapport.objects \
                                  .filter(magasins=request.POST["magasins"],\
                                            produit=request.POST["produit"])\
                                  .order_by("-date")[0]
            if request.POST.get('type_r') == "s" and \
                       last_rapport.carton_remaining \
                                < int(request.POST.get('nbr_carton')):
                m_error = u"Il ne reste que %(carton_r)s carton %(prod)s \
                            dans le magasin de %(mag)s " % \
                           {"carton_r": last_rapport.carton_remaining, \
                            "prod": last_rapport.produit.name, \
                            "mag": last_rapport.magasins.name}
                ctx.update({"message": m_error})
                drapo = True
        except:
            pass

        if request.POST.get('type_r') == "s" and last_rapport == "":
            m_error = u"Vous ne pouvez sortir de produit non entre"
            ctx.update({"message": m_error})
            drapo = True
        if form.is_valid() and drapo == False:
            form.save()
            return HttpResponseRedirect(reverse("g-rapport"))
    ctx.update({"form": form})
    return render_to_response("vente/g_rapports.html", ctx)


@login_required
def tous_rapports(request, *args, **kwargs):
    """
        Affiche l'état général des stocks pour chaque magasin
        et chaque produit
    """
    ctx = ({"user": request.user})
    # On recupere les rapports filtres pour la date demandee
    year, duration, duration_number = extract_date_info_from_url(kwargs)

    previous_date_url, todays_date_url, next_date_url, previous_date,\
    current_date, next_date, todays_date, todays_date_is_before,\
    todays_date_is_after = get_time_pagination(request, year,
                                              duration, duration_number,\
                                                            "stock-all")

    week_date_url, month_date_url, year_date_url = \
                    get_duration_pagination(year, duration, \
                                            duration_number, "stock-all")

    rapports = Rapport.get_reports_filtered_by_duration(year, duration, \
                                duration_number).values("magasins__id", \
                                "magasins__name", "produit__id", \
                                "produit__name", "produit__qtte",\
                                "nbr_carton", "date", "piece_remaining",\
                                "carton_remaining", "type_r", \
                                "auteur__username").order_by("-date")
    ctx.update(locals())
    return render_to_response("vente/all.html", ctx)


@login_required
def par_produits(request, *args, **kwargs):
    """
    """
    ctx = ({"user": request.user})
    ctx.update(csrf(request))
    id_ = int(request.POST.get("to_display", 0)) or int(kwargs["id"])
    try:
        magasin = Magasin.objects.get(id=id_)
    except Magasin.DoesNotExist:
        raise Http404

    year, duration, duration_number = extract_date_info_from_url(kwargs)

    if request.method == "POST":
        return get_redirection("par-produits", magasin,
                                year, duration, duration_number)

    navigation_form = get_navigation_form(Magasin.objects.all(),
                                          "Changer de magasin", magasin, \
                                          "par-produits", \
                                          year, duration, duration_number)

    rapports = Rapport.get_reports_filtered_by_duration(year, \
                                                       duration, \
                                                       duration_number)

    previous_date_url, todays_date_url, next_date_url,\
    previous_date, current_date, next_date, todays_date,\
    todays_date_is_before, todays_date_is_after = \
                        get_time_pagination(request, year,\
                                            duration, duration_number, \
                                            "par-produits", \
                                                additional_args=(id_, \
                                                slugify(magasin.name)))

    week_date_url, month_date_url, year_date_url =\
                                   get_duration_pagination(year,\
                                    duration, duration_number,\
                                    "par-produits",\
                                    additional_args=(id_,\
                                                    slugify(magasin.name)))
    # On filtre par magasin
    rapports = rapports.filter(magasins__id=id_).order_by("-date")
    ctx.update(locals())
    return render_to_response("vente/par_produit.html", ctx)


@login_required
def par_magasins(request, *args, **kwargs):
    """
        Affiche l'état des stocks pour chaque Magasins """
    ctx = {"user": request.user}
    ctx.update(csrf(request))
    id_ = int(request.POST.get("to_display", 0)) or int(kwargs["id"])

    # Charger l'ecole dont on veut afficher les ecoles
    # si ce village n'existe pas, mettre une page d'erreur
    try:
        produit = Produit.objects.get(id=id_)
    except Product.DoesNotExist:
        raise Http404

    year, duration, duration_number = extract_date_info_from_url(kwargs)
    # Comme partie du formulaire
    if request.method == "POST":
        return get_redirection("par-magasins", produit,
                                    year, duration, duration_number)

    navigation_form = get_navigation_form(Produit.objects.all(),
                                          "Changer de produit",
                                          produit,
                                          "par-magasins",
                                          year, duration, duration_number)

    total_incomming, total_consumption, total_remaining = 0, 0, 0

    # On a filtrer par entrée, mois, année, nom de produit
    rapports = Rapport.get_reports_filtered_by_duration(year,
                                                     duration,
                                                     duration_number)

    previous_date_url, todays_date_url, next_date_url,\
    previous_date, current_date, next_date,\
    todays_date, todays_date_is_before,\
    todays_date_is_after = get_time_pagination(request, year, duration,\
                                                duration_number,\
                                                "par-magasins",
                                                additional_args=(id_,
                                                slugify(produit.name)))
    week_date_url,\
    month_date_url,\
    year_date_url = get_duration_pagination(year, duration,\
                                            duration_number,\
                                            "par-magasins",\
                                            additional_args=(id_,\
                                                slugify(produit.name)))
    # On filtre par produit
    rapports = rapports.filter(produit__id=id_).order_by("-date")
    # Todo faire la somme des dernières restants en fonction de la date
    ctx.update(locals())
    return render_to_response("vente/par_magasin.html", ctx)


@login_required
def delete_confirm(request, *args, **kwargs):
    """
        Confirmation de la suppression d'un rapport
    """
    try:
        # On recupere le numero du rapport depuis l'url
        id_report = kwargs["num"]
        # On recupere ce rapport
        rapport = Rapport.objects.get(id=id_report)
        # On constitue l'url du lien pointant sur la vue
        # de la suppression du rapport
        rapport.url_delete = reverse("delete", args=[rapport.id])
        ctx = {"rapport": rapport, "user": request.user}
        return render_to_response("vente/delete.html", ctx)
    except UnboundLocalError:
        pass


@login_required
def deleting(request, *args, **kwargs):
    """
        Suppression de rapport
    """
    # On recupere le numero du rapport depuis l'url
    id_report = kwargs["num"]
    try:
        rapport = Rapport.objects.get(id=id_report)
        rapports = Rapport.objects.filter(produit__name=rapport.produit.name, \
                                      magasins__name=rapport.magasins.name, \
                                      date__gt=rapport.date).order_by('-date')
        # Supprime le rapport
        rapport.delete()
        if rapports:
            for report in rapports:
                report.save()
    except:
        pass
    return HttpResponseRedirect(reverse("g-rapport"))


@login_required
def rapport_periodique(request):

    ctx = {"user": request.user}
    ctx.update(csrf(request))
    form = rapport_periodiqueForm()
    rapportsp = ""
    date_debut = ""
    date_fin = ""
    if request.method == "POST":
        try:
            date_debut = request.POST["date_debut"]
            date_fin = request.POST["date_fin"]
            day, month, year = date_debut.split("-")
            date_de = year + "-" + month + "-" + day
            if date_fin == "":
                d = date.today()
                date_fi = str(d.year) + "-" + str(d.month) + "-" + str(d.day)
                date_fin = str(d.day) + "-" + str(d.month) + "-" + str(d.year)
            else:
                day, month, year = date_fin.split("-")
                date_fi = year + "-" + month + "-" + day
            rapportsp = Rapport.objects.filter(date__gte=date_de, \
                                                date__lte=date_fi) \
                                       .order_by("-date")
            if "commande" in request.session:
                del request.session["commande"]
            if "rapport_periodique" in request.session:
                del request.session["inventaire"]
            request.session["rapport_periodique"] = [date_debut, \
                                                    date_fin, rapportsp]
        except ValueError:
            pass
        ctx.update({"form": form, "date_debut": date_debut, \
                    "date_fin": date_fin, "rapports": rapportsp})
        if not rapportsp:
            ctx.update({"form": form, "massage": \
                                (u"Pas de rapport pour cette periode")})
        return render_to_response("vente/rapport_periodique.html", ctx)
    else:
        ctx.update({"form": form, "massage": \
                                (" Choisie une periode pour commencer")})
    return render_to_response("vente/rapport_periodique.html", ctx)
