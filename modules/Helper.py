import os
import os.path

class Helper(object):
    def readHelper(self, name):
        if not hasattr(self, name):
            if os.path.isfile('./helpers/%s.py' % name):
                helper = __import__('helpers.%s' % name)
                helper = getattr(helper, name)
                helper = getattr(helper, name)()
                setattr(self, name, helper)
            else:
                raise HelperNotFound('helper %s is not found' % name)
        return getattr(self, name)

    def getHelper(self, name):
        return getattr(self, name)
