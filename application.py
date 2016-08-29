import os
import json
import config
import logging
import sys
from flask import Flask, jsonify

#determine environment
if 'APP_ENV' in os.environ:
  app_env = os.environ['APP_ENV']
else:
  app_env = 'development'
  logging.basicConfig(filename='log/{}.log'.format(app_env), level=logging.INFO)

#load config
with open('config/{}.json'.format(app_env)) as data_file:
  jsonConfig = json.load(data_file)
  for key in jsonConfig:
    setattr(config, key, jsonConfig[key])

#set up the app.
from my_app import application
application = application

if __name__ == '__main__':  
  logging.info('\n\nBootin up My App...\n\n')
  print('\n\nBootin up My App...\n')
  print('http://{}:{}\n'.format(config.server['hostname'], config.server['port']))
  application.run(
    debug=config.server['debug'],
    host=config.server['hostname'],
    port=config.server['port']
  )
