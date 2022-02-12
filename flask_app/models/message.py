from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from datetime import date
from flask_app.models import user


class Message:
    def __init__(self, data):
        self.id = data['id']
        self.sender_id=data['sender_id']
        self.receiver_id=data['receiver_id']
        self.content=data['content']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

# CREATE
    @classmethod
    def create_message(cls, data):
        query ="""
        INSERT INTO messages
        (sender_id, receiver_id, content)
        VALUES (%(sender_id)s, %(receiver_id)s, %(content)s);
        """
        return connectToMySQL("private_wall_schema").query_db(query, data)
# READ
    @classmethod
    def get_all_for_user(cls, id):
        data={
            'id':id
        }
        query ="""
        SELECT *
        FROM messages
        WHERE receiver_id=%(id)s;
        """
        return connectToMySQL("private_wall_schema").query_db(query, data)
#UPDATE


#DELETE


#STATIC
