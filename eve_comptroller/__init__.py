from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config

from eve_comptroller import settings as app_config
from eve_comptroller.models import DBSession, Base
from eve_comptroller.auth import list_groups


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    
    authn_policy = AuthTktAuthenticationPolicy(settings['eve_comptroller.authn_secret'],
                                               callback=list_groups,
                                               hashalg=app_config.auth_hmac,
                                               timeout=app_config.auth_max_age,
                                               max_age=app_config.auth_max_age)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('root', '/')
    config.add_route('register', '/auth/register')
    config.add_route('activate', '/auth/activate')
    config.add_route('login', '/auth/login')
    config.add_route('app', '/app/*traverse',
                     factory='eve_comptroller.resources.bootstrap')
    config.scan('.views')
    return config.make_wsgi_app()
