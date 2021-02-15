from dataclasses import dataclass


@dataclass
class DBData:
    def __init__(self, name: str, password: str, description: str = None) -> None:
        if not name or not isinstance(name, str):
            raise TypeError("name is None or not a string")
        if not password or not isinstance(password, str):
            raise TypeError("password is None or not a string")
        if not isinstance(description, str):
            raise TypeError("description is not a string")
        self.name = name
        self.password = password
        self.description = description

    def __str__(self):
        return str(f"DBData: {self.name} {self.password} {self.description}")