class Person(object):
    id = int()
    name = ''
    surname = ''
    patr_name = ''

    work_info = []  # [(year, work_id)]
    income_info = []  # [(year, income)]
    relative_info = []  # [(year, user_id)]
    region_info = []  # [(year, id)]
    real_estates = []  # [(year, id)]
    vehicles_info = []  # [(year, brand_id)]

    def __init__(self, id_, name_, surname_, patr_name_):
        self.id = id_
        self.name = name_
        self.surname = surname_
        self.patr_name = patr_name_


class PersonFactory(object):
    def create(self, person_dict: dict):
        main_dict = person_dict["main"]
        person_dict = main_dict["person"]
        result = Person(
            person_dict["id"],
            person_dict["given_name"],
            person_dict["family_name"],
            person_dict["patronymic_name"]
        )

        year = main_dict["year"]
        work_id = main_dict["office"]["id"]
        result.work_info.append((year, work_id))

        vehicles_dict = person_dict["vehicles"]
        vehicles = [(year, vehicles_dict[i]["brand"]["id"] for i in len(vehicles_dict))]
        result.vehicles_info.append([(year, i) for i in vehicles])





        return result

