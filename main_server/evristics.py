from person import Person
import tools


# Return an instance of the RelationShip
def get_true_evristics(person_1: Person, person_2: Person):
    true_evrs = []
    for evr_t in [CommonEstateEvr,
                CommonRigions,
                CommonWorkEvr,
                SurnameEvr,
                PatrNameEvr]:
        evr = evr_t()
        evr.fit(person_1, person_2)
        if evr.status():
            true_evrs.append(evr)
    return true_evrs

class Evristic(object):
    def fit(self):
        pass

    def status(self):
        return False

    def to_dict(self):
        return None

class CommonEstateEvr(Evristic):
    common_estate = [] # (reg_id, square)

    def fit(self, p1: Person, p2: Person):
        p1_estate = set([(estate['reg_id'], estate['square'])\
                for estate in p1.real_estates\
                    if estate['reg_id'] and estate['square']])
        p2_estate = set([(estate['reg_id'], estate['square'])\
                for estate in p2.real_estates\ 
                    if estate['reg_id'] and estate['square']])

        self.common_estate = list(p1_estate & p2_estate)

    def status(self):
        return len(self.common_estate) != 0

    def to_dict(self):
        return { "common_estate" : self.common_estate }

class CommonRigions(Evristic):
    common_regions = [] # (year, id)

    def fit(self, p1: Person, p2: Person):
        p1_regions = set()
        for year, reg_id in p1.region_info:
            if year and reg_id:
                p1_regions.add((year, reg_id))

        p2_regions = set()
        for year, reg_id in p2.region_info:
            if year and reg_id:
                p2_regions.add((year, reg_id))
        
        self.common_regions = list(p1_regions & p2_regions)

    def status(self):
        return len(self.common_regions) != 0

    def to_dict(self):
        return { "commin_regions" : self.common_regions }

class CommonWorkEvr(Evristic):
    common_office = []  # (year, id)
    
    def fit(self, p1: Person, p2: Person):
        p1_work = set(p1.work_info)
        p2_work = set(p1.work_info)

        self.common_office = list(p1_work & p2_work)

    def status(self):
        return len(self.common_office) != 0

    def to_dict(self):
        return { "commin_office" : self.common_office }

class SurnameEvr(Evristic):
    has_same_surname = False

    def fit(self, p1: Person, p2: Person):
        self.has_same_surname = tools.acceptable_pref(p1.surname, p2.surname, 2)

    def status(self):
        return self.has_same_surname

    def to_dict(self):
        return None

class PatrNameEvr(Evristic):
    has_same_patr_name = False

    def fit(self, p1: Person, p2: Person):
        self.has_same_patr_name = tools.acceptable_pref(p1.name, p2.patr_name, 1)\
                               or tools.acceptable_pref(p2.name, p1.patr_name, 1)
    def status(self):
        return self.has_same_patr_name

    def to_dict(self):
        return None