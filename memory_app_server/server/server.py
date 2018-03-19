from flask import Flask, redirect, json, request, make_response, Response
from flask_pymongo import PyMongo

# app = Flask(__name__)
name = 'memory_app'
app = Flask(name)
mongo = PyMongo(app)

# cannot do the below, error stating need to declare app_context?
# db = mongo.db


@app.route('/')
def index():
    # mongo.db.accounts.insert_one({
    #    '_id': 'dinho', 'memory_systems': {}  
    # })
    # return 'Hi there'
    return redirect('http://localhost:5000/account/dinho')


@app.route('/practise_words/')
def practise_words_show():
    words = mongo.db.practise_words.find_one()['words']
    # still need to json as list item returned from mongodb
    # is not callable (which is what flask tries to do with it)
    return json.jsonify(words)


@app.route('/account/<account_name>/')
def account_show(account_name):
    # mongodb returns a cursor or dict object depending on
    # whether find or find_one is used.
    # netiher can be used as is by flask, need to convert it.
    # Say to a JSON.
    account = mongo.db.accounts.find_one({"_id": account_name})
    return json.jsonify(account)


@app.route('/account/<account_name>/systems/<chosen_system>/', methods=['GET', 'POST'])
def account_memory_system_show(account_name, chosen_system):
    account = mongo.db.accounts.find_one({"_id": account_name})
    
    acceptable_systems = mongo.db.accepted_memory_systems.find()
    chosen_system_accepted = False

    for system in acceptable_systems:
        if chosen_system == system['system']:
            chosen_system_accepted = True
            break
    
    if not chosen_system_accepted:
        return json.jsonify({"error": "Memory system chosen is unavailable."})


    if request.method == 'GET':
        try:
            memory_system_response = account['memory_systems'][chosen_system]
            return json.jsonify(memory_system_response)
        except KeyError:
            # I shouldn't do the below, it creates on a GET route
            # not safe, and not expected behaviour of route
            # 
            # mongo.db.accounts.update_one({"_id": account_name}, 
            #                             {'$set': {'memory_systems': {chosen_system: {}}}})
            # updated_account = mongo.db.accounts.find_one({"_id": account_name})
            # memory_system_response = updated_account['memory_systems'][chosen_system]
            return json.jsonify({})
    else:
        body = request.get_json()
        # print(body)

        data_for_update = {'memory_systems': {chosen_system: body}}
        mongo.db.accounts.update_one({"_id": account_name}, {'$set': data_for_update})

        # below returns hi
        # return Response({"hi": "hello"}, 201)
        
        # below returns olahi
        # return Response({"hi": "hello", "ola": "yola"}, 201)

        # below returns Data saved
        # return Response('Data saved', 201)

        # this returns the body, and the status
        # json.jsonify wasn't working (not shown not working here) as it comes  
        # as a single dict. json.dumps just returns an array with the jsonified matter
        # error, which is therefore iterable which is one of the errors wthat appeared
        # when trying to use jsonify. Jsonify also comes with a status.

        # return Response(json.dumps({"hi": "hello", "ola": "yola"}), 201)
        return Response(json.dumps(body), 201)

        # below has same problem as earlier responses where it returns the keys
        # looks to be getting all the keys, iterating through them, concatenation them
        # all and returning that as the body, using dumps as above fixes that and
        # returns the full json/dictionary
        # return Response(body, 201)

# trying to do it the below way is not welcome by Flask, methods should be contained
# # within one route, does not like same route name appearing more than once
# @app.route('/account/<account_name>/systems/<chosen_system>/', method=['POST'])
# def test_blah(account_name, chosen_system):
#     return 'haha'


