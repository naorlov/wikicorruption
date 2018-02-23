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

# Some evristics
def check_family(person_1, person_2):
    if tools.acceptable_pref(person_1.surname, person_1.surname, 2):
        return True
    p1_estate = person_1.real_estates
    has_common_estate = tools.has_intersection(person_1.real_estates,
                                               person_2.real_estate)
    has_common_reigon = tools.has_intersection(person_1.region_info,
                                               person_2.region_info)
    is_child = tools.acceptable_pref(person_1.name, person_2.patr_name, 1)\
                or tools.acceptable_pref(person_2.name, person_1.patr_name, 1) 
    return False
