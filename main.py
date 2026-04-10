from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Путь к базе данных (принудительно в текущей папке)
DB_PATH = os.path.join(os.path.dirname(__file__), 'ctf.db')

def setup_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Удаляем старую таблицу, если она была "битая", и создаем заново
        cursor.execute('DROP TABLE IF EXISTS system_vault')
        cursor.execute('''
            CREATE TABLE system_vault (
                id INTEGER PRIMARY KEY,
                flag_content TEXT
            )
        ''')
        # Вставляем твой новый флаг
        cursor.execute("INSERT INTO system_vault (id, flag_content) VALUES (1337, 'IIAU{11au_sql_add}')")
        conn.commit()
        conn.close()
        print("База данных успешно инициализирована")
    except Exception as e:
        print(f"Ошибка при настройке базы: {e}")

# Запускаем создание базы сразу при загрузке скрипта
setup_database()

def get_flag(user_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Специально уязвимый запрос
        query = f"SELECT flag_content FROM system_vault WHERE id = {user_id}"
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        return f"Ошибка SQL: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    msg = ""
    if request.method == 'POST':
        uid = request.form.get('id')
        if not uid:
            msg = "ВВЕДИТЕ ID"
        else:
            # Пытаемся получить флаг
            res = get_flag(uid)
            if res:
                msg = f"ОТВЕТ СЕРВЕРА: {res}"
            else:
                msg = "ОШИБКА: Доступ к этой ячейке запрещен."
    
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><meta charset="utf-8"><title>IIAU Terminal</title></head>
        <body style="background:#000;color:#0f0;text-align:center;font-family:monospace;padding-top:100px">
            <h1 style="text-shadow: 0 0 10px #0f0;">IIAU CENTRAL DATABASE</h1>
            <div style="border: 1px solid #0f0; display: inline-block; padding: 20px;">
                <p>Авторизация по протоколу SQL-ENTRY</p>
                <form method="post">
                    <input type="text" name="id" placeholder="ID..." 
                           style="background:#000;color:#0f0;border:1px solid #0f0;padding:10px;outline:none">
                    <button type="submit" 
                            style="background:#0f0;color:#000;border:none;padding:10px 20px;cursor:pointer;font-weight:bold">
                        ВХОД
                    </button>
                </form>
                <p style="margin-top:20px; font-weight:bold; color:#0f0">{{msg}}</p>
            </div>
        </body>
        </html>
    ''', msg=msg)

if __name__ == "__main__":
    app.run()
