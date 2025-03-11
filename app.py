from flask import Flask, render_template, request, redirect
import psycopg2
import psycopg2.extras
from config import DB_CONFIG

app = Flask(__name__)

# Connect to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

# Create table if not exists
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS todo (
            id SERIAL PRIMARY KEY,
            content VARCHAR(200) NOT NULL,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

create_table()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        task_content = request.form['content']
        cur.execute("INSERT INTO todo (content) VALUES (%s)", (task_content,))
        conn.commit()

    cur.execute("SELECT * FROM todo ORDER BY date_created DESC")
    tasks = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM todo WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        new_content = request.form['content']
        cur.execute("UPDATE todo SET content = %s WHERE id = %s", (new_content, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/')

    cur.execute("SELECT * FROM todo WHERE id = %s", (id,))
    task = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)