from django.db import connection


class WorkOrder:
    def __init__(self, id, title, description, status):
        self.id = id
        self.title = title
        self.description = description
        self.status = status

    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, description, status FROM work_order")
            rows = cursor.fetchall()

        return [
            WorkOrder(row[0], row[1], row[2], row[3])
            for row in rows
        ]