from django.db import connection


class WorkOrderHistory:
    def __init__(self, id, date, user, action, work_order_id):
        self.id = id
        self.date = date
        self.user = user
        self.action = action
        self.work_order_id = work_order_id

    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT h.id, h.date, u.name, h.action, h.id_work_order "
                "FROM work_order_history h "
                "LEFT JOIN `user` u ON u.id = h.id_user "
                "ORDER BY h.date DESC"
            )
            rows = cursor.fetchall()

        return [
            WorkOrderHistory(row[0], row[1], row[2], row[3], row[4])
            for row in rows
        ]