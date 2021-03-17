import os
import pydicom 
import cv2
import numpy as np
from flask import Flask, send_file, send_from_directory, safe_join, abort, render_template, url_for, jsonify
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config["CLIENT_IMAGES"] = "C:/Users/juanp/Desktop/Apps/DicomFlask/images"
    app.static_folder = 'static'
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return render_template("./viewer/viewer.html")
    @app.route('/get_segmentation/<image_name>')
    def get_segmentation(image_name):
        img =pydicom.read_file("C:/Users/juanp/Desktop/Apps/DicomFlask/images/"+image_name)
        res = {}
        pix = np.float32(img.pixel_array)/2**16*2**8
        r, img_t =cv2.threshold(pix, pix.max()*.3, pix.max(), 0  )
        contours, hierarchy = cv2.findContours(img_t.astype("uint8"), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for i,contour in enumerate(contours):
            data = {}
            c  =cv2.drawContours(pix, contours, i,9.75,5)
            x, y, w, h=cv2.boundingRect(contour)
            rect =cv2.rectangle(img_t.copy(), (x, y), (x + w - 1, y + h - 1), 255, 2)
            p = pix[x:x+w, y:y+h ]
            distance = ((((x+w)/2 -512/2)*img.PixelSpacing[0])**2 +(((y+h)/2- 512/2)*img.PixelSpacing[1])**2)**0.5
            data["mean"]=img.pixel_array.mean()
            data["std"]=p.std()
            data["area"]=w*img.PixelSpacing[0]*h*img.PixelSpacing[1]
            data["distance"]=distance
            data["w"]= abs(w)*img.PixelSpacing[0]
            data["h"]= abs(h)*img.PixelSpacing[1]
            
            data["coords"] = [x,y,w,h]
            res[w*h] = data

        return jsonify(res)
    
    @app.route("/get-image/<image_name>")
    def get_image(image_name):
        
        try:
            return send_from_directory(app.config["CLIENT_IMAGES"], filename=image_name, as_attachment=True)
        except FileNotFoundError:
            abort(404)
    return app
