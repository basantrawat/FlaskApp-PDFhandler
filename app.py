from flask import Flask, render_template, request
import PyPDF2


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/pdfMerger', methods=['GET', 'POST'])
def pdfMerger():   
    pdfs = ['']
    if(request.method=='POST'):
        pdfs = request.form.getlist('filename')
        if pdfs==['']:
            file_path=""
            return render_template('pdfMerger.html', msg="Choose Some Files First", pdfFile=file_path)
        else:
            msg=""
            pdfMerger = PyPDF2.PdfFileMerger()      
            for pdf in pdfs: 
                pdfMerger.append('pdfFiles/'+pdf) 
                pdfMerger.write('mergedPDF/mergedPDFOutput.pdf')
            file_path = 'mergedPDF/mergedPDFOutput.pdf'
            return render_template('pdfMerger.html', pdfFile=file_path, msg=msg)
    
    else:
        return render_template('pdfMerger.html', pdfFile="")



@app.route('/pdfMergerOrdered', methods=['GET', 'POST'])
def pdfMergerOrdered():   
    if(request.method=='POST'):
        pdf1 = request.form.get('filename1')
        pdf2 = request.form.get('filename2')
        pdf3 = request.form.get('filename3')
        pdf4 = request.form.get('filename4')
        
        pdfs = [pdf1,pdf2,pdf3,pdf4]
        pdfMerger = PyPDF2.PdfFileMerger() 

        if pdfs==['', '', '', '']:
            file_path=""
            return render_template('pdfMergerOrdered.html', msg="Choose Some Files First", pdfFile=file_path)
        else:
            for pdf in pdfs: 
                if pdf!='':
                    pdfMerger.append('pdfFiles/'+pdf) 
                    pdfMerger.write('mergedPDF/mergedPDFOutput.pdf')
            
            file_path = 'mergedPDF/mergedPDFOutput.pdf'
            return render_template('pdfMergerOrdered.html', pdfFile=file_path, msg='')

    else:
        return render_template('pdfMergerOrdered.html', pdfFile='')



@app.route('/pdfToText', methods=['GET', 'POST'])
def pdfToText():   
    if(request.method=='POST'):
        pdffile = request.form.get('filename')
        # creating a pdfFile object 
        pdfFileObj = open(f'pdfFiles/{pdffile}', 'rb') 
        # creating a pdfReader object 
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        # Printing Number of pages in pdf file
        pages = pdfReader.numPages

        ConvertedTextData = ''
        for i in range(pages):
            # creating a page object 
            pageObj = pdfReader.getPage(i)
            # extracting text from page 
            content = pageObj.extractText()
            ConvertedTextData = ConvertedTextData + content
            ConvertedTextData = ConvertedTextData + '\n'

        pdfFileObj.close()
        return render_template('pdfToText.html', convertedData=ConvertedTextData)
    else:
        return render_template('pdfToText.html')
        
@app.route('/splitPdf', methods=['GET', 'POST'])
def splitPdf():    
    if(request.method=='POST'):
        pdffile = request.form.get('filename')

        f = open(pdffile, "rb")
        inputpdf = PyPDF2.PdfFileReader(f)
        for i in range(inputpdf.numPages):
            output = PyPDF2.PdfFileWriter()
            output.addPage(inputpdf.getPage(i))
            name = pdffile[:-4]+"-Page "+str(i)+".pdf"
            outputStream = open(name, "wb")
            output.write(outputStream)
            
        return render_template('splitPdf.html', msg="Successfully Splited the PDF")

    else:
        return render_template('splitPdf.html', msg="")

    # # Listing all the file in directory
    # files = [f for f in os.listdir(".") if os.path.isfile(f)]

    # #Selecting only PDF files from above list
    # files = list(filter(lambda f: f.lower().endswith((".pdf")), files))
    # # print(files)



app.run(debug=True)