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

class Accountant(Resource):
    pass

class PosManager(Resource):
    pass

root = Root('Home')

def bootstrap(request):
    if not root.values():
        root['acct'] = Accountant('acct', root, 'Accountant')
        root['pos'] = PosManager('pos', root, 'POS Manager')

    return root

