from main import connect_to_database, save_file_json, load_pickle, read_file, fixNumber, query

def execute():
    db = connect_to_database(3)

    items1 = load_pickle('task_3_var_71_part_1.pkl')
    invalid = {'acousticness', 'energy', 'popularity'}
    items1 = [{x: fixNumber(d[x]) for x in d if x not in invalid} for d in items1]
    items2 = read_file('task_3_var_71_part_2.text', parse_file)


    create_table(db)
    # insert_data(db, items1)
    # insert_data(db, items2)


    save_file_json(3, "task_1", query1(db))
    save_file_json(3, "task_2", query2(db))
    save_file_json(3, "task_3", query3(db))
    save_file_json(3, "task_4", query4(db))

    db.close()

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

def create_table(db):
    cursor = db.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS music (
            id              INTEGER PRIMARY KEY ASC,
            artist          TEXT (255),
            song            TEXT (255),
            duration_ms     INTEGER,
            year            INTEGER,
            tempo           INTEGER,
            genre           TEXT (255)
            )""")
    db.commit()

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
            INSERT INTO music (artist, song, duration_ms, year, tempo, genre)
                VALUES(
                    :artist, :song, :duration_ms, :year, :tempo, :genre
                )
        """, data)

    db.commit()




def query1(db):
    return query(db, """ 
            SELECT * 
            FROM music 
            ORDER BY duration_ms DESC LIMIT 71
        """, [])

def query2(db):
    return query(db, """
            SELECT 
            MIN(duration_ms) as min,
            MAX(duration_ms) as max,
            AVG(duration_ms) as avg,
            SUM(duration_ms) as sum
            FROM music
    """, [])

def query3(db):
    return query(db, """
            SELECT
                CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM music) as count,
                artist
            FROM music
            GROUP BY artist
    """, [])

def query4(db):
    return query(db, """
            SELECT * 
            FROM music 
            WHERE duration_ms > 221933
            ORDER BY tempo DESC LIMIT 71
        """, [])


execute()