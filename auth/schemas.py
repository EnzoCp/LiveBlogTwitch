from ninja import Schema


class LoginSchema(Schema):
    username: str
    password: str


class TokenPayload(Schema):
    user_id: int