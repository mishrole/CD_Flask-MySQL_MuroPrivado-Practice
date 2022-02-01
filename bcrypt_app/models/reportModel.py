from bcrypt_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Report:
    def __init__(self, data):
        self.id = data['id']
        self.user_ip = data['user_ip']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO reports (user_id, user_ip, created_at, updated_at) VALUES (%(userId)s, %(userIp)s, NOW(), NOW());"
        return connectToMySQL('private_wall_schema').query_db(query, data)

    @classmethod
    def get_all_by_userId(cls, data):
        query = "SELECT * FROM reports WHERE user_id = %(userId)s"
        results = connectToMySQL('private_wall_schema').query_db(query, data)

        reports = []

        if results:
            if len(results) > 0:
                for report in results:
                    reports.append(cls(report))

        return reports

    @classmethod
    def findLastReportByUserId(cls, data):
        query = "SELECT * FROM reports WHERE user_id = %(userId)s order by id desc limit 1;"
        results = connectToMySQL('private_wall_schema').query_db(query, data)

        report = None

        if results:
            if len(results) > 0:
                report = cls(results[0])

        return report