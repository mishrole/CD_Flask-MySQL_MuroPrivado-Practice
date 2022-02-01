from bcrypt_app.config.mysqlconnection import connectToMySQL
from bcrypt_app.models import userModel
from datetime import datetime
from flask import flash
import re

class Message:
    def __init__(self, data):
        self.id = data['id']
        self.message = data['message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.isDeleted = data['isDeleted']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.time_ago = ''
    
    @classmethod
    def get_all_by_receiver(cls, data):
        query = "SELECT * FROM messages JOIN users sender ON sender.id = messages.sender_id JOIN users receiver ON receiver.id = messages.receiver_id WHERE messages.receiver_id = %(receiverId)s and messages.isDeleted like 0 order by sender.firstname asc;"
        results = connectToMySQL('private_wall_schema').query_db(query, data)

        messages = []

        # Filtrar Ids de usuarios que enviaron los mensajes (senderId)
        sendersIds = []
        [sendersIds.append(x['sender.id']) for x in results if x['sender.id'] not in sendersIds]
        
        # Agrupar mensajes por senderId
        for senderId in sendersIds:
            # Filtrar data de senderId actual
            senderMessages = [d for d in results if d['sender.id'] == senderId]

            sender_data = {
                'id': senderMessages[0]['sender.id'],
                'firstname': senderMessages[0]['firstname'],
                'lastname': senderMessages[0]['lastname'],
                'birthday': senderMessages[0]['birthday'],
                'gender': senderMessages[0]['gender'],
                'email': senderMessages[0]['email'],
                'password': '', # Not exposed
                'created_at': senderMessages[0]['sender.created_at'],
                'updated_at': senderMessages[0]['sender.updated_at'],
                'isBlocked': senderMessages[0]['isBlocked']
            }

            sender = userModel.User(sender_data)

            for senderMessage in senderMessages:
                message = cls(senderMessage)
                message.time_ago = Message.ago(senderMessage['created_at'])
                sender.messages.append(message)

            messages.append(sender)

        return messages

    @classmethod
    def count_all_by_sender(cls, data):
        query = "SELECT count(*) as total_sent FROM messages JOIN users sender ON sender.id = messages.sender_id JOIN users receiver ON receiver.id = messages.receiver_id WHERE messages.sender_id = %(senderId)s and messages.isDeleted like 0;"
        result = connectToMySQL('private_wall_schema').query_db(query, data)

        total = 0

        if result:
            if len(result) > 0:
                total = result[0]['total_sent']

        return total

    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (sender_id, receiver_id, message, created_at, updated_at) VALUES (%(senderId)s, %(receiverId)s, %(message)s, NOW(), NOW());"
        return connectToMySQL('private_wall_schema').query_db(query, data)

    @classmethod
    def findMessageById(cls, data):
        query = "SELECT * FROM messages WHERE id = %(messageId)s;"
        results = connectToMySQL('private_wall_schema').query_db(query, data)

        message = None

        if results:
            if len(results) > 0:
                message = cls(results[0])
            
        return message

    @classmethod
    def deleteLogically(cls, data):
        query = "UPDATE messages SET isDeleted = 1 WHERE messages.id = %(messageId)s;"
        return connectToMySQL('private_wall_schema').query_db(query, data)

    @staticmethod
    def ago(input_date):
        total_seconds = abs((input_date - datetime.now()).total_seconds())

        sec_value = total_seconds % (24 * 3600)
        hours = sec_value // 3600
        sec_value %= 3600
        min = sec_value // 60
        sec_value %= 60
        days = hours / 24
        years = days / 365.25

        if int(years) > 0:
            result = f"{int(years)} year ago"
            if int(years) > 1:
                result = f"{int(years)} years ago"
        elif int(days) > 0:
            result = f"{int(days)} day ago"
            if int(days) > 1:
                result = f"{int(days)} days ago"
        elif int(hours) > 0:
            result = f"{int(hours)} hour ago"
            if int(hours) > 1:
                result = f"{int(hours)} hours ago"
        elif int(min) > 0:
            result = f"{int(min)} minute ago"
            if int(min) > 1:
                result = f"{int(min)} minutes ago"
        elif int(sec_value) > 0:
            result = f"{int(sec_value)} second ago"
            if int(sec_value) > 1:
                result = f"{int(sec_value)} seconds ago"

        return result

    @staticmethod
    def validateMessage(data):
        is_valid = True
        print(data, 'validate')

        message = data['message']
        receiverId = data['receiverId']
        senderId = data['senderId']

        if len(message) < 5:
            flash('Message must be at least 5 characters long', 'send_error')
            is_valid = False

        if userModel.User.findUserById({'userId': receiverId}) == None or userModel.User.findUserById({'userId': senderId}) == None:
            flash('Invalid receiver or sender', 'send_error')
            is_valid = False

        return is_valid
