import pickle
import sqlite3
import logging


logging.basicConfig(format='[%(levelname)s %(asctime)s] %(name)s: %(message)s', level=logging.DEBUG)


def create_table():
    # DATABASE
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()

    # CREATING TABLE FOR POSTS
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object BLOB
    );
    ''')

    # APPLYING CHANGES AND CLOSE CONNECTION
    connection.commit()
    connection.close()
    logging.debug('Table created, if not existed')


# DATABASE FUNCTIONS
def add_post_to_db(post):
    logging.debug(f'original: {post}')
    post_pickled = pickle.dumps(post)
    logging.debug(f'pickled: {post_pickled}')
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO Posts (object) VALUES (?);",
        (post_pickled, )
    )

    connection.commit()
    connection.close()


def pop_post_from_db():
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, object FROM Posts ORDER BY id DESC LIMIT 1"
    )

    # post = cursor.fetchall()[-1]
    posts = cursor.fetchall()
    connection.commit()
    if not posts:
        connection.close()
        logging.info('Schedule is empty')
        return False

    post_id, post_blob = posts[-1]
    logging.info(f'Post is grabbed: id {post_id}')

    cursor.execute(
        "DELETE FROM Posts WHERE id=?",
        (post_id, )
    )

    connection.commit()
    connection.close()

    post_object = pickle.loads(post_blob)

    return post_object


def get_all_posts_from_db():
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM Posts ORDER BY id"
    )

    posts = cursor.fetchall()

    connection.commit()
    connection.close()

    return posts


if __name__ == "__main__":
    # Dumb tests:
    create_table()
    print('Creating posts:')
    add_post_to_db([1, 2, 3])
    add_post_to_db([2, 2, 3])
    add_post_to_db([3, 2, 3])

    print('Grabbing posts one by one:')
    print(pop_post_from_db())
    print(pop_post_from_db())
    print(pop_post_from_db())

    print('All posts remaining:', get_all_posts_from_db())

# message = Message(id=28, peer_id=PeerChannel(channel_id=3120947094),
#                   date=datetime.datetime(2025, 10, 5, 16, 11, 51, tzinfo=datetime.timezone.utc), message='test!',
#                   out=False, mentioned=False, media_unread=False, silent=False, post=True, from_scheduled=False,
#                   legacy=False, edit_hide=False, pinned=False, noforwards=False, invert_media=False, offline=False,
#                   video_processing_pending=False, paid_suggested_post_stars=False, paid_suggested_post_ton=False,
#                   from_id=None, from_boosts_applied=None, saved_peer_id=None, fwd_from=None, via_bot_id=None,
#                   via_business_bot_id=None, reply_to=None, media=None, reply_markup=None, entities=[], views=1,
#                   forwards=0, replies=None, edit_date=None, post_author=None, grouped_id=None, reactions=None,
#                   restriction_reason=[], ttl_period=None, quick_reply_shortcut_id=None, effect=None, factcheck=None,
#                   report_delivery_until_date=None, paid_message_stars=None, suggested_post=None)
