class AuthroizedCodeVO:
    code = ""
    email = ""

    def __init__(self, code, email):
        self.code = code
        self.email = email

    @property
    def json(self):
        return {
            "code": self.code,
            "email": self.email,
        }
