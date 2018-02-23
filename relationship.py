from person import Person
import tools

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

def check_family(person_1, person_2):
    for id in person_1.relative_info:
        if id == person_2.id:
            return True
    mlen = min(len(person_1.surname), len(person_2.surname))
    if tools.common_pref_len(person_1.surname, person_1.surname)  >= mlen - 2:
        return True
    return False
