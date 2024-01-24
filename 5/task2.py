import pymongo
from main import read_file, save_file_json, fixNumber

def execute():
    client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    db = client.test_database
    collection = db.example_collection

    data = read_file('task_2_item.text', parse_file)
    # collection.insert_many(data)

    save_file_json(2, "task_1", collection.aggregate([
        {"$group": {"_id": None, "min_salary": {"$min": "$salary"}, "avg_salary": {"$avg": "$salary"}, "max_salary": {"$max": "$salary"}}}
    ]))

    save_file_json(2, "task_2", collection.aggregate([
        {"$group": {"_id": "$job", "count": {"$sum": 1}}}
    ]))

    save_file_json(2, "task_3", collection.aggregate([
        {"$group": {"_id": "$city", "min_salary": {"$min": "$salary"}, "avg_salary": {"$avg": "$salary"}, "max_salary": {"$max": "$salary"}}}
    ]))

    save_file_json(2, "task_4", collection.aggregate([
        {"$group": {"_id": "$job", "min_salary": {"$min": "$salary"}, "avg_salary": {"$avg": "$salary"}, "max_salary": {"$max": "$salary"}}}
    ]))

    save_file_json(2, "task_5", collection.aggregate([
        {"$group": {"_id": "$city", "min_age": {"$min": "$age"}, "avg_age": {"$avg": "$age"}, "max_age": {"$max": "$age"}}}
    ]))
    
    save_file_json(2, "task_6", collection.aggregate([
        {"$group": {"_id": "$job", "min_age": {"$min": "$age"}, "avg_age": {"$avg": "$age"}, "max_age": {"$max": "$age"}}}
    ]))
    
    save_file_json(2, "task_7", collection.aggregate([
        {"$group": {"_id": "$age", "max_salary": {"$max": "$salary"}}},
        {"$sort": {"_id": 1}},
        {"$limit": 1}
    ]))

    save_file_json(2, "task_8", collection.aggregate([
        {"$group": {"_id": "$age", "min_salary": {"$min": "$salary"}}},
        {"$sort": {"_id": -1}},
        {"$limit": 1}
    ]))

    save_file_json(2, "task_9", collection.aggregate([
        {"$match": {"salary": {"$gt": 50000}}},
        {"$group": {"_id": "$city", "min_age": {"$min": "$age"}, "avg_age": {"$avg": "$age"}, "max_age": {"$max": "$age"}}},
        {"$sort": {"_id": 1}}
    ]))

    save_file_json(2, "task_10", collection.aggregate([
        {"$match": {"age": {"$in": list(range(18, 25)) + list(range(50, 65))}}},
        {"$group": {"_id": {"city": "$city", "job": "$job"}, "min_salary": {"$min": "$salary"}, "avg_salary": {"$avg": "$salary"}, "max_salary": {"$max": "$salary"}}}
    ]))

    save_file_json(2, "task_11", collection.aggregate([
        {"$match": {"city": "Астана", "job": "Строитель"}},
        {"$group": {"_id": "$year", "avg_salary": {"$avg": "$salary"}}},
        {"$sort": {"avg_salary": -1}}
    ]))


def parse_file(lines):
    result = []
    item = dict()
    for line in lines:
        if line == '=====\n':
            result.append(item)
            item = dict()
        else:
            row = line.strip().split("::")
            item[row[0]] = fixNumber(row[1])
        pass

    return result

execute()
