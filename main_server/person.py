import tools

class Person(object):
    id = int()
    name = ''
    surname = ''
    patr_name = ''

    real_estates = [
        # {
        #    'year' : 0,
        #    'reg_id' : 0,
        #    'type_id' : 0,
        #    'square' : 0.0
        # }
    ]

    work_info = []  # [(year, work_id)]

    income_info = []  # [(year, income)]

    relative_info = []  # [(year, user_id)]

    region_info = []  # [(year, id)]

    vehicles_info = []  # [(year, brand_id)]

    def __init__(self, id_, name_, surname_, patr_name_):
        self.id = id_
        self.name = name_
        self.surname = surname_
        self.patr_name = patr_name_

    def update_estates(self, person_dict):
        pass

    def update_work(self, person_dict):
        pass

    def update_income(self, person_dict):
        pass

    def update_region(self, person_dict):
        pass

    def update(self, person_dict):
        year = person_dict["main"]["year"]

        ### REAL ESTATES ###

        estates_dict = person_dict["real_estates"]
        for i in range(len(estates_dict)):
            current_estate = estates_dict[i]
            inner_estate = {
                "year": year,
                "reg_id": tools.extract_field(current_estate["region"], 'id'),
                "type_id": tools.extract_field(current_estate["type"]), 'id),
                "square": round(current_estate["square"]) if current_estate["square"] else None
            }
            # if inner_estate in self.real_estates:
            #   continue
            self.real_estates.append(inner_estate)

        ### WORK INFO ###

        work_dict = person_dict["main"]["office"]
        work_id = work_dict["id"]
        self.work_info.append((year, work_id))

        ### INCOME INFO ###

        if len(person_dict["incomes"]) != 0:
            income_dict = person_dict["incomes"][0]
            income_amount = income_dict["size"]
            self.income_info.append((year, income_amount))
        else:
            self.income_info.append((year, 0))

        ### RELATIVE INFO ###
        # in progress

        ### REGION INFO ###

        self.region_info.append((year, tools.extract_field(work_dict["region"], "id"))

        ### VEHICLE INFO ###

        vehicles_dict = person_dict["vehicles"]
        for i in range(len(vehicles_dict)):
            inner_vehicle = (year, vehicles_dict[i]["brand"])
            self.vehicles_info.append(inner_vehicle)
        return

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __str__(self):
        return self.name


class PersonFactory(object):
    @classmethod
    def create(cls, person_dict: dict):
        main_dict = person_dict["main"]
        person_dict = main_dict["person"]
        result = Person(
            person_dict["id"],
            person_dict["given_name"],
            person_dict["family_name"],
            person_dict["patronymic_name"]
        )

        return result
