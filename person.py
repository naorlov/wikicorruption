class Person(object):
    id = int()
    name = ''
    surname = ''
    patr_name = ''

    work_info = [] # [(year, work_id)]
    income_info = [] # [(year, income)]
    relative_info = [] # [(year, user_id)]
    region_info = [] # [(year, id)]
    real_estates = [{ 'year' : 0,
                     'reg_id' : 0,
                     'type_id' : 0,
                     'square' : 0.0}]
    vehicles_info = [] # [(year, brand_id)]
    def __init__(self):
        pass

def person_factory(mongo_dict):
    return Person()