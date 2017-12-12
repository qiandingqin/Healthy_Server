#encoding=utf-8
from flask import Flask
from controller.index import model as index
from controller.user import model as user

app = Flask(__name__)
app.register_blueprint(index, )
app.register_blueprint(user, )
