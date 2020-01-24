from fpdf import FPDF
from datetime import datetime
import os
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
import img2pdf

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()
    for path in paths:

        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)

class newEmail(Resource):
    def post(self):

        data     = request.form['name']
        image_files = request.files.getlist("file[]")
        pdf_filer = []
        try:
            pdf = FPDF()
            pdf.compress = False
            pdf.add_page()
            pdf.set_font('Arial', '', 14)  
            pdf.ln(10)
            pdf.write(5, data)
            pdf.output('header.pdf', 'F')

            print('Liste: ')
            print(pdf_filer)
            pdf_filer.append('header.pdf')

            for img in image_files:
                kind = os.path.splitext(img.filename)[1] 
                if (kind == '.pdf'):
                    img.save(img.filename)

                    pdf_filer.append(img.filename)
                else:
                    filename = img.filename+'.pdf'
                    pdf_file = open(filename,'wb')
                    pdf_file.write(img2pdf.convert(img))
                    pdf_filer.append(img.filename+'.pdf')
                    pdf_file.close()

            merge_pdfs(pdf_filer, output='result/'+ str(datetime.today().strftime('%Y-%m-%d-%H%M%S')) + '_bilag.pdf')

            return {'message': 'Success'}
        except:
            return {'message': 'Error'}

api.add_resource(newEmail, '/')

if __name__ == '__main__':
    app.run(debug=True)