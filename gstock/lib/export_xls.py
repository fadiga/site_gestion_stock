#!usr/bin/env python
# -*- coding= UTF-8 -*-
#maintainer: Fadiga

import xlwt
import StringIO
from datetime import date


font_title = xlwt.Font()
font_title.name = 'Times New Roman'
font_title.bold = True
font_title.height = 19 * 0x14
font_title.underline = xlwt.Font.UNDERLINE_DOUBLE

font1 = xlwt.Font()
font1.name = 'Verdana'
font1.height = 10 * 0x14
font1.bold = True

borders_title = xlwt.Borders()
borders_title.left = 0
borders_title.right = 0
borders_title.top = 0
borders_title.bottom = 1

borders = xlwt.Borders()
borders.left = 1
borders.right = 1
borders.top = 1
borders.bottom = 1

al = xlwt.Alignment()
al.horz = xlwt.Alignment.HORZ_CENTER
al.vert = xlwt.Alignment.VERT_CENTER
al1 = xlwt.Alignment()
al1.horz = xlwt.Alignment.HORZ_RIGHT

color = xlwt.Pattern()
color.pattern = xlwt.Pattern.SOLID_PATTERN
color.pattern_fore_colour = 22

style_title = xlwt.XFStyle()
style_title.font = font_title
style_title.alignment = al
style_title.borders = borders_title

style_t_table = xlwt.XFStyle()
style_t_table.font = font1
style_t_table.pattern = color
style_t_table.alignment = al
style_t_table.borders = borders

style_row_table = xlwt.XFStyle()
style_row_table.borders = borders

style = xlwt.XFStyle()
style.alignment = al1


def write_xls_commande(rapport):
    ''' Export data '''
    # Principe
    # write((nbre ligne - 1), nbre colonne, "contenu", style(optionnel).
    # write_merge((nbre ligne - 1), (nbre ligne - 1) + nbre de ligne
    # à merger, (nbre de colonne - 1), (nbre de colonne - 1) + nbre
    # de colonne à merger, u"contenu", style(optionnel)).
    book = xlwt.Workbook(encoding='ascii')
    sheet = book.add_sheet(u"La commande")
    rowx = 0
    sheet.write_merge(rowx, rowx + 2, 0, 3,\
                            u"NOUVEAUX COMMENDE DE ULTIMO", style_title)
    rowx += 4
    sheet.write_merge(rowx, rowx, 1, 2, \
                                u"NUMERO  DE  COMMENDE  DKM… N°", style)
    sheet.write_merge(rowx, rowx, 3, 3, rapport[1])
    rowx += 2
    sheet.write_merge(rowx, rowx, 1, 2, u"DATE DE COMMENDE: ", style)
    date_com = "Bko le %s" % date.today().strftime("%d/%m/%Y")
    sheet.write_merge(rowx, rowx, 3, 3, date_com)

    sheet.col(1).width = 0x0d00 * 3
    sheet.col(3).width = 0x0d00 * 2
    hdngs = [u"Quantite", u"Designation du produit", u"P.U", u"Prix"]
    rowx += 3
    for colx, value in enumerate(hdngs):
        sheet.write(rowx, colx, value, style_t_table)
    rowx += 1
    for prod in rapport[0]:
        if rapport[0][prod]:
            sheet.write(rowx, 0, int(rapport[0][prod]), style_row_table)
        sheet.write(rowx, 1, prod, style_row_table)
        sheet.write(rowx, 2, "", style_row_table)
        sheet.write(rowx, 3, "", style_row_table)
        rowx += 1
    if rowx > 15:
        sheet.write(rowx, 2, u"TOTAL", style_t_table)
        sheet.write(rowx, 3, "", style_row_table)
    else:
        sheet.write(45, 2, u"TOTAL", style_t_table)
        sheet.write(45, 3, "", style_row_table)

    stream = StringIO.StringIO()
    book.save(stream)
    return stream


def write_xls_inventaire(rapport):
    book = xlwt.Workbook(encoding='ascii')
    sheet = book.add_sheet(u"inventaire")
    rowx = 0
    sheet.write_merge(rowx, rowx + 2, 0, 3,\
                            u"L'INVENTAIRE", style_title)
    rowx += 3
    sheet.write_merge(rowx, rowx, 3, 3, "")
    rowx += 2
    sheet.write_merge(rowx, rowx, 1, 2, u"DATE: ", style)
    date_com = "Bko le %s" % date.today().strftime("%d/%m/%Y")
    sheet.write_merge(rowx, rowx, 3, 3, date_com)

    sheet.col(1).width = 0x0d00 * 3
    sheet.col(2).width = 0x0d00 * 1.3
    sheet.col(3).width = 0x0d00 * 1.2
    hdngs = [u"Magasin", u"Designation du produit", u"Carton Restant", \
                                                        u"Piece Restant"]
    rowx += 3
    for colx, value in enumerate(hdngs):
        sheet.write(rowx, colx, value, style_t_table)
    rowx += 1
    for rap in rapport:
        sheet.write(rowx, 0, str(rap["mag"]), style_row_table)
        sheet.write(rowx, 1, str(rap["prod"]), style_row_table)
        sheet.write(rowx, 2, int(rap["carton_r"]), style_row_table)
        sheet.write(rowx, 3, int(rap["piece_r"]), style_row_table)
        rowx += 1
    stream = StringIO.StringIO()
    book.save(stream)
    return stream


def rapport_p_export_excel(rapport):
    
    book = xlwt.Workbook(encoding='ascii')
    sheet = book.add_sheet(u"Rapport")
    rowx = 0
    sheet.write_merge(rowx, rowx + 2, 0, 6,\
                                     u"RAPPORT PERIODIQUE", style_title)
    rowx += 3
    sheet.write_merge(rowx, rowx, 3, 3, "")
    rowx += 2
    sheet.write_merge(rowx, rowx, 1, 2, u"Les rapports du: ", style)
    periode = " %s au %s " % (rapport[0],  rapport[1])
    sheet.write_merge(rowx, rowx, 3, 5, periode)

    sheet.col(0).width = 0x0d00 * 0.8
    sheet.col(1).width = 0x0d00 * 1.2
    sheet.col(2).width = 0x0d00 * 1.5
    sheet.col(4).width = 0x0d00 * 1.1
    hdngs = [u"Auteur",u"Magasin", u"Produit", u"N carton", \
                        u"Carton R", u"Pièce R", u"Date"]
    rowx += 3
    for colx, value in enumerate(hdngs):
        sheet.write(rowx, colx, value, style_t_table)
    rowx += 1
    for rap in rapport[2]:
        if rap.type_r == "e":
            magasins = "+ " + str(rap.magasins.name)
        if rap.type_r == "s":
            magasins = "- " + str(rap.magasins.name)
        sheet.write(rowx, 0, str(rap.auteur.username), style_row_table)
        sheet.write(rowx, 1, magasins, style_row_table)
        sheet.write(rowx, 2, str(rap.produit.name), style_row_table)
        sheet.write(rowx, 3, int(rap.nbr_carton), style_row_table)
        sheet.write(rowx, 4, int(rap.carton_remaining), style_row_table)
        sheet.write(rowx, 5, int(rap.piece_remaining), style_row_table)
        sheet.write(rowx, 6, str(rap.date.strftime("%d/%m/%Y")), style_row_table)
        rowx += 1
    stream = StringIO.StringIO()
    book.save(stream)
    return stream


