# import flask dependencies
from flask import Flask, request, make_response, jsonify
import json
from wordgame import get_first_word

# initialize the flask app
app = Flask(__name__)
log = app.logger

# default route
@app.route('/')
def index():
    return 'Hello World!'

# function for responses
def results(res):
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    action = req.get('queryResult').get('action')

    # return a fulfillment response
    return {'fulfillment_messages': [{'text': {'text': [res]}}]}

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
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

    if action == 'first':
        res = get_first_word()
    
    print('Action: ' + action)
    print('Response: ' + res)
    
    return make_response(jsonify(results(res)))

# run the app
if __name__ == '__main__':
   app.run()