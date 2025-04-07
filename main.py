from flask import Flask, jsonify, request
from DAL.db_utils import load_users
from user_parsers import parse_users, parse_user
from DAL.db_utils import save_user_to_json
from DAL.db_utils import override_all_users
from user_parsers import UserDict
from models import User
from user_validators import is_valid_phone
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "idan_super_secret"

from functools import wraps
from flask import request, jsonify

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None


        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        user_id = verify_token(token)
        if not user_id:
            return jsonify({"message": "Token is invalid or expired"}), 401

        return f(user_id=user_id, *args, **kwargs)
    return decorated



def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["user_id"]
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Token invalid

import json
import bcrypt
app = Flask(__name__)
VALID_ADDRESSES = ["tel aviv", "jerusalem", "kfar-saba", "petah tikwa"]



SECRET_KEY = "idan_super_secret"

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["user_id"]
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Token invalid

# Get all user names
@app.route("/users", methods=["GET"])
@token_required
def get_users(user_id):
    users = parse_users(load_users())
    return jsonify([user.name for user in users.values()])

@app.route("/users/<name>", methods=["DELETE"])
def delete_user_by_name(name):
    users = parse_users(load_users())
    for user_id in users.keys():
        if users[user_id].name == name:
            print(users[user_id])
            del users[user_id]
            break
    users_dict = uppacking_users_to_json(users)
    override_all_users(users_dict)
    return jsonify({"message": "user deleted"}), 201


    return jsonify({"error": "user not found"}), 404

def uppacking_users_to_json(users_array: [User]) -> UserDict:
    user_dict = {}
    for user in users_array.values():
        user_json = {"id":str(user.id), "phone":str(user.phone), "name": str(user.name), "adress":str(user.address)}
        user_dict[user.id] = user_json
    return user_dict
# Get user details by name
@app.route("/users/<name>", methods=["GET"])
def get_user_by_name(name):
    users = parse_users(load_users())
    for user in users.values():
        if user.name == name:
            return jsonify(user)
    return jsonify({"error": "user not found"}), 404

@app.route("/users/<id>", methods=["PATCH"])
def update_user_details(id):
    new_user_object = request.json
    curr_user_object = load_users()[id]
    new_address, new_phone = new_user_object["address"],  new_user_object["phone"]
    if new_address not in VALID_ADDRESSES:
        return jsonify({"message": "address is not valid"}), 400
    if not is_valid_phone(new_phone):
        return jsonify({"message": "phone is not valid"}), 400
    update_user_json_details(id, new_address, new_phone)
    # if curr_user_object["address"] == new_address and curr_user_object["phone"] == new_phone:
    #        return jsonify({"message": "address and phone are equal to previous "}), 201
    save_user_updates(curr_user_object, new_user_object)
    return jsonify({"message": "user details updated"}), 201

def save_user_updates(old_user_values: dict, new_user_values: dict) -> None:

    with open("logs.json", "r") as file:
        current_logs = json.load(file)
        print(current_logs)

    with open("logs.json","w") as file:
        update_user_dict_object = {}
        formatted = datetime.now.strftime("%Y-%m-%d %H:%M:%S")
        current_logs[formatted] = {"old_details":old_user_values, "new_details": new_user_values }
        json.dump(current_logs, file, indent=4)



# Create a new user
@app.route("/users", methods=["POST"])
def create_user():
    user_dict = request.json
    parsed_user = parse_user(user_dict)
    if user_dict == None:
        return
    result = save_user_to_json(parsed_user)
    if result == 0:
        return jsonify({"message": "user already exists"}), 409
    return jsonify({"message": "user created"}), 201

def update_user_json_details(id: str, address: str, phone: str) -> None:
    current_users_dict = load_users()
    current_users_dict[id]["address"] = address
    current_users_dict[id]["phone"] = phone
    override_all_users(current_users_dict)


@app.route("/register", methods=["POST"])
def register():
    userdata = request.json
    password = userdata["password"]
    userdata["password"] = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    parsed_user = parse_user(userdata)
    result = save_user_to_json(parsed_user)
    # if result == 0:
    #     return jsonify({"message": "User already exists"}), 409
    return jsonify({"message": "User registered"}), 201


@app.route("/login", methods=["POST"])
def login():
    password = request.json["password"]
    id = request.json["id"]
    if id in load_users().keys():
        password_validation = bcrypt.checkpw(password.encode(), load_users()[id]["password"].encode() )
        if password_validation:
            token = generate_token(id)

            return jsonify({"message": "Successful login", "token": token},), 201

    return jsonify({"message": "Password is not matched."}), 400


# Start server and load initial users
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4500)
