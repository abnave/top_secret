import flask
from flask import render_template
#librarires for image to Text 
import pytesseract
from PIL import Image
import pyttsx3
import os
import werkzeug
#import re
#libraries for text summarization
from gensim.summarization import summarize
#pytesseract.pytesseract.tesseract_cmd = '/app/vendor/tesseract-ocr/bin/tesseract'
#pytesseract.pytesseract.tesseract_cmd ='/app/.apt/usr/bin/tesseract'

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def simple():
	return "<h3>This is simple GET request Successfull!!</h3>"

@app.route('/', methods=['GET', 'POST'])
def handle_request():
	#importing image from android-app
	imagefile = flask.request.files['image']
	#imagefile.seek(0, os.SEEK_END)
	#if imagefile.tell() == 0:
	#	return "<h2>Post request doesn't contain image body</h2>"
	filename = werkzeug.utils.secure_filename(imagefile.filename)
	print("\nReceived image File name : " + imagefile.filename)
	imagefile.save(filename)
	#img to text code
	image= Image.open(filename)
	result=pytesseract.image_to_string(image)
	result=result.replace("\n"," ")
	#result=re.sub('-', '', result)
	with open('information.txt',mode='w') as file:
		file.write(result)
		print(result)
	 
	# text_summarization    
	mytext1=open("information.txt","r")
	summary_text=summarize(mytext1.read())
	print(summary_text)
	with open('summary.txt',mode='w') as file:
		file.write(summary_text)    
	if summary_text == "":
		return "Image doesn't contain any text"
	return summary_text


@app.route('/readme', methods=['GET', 'POST'])
def readme():
	return render_template('readme.html')

if __name__ == '__main__':  
    app.run(host="0.0.0.0", port=5009, debug=True)
#app.run()
