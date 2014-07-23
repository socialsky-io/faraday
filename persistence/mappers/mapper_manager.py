'''
Faraday Penetration Test IDE - Community Version
Copyright (C) 2013  Infobyte LLC (http://www.infobytesec.com/)
See the file 'doc/LICENSE' for the license information

'''


from persistence.mappers.data_mappers import Mappers

# NOTE: This class is intended to be instantiated by the
# service or controller that needs it.
# IMPORTANT: There should be only one instance of this
# class, since it creates the datamappers and those should
# be unique too (they have identity maps for every model object)


class MapperManager(object):
    def __init__(self):
        # create and store the datamappers
        self.mappers = {}

    def createMappers(self, dbconnector):
        self.mappers.clear()
        for tmapper, mapper in Mappers.items():
            self.mappers[tmapper] = mapper(self, dbconnector)

    def save(self, obj):
        if self.mappers.get(obj.__class__.__name__, None):
            self.mappers.get(obj.__class__.__name__).save(obj)
            return True
        return False

    def find(self, obj_id):
        mappers = list(self.mappers.values())
        while len(mappers):
            mapper = mappers.pop()
            obj = mapper.find(obj_id)
            if obj:
                return obj
        return None

    def remove(self, obj_id):
        obj = self.find(obj_id)
        if obj:
            self.mappers.get(obj.__class__.__name__).delete(obj_id)
            return True
        return False

    def getMapper(self, type):
        return self.mappers.get(type, None)
