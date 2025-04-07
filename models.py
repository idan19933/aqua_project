from dataclasses import dataclass


@dataclass
class User:
    id: str
    phone: str
    name: str
    address: str
    password: str
