from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
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
