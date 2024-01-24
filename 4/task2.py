from main import connect_to_database, save_file_json, load_pickle, query

def execute():
    db = connect_to_database(1)
    create_table(db)
    # insert_data(db, load_pickle('task_2_var_71_subitem.pkl'))

    save_file_json(2, "task_1", query1(db, "Кубло 17"))
    save_file_json(2, "task_2", query2(db))
    save_file_json(2, "task_3", query3(db))

    db.close()

def create_table(db):
    cursor = db.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS building_subitem (
            id              INTEGER PRIMARY KEY ASC,
            id_building     INTEGER REFERENCES building (id),
            name            TEXT (255),
            rating          INTEGER,
            convenience     INTEGER,
            security        INTEGER,
            functionality   INTEGER,
            comment         TEXT (255)
            )""")
    db.commit()

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
           INSERT INTO building_subitem (id_building, name, rating, convenience, security, functionality, comment)
           VALUES(
                (SELECT id FROM building WHERE name = :name),
                :name, :rating, :convenience, :security, :functionality, :comment
           )
        """, data)

    db.commit()

def query1(db, name):
    return query(db, """ 
            SELECT * 
            FROM building_subitem
            WHERE id_building = (SELECT id FROM building WHERE name = ?) 
        """, [name])

def query2(db):
    return query(db, """ 
           SELECT *
           FROM building_subitem, building
           WHERE building_subitem.id_building = building.id 
        """, [])

def query3(db):
    return query(db, """ 
           SELECT *
           FROM building_subitem, building
           WHERE building_subitem.id_building = building.id and building_subitem.rating > 4.8 and building.year > 2020
        """, [])


execute()