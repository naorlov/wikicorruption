from main_server.person import Person
import main_server.tools as tools


def find_relations(person_1: Person, person_2: Person, deep=False, db=None):
    true_heus = []
    evrs = [CommonEstateHeu, SurnameHeu, CommonWorkHeu]
    if deep:
        evrs.extend([PatrNameHeu, CommonRegions])
    for heu_t in evrs:
        heu = heu_t()
        heu.fit(person_1, person_2, db)
        if heu.status():
            true_heus.append(heu.to_dict())
    return true_heus


class Heuristic(object):
    def __init__(self):
        self.dict_repr = {'plus_w': 0, 'minus_w': 0}

    def fit(self, p1: Person, p2: Person, db):
        pass

    def status(self):
        return False

    def to_dict(self):
        return self.dict_repr


class CommonEstateHeu(Heuristic):
    def __init__(self):
        super().__init__()
        self.common_estate = []  # (reg_id, square)

    def fit(self, p1: Person, p2: Person, db=None):
        p1_estate = set([(estate['reg_id'], estate['square'])
                         for estate in p1.real_estates
                         if estate['reg_id'] and estate['square']])
        p2_estate = set([(estate['reg_id'], estate['square'])
                         for estate in p2.real_estates
                         if estate['reg_id'] and estate['square']])

        self.common_estate = list(p1_estate & p2_estate)

    def status(self):
        return len(self.common_estate) != 0

    def to_dict(self):
        self.dict_repr["common_estate"] = self.common_estate
        self.dict_repr["plus_w"] = 20
        return self.dict_repr


class CommonRegions(Heuristic):
    def __init__(self):
        super().__init__()
        self.common_regions = []  # (year, id)

    def fit(self, p1: Person, p2: Person, db=None):
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
        self.dict_repr["common_regions"] = self.common_regions
        self.dict_repr["plus_w"] = 10
        return self.dict_repr


class CommonWorkHeu(Heuristic):
    def __init__(self):
        super().__init__()
        self.common_office = []  # (year, id)

    def fit(self, p1: Person, p2: Person, db=None):
        p1_work = set(p1.work_info)
        p2_work = set(p1.work_info)
        self.common_office = [item for item in p1_work & p2_work if item[1] != 14]

    def status(self):
        return len(self.common_office) != 0

    def to_dict(self):
        self.dict_repr["common_office"] = self.common_office
        self.dict_repr["plus_w"] = 50
        return self.dict_repr


class SurnameHeu(Heuristic):
    def __init__(self):
        super().__init__()
        self.has_same_surname = False

    def fit(self, p1: Person, p2: Person, db=None):
        self.has_same_surname = tools.acceptable_pref(p1.surname, p2.surname, 2)

    def status(self):
        return self.has_same_surname

    def to_dict(self):
        self.dict_repr["surname"] = []
        self.dict_repr["plus_w"] = 50
        return self.dict_repr


class PatrNameHeu(Heuristic):
    def __init__(self):
        super().__init__()
        self.has_same_patr_name = False

    def fit(self, p1: Person, p2: Person, db=None):
        self.has_same_patr_name = tools.acceptable_pref(p1.name, p2.patr_name, 3) or \
                                  tools.acceptable_pref(p2.name, p1.patr_name, 3)

    def status(self):
        return self.has_same_patr_name

    def to_dict(self):
        self.dict_repr["patrname"] = []
        self.dict_repr["plus_w"] = 10
        return self.dict_repr
