import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from face_recon import load_face

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.secret_key = "edlain"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
   return render_template("index.html")

@app.route('/', methods=['POST'])
def upload_image():
   if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
   file = request.files['file']
   if file.filename == '':
      flash('No image selected for uploading')
      return redirect(request.url)
   if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      flash('Image successfully uploaded and displayed below')
      load_face(filename)
      return render_template('index.html', filename=filename)
   else:
      flash('Allowed image types are - png, jpg, jpeg')
      return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
   return redirect(url_for('static', filename='uploads/'+filename), code=301)

if __name__ == '__main__':
   app.run()