from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# ПРИНУДИТЕЛЬНАЯ НАСТРОЙКА БАЗЫ ПРИ ЗАПУСКЕ
def setup_database():
    conn = sqlite3.connect('ctf.db')
    cursor = conn.cursor()
    # Создаем таблицу
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_vault (
            id INTEGER PRIMARY KEY,
            flag_content TEXT
        )
    ''')
    # Проверяем флаг
    cursor.execute("SELECT * FROM system_vault WHERE id=1337")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO system_vault (id, flag_content) VALUES (1337, 'IIAU{bcdcbia_axb_silA}')")
    conn.commit()
    conn.close()

# Запускаем настройку базы прямо сейчас
setup_database()

def get_flag(user_id):
    try:
        conn = sqlite3.connect('ctf.db')
        cursor = conn.cursor()
        # ТА САМАЯ УЯЗВИМОСТЬ: прямая склейка строки
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
            res = get_flag(uid)
            if res:
                msg = f"[УСПЕХ]: {res}"
            else:
                msg = "[ОШИБКА]: Доступ запрещен"
    
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><meta charset="utf-8"><title>IIAU TERMINAL</title></head>
        <body style="background:#000;color:#0f0;text-align:center;font-family:monospace;padding-top:100px">
            <h1>IIAU REMOTE TERMINAL</h1>
            <form method="post">
                <input type="text" name="id" placeholder="ID..." style="background:#111;color:#0f0;border:1px solid #0f0;padding:10px">
                <button type="submit" style="background:#0f0;color:#000;border:none;padding:10px 20px;cursor:pointer;font-weight:bold">ВХОД</button>
            </form>
            <p style="font-size:18px; color:#0f0; margin-top:30px">{{msg}}</p>
        </body>
        </html>
    ''', msg=msg)

if __name__ == "__main__":
    app.run()
