import pymysql

# MySQL 서버에 연결
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='0000',
    database='flaskproject',
    cursorclass=pymysql.cursors.DictCursor
)

class Answer:
    def __init__(self):
        self.create_table()

    def create_table(self):
        with connection.cursor() as cursor:
            # answer 테이블 생성 SQL 문장
            create_table_sql = """
                                    CREATE TABLE IF NOT EXISTS answer (
                                        id INT AUTO_INCREMENT PRIMARY KEY,
                                        question_id INT,
                                        content VARCHAR(200) ,
                                        create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        FOREIGN KEY (question_id) REFERENCES question(id)
                                    )"""
            cursor.execute(create_table_sql)
            connection.commit()
    @staticmethod
    def select_question(question_id):
        cursor = connection.cursor()
        cursor.execute('select * from question where id = %s', question_id)
        return  cursor.fetchall()

    @staticmethod
    def insert_answer(question_id, content):
        cursor = connection.cursor()
        query = f"insert into answer(question_id, content) values('{question_id}', '{content}')"
        cursor.execute(query)
        connection.commit()

    @staticmethod
    def how_many_answers(id):
        cursor = connection.cursor()
        ## answer테이블에서 현재 답변 몇 개 있는지
        cursor.execute('select count(content) from answer where question_id = %s', id)
        result = cursor.fetchall()
        return result[0]['count(content)']

class Question:
    def __init__(self):
        self.create_table()

    def create_table(self):
        with connection.cursor() as cursor:
            # question 테이블 생성 SQL 문장
            create_table_sql = """
                                CREATE TABLE IF NOT EXISTS question (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    subject VARCHAR(45),
                                    content VARCHAR(200),
                                    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                )"""
            cursor.execute(create_table_sql)
            connection.commit()

    @staticmethod
    def select_all_order_list():
        cursor = connection.cursor()
        cursor.execute('select * from question order by create_date desc')
        return cursor.fetchall()


    @staticmethod
    def select_one(id):
        cursor = connection.cursor()
        cursor.execute('select * from question where id = %s', id)
        result = cursor.fetchone()

        ## answer테이블에서 현재 답변 몇 개 있는지
        cursor.execute('select content, create_date from answer where question_id = %s order by id', id)
        try:
            result['answer_set'] = cursor.fetchall()
        except:
            pass

        return result

    def insert_question(subject,content):
        cursor = connection.cursor()
        query = f"insert into question(subject, content) values('{subject}', '{content}')"
        cursor.execute(query)
        connection.commit()

class User:
    def __init__(self):
        self.create_table()

    def create_table(self):
        with connection.cursor() as cursor:
            # question 테이블 생성 SQL 문장
            create_table_sql = """
                                CREATE TABLE IF NOT EXISTS User (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                username VARCHAR(50) NOT NULL UNIQUE,
                                password VARCHAR(255) NOT NULL,
                                email VARCHAR(100) NOT NULL UNIQUE
                              )"""
            cursor.execute(create_table_sql)
            connection.commit()

    @staticmethod
    def select_one(username):
        cursor = connection.cursor()
        cursor.execute('select * from user where username = %s', username)
        return cursor.fetchone()

    @staticmethod
    def create_user(username, password, email):
        cursor = connection.cursor()
        query = f"insert into user(username, password, email) values('{username}', '{password}', '{email}')"
        cursor.execute(query)
        connection.commit()
