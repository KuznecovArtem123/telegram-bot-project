import sqlalchemy as db
from emoji import emojize 
from random import choice
import settings

engine = db.create_engine('sqlite:///users.db')

conn=engine.connect()

metadata = db.MetaData()

users = db.Table('users', metadata, 
                 db.Column('id', db.Integer, primary_key=True),
                 db.Column('first_name', db.Text, nullable=True),
                 db.Column('last_name', db.Text, nullable=True),
                 db.Column('username', db.Text, nullable=False),
                 db.Column('chat_id', db.Integer, nullable=False),
                 db.Column('smile', db.Text, nullable=True),
                 db.Column('is_subscribed', db.Integer, nullable=False, default=False),
                 )
metadata.create_all(engine)

def get_or_create_user(users, effective_user, message):
    with engine.begin() as connection:
        query = db.select(users).where(users.c.id == effective_user.id)
        result = connection.execute(query).fetchone()

        if not result:
            ins = db.insert(users).values(
                id=effective_user.id,
                first_name=effective_user.first_name,
                last_name=effective_user.last_name,
                username=effective_user.username,
                chat_id=message.chat.id
            )
            connection.execute(ins)
            result = connection.execute(query).fetchone()
        return result
    
def get_user_smile(user_table,user_data):
    if user_data.smile:
        return emojize(user_data.smile,language="alias")
    best_choise = choice(settings.USER_EMOJI)
        
    with engine.begin() as connection:
        upd = (
            db.update(user_table)
            .where(user_table.c.id == user_data.id)
            .values({"smile":best_choise})
        )
        connection.execute(upd)
    return emojize(best_choise,language=("alias"))

def toggle_subscription(users, effective_user):
    new_value = not effective_user.is_subscribed

    with engine.begin() as connection:
        upd = db.update(users).where(users.c.id == effective_user.id).values({'is_subscribed': new_value})
        connection.execute(upd)