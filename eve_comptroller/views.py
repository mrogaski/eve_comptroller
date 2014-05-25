from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .resources import (Resource,
                        Accountant,
                        PosManager)


class EveComptrollerViews(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(route_name='root', renderer='templates/home.html')
    def home(self):
        page_title = 'Home'
        return dict(page_title=page_title)

    @view_config(route_name='register',
                 renderer='templates/register.html')
    def register(self):
        page_title = 'Register'
        return dict(page_title=page_title)

    @view_config(route_name='activate',
                 renderer='templates/activate.html')
    def activate(self):
        page_title = 'Activate'
        return dict(page_title=page_title)

    @view_config(route_name='login',
                 renderer='templates/login.html')
    def login(self):
        page_title = 'Login'
        return dict(page_title=page_title)

