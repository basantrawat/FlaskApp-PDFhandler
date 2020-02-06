from flask import Flask, render_template, request
import PyPDF2
import os
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "F:\\PROGRAMMING\\Python\\PdfHandling\\uploadFolder"


@app.route('/', methods=['GET', 'POST'])
@app.route('/pdfMerger', methods=['GET', 'POST'])
def pdfMerger():   
    # files_name = ['']
    if(request.method=='POST'):
        files_name = request.files.getlist('filename[]')

        '''UPLOADING THE FILE TO A SPECIFIC LOCATION'''
        for file_name in files_name:
            file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_name.filename)))

        '''MERGING THE UPLOADED FILES'''
        pdfMerger = PyPDF2.PdfFileMerger()      
        for file_name in files_name: 
            pdfMerger.append('uploadFolder/' + secure_filename(file_name.filename)) 
    
        name = secure_filename(files_name[0].filename)[:-4]+"-MergedFile"+".pdf"
        pdfMerger.write('mergedPDF/%s' % name)
        
        '''RETURNING THE PAGE WITH URL LINK OF MERGED FILE'''
        file_path = 'mergedPDF/' + name
        return render_template('pdfMerger.html', msg="Merged Successfully", file_path=file_path) 
    
    else:
        return render_template('pdfMerger.html', msg="", file_path="")



@app.route('/pdfMergerOrdered', methods=['GET', 'POST'])
def pdfMergerOrdered():   
    if(request.method=='POST'):
        '''GETING THE FILE NAMES BY POST REQUEST'''
        selected_files=[]
        for i in range(4):
            selected_files.append(request.files.get('filename%s' % (i+1)))

        '''UPLOADING THE FILE TO A SPECIFIC LOCATION'''
        for i in range(4):
            if selected_files[i].filename!='':
                selected_files[i].save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(selected_files[i].filename)))
        
        '''MAKING ARRAY OF ALL FILES TO BE MERGED'''
        pdfMerger = PyPDF2.PdfFileMerger() 
        for i in range(4):
            if selected_files[i].filename!='':
                pdfMerger.append('uploadFolder/' + secure_filename(selected_files[i].filename)) 
        
        
        name = secure_filename(selected_files[0].filename)[:-4]+"-MergedFile"+".pdf"
        pdfMerger.write('mergedPDF/%s' % name)
         
        '''RETURNING THE PAGE WITH URL LINK OF MERGED FILE'''
        file_path = 'mergedPDF/' + name
        return render_template('pdfMergerOrdered.html', msg="Merged Successfully", pdfFile=file_path)

    else:
        return render_template('pdfMergerOrdered.html', msg="", pdfFile="")



@app.route('/pdfToText', methods=['GET', 'POST'])
def pdfToText():   
    if(request.method=='POST'):
        file_name = request.files.get('filename')
        
        '''UPLOADING FILE TO SERVER'''
        file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_name.filename)))

        '''CONVERTING PDF TO TEXT'''
        pdfFileObj = open(f'uploadFolder/{secure_filename(file_name.filename)}', 'rb') 
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        
        # Storing Number Of Pages in PDF
        numberOfPages = pdfReader.numPages

        ConvertedTextData = ''
        for i in range(numberOfPages):
            pageObj = pdfReader.getPage(i)
            content = pageObj.extractText()
            ConvertedTextData = ConvertedTextData + content + '\n\n'
        pdfFileObj.close()

        return render_template('pdfToText.html', convertedData=ConvertedTextData)

    else:
        return render_template('pdfToText.html')
        


@app.route('/splitPdf', methods=['GET', 'POST'])
def splitPdf():    
    if(request.method=='POST'):
        file_name = request.files.get('filename')
        strFileName = secure_filename(file_name.filename)
        '''UPLOADING FILE TO SERVER'''
        file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_name.filename)))

        f = open('uploadFolder/%s' % strFileName, "rb")
        pdfInput = PyPDF2.PdfFileReader(f)

        for i in range(pdfInput.numPages):
            output = PyPDF2.PdfFileWriter()
            output.addPage(pdfInput.getPage(i))
            name = strFileName[:-4]+"-Page "+str(i)+".pdf"
            outputFiles = open('splitedFiles/'+name, "wb")
            output.write(outputFiles)
            
        return render_template('splitPdf.html', msg="Successfully Splited the PDF")

    else:
        return render_template('splitPdf.html', msg="")

app.run(debug=True)