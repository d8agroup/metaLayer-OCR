from flask import Flask, request, jsonify, make_response
from configuration import *
from PIL import Image
from tesseract import Tesseract

app = Flask(__name__)

@app.route('/test')
def test():
    return "worked"

@app.route('/services/1/ocr', methods=['POST'])
def extract_text_from_image():
    #Check for the presence of the image
    if 'image' not in request.files:
        return jsonify(JSON_NOIMAGE)
    
    if 'image_id' not in request.form:
        return jsonify(JSON_NOIMAGEID)
    
    #extract the image 
    file = request.files['image']
    
    try:
        image = Image.open(file)
    except Exception, e:
        if MASK_ERRORS:
            return jsonify(JSON_NONEIMAGE)
        raise e
    
    image_id= request.form['image_id']
    
    tesseract = Tesseract(image_id, TESSERACT_EXE, TESSERACT_SCRATCH, TESSERACT_CLEANUP)
    
    try:
        text = tesseract.image_to_string(image)
    except Exception, e:
        if MASK_ERRORS:
            return jsonify(JSON_OCRFAILED)
        raise e;
        
    return jsonify(JSON_SUCCESS, text=text)