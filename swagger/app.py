from flask import Flask
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from flask_restplus import Resource, Api,reqparse, Namespace
from todo import Todo
from todo_1 import Todo_1

app = Flask(__name__)
api = Api(app, version='1.0', title='Description API',
          description='Azothbio Platform API Description',
          contact="evahong@azothbio.com",
          license="AzothBio")
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
api.add_namespace(Todo, '/')
api.add_namespace(Todo_1, '/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8108, debug=True)
