#from crypt import methods
import os
#from socket import J1939_MAX_UNICAST_ADDR
from turtle import title
from urllib.robotparser import RequestRate
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import  setup_db, Drink
from .auth.auth import AuthError, requires_auth
#from .database.models import db_drop_and_create_all

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''

#db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
# Get drinks
@app.route('/drinks', methods=['GET'])
def Get_Drinks():
    try:
        drinks_all = Drink.query.all()
        if drinks_all is None:
            abort(404)
        drinks_all_shorts = [drink.short() for drink in drinks_all]
        return jsonify (
            {'success':True,
            'drinks': drinks_all_shorts}
        , 200)
    except:
        abort(404)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
# Get details of the drinks
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_det(payload):
    try:
        drinks_details = Drink.query.order_by(Drink.id).all()
        if drinks_details is None:
            abort(404)
        drinks_details_shorts = [drink.short for drink in drinks_details]
        return jsonify({
            'success':True,
            'drinks':drinks_details_shorts
        }, 200)
    except:
        abort(404)

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def Post_Drinks(payload):
    try:
        data_post = request.get_json()
        title = data_post.get('title', None)
        recipe = data_post.get('recipe', None)

        if title is None or recipe is None:
            abort(404)
        drink_post = Drink(title=title, recipe=json.dumps(recipe))

        drink_post.insert()

        return jsonify({
            'success': True,
            'drinks': [drink_post.long()]
        }, 200)

    except:
        abort(404)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
# Modify the specific drink by the method PATCH:
@app.route('/drinks/<d_id>',methods=["PATCH"])
@requires_auth('patch:drinks')
def patch_drink_details(payload, d_id):
    try:
        drink_to_patch = Drink.query.get(d_id)
        if not drink_to_patch:
            abort(404)
        data = request.get_json()
        title = data.get('title')
        recipe = data.get('recipe')
        if title is not None:
            drink_to_patch.title = title
        if recipe is not None:
            drink_to_patch.recipe = recipe
        
        drink_to_patch.update()
        return jsonify({
            'success': True,
            'drinks': [drink_to_patch.long()]
        }, 200)
    except:
        abort(404)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
# Delete a drinks by the id : 
@app.route('/drinks/<d_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink_by_id(payload, d_id):
    try:
        drink_id = Drink.query.get(d_id)
        if not drink_id:
            abort(404)
        drink_id.delete()
        return jsonify({

            'success': True,
            'delete': d_id
        }, 200)
    except:
        abort(44) 
    

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404
'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def handle_auth(e):
    return jsonify({
        "success": False,
        "error": e.status_code,
        'message': e.error
    }), 401