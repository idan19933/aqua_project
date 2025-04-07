import json
from dataclasses import asdict
from flask import Flask, jsonify

from models import User

USER_FILE_PATH = "DAL/users.json"  # Will hold the JSON file path


def load_users() -> dict:
    with open(USER_FILE_PATH, "r") as users_file:
        return json.load(users_file)


def save_user_to_json(user: User) -> None:
    current_users_dict = load_users()
    if user.id in current_users_dict.keys():
        return  0
    current_users_dict[user.id] = asdict(user)
    with open(USER_FILE_PATH, "w") as f:
        json.dump(current_users_dict, f, indent=4)





def override_all_users(users: dict):
    with open(USER_FILE_PATH, "w") as f:
        json.dump(users, f, indent=4)

