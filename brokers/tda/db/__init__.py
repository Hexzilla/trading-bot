from db.sqlite import create_connection, create_table

sql_create_auths_table = """ CREATE TABLE IF NOT EXISTS auths (
                                    api_key text PRIMARY KEY,
                                    oauth_state text,
                                    expiration_date DATETIME 
                                ); """

sql_create_account_info_table = """ CREATE TABLE IF NOT EXISTS account_info (
                                        user_id text PRIMARY KEY,
                                        enabled_user INTEGER
                                    ); """

sql_create_account_order_info_table = """ CREATE TABLE IF NOT EXISTS account_order_info (
                                                user_id text PRIMARY KEY,
                                                account_balance NUMERIC,
                                                date Date,
                                                gains_losses_daily text
                                            ); """

sql_create_order_management_table = """ CREATE TABLE IF NOT EXISTS order_management (
                                            user_id text,
                                            ticker_symbol text,
                                            net_cost text,
                                            action text,
                                            status text,
                                            price_type text,
                                            date Date,
                                            message_details text
                                        ); """


def create_tables():
    conn = create_connection()

    if conn is not None:
        create_table(conn, sql_create_auths_table)
        create_table(conn, sql_create_account_info_table)
        create_table(conn, sql_create_account_order_info_table)
        create_table(conn, sql_create_order_management_table)
    else:
        print('Error! Could not open DB connection')
