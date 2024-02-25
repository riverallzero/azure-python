from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL 연결 설정
config = {
    'host': '<server-name>.mysql.database.azure.com',
    'user': '<user-name>',
    'password': '<password>',
    'database': '<database-name>',
}


# 데이터베이스 연결 함수
def connect_to_database():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("CREATE TABLE IF NOT EXISTS inventory (id serial PRIMARY KEY, title VARCHAR(50), contents VARCHAR(300), status VARCHAR(20));")

    return conn


# 데이터베이스로부터 할일 목록을 가져오는 함수
def get_tasks():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventory;")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()

    return tasks


@app.route('/')
def index():
    tasks = get_tasks()

    return render_template('templates/index.html', tasks=tasks)


# 할일 추가
@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title'].strip()
    description = request.form['description'].strip()
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (title, contents) VALUES (%s, %s);", (title, description))
    conn.commit()
    cursor.close()
    conn.close()

    return print('added')


# 할일 삭제
@app.route('/delete_task', methods=['POST'])
def delete_task():
    title = request.form['title'].strip()
    description = request.form['description'].strip()
    print('for', title, description)
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE title = %s AND contents = %s;", (title, description,))
    conn.commit()
    cursor.close()
    conn.close()

    return print('deleted')


if __name__ == '__main__':
    app.run(debug=True)
