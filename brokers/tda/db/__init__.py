from db.sqlite import create_connection, create_table

sql_create_auths_table = """ CREATE TABLE IF NOT EXISTS auths (
                                    api_key text PRIMARY KEY,
                                    oauth_state text,
                                    expiration_date DATETIME 
                                ); """


def create_tables():
    conn = create_connection()

    if conn is not None:
        create_table(conn, sql_create_auths_table)
    else:
        print('Error! Could not open DB connection')
