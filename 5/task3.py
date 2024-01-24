import pymongo
from main import read_csv, save_file_json, fixNumber

def execute():
    client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    db = client.test_database
    collection = db.example_collection

    data = read_csv('task_3_item.csv', ";")
    # collection.insert_many(data)


    selected_jobs = ["Повар", "Психолог"]
    selected_cities = ["Льейда", "Вроцлав"]   


    collection.delete_many({"$or": [{"salary": {"$lt": 25000}}, {"salary": {"$gt": 175000}}]})
    save_file_json(3, "task_1", collection.find())

    collection.update_many({}, {"$inc": {"age": 1}})
    save_file_json(3, "task_2", collection.find())

    collection.update_many({"job": {"$in": selected_jobs}}, {"$mul": {"salary": 1.05}})
    save_file_json(3, "task_3", collection.find())

    collection.update_many({"city": {"$in": selected_cities}}, {"$mul": {"salary": 1.07}})
    save_file_json(3, "task_4", collection.find())

    collection.update_many(
        {"city": "Тбилиси", "job": {"$in": ["Менеджер", "Программист"]}, "age": {"$gte": 30, "$lte": 50}}, 
        {"$mul": {"salary": 1.1}}
        )
    save_file_json(3, "task_5", collection.find())

    collection.delete_many({"year": {"$lt": 2000}})
    save_file_json(3, "task_6", collection.find())

execute()
