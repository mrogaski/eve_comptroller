import logging
log = logging.getLogger(__name__)

from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget

from sqlalchemy.exc import DBAPIError
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer


from eve_comptroller.models import DBSession, User
from eve_comptroller.resources import Resource, Accountant, PosManager
from eve_comptroller.auth import check_credentials
from eve_comptroller.forms import LoginSchema

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
        error_message = ''
        username = ''
        password = ''
        login_url = self.request.route_url('login')
        referer = self.request.referer
        if referer is None or referer == login_url:
            target = '/'
        else:
            target = referer

        form = Form(self.request,schema=LoginSchema())
        
        if form.validate():
            username = form.data['username']
            password = form.data['password']
            if check_credentials(username, password):
                headers = remember(self.request, username)
                return HTTPFound(location=target, headers=headers)
            else:
                error_message = 'Login failed; invalid username or password.'
                
        return dict(renderer=FormRenderer(form),
                    page_title=page_title,
                    error_message=error_message,
                    username=username,
                    password=password)
            


