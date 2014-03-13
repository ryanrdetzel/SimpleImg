"""
    Simple server that accepts an image and resizes/rotates it
"""
import os

from PIL import Image
from PIL.ExifTags import TAGS
from flask import Flask, jsonify, render_template,  url_for, request


app = Flask(__name__)

size = (800, 800)

UPLOAD_FOLDER='/var/www/simpleimg.com/content/'
UPLOAD_URL='http://simpleimg.com/content'

@app.route("/")
def index():
    return render_template('index.html')


def allowed_file(filename):
    for ext in ['jpg', 'png']:
        if filename.lower().endswith(ext):
            return True
    return False


def cleanup_image(filename):
    """
        Create a smaller version of the image and rotate it if need be
    """
    thumbfile = "thumb-%s" % filename
    im = Image.open(os.path.join(UPLOAD_FOLDER, filename))
    exifdict = im._getexif()
    orientation = None
    if len(exifdict):
        for k in exifdict.keys():
            if k in TAGS.keys() and TAGS[k] == 'Orientation':
                orientation = exifdict[k]

    if orientation == 3:
        im=im.rotate(180, expand=True)
    elif orientation == 6:
        im=im.rotate(270, expand=True)
    elif orientation == 8:
        im=im.rotate(90, expand=True)
 
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(os.path.join(UPLOAD_FOLDER, thumbfile), "JPEG")

    return thumbfile


def handleUpload(files):
    if not files:
       return None
    filenames = []
    saved_files_urls = []
    for key, file in files.iteritems():
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filename = cleanup_image(filename)
            filenames.append("%s/%s" % (UPLOAD_URL, filename))
    return filenames


@app.route('/upload', methods=['POST'])
def upload():
    try:
        files = request.files
        uploaded_files = handleUpload(files)
        return jsonify({'files': uploaded_files})
    except:
        return jsonify({'status': 'error'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
