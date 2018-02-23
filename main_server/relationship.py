from person import Person
import tools

class RelationShip(object):
    confidence = 0.0
    def __init__(self, confidence):
        self.confidence = confidence

    def __str__(self):
        return 'base relation'

class FamilyRelationShip(RelationShip):
    def __str__(self):
        return 'family relation: {}'.format(str(self.confidence))

class WorkRelationShip(RelationShip):
    def __str__(self):
        return 'work relation: {}'.format(str(self.confidence))

# Return an instance of the RelationShip
def find_realations(person_1: Person, person_2: Person):
    fam_score = check_family(person_1, person_2)
    work_score = check_work(person_1, person_2)
    if fam_score >= 0.4:
        yield FamilyRelationShip(fam_score)
    if work_score >= 0.5:
        yield FamilyRelationShip(fam_score)

# Some evristics
def check_family(person_1: Person, person_2: Person):
    confidence = 0.0
    if tools.acceptable_pref(person_1.surname, person_1.surname, 2):
        confidence += 0.3
    p1_estate = set([(estate['reg_id'], estate['square']) for estate in person_1.real_estate])
    p2_estate = set([(estate['reg_id'], estate['square']) for estate in person_2.real_estate])
    if (len(p1_estate & p2_estate) != 0):
        confidence += 0.3

    has_common_reigon = tools.has_intersection(person_1.region_info,
                                               person_2.region_info)
    if has_common_reigon:
        confidence += 0.1

    is_child = tools.acceptable_pref(person_1.name, person_2.patr_name, 1)\
                or tools.acceptable_pref(person_2.name, person_1.patr_name, 1)
    if is_child:
        confidence += 0.1

    return confidence

def check_work(person_1: Person, person_2: Person):
    has_common_reigon = tools.has_intersection(person_1.region_info,
                                               person_2.region_info)
    if not has_common_reigon:
        return 0.0
    confidence = 0.5
    p1_work = set(person_1.work_info)
    p2_work = set(person_2.work_info)
    if len(p1_work & p2_work) != 0:
        confidence += 0.5
    return confidence
