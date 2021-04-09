from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from ninja import Router
from .jwt import AuthBearer, AuthBearerSuperUser, create_token, get_current_user
from ninja import Form
from django.contrib.auth.models import User
from .schemas import LoginSchema
from django.contrib.auth import logout

router = Router()


@router.post('/signup/')
def signup(request, payload: LoginSchema):
    pay = dict(payload)
    user = User.objects.create(username=pay['username'])
    user.set_password(raw_password=pay['password'])
    print(user.id)
    user.save()
    return f'User created'


@router.post('/login/')
def login(request, payload: LoginSchema):
    pay = dict(payload)
    print(pay)
    user = get_object_or_404(User, username=pay['username'])
    if check_password(pay['password'], user.password):
        token = create_token(user.id)
        return {
            'Credentials': token,
            'User': {
                'username': user.username,
                'user_id': user.id,
            },
        }

