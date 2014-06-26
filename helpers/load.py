class load(object):
    def load(self, path):
        path = [i[0].lower() + i[1:] for i in path.split('_')]
        name = path[-1]
        path = '.'.join(path)
        inst = __import__(path)
        inst = getattr(inst, name)
        inst = getattr(inst, name)()
        return inst

