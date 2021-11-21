from flask import request
from flask_restplus import Resource, Api, Namespace, fields, reqparse

from JH_AiP import UI_aip_x5_l

#app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
todos_id = {}
todos_smile= {}
count =0 


Todo_1 = Namespace(
    name="Prediction available compound",
    description="예측 가능한 compound 기준.")

todo1_fields = Todo_1.model('AiP450', {  # Model 객체 생성
    'Organic compound' : fields.String(description = "Include only C,H,O,N,B,S,P,F,Cl,Br,I"),
    'Molecular weight' : fields.String(description='200~700'),
    '3D': fields.String(description='Generate 3d conformer descriptor'),
    'LatX' : fields.String(description='Generate latX desciptor'),
    })


@Todo_1.route('input/check_compound')
class TodoPost(Resource):
    @Todo_1.doc(params={'Organic compound':"Include only C,H,O,N,B,S,P,F,Cl,Br,I", 'Molecular weight':'Range in 200~700','3D':'Generate 3d conformer descriptor','LatX':'Generate latX desciptor'}) 
    def post(self):
        """predict cyp450 inhibitor."""


