from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import json
import requests
from fuzzywuzzy import process
import time
import calendar

from calc import Calculator

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class AppContext(metaclass=SingletonMeta):
    _app = None

    @classmethod
    def app(cls):
        if cls._app is None:
            cls._app = Flask(__name__)
        return cls._app

appcontext = AppContext()
app = appcontext.app()
api = Api(app, version='1.0', title='a calculator api',description='a calculator api',)
CORS(app, resources={r'/*': {'origins': '*'}})
ns = api.namespace('calculon', description='an pretty simple calculator')

@ns.route('/calc/')
class Calc(Resource):

    @ns.doc('post')
    def post(self):
      json_data = request.get_json(force=True)
      oper = json_data['operation']
      result = 0
      if oper == '*':
         c = Calculator()
         result = c.multiply(json_data['num1'],json_data['num2'])
      if oper == '/':
         c = Calculator()
         result = c.devide(json_data['num1'],json_data['num2'])
      if oper == '+':
         c = Calculator()
         result = c.add(json_data['num1'],json_data['num2'])
      if oper == '-':
         c = Calculator()
         result = c.subtract(json_data['num1'],json_data['num2'])
      return {'result': '{}'.format(result)}   



if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000)


