# Receive as arguments the pdf to combine and put the watermark.
# Watermark file should be at the same directory level and be called
# wtr.pdf

import PyPDF2
import sys

inputs = sys.argv[1:]


def pdf_combiner(pdf_list):
    merger = PyPDF2.PdfFileMerger()
    for pdf in pdf_list:
        merger.append(pdf)

    merger.write('combined_pdf.pdf')


def pdf_watermark():
    watermark = PyPDF2.PdfFileReader(open('wtr.pdf', 'rb'))
    template = PyPDF2.PdfFileReader(open('combined_pdf.pdf', 'rb'))
    output = PyPDF2.PdfFileWriter()

    for i in range(template.getNumPages()):
        page = template.getPage(i)
        page.mergePage(watermark.getPage(0))

        output.addPage(page)

    with open('watermarked.pdf', 'wb') as file:
        output.write(file)


pdf_combiner(inputs)

pdf_watermark()

