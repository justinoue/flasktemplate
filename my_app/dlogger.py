import config
import logging
import sys
import os
import pprint
from flask import request

dlogger1 = logging.getLogger(__name__)

enable_airbrake = config.airbrake['enabled']

if enable_airbrake:
  import airbrake
  os.environ['AIRBRAKE_API_KEY'] = config.airbrake['api_key']
  os.environ['AIRBRAKE_PROJECT_ID'] = config.airbrake['project_id']
  os.environ['AIRBRAKE_ENVIRONMENT'] = config.airbrake['env']
  dlogger2 = airbrake.getLogger()

def info(i):
  dlogger1.info(i)
  log_debug(i)

def log(e):
  log_classic(e)
  if enable_airbrake:
    log_airbrake(e)

def log_debug(i):
  if config.server['debug']:
    print('\n\n')
    pprint.pprint(i)
    print('\n')

def log_classic(e):
  dlogger1.error(e)

def log_airbrake(e):
  try:
    d = {
      'url': request.url,
      'path': request.path,
      'method': request.method,
      'values': request.values,
      'body': request.data.decode(),
      'headers': request.headers,
      'remote_addr': request.remote_addr
    }

    try:
      d['headers'] = []
      for h in request.headers:
        d['headers'].append({h[0]: h[1]})
    except Exception as ex:
      pass

    dlogger2.exception(e, extra=d)
  except Exception as ex:
    dlogger2.exception(e)
