import os, sys
sys.path.append('../JH_AiP')
import numpy as np
import pandas as pd

import tensorflow as tf

from JH_AiP import UI_aip_x5_l

from flask import Flask
from flask import request
from flask_restful import Api, Resource, reqparse

import tensorflow.compat.v1 as tf
CUDA_VISIBLE_DEVICES=0
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
tf.keras.backend.set_session(tf.Session(config=config))

app = Flask (__name__)
#@app.route('/aip450')


class test_aip(Resource):
    def get(self):
        #print("#### make descriptor")
        try:
            feature = request.get_json()
            print("Feature :",feature)
            #idd = pd.DataFrame(feature)
            js_a = UI_aip_x5_l.mk_descriptor(feature, "test_0908")
            return js_a
        except Exception as e:
            return {'error': str(e)}

api = Api(app)
api.add_resource(test_aip,'/test_aip')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8106,threaded=False,debug=False)
