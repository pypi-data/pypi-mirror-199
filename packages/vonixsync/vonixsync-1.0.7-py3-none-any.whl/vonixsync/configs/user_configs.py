class UserConfigs:
    def __init__(self, token):
        self.__token = token

    def auth_header(self):
        return {"Authorization": f"Bearer {self.__token}"}

    def token(self):
        return self.__token
