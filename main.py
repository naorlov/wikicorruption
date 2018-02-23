import networkx
import settings
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient(settings.server_url)
    database = client[settings.db_name]
    page = database.declarations




