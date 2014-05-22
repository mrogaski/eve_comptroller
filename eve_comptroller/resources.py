class Resource(dict):
    def __init__(self, name, parent, title):
        self.__name__ = name
        self.__parent__ = parent
        self.title = title

class Root(Resource):
    __name__ = ''
    __parent__ = None
    def __init__(self, title):
        self.title = title

class Registration(Resource):
    pass

class Activation(Resource):
    pass
          
class Admin(Resource):
    pass

class Preferences(Resource):
    pass

root = Root('Home')

def bootstrap(request):
    if not root.values():
        root['register'] = Registration('register', root, 'Registration')
        root['activate'] = Activation('activate', root, 'Activation')
        root['pref'] = Preferences('pref', root, 'Preferences')
        root['admin'] = Admin('admin', root, 'Administration')

    return root

