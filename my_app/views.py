from flask import jsonify
from my_app import application, decorators, dlogger
#from my_app.handlers import

@application.route('/', methods=["GET"])
def index():
  return jsonify({"message": "hi!"})
