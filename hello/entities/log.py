from django.db import connection


class Log:
    def __init__(self, id, date, description, user, modulo):
        self.id = id
        self.date = date
        self.description = description
        self.user = user
        self.modulo = modulo

    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT l.id, l.date, l.description, u.name, l.modulo "
                "FROM log l "
                "LEFT JOIN `user` u ON u.id = l.id_user "
                "ORDER BY l.date DESC"
            )
            rows = cursor.fetchall()

        return [
            Log(row[0], row[1], row[2], row[3], row[4])
            for row in rows
        ]