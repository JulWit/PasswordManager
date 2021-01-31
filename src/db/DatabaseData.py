
class DatabaseData:
    def __init__(self, name, password, description=None):
        if not name or not isinstance(name, str):
            raise TypeError("name is None or not a string")
        if not password or not isinstance(password, str):
            raise TypeError("password is None or not a string")
        if not isinstance(description, str):
            raise TypeError("description is not a string")
        self._name = name
        self._password = password
        self._description = description

    def __str__(self):
        return str(f"DatabaseData: {self._name}, {self._password}, {self._description}")

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        self._password = password

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        self._description = description
