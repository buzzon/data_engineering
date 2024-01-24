import pymongo
from main import load_pickle, save_file_json

client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
db = client.test_database
collection = db.example_collection

data = load_pickle("task_1_item.pkl")

# collection.insert_many(data)

save_file_json(1, "task_1", collection.find().sort("salary", -1).limit(10))
save_file_json(1, "task_2", collection.find({'age': {'$lt': 30}}).sort("salary", -1).limit(15))
save_file_json(1, "task_3", collection
               .find({"city": "Камбадос", "job": {"$in": ["Продавец", "Строитель", "Программист"]}})
               .sort("age", pymongo.ASCENDING)
               .limit(10))

save_file_json(1, "task_4", collection.count_documents(
    {"age": {"$gte": 20, "$lte": 50},
        "year": {"$in": [2019, 2020, 2021, 2022]},
        "$or": [
            {"salary": {"$gt": 50000, "$lte": 75000}},
            {"salary": {"$gt": 125000, "$lt": 150000}}
        ]}
))