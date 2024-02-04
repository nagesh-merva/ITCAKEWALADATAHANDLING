
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS 
import os

app = Flask(__name__)
CORS(app, supports_credentials=True, allow_headers=["Content-Type"], methods=["OPTIONS", "POST"]) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ordersDATA.db')



db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    with_egg = db.Column(db.Boolean, nullable=False)
    eggless = db.Column(db.Boolean, nullable=False)
    message = db.Column(db.String(200), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    product_price = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Todo {self.id}>'
    
    
@app.route('/')
def index():
    tasks = Todo.query.order_by(Todo.date_created.desc()).all()
    return render_template('index.html', tasks=tasks)

@app.route('/api/save_form_data', methods=['POST', 'OPTIONS'])
def save_form_data():
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight request handled"}), 200
    data = request.json
    print("Received form data:", data) 

    new_todo = Todo(
        location=data['location'],
        contact =data['contact'],
        date=data['date'],
        with_egg=data['withEgg'],
        eggless=data['eggless'],
        message=data['message'],
        product_name=data['productNametxt'],
        product_price=data['productPricetxt'],
        action=data['action']
    )

    try:
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({"message": "Form data added to the database successfully"}), 201
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({"message": "Failed to add form data to the database"}), 500
    
    
#****** DONT TOUCH ********** for use of deleting the database ****** DONT TOUCH **********
# @app.route('/api/empty_database', methods=['POST'])
# def empty_database():
#     try:
#         Todo.query.delete()
#         db.session.commit()
#         return jsonify({"message": "Database emptied successfully"}), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         db.session.rollback()
#         return jsonify({"message": "Failed to empty the database"}), 500

with app.app_context():
    db.create_all()

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500

