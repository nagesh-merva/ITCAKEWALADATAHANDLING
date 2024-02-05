from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True, allow_headers=["Content-Type"], methods=["OPTIONS", "POST"])

mongo_uri = 'mongodb+srv://ITcakewala_data:hP6XmyvfGtWtjWsL@cluster0.inknx40.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(mongo_uri)
db = client['ITcakewaladatabase']

class Todo:
    def __init__(self, data):
        self.collection = db['todos']
        self.data = data

    def save(self):
        self.collection.insert_one(self.data)

def index():
    tasks_cursor = Todo.query.order_by(Todo.date_created.desc())
    tasks = list(tasks_cursor)
    
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
