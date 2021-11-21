from flask import request
from flask_restplus import Resource, Api, Namespace, fields, reqparse

from JH_AiP import UI_aip_x5_l

#app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
todos_id = {}
todos_smile= {}
count =0 


Todo = Namespace(
    name="Platform",
    description="Platform description 작성하기 위해 사용하는 API.")

todo_fields = Todo.model('AiP450', {  # Model 객체 생성
    'version' : fields.String(example= "v1"),
    'model' : fields.String(example='cytochrome p450 1a2, 2c9, 2c19, 3a4, 2d6 type'),
    'id': fields.String(description='compound ID', required=True, example="imatinib"),
    'SMILES' : fields.String(description='compound smile code', required=True, example="CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5"),
    'result' : fields.String(description='inhibition probability in 10uM')
    })

todo_fields1 = Todo.model('AiGPro', {  # Model 객체 생성
    'version' : fields.String(example= "v1"),
    'model' : fields.String(example='G-protein inhibitor prediction'),
    'id': fields.String(description='compound ID', required=True, example="imatinib"),
    'SMILES' : fields.String(description='compound smile code', required=True, example="CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5"),
    #'result' : fields.String(description='log(IC50)', example="1uM = 0, 0.1uM = -2.3, 0.01uM = -4.6, 1nM = -6.9")
    'result' : fields.String(description='pIC50')
    })

todo_fields2 = Todo.model('AiKPro', {  # Model 객체 생성
    'version' : fields.String(example= "v1"),
    'model' : fields.String(example='Kinase inhibitor prediction'),
    'id': fields.String(description='compound ID', required=True, example="imatinib"),
    'SMILES' : fields.String(description='compound smile code', required=True, example="CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5"),
    'result' : fields.String(description='inhibition probability in 1uM')
    })

todo_fields3 = Todo.model('AiCAD', {  # Model 객체 생성
    'version' : fields.String(example= "v1"),
    'model' : fields.String(example='Cancer cell line drug prediction'),
    'id': fields.String(description='compound ID', required=True, example="imatinib"),
    'SMILES' : fields.String(description='compound smile code', required=True, example="CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5"),
    #'result' : fields.String(description='log(IC50)', example="1uM = 0, 0.1uM = -2.3, 0.01uM = -4.6, 1nM = -6.9")
    'result' : fields.String(description='pIC50')

    })

todo_fields4 = Todo.model('AiCADs', {  # Model 객체 생성
   'version' : fields.String(example= "v1"),
    'model' : fields.String(example='Cancer cell line(60) druc prediction'),
    'id': fields.String(description='compound ID', required=True, example="imatinib"),
    'SMILES' : fields.String(description='compound smile code', required=True, example="CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5"),
    'result' : fields.String(description='inhibition probability in 1uM')
    })

@Todo.route('input/AiP450')
class TodoPost(Resource):
    @Todo.expect(todo_fields)
    @Todo.response(201, 'Success')
    @Todo.response(404, 'Bad request')
    def post(self):
        """predict cyp450 inhibitor."""
        global count
        global todos_id
        global todos_smile
        todo_fields_with_id = Todo.inherit('Todo With ID', todo_fields, {'todo_id': fields.Integer(description='a Todo ID')})
        idx = count
        count += 1
        todos_id[idx] = request.json.get('id')
        todos_smile[idx] = request.json.get('SMILES')
        return {
            'todo_id': idx,
            'ID': todos_id[idx],
            'SMILES' : todos_smile[idx]
        }, 201


@Todo.route('input/AiGPro')
class TodoPost(Resource):
    @Todo.expect(todo_fields1)
    @Todo.response(201, 'Success')
    @Todo.response(404, 'Bad request')
    def post(self):
        """predict G-protein inhibitor."""
        global count
        global todos_id
        global todos_smile
        todo_fields_with_id = Todo.inherit('Todo With ID', todo_fields, {'todo_id': fields.Integer(description='a Todo ID')})
        idx = count
        count += 1
        todos_id[idx] = request.json.get('id')
        todos_smile[idx] = request.json.get('SMILES')
        return {
            'todo_id': idx,
            'ID': todos_id[idx],
            'SMILES' : todos_smile[idx]
        }, 201


@Todo.route('input/AiKPro')
class TodoPost(Resource):
    @Todo.expect(todo_fields2)
    @Todo.response(201, 'Success')
    @Todo.response(404, 'Bad request')
    def post(self):
        """predict Kinase inhibitor."""
        global count
        global todos_id
        global todos_smile
        todo_fields_with_id = Todo.inherit('Todo With ID', todo_fields, {'todo_id': fields.Integer(description='a Todo ID')})
        idx = count
        count += 1
        todos_id[idx] = request.json.get('id')
        todos_smile[idx] = request.json.get('SMILES')
        return {
            'todo_id': idx,
            'ID': todos_id[idx],
            'SMILES' : todos_smile[idx]
        }, 201

@Todo.route('input/AiCAD')
class TodoPost(Resource):
    @Todo.expect(todo_fields3)
    @Todo.response(201, 'Success')
    @Todo.response(404, 'Bad request')
    def post(self):
        """predict Cancer cell line inhibitor."""
        global count
        global todos_id
        global todos_smile
        todo_fields_with_id = Todo.inherit('Todo With ID', todo_fields, {'todo_id': fields.Integer(description='a Todo ID')})
        idx = count
        count += 1
        todos_id[idx] = request.json.get('id')
        todos_smile[idx] = request.json.get('SMILES')
        return {
            'todo_id': idx,
            'ID': todos_id[idx],
            'SMILES' : todos_smile[idx]
        }, 201


@Todo.route('input/AiCADs')
class TodoPost(Resource):
    @Todo.expect(todo_fields4)
    @Todo.response(201, 'Success')
    @Todo.response(404, 'Bad request')
    def post(self):
        """predict 60-cancer cell line inhibitor."""
        global count
        global todos_id
        global todos_smile
        todo_fields_with_id = Todo.inherit('Todo With ID', todo_fields, {'todo_id': fields.Integer(description='a Todo ID')})
        idx = count
        count += 1
        todos_id[idx] = request.json.get('id')
        todos_smile[idx] = request.json.get('SMILES')
        return {
            'todo_id': idx,
            'ID': todos_id[idx],
            'SMILES' : todos_smile[idx]
        }, 201

