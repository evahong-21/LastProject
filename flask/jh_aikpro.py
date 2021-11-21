import os, sys
sys.path.append('./JH_AiK')
import numpy as np
import pandas as pd

import tensorflow as tf

from JH_AiK import UI_AiK_x5

from flask import Flask
from flask import request
from flask_restful import Api, Resource, reqparse

import tensorflow.compat.v1 as tf
CUDA_VISIBLE_DEVICES=0
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
tf.keras.backend.set_session(tf.Session(config=config))

app = Flask (__name__)


class test_aik(Resource):
    def get(self):
        try:
            feature = request.get_json()
            idd = pd.DataFrame(feature)
            path_in="./JH_AiK/aik_input.tsv"
            idd.to_csv("./JH_AiK/aik_input.tsv", sep='\t',index=False)
            
            fn_mkdata="./JH_AiK/aik_kis.tsv" #kid,id,smi
            UI_AiK_x5.make_in(path_in,fn_mkdata)
            UI_AiK_x5.ex_doit("UI_AiK",fn_mkdata)
            df_all_json = UI_AiK_x5.pre_doit("UI_AiK")

            return df_all_json
        except Exception as e:
            return {'error': str(e)}

api = Api(app)
api.add_resource(test_aik,'/test_aik')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8105,threaded=False,debug=False)
