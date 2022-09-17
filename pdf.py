#!/usr/bin/python3
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import io
import os
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import mm, inch
from reportlab.lib.colors import black
import sys
import secret
from datetime import datetime

def main(date, horaire, cours, prof, dateweek, promo):
    H1 = horaire[0][0]
    H2 = horaire[1][0]
    M1 = horaire[0][1]
    M2 = horaire[1][1]
    tdelta = datetime.strptime(H2+M2, '%H%M') - datetime.strptime(H1+M1, '%H%M')
    HD, reste = divmod(tdelta.seconds, 3600)
    MD, secondes = divmod(reste, 60)
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.drawString(23 * mm, 178 * mm, date)
    can.drawString(108 * mm, 167 * mm, str(HD) + "H" + str(MD))
    can.drawString(188 * mm, 181 * mm, H1 + "H" + M1)
    can.drawString(182 * mm, 177 * mm, H2 + "H" + M2)
    # In case of multiple teachers we split them and then add as new line
    textobject = can.beginText(235 * mm, 178 * mm)
    textobject.setFont("Helvetica", 8)
    prof = prof.split('\x0a')
    for line in prof:
        textobject.textLine(line)

    can.drawText(textobject)

    can.setFont("Helvetica-Bold", 8)
    can.drawString(33 * mm, 167 * mm, cours)
    H2 = int(H2)
    can.setFillColor(black)
    if H2 < 13:
        can.rect(81*mm, 178*mm, 2*mm, 1.75*mm, fill=1)
    else:
        can.rect(104*mm, 178*mm, 2*mm, 1.75*mm, fill=1)




    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    week_num = dateweek.isocalendar().week
    filename = '/home/mchouteau/Feuille-temps/'+secret.ANNEE[promo]+'/%s.pdf' % week_num
    reference_pdf = PdfFileReader(open('./FichePrésence-'+secret.ANNEE[promo]+'.pdf', "rb"))
    output = PdfFileWriter()
    merger = PdfFileMerger()
    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    if os.path.isfile(filename):
        existing_pdf = PdfFileReader(open(filename, "rb"))
        # add the "watermark" (which is the new pdf) on the existing page
        page = reference_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # finally, write "output" to a real file
        outputStream = open('/home/mchouteau/Feuille-temps/'+secret.ANNEE[promo]+'/temp.pdf', 'wb')
        output.write(outputStream)
        outputStream.close()
        merger.append(existing_pdf)
        merger.append('/home/mchouteau/Feuille-temps/'+secret.ANNEE[promo]+'/temp.pdf')
        merger.write(filename)
    else:
        # add the "watermark" (which is the new pdf) on the existing page
        page = reference_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # finally, write "output" to a real file
        outputStream = open(filename, 'wb')
        output.write(outputStream)
        outputStream.close()
    
