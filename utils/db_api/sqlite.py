import sqlite3


class Database:
    def __init__(self, db_path: str = 'test_bot.db'):
        self.db_path = db_path

    @property
    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_table_users(self):
        cur = self.connect.cursor()
        try:
            cur.execute("""
                CREATE TABLE users(
                    id INT PRIMARY KEY NOT NULL, 
                    fullname VARCHAR(100) NOT NULL, 
                    phone VARCHAR(20) NOT NULL, 
                    email VARCHAR(50) NULL, 
                    birthday DATE NULL,
                    urinish INT DEFAULT 0 NULL
                    )
            """)
            print("Jadval yaratildi")
        except sqlite3.OperationalError as err:
            print(err)
        self.connect.close()

    def select_users(self):
        cur = self.connect.cursor()
        res = cur.execute("""
            SELECT * FROM users
        """)
        self.connect.close()
        return res.fetchall()

    def select_user(self, user_id):
        cur = self.connect.cursor()
        res = cur.execute(f"""
            SELECT * FROM users WHERE id={user_id}
        """)
        return res.fetchone()

    def select_users_ids(self):
        cur = self.connect.cursor()
        res = cur.execute("""
            SELECT id FROM users
        """)
        ids = [set_obj[0] for set_obj in res.fetchall()]
        self.connect.close()
        return ids

    def add_user(self, id, fullname, phone, email=None, birthday=None, commit=True):
        conn = self.connect
        cur = conn.cursor()
        SQL = """
            INSERT INTO users (id, fullname, phone, email, birthday)
            VALUES
            (?, ?, ?, ?, ?)
        """
        cur.execute(SQL, (id, fullname, phone, email, birthday))
        if commit:
            conn.commit()
            print("Bazaga user qo'shildi")
            conn.close()

    def add_email_birthday(self, user_id, email, birthday, commit=True):
        conn = self.connect
        cur = conn.cursor()
        SQL = """
            UPDATE users SET email=?, birthday=? WHERE id=?
        """
        cur.execute(SQL, (email, birthday, user_id))
        if commit:
            conn.commit()
            print("To'liq ro'yxatdan o'tildi")
            conn.close()

    def delete_user(self, user_id, commit=True):
        con = self.connect
        cur = con.cursor()
        SQL = """
                    DELETE FROM users WHERE id=?
                """
        cur.execute(SQL, (user_id,))
        if commit:
            con.commit()
            print("User ochirildi")
            con.close()

    def update_email(self, user_id, email, commit=True):
        con = self.connect
        cur = con.cursor()
        SQL = """
                UPDATE users SET email=? WHERE id=?
            """
        cur.execute(SQL, (email, user_id))
        if commit:
            con.commit()
            print("Email ozgartirildi")
            con.close()

    def update_number(self, user_id, number, commit=True):
        con = self.connect
        cur = con.cursor()
        SQL = """
                       UPDATE users SET phone=? WHERE id=?
                   """
        cur.execute(SQL, (number, user_id))
        if commit:
            con.commit()
            print("Phone ozgartirildi")
            con.close()

    def update_birthday(self, user_id, birthday, commit=True):
        con = self.connect
        cur = con.cursor()
        SQL = """
                UPDATE users SET birthday=? WHERE id=?
            """
        cur.execute(SQL, (birthday, user_id))
        if commit:
            con.commit()
            print("Tugilgan kun ozgartirildi")
            con.close()

    def update_fullname(self, user_id, fullname, commit=True):
        con = self.connect
        cur = con.cursor()
        SQL = """
                        UPDATE users SET fullname=? WHERE id=?
                    """
        cur.execute(SQL, (fullname, user_id))
        if commit:
            con.commit()
            print("Fullname ozgartirildi")
            con.close()

    def update_urinish(self, user_id, urinish, commit=True):
        conn = self.connect
        cur = conn.cursor()
        SQL = """
                    UPDATE users SET urinish=? WHERE id=?
                """
        cur.execute(SQL, (urinish, user_id))
        if commit:
            conn.commit()
            print("Urinish oshirildi!")
            conn.close()

    def del_users(self):
        con = self.connect
        cur = con.cursor()
        SQL = """
                DROP TABLE users
            """
        cur.execute(SQL)
        con.commit()
        self.create_table_users()

    def create_table_tests(self):
        cur = self.connect.cursor()
        try:
            cur.execute("""
                CREATE TABLE tests(
                    photo VARCHAR(100) NULL, 
                    questions TEXT NOT NULL, 
                    variant1 VARCHAR(20) NOT NULL, 
                    variant2 VARCHAR(20) NOT NULL, 
                    variant3 VARCHAR(20) NOT NULL,
                    variant4 VARCHAR(20) NOT NULL,
                    at_date TIMESTAMP NULL
                    )
            """)
            print("Jadval yaratildi")
        except sqlite3.OperationalError as err:
            print(err)
        self.connect.close()

    def add_test(self, questions, variant1, variant2, variant3, variant4, photo=None, commit=True):
        conn = self.connect
        cur = conn.cursor()
        SQL = """
            INSERT INTO tests(photo, questions, variant1, variant2, variant3, variant4)
            VALUES
            (?, ?, ?, ?, ?, ?)
        """
        cur.execute(SQL, (photo, questions, variant1, variant2, variant3, variant4))
        if commit:
            conn.commit()
            print("Test muvaffaqiyatli qoshildi")
            conn.close()

    def del_tests(self):
        con = self.connect
        cur = con.cursor()
        SQL = """
                DROP TABLE tests
            """
        cur.execute(SQL)
        con.commit()
        self.create_table_tests()

    def select_tests(self):
        cur = self.connect.cursor()
        res = cur.execute("""
                    SELECT * FROM tests
                """)
        self.connect.close()
        return res.fetchall()

    def select_count_tests(self):
        cur = self.connect.cursor()
        res = cur.execute("""
            SELECT count(*) FROM tests
        """)
        self.connect.close()
        return res.fetchone()[0]


# obj = Database()
# obj.create_table_tests()
# obj.del_tests()
# obj.add_test('savol', 'q', 'e', 't', 's')
# print(obj.select_tests())
# obj.create_table_users()
# print(obj.add_user(2, 'df', '43253'))
# obj.delete_user(2)
# obj.add_email_birthday(1, 'afds', '1.1.1')
# obj.del_users()
# print(obj.select_user(1))
# print(obj.select_users())

# obj = Database()
# obj.create_table_tests()
# obj.add_test("srethrn", "wege", "wgrheh", "egerer", "wegerger")
# print(obj.select_tests())
# print(obj.select_tests())
# dict1 = {}
# print(dict1['a'])
# print(obj.select_count_tests())
