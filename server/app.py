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

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = [msg.to_dict() for msg in Message.query.all()]
        resp = make_response(messages, 200)
        return resp

    elif request.method == 'POST':
        message = Message(
            body=request.json.get('body'),
            username=request.json.get('username')
        )
        db.session.add(message)
        db.session.commit()

        msg_dict = message.to_dict()
        resp = make_response(msg_dict, 201)
        return resp

@app.route('/messages/<int:id>', methods=['GET','PATCH', 'DELETE'])
def messages_by_id(id):
    if request.method == 'GET':
        message = Message.query.filter(Message.id == id).first()
        resp = jsonify({
            'id': message.id,
            'body': message.body,
            'username': message.username,
            'created_at': message.created_at,
            'updated_at': message.updated_at
        })
        return resp, 200
    
    if request.method == 'PATCH':
        message = Message.query.filter(Message.id == id).first()
        for attr in request.json:
            setattr(message, attr, request.json.get(attr))
        
        db.session.add(message)
        db.session.commit()

        resp = jsonify({
            'id': message.id,
            'body': message.body,
            'username': message.username,
            'created_at': message.created_at,
            'updated_at': message.updated_at
        })
        return resp
    
    elif request.method == 'DELETE':
        message = Message.query.filter(Message.id == id).first()
        db.session.delete(message)
        db.session.commit()

        resp_body = {
            'delete_success': True,
            'message': "Deletion Successful"
        }
        resp = jsonify(resp_body)
        return resp, 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
