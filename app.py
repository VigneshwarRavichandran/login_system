from flask import request, Flask, jsonify
from operations import Operate

app = Flask(__name__) 

db = Operate(app)

@app.route('/register', methods=['POST'])
def register():
    # Request a json content with username and password for register
    data = request.get_json()
    username = data['username']
    password = data['password']
    # Check whether the username already exists
    if db.existing_username(username):
        return jsonify({
            "message" : "Username already exists"
            })
    else:
        # Create a new user
        db.create_user(username, password)
        return jsonify({
            "message" : "New user created"
            })


@app.route('/login', methods=['POST'])
def login():
    # Request a json content with username and password for login
    data = request.get_json()
    username = data['username']
    password = data['password']
    # Check whether the user credentials are valid
    if db.existing_user(username, password):
        # Get the user token and return the user token
        user_token = db.get_token(username, password)
        return jsonify(user_token)
    else:
        return jsonify({
            "message" : "invalid user"
            })

@app.route('/show', methods=['GET'])
def show():
    # Request a header with user token
    user_token = request.headers['Authorization']
    # Check whether the user token is valid
    if db.existing_token(user_token):
        # Show the content for authorised user
        show_content = db.get_content()
        return jsonify(show_content)
    else:
        return jsonify({
        "message" : "Unauthorized user"
        })


if __name__ == '__main__':
    app.run(debug=True)
