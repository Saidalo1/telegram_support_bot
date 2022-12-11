import sqlite3

path = 'database.db'


class BannedUsers:
    def __init__(self, telegram_user_id, id=None):
        self.telegram_user_id = telegram_user_id
        self.id = id

    def get_by_id(telegram_user_id):
        with sqlite3.connect(path) as conn:
            res = conn.execute(f"""
                    Select Id From blacklist where telegram_user_id={telegram_user_id}

                """)

            for item in res:
                return item[0]

    def save(self):
        with sqlite3.connect(path) as conn:
            conn.execute(f"""
                    Insert Into blacklist (telegram_user_id) Values ({self.telegram_user_id})
                """)

    def delete(self):
        with sqlite3.connect(path) as conn:
            conn.execute(f"""
                    Delete from blacklist Where telegram_user_id={self.telegram_user_id}
                """)

    def __str__(self) -> str:
        return f'{self.telegram_user_id}'
