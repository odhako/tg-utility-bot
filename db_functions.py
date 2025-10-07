import os
import sqlite3
import logging


logging.basicConfig(format='[%(levelname)s %(asctime)s] %(name)s: %(message)s', level=logging.INFO)


def create_db(db_name):
    connection = sqlite3.connect(f'{db_name}.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER
    );
    ''')

    connection.commit()
    connection.close()
    logging.debug('Table created, if not existed')


# DATABASE FUNCTIONS
def add_post_to_db(db, post_id):
    logging.debug(f'Added to db: post id {post_id}')
    connection = sqlite3.connect(f'{db}.db')
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO Posts (post_id) VALUES (?);",
        (post_id, )
    )

    connection.commit()
    connection.close()


def pop_post_from_db(db) -> int or False:
    connection = sqlite3.connect(f'{db}.db')
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, post_id FROM Posts ORDER BY id DESC LIMIT 1"
    )

    posts = cursor.fetchall()
    connection.commit()

    if not posts:
        connection.close()
        logging.info('Schedule is empty')
        return False

    post_db_id, post_tg_id = posts[-1]
    logging.info(f'Post is grabbed: db_id = {post_db_id}, tg_id = {post_tg_id}')

    cursor.execute(
        "DELETE FROM Posts WHERE id=?",
        (post_db_id, )
    )

    connection.commit()
    connection.close()

    return post_tg_id


def get_all_posts_from_db(db) -> list:
    connection = sqlite3.connect(f'{db}.db')
    cursor = connection.cursor()

    cursor.execute(
        "SELECT (id) FROM Posts"
    )

    posts = cursor.fetchall()

    connection.commit()
    connection.close()

    return posts


def db_has_data(db):
    connection = sqlite3.connect(f'{db}.db')
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM Posts LIMIT 1"
    )

    some_data = cursor.fetchall()

    connection.commit()
    connection.close()

    if some_data:
        return True
    else:
        return False


if __name__ == "__main__":
    # Dumb tests:
    logging.basicConfig(level=logging.DEBUG)
    test_db = 'tests'
    create_db(db_name=test_db)
    logging.debug('Creating posts:')
    add_post_to_db(test_db, 1)
    add_post_to_db(test_db, 2)
    add_post_to_db(test_db, 3)

    logging.debug('Grabbing posts one by one:')
    logging.debug(pop_post_from_db(test_db))
    logging.debug(pop_post_from_db(test_db))
    logging.debug(pop_post_from_db(test_db))

    logging.info(('All posts remaining:', get_all_posts_from_db(test_db)))
    os.remove(f'{test_db}.db')
