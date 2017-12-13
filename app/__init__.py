#encoding=utf-8
from flask import Flask
from controller.index import model as index
from controller.user import model as user
from controller.seller import model as seller

app = Flask(__name__)
app.register_blueprint(index, )
app.register_blueprint(user, )
app.register_blueprint(seller,)
