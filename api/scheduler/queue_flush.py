import sqlite3

def clear_queue():
    try:
        conn = sqlite3.connect('./database.db')
        conn.execute("DELETE FROM task WHERE task_status = 'S' AND \
        updated_at <= Datetime('now', '-5 minutes', 'localtime')")
        conn.commit()
        # print('Stopped task older than 10 mins deleted')
    except Exception as ex:
        print(ex)
    finally:
        conn.close()