from user_validators import is_valid_id, is_valid_phone
from models import User

UserDict = dict[str, User]


def parse_users(users: dict) -> UserDict:
    users_map: UserDict = dict()

    for user_id in users:
        user_dict = users[user_id]
        user = parse_user(user_dict)
        if user:
            users_map[user_id] = user

    return users_map


def parse_user(user: dict):
    id = user.get("id", "")
    phone = user.get("phone", "")
    name = user.get("name", "")
    address = user.get("address", "")
    password = user.get("password", "")

    if is_valid_id(id) and is_valid_phone(phone):
        return User(id=id, phone=phone, name=name, address=address, password=password)
    else:

        if not is_valid_id(id):
            raise ValueError(f"User id of {name} is invalid.")

        elif not is_valid_phone(phone):
            raise ValueError(f"Phone number of {name} is invalid.")

