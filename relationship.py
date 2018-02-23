from person import Person

class RelationShip(object):
    def __str__(self):
        return 'base relation'

class FamilyRelationShip(RelationShip):
    def __str__(self):
        return 'family relation'

class WorkRelationShip(RelationShip):
    def __str__(self):
        return 'work relation'

# Return an instance of the RelationShip
def find_realation(person_1, person_2):
    pass
