import os, sys
sys.path.append('./JH_AiG')
import numpy as np
import pandas as pd

import tensorflow as tf

from JH_AiG import UI_AiG_x5

from flask import Flask
from flask import request
from flask_restful import Api, Resource, reqparse

import tensorflow.compat.v1 as tf
CUDA_VISIBLE_DEVICES=0
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
tf.keras.backend.set_session(tf.Session(config=config))

app = Flask (__name__)


class test_aig(Resource):
    def get(self):
        try:
            feature = request.get_json()
            idd = pd.DataFrame(feature)
            #make ligands.tsv file
            path_in="./input.tsv"
            idd.to_csv("./input.tsv", sep='\t',index=False)
            UI_AiG_x5.read_input("aig_test", path_in)

            #make gxy
            UI_AiG_x5.make_gxy("aig_test", path_in)


            #make midsmi.tsv file
            l_midsmi = UI_AiG_x5.get_midsmi_to_calc("./JH_AiG/gpro_data/hmm_gpro_v02/sel_hmm_aln.fas", "aig_test")

            print("\n\n Start Make descriptor >>y>>>")
            l_set_pid = UI_AiG_x5.ex_doit("aig_test", "./JH_AiG/gpro_data/hmm_gpro_v02/sel_hmm_aln.fas")

            df_all_json = UI_AiG_x5.pre_doit("aig_test",l_set_pid)

            return df_all_json
        except Exception as e:
            return {'error': str(e)}

api = Api(app)
api.add_resource(test_aig,'/test_aig')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8107,threaded=False,debug=False)
