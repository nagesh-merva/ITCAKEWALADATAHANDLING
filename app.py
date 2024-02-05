from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, supports_credentials=True, allow_headers=["Content-Type"], methods=["OPTIONS", "POST"])

# Set your MongoDB Atlas connection string here
mongo_uri = 'mongodb+srv://ITcakewala_data:hP6XmyvfGtWtjWsL@cluster0.inknx40.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(mongo_uri)
db = client['ITcakewaladatabase']

# Your Todo model definition
class Todo:
    def __init__(self, data):
        self.collection = db['todos']
        self.data = data

    def save(self):
        self.collection.insert_one(self.data)

@app.route('/')
def index():
    tasks = db.todos.find().sort('date_created', -1)
    return render_template('index.html', tasks=tasks)

@app.route('/api/save_form_data', methods=['POST', 'OPTIONS'])
def save_form_data():
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight request handled"}), 200
    data = request.json
    print("Received form data:", data)

    new_todo = Todo({
        'location': data['location'],
        'contact': data['contact'],
        'date': data['date'],
        'with_egg': data['withEgg'],
        'eggless': data['eggless'],
        'message': data['message'],
        'product_name': data['productNametxt'],
        'product_price': data['productPricetxt'],
        'action': data['action'],
        'date_created': datetime.utcnow()
    })

    try:
        new_todo.save()
        return jsonify({"message": "Form data added to the database successfully"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to add form data to the database"}), 500

if __name__ == '__main__':
    app.run(debug=True)
