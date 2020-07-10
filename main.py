# import flask dependencies
from flask import Flask, request, make_response, jsonify
import json
from wordgame import get_first_word
from wordgame import get_next_word_from_db

# initialize the flask app
app = Flask(__name__)
log = app.logger

# default route
@app.route('/')
def index():
    return 'Hello World!'

# function for responses
def results(res, source):
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    # action = req.get('queryResult').get('action')
    if source == 'df':
      # return formatted fulfillment response for requests from Dialogflow
      return {'fulfillment_messages': [{'text': {'text': [res]}}]}
    else:
      # return normal response for other sources
      return {'bot_word':{'word':res,'last_letter':res[-1]}}

# create a route for webhook
@app.route('/webhook', methods=['POST'])
def webhook(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    req = request.get_json(silent=True, force=True)
    source = ''
    try:
        action = req.get('queryResult').get('action')
        if 'source' in req:
          source = req.get('source')
        if 'user_word' in req:
          user_word = req.get('user_word')
        if 'level' in req:
          level = req.get('level')
    except AttributeError:
        return 'json error'

    if action == 'first':
        res = get_first_word()
    if action == 'getword':
        res = get_word(request)
        if res.startswith('ERROR'):
            return res
    
    print('Action: ' + action)
    print('Response: ' + res)
    return make_response(jsonify(results(res, source)))


def get_word(request):
  
  req = request.get_json(silent=True, force=True)
  level = '1'   # default level is 1
  source = ''   
  
  try:
    if 'user_word' in req:
      user_word = req.get('user_word')
    else:
      return 'Error: Missing user_word'
    if 'level' in req:
      level = req.get('level')
  except AttributeError:
    return 'json error'
  
  bot_word_dict = get_next_word_from_db(user_word,[],level)
  bot_word = bot_word_dict.get('word')
  if bot_word != '':
    return bot_word
  else:
    return bot_word_dict.get('error')

# Function to test the API from localhost
@app.route('/webhooklocal', methods=['POST'])
def webhooklocal():
  
  res = webhook (request)
  return res

# run the app
if __name__ == '__main__':
   app.run()