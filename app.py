# app.py

import os

import boto3 #kit SDK AWS per Python

from flask import Flask, jsonify, request #jsonify converte output Json in un oggetto
app = Flask(__name__) #crea istanza di un oggetto Flask

USERS_TABLE = os.environ['USERS_TABLE'] #os.environ restituisce un dizionario di variabili ambientali
client = boto3.client('dynamodb') #crea un client di servizio di basso livello 

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/users")
def get_users():
    resp = client.scan(
        TableName=USERS_TABLE
    )
    items = resp['Items']

    return jsonify(items)

@app.route("/users/<string:user_id>")
def get_user(user_id):
    resp = client.get_item( #metodo get_item restituisce un set di attributi per l'elemento con la chiave primaria data
        TableName=USERS_TABLE,
        Key={
            'userId': { 'S': user_id } #S indica attributo di tipo string
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'User does not exist'}), 404

    return jsonify({
        'userId': item.get('userId').get('S'),
        'name': item.get('name').get('S')
    })


@app.route("/users", methods=["POST"])
def create_user():
    user_id = request.json.get('userId')
    name = request.json.get('name')
    if not user_id or not name:
        return jsonify({'error': 'Please provide userId and name'}), 400

    resp = client.put_item(
        TableName=USERS_TABLE,
        Item={
            'userId': {'S': user_id },
            'name': {'S': name }
        }
    )

    return jsonify({
        'userId': user_id,
        'name': name
    })

