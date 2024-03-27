from flask import Flask, render_template,request,redirect,send_from_directory,send_file
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from main import image_compressor
import os

app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['DOWNLOAD_DIRECTORY'] = 'downloads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = ['.jpg','.jpeg','.png']

def display(dir):
  files = os.listdir(dir)
  images = []
 
  for file in files:
    extension = os.path.splitext(file)[1].lower()
    if extension in app.config['ALLOWED_EXTENSIONS']:
      images.append(file)
  return images
# display(app.config['DOWNLOAD_DIRECTORY'])
@app.route('/')
def index():
  images = display(app.config['UPLOAD_DIRECTORY'])
  return render_template('index.html',images = images)

@app.route('/upload',methods=['POST'])
def upload():
  try:
    file = request.files['image']
    extension = os.path.splitext(file.filename)[1].lower()

    if file:
      if extension not in app.config['ALLOWED_EXTENSIONS']:
        return 'File is not an image'
      file.save(os.path.join(
        app.config['UPLOAD_DIRECTORY'],
        secure_filename(file.filename)
      ))
    return redirect('/')
  except RequestEntityTooLarge:
    return render_template('Entitytoolarge.html')

@app.route('/serve_upload_image/<filename>',methods=['GET'])
def serve_upload_image(filename):
  return send_from_directory(app.config['UPLOAD_DIRECTORY'],filename)

@app.route('/serve_download_image/<filename>',methods=['GET'])
def serve_download_image(filename):
  return send_from_directory(app.config['DOWNLOAD_DIRECTORY'],filename)


@app.route('/pca', methods=['POST'])
def process():
    if request.method == 'POST':
        pca = request.form['pca']
        try:
          pca = int(pca)
          image_compressor(pca)
          images = display(app.config['DOWNLOAD_DIRECTORY'])
          return render_template('pca.html',pca = pca,images = images)
        except ValueError:
          return 'EE'
        

@app.route('/download')
def download():
  dir_path = os.path.join('.','downloads')
  return send_file(dir_path,as_attachment=True)
  pass
if __name__ == '__main__':
    app.run(debug=True)
  