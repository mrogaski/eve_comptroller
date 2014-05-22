from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .resources import (Root,
                        Registration,
                        Activation, 
                        Preferences, 
                        Admin)

from .models import (DBSession,
                     MyModel)


class EveComptrollerViews(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(renderer='templates/home.html')
    def home(self):
        page_title = 'Home'
        try:
            one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
        except DBAPIError:
            return Response(conn_err_msg, content_type='text/plain', status_int=500)
        return dict(page_title=page_title)

    conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_eve_comptroller_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

    @view_config(context=Registration, 
                 renderer='templates/register.html')
    def register(self):
        page_title = 'Register'
        return dict(page_title=page_title)

