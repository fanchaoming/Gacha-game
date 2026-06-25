# db.py
import mysql.connector
import os
class GameDataRepository:
    """
    数据持久化层：负责 MySQL 的连接、建表、读写操作。
    业务逻辑层（GameState）通过该类与数据库交互，不直接写 SQL。
    """

    def __init__(self):
        # 从“环境变量”里取密码，如果取不到就用空字符串（保证程序不报错）
        self.host = os.getenv('DB_HOST', '127.0.0.1')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')  # ← 重点！这里不再写死密码
        self.database = os.getenv('DB_NAME', 'draw_game')
        self._init_db()
    def _get_connection(self):
        """获取数据库连接（每次调用都会新建连接）"""
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def _init_db(self):
        """
        初始化数据库：
        1. 如果数据库不存在则创建
        2. 如果表不存在则创建
        3. 如果无记录则插入默认用户（id=1）
        """
        # 先不指定 database，连接默认库创建数据库
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        conn.close()

        # 再连接到目标数据库
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                id INT PRIMARY KEY CHECK (id = 1),
                coin INT DEFAULT 0,
                total_pulls INT DEFAULT 0
            )
        ''')
        # 如果表为空，插入默认用户
        cursor.execute("SELECT COUNT(*) FROM user_data")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO user_data (id, coin, total_pulls) VALUES (1, 0, 0)")
        conn.commit()
        conn.close()

    def load_coin(self):
        """从数据库读取 coin 值，若记录不存在则返回 0"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT coin FROM user_data WHERE id = 1")
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else 0

    def save_coin(self, coin):
        """更新数据库中的 coin 值"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE user_data SET coin = %s WHERE id = 1", (coin,))
        conn.commit()
        conn.close()
