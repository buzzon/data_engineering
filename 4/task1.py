from main import connect_to_database, save_file_json, load_pickle

def execute():
    db = connect_to_database(1)
    create_table(db)
    # insert_data(db, load_pickle('task_1_var_71_item.pkl'))

    save_file_json(1, "task_1", get_top(db))
    save_file_json(1, "task_2", get_describe(db))
    save_file_json(1, "task_3", get_frequency(db))
    save_file_json(1, "task_4", get_top_filter(db))

    db.close()

def create_table(db):
    cursor = db.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS building (
            id          INTEGER    PRIMARY KEY ASC,
            name        TEXT (255),
            street      TEXT (255),
            city        TEXT (255),
            zipcode     INTEGER,
            floors      INTEGER,
            year        INTEGER,
            parking     BOOLEAN,
            prob_price  INTEGER,
            views       INTEGER
            )""")
    db.commit()

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO building (name, street, city, zipcode, floors, year, parking, prob_price, views)
        VALUES(
            :name, :street, :city, :zipcode, :floors,
            :year, :parking, :prob_price, :views
        )
    """, data)

    db.commit()


def get_top(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT * 
        FROM building 
        ORDER BY prob_price DESC LIMIT 72
        """)
    res = res.fetchall()

    items_list = []

    for row in res:
        items_list.append(dict(row))
    cursor.close()

    return items_list


def get_top_filter(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT * 
        FROM building 
        WHERE views > 2400
        ORDER BY prob_price DESC LIMIT 72
        """)

    res = res.fetchall()

    items_list = []

    for row in res:
        items_list.append(dict(row))
    cursor.close()

    return items_list


def get_describe(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT 
        MIN(prob_price) as min,
        MAX(prob_price) as max,
        AVG(prob_price) as avg,
        SUM(prob_price) as sum
        FROM building
    """)

    items_st = []
    res = res.fetchone()
    items_st.append(dict(res))
    cursor.close()

    return items_st

def get_frequency(db):
    cursor = db.cursor()

    result_tag = cursor.execute("""
        SELECT
            CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM building) as count,
            city
        FROM building
        GROUP BY city
                
    """)
    items_tag = []
    for row in result_tag.fetchall():
        items_tag.append(dict(row))
    cursor.close()
    return items_tag


execute()