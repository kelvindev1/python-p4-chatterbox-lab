from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.order_by(Message.created_at.asc()).all()]
        response =  make_response(messages, 200)
        return response
    
    elif request.method == 'POST':
        json_data = request.get_json()
        new_message = Message(
            body = json_data.get("body"),
            username = json_data.get("username")
        )
        db.session.add(new_message)
        db.session.commit()

        news_message_dict = new_message.to_dict()
        response = make_response(news_message_dict, 201)
        return response



@app.route('/messages/<int:id>', methods = ['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if request.method == 'PATCH':
        updated_message = request.get_json()
        for attr in updated_message:
            setattr(message, attr, updated_message.get(attr))
            db.session.commit()
            
            message_dict = message.to_dict()
            response = make_response(message_dict, 200)
            return response
        
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {"Sucess": True, "message": "Message deleted"}
        return response_body

if __name__ == '__main__':
    app.run(port=5555, debug=True)
