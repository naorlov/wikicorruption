import networkx
import settings
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient(settings.server_url)
    database = client[settings.db_name]
    page = database.declarations

    cursor = page.find()
    for item in page.find():
        main_dict = item["main"]["person"]
        if len(main_dict["family_name"]) <= 3:
            print(main_dict["family_name"])



