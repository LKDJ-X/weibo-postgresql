import psycopg2

INTERNAL_ERROR = 'Internal error occurred, please try again later'

conn = None

def init():
    global conn
    conn = psycopg2.connect(database="weibo", user="postgres", password="123456", host="localhost", port="5432")
    print("connect database weibo successfully")

def init_test():
    global conn
    conn = psycopg2.connect(database="weibo_test", user="postgres", password="123456", host="localhost", port="5432")
    print("connect database weibo successfully")


def shutdown():
    conn.close()


def execute_query(query, args=None, commit=False):
    global conn

    if conn is None:
        init()
        
    cur = None

    try:
        cur = conn.cursor()
        cur.execute(query, args)

        if commit:
            conn.commit()

        return cur.fetchall()

    except Exception as ex:
        print(ex)
        return None

    finally:
        if cur is not None:
            cur.close()

def execute(query, args=None):
    global conn

    if conn is None:
        init()

    cur = None

    try:
        cur = conn.cursor()
        cur.execute(query, args)

        conn.commit()

    except Exception as ex:
        print(ex)

    finally:
        if cur is not None:
            cur.close()


def execute_update(query, args=None):
    global conn

    if conn is None:
        init()

    cur = None

    try:
        cur = conn.cursor()
        cur.execute(query, args)

        conn.commit()

        return cur.rowcount

    except Exception as ex:
        print(ex)
        return 0

    finally:
        if cur is not None:
            cur.close()
