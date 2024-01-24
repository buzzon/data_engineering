from main import connect_to_database, save_file_json, read_json, read_csv, fixNumber, query

def execute():
    db = connect_to_database(4)
    create_table(db)

    items = read_csv('task_4_var_71_product_data.csv',";")
    updates = read_json('task_4_var_71_update_data.json')
    transactions(db, updates)

    # insert_data(db, [{items[0][i]:item[i] for i in range(len(item))} for item in items[1]] )

    save_file_json(4, "task_1", query1(db))
    save_file_json(4, "task_2", query2(db))
    save_file_json(4, "task_3", query3(db))
    save_file_json(4, "task_4", query4(db))

    db.close()

def transactions(db, updates):
    cursor = db.cursor()
    for action in updates:
        param = action["param"]
        name = action["name"]
        if action['method'] == "available":
            cursor.execute("UPDATE product SET isAvailable = ? WHERE name = ?  ", [param, name])
            cursor.execute("UPDATE product SET version = version + 1  WHERE name = ? ", [name])
        elif action['method'] == "quantity_sub":
            res = cursor.execute("UPDATE product SET quantity = (quantity + ?) WHERE (name = ?) AND ((quantity + ?) > 0)",[param, name, param])
            if res.rowcount > 0:
                cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
        elif action['method'] == "remove":
            # cursor.execute(" DELETE FROM product WHERE name = ? ", [name])
            pass
        elif action['method'] == "price_abs":
            res = cursor.execute("UPDATE product SET price = (price + ?) WHERE (name = ?) AND ((price + ?) > 0)", [param, name, param])
            if res.rowcount > 0:
                cursor.execute(" UPDATE product SET version = version + 1  WHERE name = ? ", [name])
        elif action['method'] == "quantity_add":
            cursor.execute("UPDATE product SET quantity = (quantity + ?) WHERE (name = ?)",[param, name])
            cursor.execute("UPDATE product SET version = version + 1  WHERE name = ? ", [name])
        elif action['method'] == "price_percent":
            cursor.execute(" UPDATE product SET price = ROUND(price * (1 + ?), 2) WHERE name = ? ", [param, name])
            cursor.execute(" UPDATE product SET version = version + 1  WHERE name = ? ", [name])
    db.commit()

def create_table(db):
    cursor = db.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS product (
            id              INTEGER PRIMARY KEY ASC,
            name            TEXT (255),
            price           INTEGER,
            quantity        INTEGER,
            type            TEXT (255),
            fromCity        TEXT (255),
            isAvailable     BOOLEAN,
            views           INTEGER,
            version         INTEGER
            )""")
    db.commit()

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
            INSERT INTO product (name, price, quantity, type, fromCity, isAvailable, views, version)
                VALUES(
                    :name, :price, :quantity, :type, :fromCity, :isAvailable, :views, 0
                )
        """, data)

    db.commit()

def query1(db):
    return query(db, "SELECT * FROM product ORDER BY version DESC LIMIT 10", [])

def query2(db):
    return query(db, """
            SELECT 
            type,
            MIN(price) as min,
            MAX(price) as max,
            AVG(price) as avg,
            SUM(price) as sum
            FROM product
            GROUP BY type
    """, [])

def query3(db):
    return query(db, """
        SELECT 
        type,
        MIN(quantity) as min,
        MAX(quantity) as max,
        AVG(quantity) as avg,
        SUM(quantity) as sum
        FROM product
        GROUP BY type
    """, [])

def query4(db):
    return query(db, """
        SELECT *
        FROM product
        WHERE views < 500
        ORDER BY views DESC
    """, [])


execute()