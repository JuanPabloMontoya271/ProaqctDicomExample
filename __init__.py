import os
import pydicom 
import cv2
import numpy as np
from flask import Flask, send_file, send_from_directory, safe_join, abort, render_template, url_for, jsonify
from flask_cors import CORS
import boto3
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
        client = boto3.client("s3",region_name="us-east-2",
                          aws_access_key_id="AKIAQMXFNQFGDTPB77J2",
                          aws_secret_access_key="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")
        response = client.generate_presigned_url('get_object',Params={'Bucket': "proaqc-dicom-node",'Key':  'media/DICOM/Alleghany Regional Hospital/CT/Daily_QC/GE MEDICAL SYSTEMS/LightSpeed Pro 16/ct16/20140805/20140805.dcm'},ExpiresIn=100)
        print(response)

        return render_template("./viewer/viewer.html")
    @app.route('/get_segmentation/<image_name>')
    def get_segmentation(image_name):
        img =pydicom.read_file("C:/Users/juanp/Desktop/Apps/DicomFlask/images/"+image_name)
        rs,ri = img.RescaleSlope, img.RescaleIntercept
        huMap = img.pixel_array*rs+ri
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
            hu = huMap[x:x+w,y:y+h]
            center = ((x+w)//2, (y+h)//2)
            

            
            distance = ((((x+w)/2 -huMap.shape[0]/2)*img.PixelSpacing[0])**2 +(((y+h)/2- huMap.shape[1]/2)*img.PixelSpacing[1])**2)**0.
            
            data["mean"]=hu.mean()
            data["std"]=hu.std()
            data["area"]=w*img.PixelSpacing[0]*h*img.PixelSpacing[1]
            data["distance"]=distance
            data["w"]= abs(w)*img.PixelSpacing[0]
            data["h"]= abs(h)*img.PixelSpacing[1]
            data["center"] = center
            data["coords"] = [x,y,w,h]
            res[w*h] = data
        
        c = res[list(res.keys())[-1]]["center"]
        coords =res[list(res.keys())[-1]]["coords"]
        
        sampleA =huMap[c[0]-25:c[0]+25,c[1]-25:c[1]+25 ]
        sampleB =huMap[coords[0]-50:coords[0], coords[1]:coords[1]+50]
        
        res[list(res.keys())[-1]]["sampleA"] = [sampleA.mean(), sampleA.std()]
        res[list(res.keys())[-1]]["sampleB"] = [sampleB.mean(), sampleB.std()]
        
        return jsonify(res)
    
    @app.route("/get-image/<image_name>")
    def get_image(image_name):
        
        try:
            return send_from_directory(app.config["CLIENT_IMAGES"], filename=image_name, as_attachment=True)
        except FileNotFoundError:
            abort(404)
    return app
