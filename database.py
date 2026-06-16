import sqlite3

class Database:
    def __init__(self, db_name="whatsapp_agent.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS chat_history (
            sender TEXT,
            message TEXT,
            role TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_message(self, sender, message, role):
        query = "INSERT INTO chat_history (sender, message, role) VALUES (?, ?, ?)"
        self.conn.execute(query, (sender, message, role))
        self.conn.commit()

    def get_history(self, sender, limit=5):
        query = "SELECT role, message FROM chat_history WHERE sender = ? ORDER BY timestamp DESC LIMIT ?"
        cursor = self.conn.execute(query, (sender, limit))
        history = cursor.fetchall()
        # ترتيبها من الأقدم للأحدث ليقرأها الذكاء الاصطناعي بشكل صحيح
        return history[::-1]
